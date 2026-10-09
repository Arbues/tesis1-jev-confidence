# -*- coding: utf-8 -*-
"""Tests de la transferencia de umbrales (la matriz) y de la estadística."""
import random

from src.jev_conf_metrics.definiciones import (
    aplicar_l0, aplicar_l1, conf_ent, conf_jev, conf_pmax, phi_inv,
)
from src.jev_conf_metrics.transferencia import (
    bh_fdr, bootstrap_delta, celda, cobertura, fold_de, umbral_para_cobertura,
)


def _probs(n_items=2000, k=4, seed=7):
    rng = random.Random(seed)
    out = []
    for _ in range(n_items):
        p = [rng.random() ** 2 + 0.1 for _ in range(k)]
        s = sum(p)
        out.append([x / s for x in p])
    return out


def test_cobertura_y_umbral():
    confs = [i / 100 for i in range(101)]
    assert abs(cobertura(confs, 0.5) - 51 / 101) < 1e-9
    tau, emp = umbral_para_cobertura(confs, 0.80)
    assert cobertura(confs, tau) <= 0.80
    assert emp >= 1


def test_porte_directo_no_transfiere_ni_dentro_de_la_clase():
    """El porte que practica el ecosistema (τ tal cual, sin mapa) falla aunque A y B sean
    equivalentes en orden: `jev` y `pmax` viven en escalas afines distintas."""
    probs = _probs()
    rng = random.Random(3)
    a = [conf_jev(p) for p in probs]
    b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    r = celda(a, b, a, b, c, 0.80)
    assert abs(r["delta"]) > 0.05, r


def test_porte_con_mapa_es_exacto_jev_pmax():
    """Prop.1: con el mapa φ explícito, la cobertura se conserva (hasta un ítem, por la
    discretización del umbral). Es el sentido en que la transferencia es 'exacta'."""
    probs = _probs()
    rng = random.Random(3)
    a = [conf_jev(p) for p in probs]
    b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    # mapa A->B: de la escala de `jev` a la de `pmax` (φ⁻¹)
    r = celda(a, b, a, b, c, 0.80, mapa=lambda t: phi_inv(t, 4))
    assert abs(r["delta_mapa"]) <= 1.0 / len(a) + 1e-9, r
    assert abs(r["delta_mapa"]) < abs(r["delta"]), r


def test_transferencia_fallida_ent_pmax():
    """Prop.2: ent -> pmax no transfiere ni con mapa (no existe φ estricta)."""
    probs = _probs()
    rng = random.Random(3)
    a = [conf_ent(p) for p in probs]
    b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    r = celda(a, b, a, b, c, 0.80)
    assert abs(r["delta"]) > 1e-3, r
    assert "delta_mapa" not in r


def test_fold_determinista_y_balanceado():
    assert fold_de("abc") == fold_de("abc")
    folds = {fold_de(f"item-{i}") for i in range(2000)}
    assert folds == {0, 1, 2, 3, 4}
    cuenta = [sum(1 for i in range(2000) if fold_de(f"item-{i}") == f) for f in range(5)]
    assert all(250 < c < 550 for c in cuenta), cuenta


def test_bootstrap_da_intervalo_ordenado():
    probs = _probs(500)
    rng = random.Random(5)
    b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    tau, _ = umbral_para_cobertura(b, 0.80)
    r = bootstrap_delta(b, c, tau, 0.80, B=300)
    assert r["ic95_lo"] <= r["delta_media"] <= r["ic95_hi"]
    assert 0.0 <= r["p"] <= 1.0


def test_bh_fdr():
    rechaza, q = bh_fdr([0.001, 0.02, 0.5, 0.9])
    assert rechaza[0] is True and rechaza[3] is False
    assert all(0.0 <= x <= 1.0 for x in q)
    assert q == sorted(q), "los q-valores deben ser monótonos en el orden de p"


def test_transformaciones_anyjev():
    p = [0.0118, 0.4629, 0.5253]
    assert aplicar_l1(p, 1.0) == p or all(abs(x - y) < 1e-12 for x, y in zip(aplicar_l1(p, 1.0), p))
    frio = aplicar_l1(p, 0.5)
    assert frio[2] > p[2], "T<1 debe agudizar"
    caliente = aplicar_l1(p, 2.0)
    assert caliente[2] < p[2], "T>1 debe suavizar"
    l0 = aplicar_l0(p, [0.2, 0.2, 0.2])
    assert abs(sum(l0) - 1.0) < 1e-12 and all(x >= 0 for x in l0)
