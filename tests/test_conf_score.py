# -*- coding: utf-8 -*-
"""Tests de la DEFINICIÓN EXT-1: `conf_score` (TypeSafe `score`, MAD_unif).

Es una **extensión declarada** (19-oct-2026), posterior al pre-registro `10.5281/zenodo.23266795`.
Por eso vive en `CONFIDENCES_EXT` y NO en `CONFIDENCES`: el nivel `raw` sellado no se mueve.

Fuente de la fórmula: `docs.typesafe.ai/confidence` (verificada en vivo el 12-oct-2026) y
`docs/adaptador-typesafe-contrato.md` §3.4.
"""
import math

import pytest

from src.jev_conf_metrics.definiciones import (
    CONFIDENCES, CONFIDENCES_EXT, all_confidences, conf_jev, conf_score, score_mad_unif,
)


def test_mad_unif_valores_conocidos():
    # n=2 -> (0.5+0.5)/2 = 0.5 ; n=3 -> 2/3 ; n=5 -> (0+1+2+1+0)/5 = 1.2
    assert score_mad_unif(2) == pytest.approx(0.5)
    assert score_mad_unif(3) == pytest.approx(2 / 3)
    assert score_mad_unif(5) == pytest.approx(1.2)
    assert score_mad_unif(10) == pytest.approx(2.5)


def test_ejemplo_oficial_typesafe():
    # niveles (0, 0.57, 0.43), m=1 -> 1 - 0.43/(2/3) = 0.355
    assert conf_score([0.0, 0.57, 0.43]) == pytest.approx(0.355, abs=5e-3)


def test_sensible_a_la_distancia_y_no_solo_al_maximo():
    # misma p_max (0.5) en las dos, distinto resultado: ésa es la diferencia con conf_jev
    a = conf_score([0.0, 0.5, 0.5])   # m=1, dispersión 0.5
    b = conf_score([0.5, 0.0, 0.5])   # m=0, dispersión 1.0
    assert a == pytest.approx(0.25)
    assert b == pytest.approx(0.0)
    assert conf_jev([0.0, 0.5, 0.5]) == pytest.approx(conf_jev([0.5, 0.0, 0.5]))


def test_punto_modal_puro_es_uno():
    assert conf_score([0.0, 0.0, 1.0]) == pytest.approx(1.0)
    assert conf_score([1.0, 0.0, 0.0]) == pytest.approx(1.0)


def test_uniforme_es_cero_por_suelo():
    # dispersión media en el uniforme = MAD_unif -> 1 - 1 = 0 exacto
    assert conf_score([0.2] * 5) == pytest.approx(0.0, abs=1e-12)
    assert conf_score([0.5, 0.5]) == pytest.approx(0.0, abs=1e-12)


def test_acotada_en_0_1():
    casos = [[0.2] * 3, [0.0, 0.5, 0.5], [1 / 3] * 3, [1.0, 0.0, 0.0], [0.01, 0.98, 0.01]]
    for p in casos:
        assert 0.0 <= conf_score(p) <= 1.0


def test_ordinal_no_invariante_a_permutacion():
    # sobre etiquetas nominales la fórmula no está definida sin inventar la escala
    p = [0.1, 0.7, 0.2]
    q = [0.7, 0.1, 0.2]
    assert conf_score(p) != pytest.approx(conf_score(q))


def test_monotona_al_concentrar_en_el_nivel_modal():
    base = [0.2, 0.4, 0.2, 0.1, 0.1]
    mas = [0.1, 0.6, 0.1, 0.1, 0.1]
    assert conf_score(mas) > conf_score(base)


def test_es_una_definicion_nueva_frente_a_las_cuatro_del_pre_registro():
    p = [0.05, 0.55, 0.25, 0.10, 0.05]
    assert set(CONFIDENCES) == {"jev", "ent", "pmax", "margin"}
    assert set(CONFIDENCES_EXT) == {"score"}
    assert conf_score(p) not in {fn(p) for fn in CONFIDENCES.values()}


def test_all_confidences_no_contamina_el_nivel_sellado():
    p = [0.2, 0.5, 0.3]
    assert "score" not in all_confidences(p)          # por defecto: solo las cuatro selladas
    assert "score" in all_confidences(p, extensiones=True)
    assert len(all_confidences(p)) == 4
    assert len(all_confidences(p, extensiones=True)) == 5


def test_distribuciones_degeneradas():
    assert conf_score([1.0]) == pytest.approx(1.0)
    assert conf_score([0.0, 1.0]) == pytest.approx(1.0)
    assert not math.isnan(conf_score([0.5, 0.5]))
