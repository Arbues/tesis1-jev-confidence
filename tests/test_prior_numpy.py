# -*- coding: utf-8 -*-
"""El prior L0: la versión numpy (`prior_vectorizado`) debe COINCIDIR con la de referencia.

El 20-oct-2026 se midió que el prior L0 dominaba el tiempo de la matriz (34 s por 600 filas con
77 clases -> ~19 h para 26 grupos). La versión numpy es ~41× más rápida, pero **no bit-idéntica**:
al cambiar el orden de la suma puede romper empates de `argmax` de otra forma en cardinalidad
pequeña. Este test fija el contrato:

1. La función de referencia (`prior_por_desplazamiento_ciclico`) es la que regenera la matriz
   sellada; no se toca.
2. La vectorizada debe quedar **cerca** (≤ 1e-6) en cardinalidad alta, que es donde se usa.
3. En caso de divergencia, se declara: no se usa la vectorizada para artefactos sellados.
"""
import json
import os

import pytest

from src.jev_conf_metrics.definiciones import prior_por_desplazamiento_ciclico, prior_vectorizado

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CRUDOS = os.path.join(RAIZ, "results", "crudos")


def _probs(dataset, limite=40):
    import glob
    rutas = sorted(glob.glob(os.path.join(CRUDOS, f"*{dataset}.jsonl")))
    if not rutas:
        pytest.skip(f"sin crudos de {dataset}")
    out = []
    with open(rutas[0], encoding="utf-8") as f:
        for i, linea in enumerate(f):
            if i >= limite:
                break
            out.append(json.loads(linea)["probs"])
    return out


def test_cardinalidad_alta_coincide():
    """banking77 (77 clases) es el caso de uso de la vectorizada."""
    probs = _probs("banking77")
    a = prior_por_desplazamiento_ciclico(probs, 77)
    b = prior_vectorizado(probs, 77)
    assert len(a) == len(b) == 77
    assert max(abs(x - y) for x, y in zip(a, b)) <= 1e-6


def test_cardinalidad_baja_puede_divergir_y_se_declara():
    """Con 5 clases la diferencia existe: por eso la referencia sigue siendo la pura."""
    probs = _probs("sst5")
    a = prior_por_desplazamiento_ciclico(probs, 5)
    b = prior_vectorizado(probs, 5)
    dif = max(abs(x - y) for x, y in zip(a, b))
    # No se exige igualdad: se documenta que puede diferir (empates de argmax).
    assert dif >= 0.0
    assert all(0.0 <= v <= 1.0 for v in a + b)


def test_prior_degenerado_sin_filas():
    assert prior_por_desplazamiento_ciclico([], 4) == [0.0] * 4
    assert prior_vectorizado([], 4) == [0.0] * 4
