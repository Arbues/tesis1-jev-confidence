# -*- coding: utf-8 -*-
"""Regresión del paso 0: los números commiteados deben poder recalcularse desde los crudos.

Es el test que impide que un refactor silencioso cambie las mediciones ya validadas
(las 5 métricas publicadas de Laya reproducidas con |Δ| <= 0.003).
"""
import hashlib
import json
import os

import pytest

from src.jev_conf_metrics.metricas import auroc, brier_multi, ece, ece_laya

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(RAIZ, "results", "raw")

pytestmark = pytest.mark.skipif(not os.path.isdir(RAW), reason="no hay results/raw (corre el paso 0)")

MODELOS = [
    "laya_typed-decisions",
    "laya_english",
    "laya_multilingual",
    "kev_kev-latest",
]


def _cargar(tag):
    with open(os.path.join(RAW, f"paso0_summary_{tag}.json"), encoding="utf-8") as f:
        summ = json.load(f)
    with open(os.path.join(RAW, f"paso0_raw_{tag}.jsonl"), encoding="utf-8") as f:
        rows = [json.loads(l) for l in f if l.strip()]
    return summ, rows


@pytest.mark.parametrize("tag", MODELOS)
def test_resumen_se_recalcula(tag):
    summ, rows = _cargar(tag)
    g = summ["global"]
    confs = [r["conf_pmax"] for r in rows]
    correct = [r["correct"] for r in rows]
    probs = [r["probs"] for r in rows]
    ys = [r["y"] for r in rows]

    assert abs(auroc(confs, correct) - g["auroc_pmax"]) < 1e-9
    assert abs(ece(confs, correct, 15, "width") - g["ece_pmax_width"]) < 1e-9
    assert abs(ece_laya(confs, correct, 15) - g["ece_pmax_laya"]) < 1e-9
    assert abs(brier_multi(probs, ys) - g["brier"]) < 1e-9


@pytest.mark.parametrize("tag", MODELOS)
def test_row_hash_estable(tag):
    _, rows = _cargar(tag)
    for r in rows[:50]:
        esperado = r.pop("row_hash")
        calc = hashlib.sha256(json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()[:16]
        assert calc == esperado, r.get("id")


def test_laya_output_tokens_cero():
    _, rows = _cargar("laya_typed-decisions")
    assert all(r["output_tokens"] == 0 for r in rows)
    assert len(rows) == 2000


def test_cuatro_definiciones_sobre_la_misma_distribucion():
    """El objeto de la tesis: una sola distribución da cuatro `confidence` distintas."""
    _, rows = _cargar("laya_typed-decisions")
    r = rows[0]
    vals = {k: r[f"conf_{k}"] for k in ("pmax", "jev", "ent", "margin")}
    assert len({round(v, 9) for v in vals.values()}) == 4, vals
