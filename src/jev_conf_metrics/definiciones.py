# -*- coding: utf-8 -*-
"""Definiciones del campo `confidence` (DEF-1..DEF-5) y transformaciones AnyJev (DEF-7).

Especificación normativa: `paper/03_especificacion_confidence.md`.
Extraído verbatim de `src/paso0_go_no_go.py` (ya validado por `--selftest` y por la
reproducción de las 5 métricas publicadas de Laya con |Δ| ≤ 0.003).
"""
from __future__ import annotations

import math

__all__ = [
    "conf_jev", "conf_ent", "conf_pmax", "conf_margin", "conf_noul",
    "CONFIDENCES", "all_confidences", "order_equiv_affine_jev_pmax", "phi_inv",
    "aplicar_l0", "aplicar_l1",
]


# ======================================================================
#  DEF-1 .. DEF-5
# ======================================================================

def conf_jev(p):
    """Jev 1.13: concentración, (n·pmax − 1)/(n − 1). NO es la probabilidad ganadora."""
    n = len(p)
    if n <= 1:
        return p[0] if p else 0.0
    return (n * max(p) - 1.0) / (n - 1.0)


def conf_ent(p):
    """Laya (choice/score): 1 − H(p)/log k  (entropía normalizada)."""
    n = len(p)
    if n <= 1:
        return 1.0
    h = -sum(pi * math.log(pi) for pi in p if pi > 0)
    return max(0.0, min(1.0, 1.0 - h / math.log(n)))


def conf_pmax(p):
    """Laya `answer_confidence` / jev-lite: la probabilidad ganadora."""
    return max(p)


def conf_margin(p):
    """Margen: p_(1) − p_(2)."""
    if len(p) < 2:
        return 1.0 if p else 0.0
    s = sorted(p, reverse=True)
    return s[0] - s[1]


def conf_noul(px):
    """Primitivo `noul` (binario): max(p, 1 − p)."""
    return max(px, 1.0 - px)


# nombre -> función sobre la distribución
CONFIDENCES = {
    "jev": conf_jev,
    "ent": conf_ent,       # Laya entropía
    "pmax": conf_pmax,
    "margin": conf_margin,
}


def all_confidences(p):
    """Calcula TODAS las definiciones sobre la misma distribución (el punto del trabajo)."""
    return {name: fn(p) for name, fn in CONFIDENCES.items()}


# ======================================================================
#  Relaciones formales (Proposiciones 1 y 3)
# ======================================================================

def order_equiv_affine_jev_pmax(n):
    """φ tal que C_jev = φ(C_max) con n fijo: φ(x) = (n·x − 1)/(n − 1). (Proposición 1.)"""
    return lambda x: (n * x - 1.0) / (n - 1.0)


def phi_inv(y, n):
    """Inversa de φ: φ⁻¹(y) = (y·(n−1) + 1)/n  (mapa `pmax` → `jev`)."""
    return (y * (n - 1.0) + 1.0) / n


# ======================================================================
#  DEF-7 — transformaciones AnyJev
# ======================================================================

def aplicar_l0(p, b):
    """AnyJev L0 — debiasing SIN etiquetas: p' = Proj_Δ(p − b), recortando a ≥ 0 y renormalizando."""
    q = [max(0.0, pi - bi) for pi, bi in zip(p, b)]
    s = sum(q)
    return [x / s for x in q] if s > 0 else list(p)


def aplicar_l1(p, T):
    """AnyJev L1 — temperatura CON etiquetas: p' = softmax(log p / T)."""
    z = [math.log(max(pi, 1e-12)) / T for pi in p]
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]


def prior_por_desplazamiento_ciclico(matriz, n_clases, iters=200):
    """Estima el prior `b` de AnyJev L0 por marginalización con desplazamiento cíclico.

    `matriz`: lista de distribuciones (cada una de longitud `n_clases`). No usa etiquetas (D2).
    Método: se busca `b` tal que, al restarle `b` y renormalizar, la media de los `argmax`
    quede uniforme (cada clase ganada con la misma frecuencia).
    """
    b = [0.0] * n_clases
    lr = 0.5 / max(1, len(matriz))
    for _ in range(iters):
        cuenta = [0] * n_clases
        for p in matriz:
            q = aplicar_l0(p, b)
            cuenta[max(range(len(q)), key=lambda i: q[i])] += 1
        total = sum(cuenta) or 1
        for k in range(n_clases):
            b[k] = max(0.0, b[k] + lr * (cuenta[k] / total - 1.0 / n_clases))
    return b
