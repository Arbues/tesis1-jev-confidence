# -*- coding: utf-8 -*-
"""Backend de TypeSafe: contrato, contabilidad de coste y robustez, sin tocar la red.

El transporte se inyecta (`TypesafeBackend(transport=...)`), así que estos tests corren en el
t440 sin GPU, sin clave y sin gastar un céntimo. La verificación contra la API real (6 llamadas)
está documentada en `docs/adaptador-typesafe-contrato.md` §11.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
sys.path.insert(0, os.path.join(RAIZ, "src", "matriz"))

import pytest  # noqa: E402

from backend_typesafe import (  # noqa: E402
    MODELO_FIJO, TypesafeBackend, TypesafeError, _leer_clave, normalizar_preguntas,
    )

RESPUESTA = {
    "model": "jev-1.13.0",
    "answers": {
        "intent": {"type": "choice", "choice": "refund", "confidence": 0.94,
                   "probabilities": {"refund": 0.95, "shipping": 0.05}},
        "urgency": {"type": "score", "score": 1.36, "confidence": 0.68,
                    "legend": {"0": "Can wait", "1": "Soon"}, "probabilities": {"0": 0.01, "1": 0.99}},
        "is_spam": {"type": "noul", "noul": 0.01},
    },
    "usage": {"input_tokens": 400, "output_tokens": 71},
}


def _transporte(texto=json.dumps(RESPUESTA), status=200, capturado=None):
    def _t(cuerpo):
        if capturado is not None:
            capturado.append(json.loads(cuerpo.decode()))
        return status, texto
    return _t


# --------------------------------------------------------------- normalización
def test_choice_con_lista_pasa_a_mapa():
    q = normalizar_preguntas({"i": {"type": "choice", "criteria": ["a", "b"],
                                    "instructions": "¿Qué intenta?"}})
    assert q["i"]["criteria"] == {"a": "a", "b": "b"}
    assert q["i"]["instructions"] == "¿Qué intenta?"


def test_score_con_dict_pasa_a_lista_ordenada():
    q = normalizar_preguntas({"s": {"type": "score",
                                    "criteria": {"2": "alto", "0": "bajo", "1": "medio"}}})
    assert q["s"]["criteria"] == ["bajo", "medio", "alto"]


def test_noul_sin_criterios_no_los_inventa():
    q = normalizar_preguntas({"b": {"type": "noul", "criteria": [], "instructions": ""}})
    assert "criteria" not in q["b"]
    assert "instructions" not in q["b"]


def test_choice_sin_criterios_es_error():
    with pytest.raises(TypesafeError):
        normalizar_preguntas({"i": {"type": "choice"}})


# ------------------------------------------------------------------- llamada
def test_predict_arma_el_payload_y_adjunta_usage_a_cada_respuesta():
    enviado = []
    b = TypesafeBackend(api_key="x", transport=_transporte(capturado=enviado), dormir=lambda s: None)
    payload = b.predict("hola", {"intent": {"type": "choice", "criteria": ["refund", "shipping"]}})
    # el cuerpo que viajó a la API
    assert enviado[0]["model"] == MODELO_FIJO
    assert enviado[0]["state"] == "hola"
    assert enviado[0]["questions"]["intent"]["criteria"] == {"refund": "refund", "shipping": "shipping"}
    # `_fila()` lee usage por pregunta: tiene que estar en cada respuesta
    for nombre, ans in payload["answers"].items():
        assert ans["usage"] == {"input_tokens": 400, "output_tokens": 71}
        assert ans["model"] == "jev-1.13.0"
    assert payload["answers"]["is_spam"].get("confidence") is None  # noul no la trae


def test_contabilidad_de_coste():
    b = TypesafeBackend(api_key="x", transport=_transporte(), dormir=lambda s: None)
    b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    assert b.llamadas == 1 and b.input_tokens == 400 and b.output_tokens_total == 71
    assert b.costo_usd == pytest.approx(400 / 1e6 * 0.042)          # la salida no se cobra
    assert b.costo_por_mil_decisiones() == pytest.approx(400 / 1e6 * 0.042 * 1000)


def test_reintenta_en_429_sin_dormir_de_verdad():
    estados = []

    def transporte(cuerpo):
        estados.append(1)
        return (429, "slow down") if len(estados) < 3 else (200, json.dumps(RESPUESTA))

    b = TypesafeBackend(api_key="x", transport=transporte, dormir=lambda s: None)
    b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    assert len(estados) == 3


def test_agotar_reintentos_es_error():
    b = TypesafeBackend(api_key="x", transport=lambda c: (429, "no"), dormir=lambda s: None,
                        max_reintentos=2)
    with pytest.raises(TypesafeError):
        b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})


def test_corte_de_red_se_reintenta_y_no_tumba_la_corrida(monkeypatch):
    """Un Errno 104 (reset del par) debe absorberse como reintento, no abortar la corrida."""
    import urllib.error
    import urllib.request

    llamadas = []

    class _Fake:
        status = 200

        def read(self):
            return json.dumps(RESPUESTA).encode()

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

    def urlopen_falso(req, timeout=None):
        llamadas.append(1)
        if len(llamadas) < 3:
            raise urllib.error.URLError(ConnectionResetError(104, "Connection reset by peer"))
        return _Fake()

    monkeypatch.setattr(urllib.request, "urlopen", urlopen_falso)
    b = TypesafeBackend(api_key="x", dormir=lambda s: None)
    out = b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    assert len(llamadas) == 3
    assert "intent" in out["answers"]


def test_http_no_reintentable_es_error_con_cuerpo():
    b = TypesafeBackend(api_key="x", transport=lambda c: (422, "cuerpo inválido"),
                        dormir=lambda s: None)
    with pytest.raises(TypesafeError) as e:
        b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    assert "422" in str(e.value)


def test_presupuesto_agotado_corta():
    b = TypesafeBackend(api_key="x", transport=_transporte(), dormir=lambda s: None,
                        presupuesto_usd=0.0000001)
    b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    with pytest.raises(TypesafeError) as e:
        b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})
    assert "Presupuesto" in str(e.value)


def test_modelo_distinto_al_fijado_es_error():
    """D4: si el servidor responde otro build, la medición dejaría de ser trazable."""
    otro = json.dumps(dict(RESPUESTA, model="jev-1.14.0"))
    b = TypesafeBackend(api_key="x", transport=_transporte(otro), dormir=lambda s: None)
    with pytest.raises(TypesafeError):
        b.predict("s", {"i": {"type": "choice", "criteria": ["a"]}})


def test_info_declara_la_rejilla_y_el_precio():
    b = TypesafeBackend(api_key="x")
    assert b.info["rejilla_probabilidades"] == 0.01
    assert b.info["precio_entrada_usd_mtok"] == 0.042
    assert b.info["model_id"] == "typesafe-ai/jev"
    assert b.info["revision"] == MODELO_FIJO


# ------------------------------------------------------------------- clave
def test_clave_desde_entorno():
    assert _leer_clave(entorno={"TYPESAFE_API_KEY": "  abc  "}) == "abc"


def test_clave_desde_archivo_env(tmp_path):
    ruta = tmp_path / ".env"
    ruta.write_text("# comentario\nOTRA=1\nTYPESAFE_API_KEY='clave-x'\n", encoding="utf-8")
    assert _leer_clave(ruta_env=str(ruta), entorno={}) == "clave-x"


def test_sin_clave_es_error_explicativo(tmp_path):
    with pytest.raises(TypesafeError) as e:
        _leer_clave(ruta_env=str(tmp_path / "no-existe"), entorno={})
    assert "TYPESAFE_API_KEY" in str(e.value)
