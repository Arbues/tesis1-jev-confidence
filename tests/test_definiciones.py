# -*- coding: utf-8 -*-
"""Tests de conformidad T1-T8 de la librería `jev-conf-metrics`.

Espejo 1:1 de la tabla §6 de `paper/03_especificacion_confidence.md`.
"""
import pytest

from src.jev_conf_metrics.definiciones import (
    CONFIDENCES, all_confidences, conf_ent, conf_jev, conf_margin, conf_noul,
    conf_pmax, order_equiv_affine_jev_pmax, phi_inv,
)

N3 = 3
PROBS = [
    [0.6, 0.2, 0.2],
    [0.6, 0.4, 0.0],
    [1 / 3, 1 / 3, 1 / 3],
    [1.0, 0.0, 0.0],
    [0.0118, 0.4629, 0.5253],
]


def _rank(v):
    orden = sorted(range(len(v)), key=lambda i: v[i])
    r = [0] * len(v)
    for pos, idx in enumerate(orden):
        r[idx] = pos
    return r


def test_T1_rango():
    """T1: toda definición cae en su rango ([0,1]; `noul` en [0.5,1])."""
    for p in PROBS:
        for nombre, v in all_confidences(p).items():
            assert 0.0 <= v <= 1.0 + 1e-9, (nombre, v, p)
    for i in range(101):
        x = i / 100
        assert 0.5 - 1e-12 <= conf_noul(x) <= 1.0 + 1e-12


def test_T2_extremos():
    """T2: uniforme -> 0; one-hot -> 1 (Jev y entropía)."""
    uniforme = [1 / 3] * 3
    one_hot = [1.0, 0.0, 0.0]
    assert abs(conf_jev(uniforme)) < 1e-12
    assert abs(conf_ent(uniforme)) < 1e-12
    assert abs(conf_jev(one_hot) - 1.0) < 1e-12
    assert abs(conf_ent(one_hot) - 1.0) < 1e-12
    assert abs(conf_pmax(one_hot) - 1.0) < 1e-12


def test_T3_monotonia_en_pmax():
    """T3: Jev y pmax crecen con p_max; la entropía NO queda determinada por p_max."""
    creciente = [conf_jev([x, (1 - x) / 2, (1 - x) / 2]) for x in [0.4, 0.5, 0.6, 0.7]]
    assert creciente == sorted(creciente)


def test_T4_prop1_jev_es_phi_de_pmax():
    """T4: C_Jev = φ(C_max) con φ afín creciente, y φ⁻¹ la deshace."""
    phi = order_equiv_affine_jev_pmax(N3)
    for p in PROBS:
        assert abs(conf_jev(p) - phi(conf_pmax(p))) < 1e-12
        assert abs(phi_inv(conf_jev(p), N3) - conf_pmax(p)) < 1e-12


def test_T5_prop2_entropia_no_determinada_por_pmax():
    """T5: mismo p_max, distinta entropía -> la entropía no es función de p_max (n>=3)."""
    a, b = [0.6, 0.2, 0.2], [0.6, 0.4, 0.0]
    assert abs(max(a) - max(b)) < 1e-12
    assert abs(conf_ent(a) - conf_ent(b)) > 1e-6


def test_T6_prop3_n2_todas_equivalentes_en_orden():
    """T6/Prop.3: con n=2 las cinco definiciones ordenan idéntico -> transferencia exacta."""
    pis = [0.5 + 0.5 * i / 499 for i in range(500)]
    p2 = [[x, 1.0 - x] for x in pis]
    base = _rank([conf_pmax(p) for p in p2])
    for v in (
        [conf_jev(p) for p in p2],
        [conf_ent(p) for p in p2],
        [conf_margin(p) for p in p2],
        [conf_noul(x) for x in pis],
    ):
        assert _rank(v) == base


def test_T7_referencia_publicada():
    """T7: el ejemplo medido por el ecosistema (30 tickets) se reproduce."""
    p = [0.0118, 0.4629, 0.5253]
    assert abs(conf_jev(p) - 0.288) < 0.001
    assert abs(conf_ent(p) - 0.3199) < 0.001
    assert abs(conf_pmax(p) - 0.5253) < 1e-12


def test_T8_noul_simetrico():
    """T8: C_noul(π) = C_noul(1−π) y nunca baja de 0.5."""
    for i in range(500):
        x = i / 499
        assert abs(conf_noul(x) - conf_noul(1.0 - x)) < 1e-12
        assert conf_noul(x) >= 0.5 - 1e-12


def test_L0_iguala_las_frecuencias_de_argmax():
    """Regresión de un fallo real (08-oct-2026): el debiasing L0 no hacía nada.

    Con un paso de `0.5/len(matriz)` el prior `b` quedaba en ~0 y las frecuencias de argmax no
    se movían (el nivel `L0` era indistinguible de `raw`). El objetivo del L0 es repartirlas
    uniformemente: si este test falla, el nivel L0 de la matriz no significa lo que dice.
    """
    import random
    from src.jev_conf_metrics.definiciones import (
        aplicar_l0, prior_por_desplazamiento_ciclico,
    )

    rng = random.Random(3)
    n_clases = 4
    # distribuciones con sesgo fuerte hacia la clase 2 (como las reales)
    probs = []
    for _ in range(400):
        p = [rng.random() * 0.2 for _ in range(n_clases)]
        p[2] += 0.6
        s = sum(p)
        probs.append([x / s for x in p])

    def frecuencias(b):
        import collections
        c = collections.Counter(max(range(n_clases), key=lambda i: q[i])
                                for q in (aplicar_l0(p, b) for p in probs))
        return [c[k] / len(probs) for k in range(n_clases)]

    antes = frecuencias([0.0] * n_clases)
    assert max(antes) - min(antes) > 0.15, antes  # hay sesgo que corregir

    b = prior_por_desplazamiento_ciclico(probs, n_clases)
    despues = frecuencias(b)
    assert max(despues) - min(despues) < 0.05, (b, despues)
    assert any(x > 0 for x in b), b


def test_nombres_congelados():
    """La lista de definiciones de la matriz no puede cambiar sin tocar el pre-registro."""
    assert set(CONFIDENCES) == {"jev", "ent", "pmax", "margin"}
