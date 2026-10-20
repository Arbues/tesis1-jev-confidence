# -*- coding: utf-8 -*-
"""Backend de la API **directa** de TypeSafe (System One / Jev) para el pipeline de medición.

Es el brazo de pago de la matriz de transferencia: el modelo vive en TypeSafe, así que este
proceso solo habla HTTPS (no necesita GPU, ni torch, ni `transformers`).

Contrato verificado en vivo el 12-oct-2026 (ver `docs/adaptador-typesafe-contrato.md` §11):

- solo dos rutas: `POST /v1/systemone` y `GET /v1/models`; **no hay lote** (1 ítem = 1 request);
- el campo de opciones se llama `criteria` (mapa en `choice`, **array ordenado** en `score`);
- la respuesta trae `model` (el build que respondió; p. ej. `jev-1.13.0`) y `usage`;
- `noul` **no** trae `confidence`;
- la API devuelve `probabilities` y `confidence` **redondeadas a 2 decimales** (rejilla de 0.01);
- `output_tokens` **no** es 0 en esta API (medido: 71 con 3 preguntas, 58 y 31 con una).

La clave se lee de la variable de entorno `TYPESAFE_API_KEY` (o de `~/.env`, que es donde vive en
esta máquina). **Nunca** se escribe en el repo, en los logs ni en una fila de medición.
"""
from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

API_BASE = "https://api.typesafe.ai"
VAR_CLAVE = "TYPESAFE_API_KEY"
#: Se fija el ID versionado y NO `jev-latest`: el alias se mueve y la medición dejaría de ser
#: reproducible (D4). El 12-oct-2026 el servidor respondió `jev-1.13.0` a ambos alias.
MODELO_FIJO = "jev-1.13.0"
MODEL_ID = "typesafe-ai/jev"
#: Precio publicado (confirmado en el catálogo del gateway, 12-oct-2026): entrada 0.042 USD por
#: millón de tokens; los tokens de SALIDA no se cobran.
PRECIO_ENTRADA_USD_MTOK = 0.042
PRECIO_SALIDA_USD_MTOK = 0.0
#: Códigos que merece la pena reintentar (429 y 529 están documentados; 5xx por cortesía).
REINTENTABLES = {429, 500, 502, 503, 504, 529, 599}


class TypesafeError(RuntimeError):
    """Fallo del backend de TypeSafe (clave ausente, presupuesto agotado, respuesta inválida)."""


def _leer_clave(ruta_env=None, entorno=None):
    """Devuelve la clave desde el entorno o desde `~/.env`, sin imprimirla nunca."""
    entorno = os.environ if entorno is None else entorno
    clave = entorno.get(VAR_CLAVE)
    if clave:
        return clave.strip()
    ruta = ruta_env or os.path.join(os.path.expanduser("~"), ".env")
    try:
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith(VAR_CLAVE + "="):
                    return linea.split("=", 1)[1].strip().strip("'\"")
    except OSError:
        pass
    raise TypesafeError(
        f"Falta la clave: exporta {VAR_CLAVE} o ponla en ~/.env (nunca en este repo)."
    )


def normalizar_preguntas(preguntas):
    """Adapta las preguntas del pipeline al contrato de TypeSafe.

    El pipeline ya usa casi el mismo formato, pero hay dos diferencias que importan:

    * `choice` necesita un **mapa** {etiqueta: descripción}; si llega una lista, se convierte en
      {etiqueta: etiqueta} (sin descripción, la propia etiqueta nombra la opción);
    * `score` necesita un **array ordenado** de descripciones (la posición fija el nivel); si
      llega un dict, se ordena por la clave numérica.

    `noul` no necesita `criteria`: si llega vacía se omite (queda como sí/no).
    """
    salida = {}
    for nombre, pregunta in (preguntas or {}).items():
        q = dict(pregunta)
        tipo = q.get("type")
        criterios = q.get("criteria")
        if tipo == "choice":
            if isinstance(criterios, (list, tuple)):
                q["criteria"] = {str(c): str(c) for c in criterios}
            elif isinstance(criterios, dict):
                q["criteria"] = {str(k): v for k, v in criterios.items()}
            else:
                raise TypesafeError(f"pregunta {nombre!r}: `choice` sin `criteria`")
        elif tipo == "score":
            if isinstance(criterios, dict):
                try:
                    claves = sorted(criterios, key=lambda k: int(k))
                except (TypeError, ValueError):
                    claves = list(criterios)
                q["criteria"] = [criterios[k] for k in claves]
            elif isinstance(criterios, (list, tuple)):
                q["criteria"] = [str(c) for c in criterios]
            else:
                raise TypesafeError(f"pregunta {nombre!r}: `score` sin `criteria`")
        elif tipo == "noul":
            if not criterios:
                q.pop("criteria", None)
        if not q.get("instructions"):
            q.pop("instructions", None)
        salida[nombre] = q
    return salida


class TypesafeBackend:
    """Backend HTTP contra `api.typesafe.ai` (mismo contrato que los demás brazos del pipeline).

    Atributos útiles después de una corrida: `llamadas`, `input_tokens`, `output_tokens_total`
    y `costo_usd` (contabilidad por ítem, para la tabla de "costo por 1.000 decisiones").
    """

    def __init__(self, model=MODELO_FIJO, api_key=None, base_url=API_BASE, timeout=120,
                 max_reintentos=3, presupuesto_usd=None, transport=None, dormir=time.sleep,
                 espera_base=2.0):
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_reintentos = max_reintentos
        self.presupuesto_usd = presupuesto_usd
        #: inyectable en los tests (evita la red): recibe (bytes) y devuelve (status, texto)
        self.transport = transport
        self.dormir = dormir
        self.espera_base = espera_base
        self._clave = api_key
        # contabilidad
        self.llamadas = 0
        self.input_tokens = 0
        self.output_tokens_total = 0
        self.costo_usd = 0.0
        self.modelo_reportado = None

    # ---------------------------------------------------------------- clave / info
    @property
    def clave(self):
        if not self._clave:
            self._clave = _leer_clave()
        return self._clave

    @property
    def info(self):
        return {
            "backend": "typesafe-api",
            "base_url": self.base_url,
            "model": self.model,
            "model_id": MODEL_ID,
            "revision": self.modelo_reportado or self.model,
            "rejilla_probabilidades": 0.01,
            "precio_entrada_usd_mtok": PRECIO_ENTRADA_USD_MTOK,
            "precio_salida_usd_mtok": PRECIO_SALIDA_USD_MTOK,
            "presupuesto_usd": self.presupuesto_usd,
        }

    # ---------------------------------------------------------------- transporte
    def _post(self, cuerpo):
        if self.transport is not None:
            return self.transport(cuerpo)
        req = urllib.request.Request(
            self.base_url + "/v1/systemone", data=cuerpo, method="POST",
            headers={"Authorization": f"Bearer {self.clave}",
                     "Content-Type": "application/json", "Accept": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return r.status, r.read().decode()
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode(errors="replace")
        except (urllib.error.URLError, ConnectionError, TimeoutError, OSError) as e:
            # Corte de red / reset del par (visto en corridas largas: Errno 104 a los ~800 ítems).
            # Se devuelve un estado sintético reintentable para que el bucle de reintentos lo absorba
            # en vez de tumbar una corrida de 3.000 ítems.
            return 599, f"transporte: {type(e).__name__}: {e}"

    # ---------------------------------------------------------------- predicción
    def predict(self, state, questions):
        """Una llamada real por ítem (`questions` = todas las preguntas de ese estado).

        Devuelve el mismo sobre que los demás backends, y **adjunta `usage` y `model` a cada
        respuesta** porque `_fila()` los lee por pregunta.
        """
        if self.presupuesto_usd is not None and self.costo_usd > self.presupuesto_usd:
            raise TypesafeError(
                f"Presupuesto agotado: {self.costo_usd:.6f} USD > {self.presupuesto_usd:.6f} USD "
                f"({self.llamadas} llamadas).")
        cuerpo = json.dumps({"state": state, "model": self.model,
                             "questions": normalizar_preguntas(questions)},
                            ensure_ascii=False).encode()

        ultimo = None
        for intento in range(1, self.max_reintentos + 1):
            status, texto = self._post(cuerpo)
            if status in REINTENTABLES and intento < self.max_reintentos:
                self.dormir(self.espera_base ** intento)
                ultimo = f"HTTP {status}"
                continue
            if status != 200:
                raise TypesafeError(f"HTTP {status} de {self.base_url}: {texto[:400]}")
            break
        else:  # pragma: no cover - solo si se agotan los reintentos
            raise TypesafeError(f"agotados los reintentos ({ultimo})")

        try:
            payload = json.loads(texto)
        except ValueError as e:
            raise TypesafeError(f"respuesta no JSON: {texto[:200]}") from e

        # D4: la versión medida tiene que ser la que se declaró
        reportado = payload.get("model")
        if reportado:
            if self.modelo_reportado is None:
                self.modelo_reportado = reportado
            elif reportado != self.modelo_reportado:
                raise TypesafeError(
                    f"el modelo cambió a mitad de la corrida: {self.modelo_reportado} -> {reportado}")
            if self.model not in ("jev-latest", "jev-preview") and reportado != self.model:
                raise TypesafeError(f"se pidió {self.model} y respondió {reportado}")

        usage = payload.get("usage") or {}
        tin = int(usage.get("input_tokens") or 0)
        tout = int(usage.get("output_tokens") or 0)
        self.llamadas += 1
        self.input_tokens += tin
        self.output_tokens_total += tout
        self.costo_usd += tin / 1e6 * PRECIO_ENTRADA_USD_MTOK + tout / 1e6 * PRECIO_SALIDA_USD_MTOK

        respuestas = {}
        for nombre, ans in (payload.get("answers") or {}).items():
            if not isinstance(ans, dict):
                continue
            ans = dict(ans)
            ans["usage"] = {"input_tokens": tin, "output_tokens": tout}
            ans["model"] = reportado or self.model
            respuestas[nombre] = ans
        payload["answers"] = respuestas
        return payload

    def costo_por_mil_decisiones(self):
        """USD por 1.000 ítems (para la tabla comparativa del paper)."""
        return self.costo_usd / self.llamadas * 1000 if self.llamadas else 0.0
