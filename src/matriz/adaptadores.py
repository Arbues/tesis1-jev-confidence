# -*- coding: utf-8 -*-
"""Adaptadores de dataset: todos devuelven el MISMO formato que espera el pipeline.

Un caso es un dict:
    {"id", "workflow", "config", "state", "questions", "gold"}

donde `questions` es {nombre: {"type", "criteria" (opciones), "instructions"}} y
`gold` es {nombre: {"label", "score", "probabilities"}}.

D2: **cero anotación propia.** Las opciones y las etiquetas salen del propio dataset; si un
dataset no se puede mapear sin inventar nada, se lanza `AdaptadorNoDisponible` y se sigue.

Verificado contra la API de datasets el 08-oct-2026:
  · SetFit/sst5          [default/validation]  text · label(int64) · label_text      n = 5
  · alisawuffles/WANLI   [default/test]        premise · hypothesis · gold(string)   n = 3
  · mteb/banking77       [default/test]        text · label(int64) · label_text      n = 77
  · clinc/clinc_oos      [plus/validation]     text · intent(ClassLabel)             n = 151
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

__all__ = ["ADAPTADORES", "AdaptadorNoDisponible", "cargar", "listar"]


class AdaptadorNoDisponible(RuntimeError):
    """El dataset no se puede mapear sin inventar datos (D2). Se reporta y se sigue."""


def _hf():
    try:
        from datasets import load_dataset
    except Exception as e:  # pragma: no cover
        raise AdaptadorNoDisponible("falta `datasets`: uv pip install datasets") from e
    return load_dataset


def _opciones_de(ds, columna_clase, columna_texto=None, orden_por=None):
    """Lista de opciones ordenada, tomada del propio dataset (nunca inventada)."""
    feat = ds.features.get(columna_clase)
    nombres = getattr(feat, "names", None) if feat is not None else None
    if nombres:
        return [str(x) for x in nombres]
    if columna_texto:
        pares = sorted({(int(r[columna_clase]), str(r[columna_texto])) for r in ds})
        return [t for _, t in pares]
    vals = sorted({str(r[columna_clase]) for r in ds})
    return vals


def _indices_estratificados(ds, columna_clase, limite, seed=20261008):
    """Índices estratificados por clase, deterministas.

    Tomar los PRIMEROS N ítems de un dataset ordenado por clase es un sesgo real: en
    `clinc150` los primeros 400 ítems cubren solo 20 de las 151 clases, así que la
    cardinalidad efectiva no es la que se cree medir (detectado el 08-oct-2026). Aquí se
    reparte el presupuesto entre TODAS las clases (cuota = limite // n_clases) y se rellena
    el resto al azar con semilla fija.
    """
    import random
    rng = random.Random(seed)
    valores = list(ds[columna_clase])
    por_clase = {}
    for i, v in enumerate(valores):
        clave = int(v) if isinstance(v, int) else str(v)
        por_clase.setdefault(clave, []).append(i)
    clases = sorted(por_clase, key=str)
    for c in clases:
        rng.shuffle(por_clase[c])
    cuota = max(1, limite // len(clases))
    idx = [i for c in clases for i in por_clase[c][:cuota]]
    sobra = [i for c in clases for i in por_clase[c][cuota:]]
    rng.shuffle(sobra)
    idx.extend(sobra[:max(0, limite - len(idx))])
    return sorted(idx[:limite])


def _criteria(opciones, descripciones=None):
    """`criteria` como DICT {etiqueta: descripción}.

    Es el formato del ecosistema (`typed-decisions` lo usa) y, además, el que hace que los
    backends devuelvan las probabilidades con NOMBRE en vez de indexadas por "0".."n-1".
    """
    descripciones = descripciones or {}
    return {op: descripciones.get(op, str(op).replace("_", " ")) for op in opciones}


WANLI_DESC = {
    "entailment": "The hypothesis is entailed by the premise.",
    "neutral": "The hypothesis is neither entailed nor contradicted.",
    "contradiction": "The hypothesis contradicts the premise.",
}


# ======================================================================
#  Adaptadores
# ======================================================================

def typed_decisions(limite=None, **kw):
    """El benchmark compartido del ecosistema (2.000 decisiones / 4 flujos)."""
    from paso0_go_no_go import _load_cases
    configs = ["agent_trace_observability", "customer_service",
               "invoice_processing", "security_incidents"]
    n = limite or 500
    return _load_cases(configs, "test", n)


def sst5(limite=None, split="validation", **kw):
    """SST-5 ordinal: 5 niveles de sentimiento (el `score` ordinal del ecosistema)."""
    ds = _hf()("SetFit/sst5", split=split)
    opciones = _opciones_de(ds, "label", "label_text")
    casos = []
    for i in _indices_estratificados(ds, "label", limite or len(ds)):
        r = ds[i]
        etiqueta = opciones[int(r["label"])]
        casos.append({
            "id": f"sst5-{split}-{i}", "workflow": "sentiment", "config": "sst5",
            "state": str(r["text"]),
            "questions": {"sentiment": {
                # `score` exige criteria como LISTA de descripciones de nivel (Laya lo valida);
                # el mapa índice->etiqueta viaja en `legend` y _normalize_answer lo traduce.
                "type": "score", "criteria": list(opciones),
                "instructions": "Clasifica el sentimiento del texto en cinco niveles."}},
            "gold": {"sentiment": {"label": etiqueta, "score": int(r["label"])}},
        })
    return casos


def wanli(limite=None, split="test", **kw):
    """WANLI: inferencia de lenguaje natural, 3 opciones (la usa SemIf como verificación)."""
    ds = _hf()("alisawuffles/WANLI", split=split)
    opciones = sorted({str(r["gold"]) for r in ds})
    casos = []
    for i in _indices_estratificados(ds, "gold", limite or len(ds)):
        r = ds[i]
        casos.append({
            "id": f"wanli-{split}-{r.get('id', i)}", "workflow": "nli", "config": "wanli",
            "state": f"Premisa: {r['premise']}\nHipótesis: {r['hypothesis']}",
            "questions": {"nli": {
                "type": "choice", "criteria": _criteria(opciones, WANLI_DESC),
                "instructions": "¿Qué relación hay entre la premisa y la hipótesis?"}},
            "gold": {"nli": {"label": str(r["gold"])}},
        })
    return casos


def banking77(limite=None, split="test", **kw):
    """Banking77: 77 intenciones. Es el extremo de cardinalidad de la matriz."""
    ds = _hf()("mteb/banking77", split=split)
    opciones = _opciones_de(ds, "label", "label_text")
    if len(opciones) < 2:
        raise AdaptadorNoDisponible("banking77 sin nombres de clase utilizables")
    casos = []
    for i in _indices_estratificados(ds, "label", limite or len(ds)):
        r = ds[i]
        etiqueta = opciones[int(r["label"])]
        casos.append({
            "id": f"banking77-{split}-{i}", "workflow": "intent", "config": "banking77",
            "state": str(r["text"]),
            "questions": {"intent": {
                "type": "choice", "criteria": _criteria(opciones),
                "instructions": "¿Qué intención tiene la consulta del cliente?"}},
            "gold": {"intent": {"label": etiqueta}},
        })
    return casos


def clinc150(limite=None, split="validation", config="plus", **kw):
    """CLINC150 (`plus`): 150 intenciones + `oos`. El otro extremo de cardinalidad."""
    ds = _hf()("clinc/clinc_oos", config, split=split)
    opciones = _opciones_de(ds, "intent")
    if len(opciones) < 2:
        raise AdaptadorNoDisponible("clinc150 sin nombres de clase utilizables")
    casos = []
    for i in _indices_estratificados(ds, "intent", limite or len(ds)):
        r = ds[i]
        etiqueta = opciones[int(r["intent"])]
        casos.append({
            "id": f"clinc150-{split}-{i}", "workflow": "intent", "config": "clinc150",
            "state": str(r["text"]),
            "questions": {"intent": {
                "type": "choice", "criteria": _criteria(opciones),
                "instructions": "¿Qué intención tiene la consulta?"}},
            "gold": {"intent": {"label": etiqueta}},
        })
    return casos


def kev_suites(limite=None, split="test", **kw):
    """Suites congeladas de Kev. La estructura se inspecciona en la tarea 0.4 del plan."""
    ds = _hf()("jaredpalmer/kev-suites", split=split)
    cols = set(ds.column_names)
    if not {"state", "questions", "gold"} <= cols:
        raise AdaptadorNoDisponible(
            f"kev-suites tiene columnas {sorted(cols)}; se esperaba state/questions/gold")
    import json
    casos = []
    for i, r in enumerate(ds):
        if limite and i >= limite:
            break
        casos.append({
            "id": f"kev-suites-{split}-{i}", "workflow": r.get("workflow", "kev"),
            "config": "kev-suites",
            "state": r["state"] if isinstance(r["state"], str) else json.dumps(r["state"]),
            "questions": json.loads(r["questions"]) if isinstance(r["questions"], str) else r["questions"],
            "gold": json.loads(r["gold"]) if isinstance(r["gold"], str) else r["gold"],
        })
    return casos


ADAPTADORES = {
    "typed-decisions": typed_decisions,
    "sst5": sst5,
    "wanli": wanli,
    "banking77": banking77,
    "clinc150": clinc150,
    "kev-suites": kev_suites,
}


def listar():
    return sorted(ADAPTADORES)


def cargar(nombre, limite=None, **kw):
    if nombre not in ADAPTADORES:
        raise AdaptadorNoDisponible(f"adaptador desconocido: {nombre} (hay: {listar()})")
    return ADAPTADORES[nombre](limite=limite, **kw)
