# -*- coding: utf-8 -*-
"""Definiciones del campo `confidence` (DEF-1..DEF-5) y transformaciones AnyJev (DEF-7).

Especificación normativa: `paper/03_especificacion_confidence.md`.
Extraído verbatim de `src/paso0_go_no_go.py` (ya validado por `--selftest` y por la
reproducción de las 5 métricas publicadas de Laya con |Δ| ≤ 0.003).
"""
from __future__ import annotations

import math

__all__ = [
    "conf_jev", "conf_ent", "conf_pmax", "conf_margin", "conf_noul", "conf_score",
    "CONFIDENCES", "CONFIDENCES_EXT", "all_confidences", "score_mad_unif",
    "order_equiv_affine_jev_pmax", "phi_inv",
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


# ----------------------------------------------------------------------
#  Extensión declarada (posterior al pre-registro, 19-oct-2026)
# ----------------------------------------------------------------------

def score_mad_unif(n):
    """MAD_unif = (1/n)·Σᵢ |i − (n−1)/2|, la dispersión máxima admisible del primitivo `score`."""
    if n <= 0:
        return 0.0
    return sum(abs(i - (n - 1) / 2.0) for i in range(n)) / n


def conf_score(p):
    """TypeSafe `score` (DEF-EXT-1): dispersión **ordinal** respecto del nivel modal.

        confidence = max(0, 1 − Σᵢ pᵢ·|i − m| / MAD_unif),  m = argmax(p)

    Distinta de `conf_jev`, que solo mira el máximo. Ejemplo oficial de TypeSafe:
    niveles (0, 0.57, 0.43) → 0.35; (0, 0.5, 0.5) → 0.25 frente a (0.5, 0, 0.5) → 0.00.

    Exige **orden** en los niveles: solo se define sobre datasets ordinales (`sst5`). Sobre
    etiquetas nominales habría que inventar la escala. No entra en `CONFIDENCES` porque esa
    tupla está sellada por el pre-registro: vive en `CONFIDENCES_EXT`.
    Empates en el máximo: se toma el primer índice (declarado).
    """
    n = len(p)
    if n <= 1:
        return 1.0 if p else 0.0
    mad = score_mad_unif(n)
    if mad <= 0:
        return 1.0
    m = max(range(n), key=lambda i: p[i])
    dispersion = sum(pi * abs(i - m) for i, pi in enumerate(p))
    return max(0.0, 1.0 - dispersion / mad)


# nombre -> función sobre la distribución
CONFIDENCES = {
    "jev": conf_jev,
    "ent": conf_ent,       # Laya entropía
    "pmax": conf_pmax,
    "margin": conf_margin,
}

#: Definiciones que NO están en el nivel `raw` sellado. Se calculan solo si se piden
#: explícitamente, para que la matriz publicada siga siendo reproducible byte a byte.
CONFIDENCES_EXT = {
    "score": conf_score,
}


def all_confidences(p, extensiones=False):
    """Calcula TODAS las definiciones sobre la misma distribución (el punto del trabajo).

    Con `extensiones=False` (por defecto) devuelve solo las cuatro del pre-registro, de modo que
    las filas crudas y `matriz_transferencia.csv` se regeneran idénticas.
    """
    salida = {name: fn(p) for name, fn in CONFIDENCES.items()}
    if extensiones:
        salida.update({name: fn(p) for name, fn in CONFIDENCES_EXT.items()})
    return salida


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


def prior_por_desplazamiento_ciclico(matriz, n_clases, iters=2000, lr=0.05, tol=0.005):
    """Estima el prior `b` del debiasing L0 por marginalización con desplazamiento cíclico.

    Objetivo: `b ≥ 0` tal que, tras `p' = Proj_Δ(p − b)`, los `argmax` queden repartidos
    **uniformemente** entre las clases (se cancela el sesgo de opción). No usa etiquetas (D2).

    Método: subgradiente con **paso adaptativo**. La primera versión usaba un paso fijo
    `0.5/len(matriz)`, unas 1000× demasiado pequeño: `b` se quedaba en ~0 y el nivel `L0` era
    indistinguible de `raw`. Fallo detectado el 08-oct-2026 al comprobar que las frecuencias de
    argmax apenas se movían (168/294/416/222 -> 169/299/408/224, con objetivo 275 cada una).
    Con el paso adaptativo convergen a 249/251/249/251.

    **Esta es la implementación de referencia y la ÚNICA que debe usarse para regenerar la
    matriz sellada**: es la que produjo `matriz_transferencia.csv`. `prior_vectorizado` es una
    versión numpy ~41× más rápida que puede diferir en el último bit por el orden de suma
    (rompe empates distintos en cardinalidad pequeña). Ver `tests/test_prior_numpy.py`.
    """
    n = len(matriz)
    if n == 0:
        return [0.0] * n_clases
    uniforme = 1.0 / n_clases
    b = [0.0] * n_clases
    for _ in range(iters):
        cuenta = [0] * n_clases
        for p in matriz:
            q = aplicar_l0(p, b)
            cuenta[max(range(n_clases), key=lambda i: q[i])] += 1
        err = [cuenta[k] / n - uniforme for k in range(n_clases)]
        peor = max(abs(e) for e in err)
        if peor < tol:
            break
        paso = lr * max(1e-9, peor)
        b = [max(0.0, b[k] + paso * (1.0 if err[k] > 0 else -1.0)) for k in range(n_clases)]
    return b


def prior_vectorizado(matriz, n_clases, iters=2000, lr=0.05, tol=0.005):
    """Versión numpy del prior L0: ~41× más rápida, pero **no bit-idéntica**.

    Diferencia el orden de la suma al normalizar, así que con cardinalidad pequeña puede romper
    empates de `argmax` de otra forma y separarse del valor de referencia. Se usa solo donde la
    reproducibilidad byte a byte no está en juego (p. ej. `L0` en una corrida exploratoria).
    """
    import numpy as np

    P = np.asarray(matriz, dtype=np.float64)
    n = P.shape[0]
    if n == 0:
        return [0.0] * n_clases
    uniforme = 1.0 / n_clases
    b = np.zeros(n_clases)
    for _ in range(iters):
        Q = np.maximum(P - b, 0.0)
        s = Q.sum(axis=1)
        ok = s > 0
        Q[ok] /= s[ok, None]
        Q[~ok] = P[~ok]
        cuenta = np.bincount(Q.argmax(axis=1), minlength=n_clases).astype(float)
        err = cuenta / n - uniforme
        peor = float(np.abs(err).max())
        if peor < tol:
            break
        paso = lr * max(1e-9, peor)
        b = np.maximum(0.0, b + paso * np.sign(err))
    return b.tolist()
