# -*- coding: utf-8 -*-
"""El mapeo de etiquetas del pipeline: los DOS convenios del ecosistema.

Regresión de un fallo real (08-oct-2026): al traducir las probabilidades indexadas por
`legend` dentro de `_normalize_answer` se perdieron **todas** las preguntas `score` de
typed-decisions (800 de 2000 filas), porque su etiqueta de oro es el ÍNDICE, no el nombre.
La solución es tolerar los dos convenios en el constructor de filas.
"""
import sys
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
sys.path.insert(0, os.path.join(RAIZ, "src", "matriz"))

from medir import _fila  # noqa: E402

CASO = {"id": "x-1", "config": "c", "workflow": "w"}


def test_score_con_indices_y_legend_matchea_por_indice():
    """Laya en `score`: claves "0".."n-1" + legend; el gold es el índice."""
    ans = {"type": "score", "probabilities": {"0": 0.1, "1": 0.7, "2": 0.2},
           "legend": {"0": "bajo", "1": "medio", "2": "alto"}}
    f = _fila(CASO, "risk", ans, {"label": "1", "score": 1})
    assert f is not None
    assert f["y"] == 1 and f["correct"] == 1 and f["n_options"] == 3


def test_score_con_indices_y_legend_matchea_por_nombre():
    """El mismo payload, pero con la etiqueta de oro expresada como nombre del legend."""
    ans = {"type": "score", "probabilities": {"0": 0.1, "1": 0.7, "2": 0.2},
           "legend": {"0": "bajo", "1": "medio", "2": "alto"}}
    f = _fila(CASO, "risk", ans, {"label": "medio"})
    assert f is not None and f["y"] == 1


def test_choice_por_nombre():
    """Laya en `choice`: claves = nombres de opción, sin legend."""
    ans = {"type": "choice", "probabilities": {"sí": 0.8, "no": 0.2}}
    f = _fila(CASO, "q", ans, {"label": "no"})
    assert f is not None and f["y"] == 1 and f["correct"] == 0


def test_noul():
    ans = {"type": "noul", "noul": 0.9}
    f = _fila(CASO, "q", ans, {"label": "true"})
    assert f is not None and f["y"] == 1 and f["correct"] == 1


def test_etiqueta_desconocida_se_salta():
    ans = {"type": "choice", "probabilities": {"a": 0.5, "b": 0.5}}
    assert _fila(CASO, "q", ans, {"label": "zzz"}) is None


def test_las_cuatro_definiciones_van_en_la_fila():
    ans = {"type": "choice", "probabilities": {"a": 0.5, "b": 0.3, "c": 0.2}}
    f = _fila(CASO, "q", ans, {"label": "a"})
    vals = {k: f[f"conf_{k}"] for k in ("pmax", "jev", "ent", "margin")}
    assert len({round(v, 9) for v in vals.values()}) == 4, vals
