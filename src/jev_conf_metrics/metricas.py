# -*- coding: utf-8 -*-
"""Métricas de calibración y discriminación (stdlib puro).

Extraído verbatim de `src/paso0_go_no_go.py`; `rps` es nuevo (primitivo `score` ordinal).
"""
from __future__ import annotations

import math

__all__ = ["ece", "ece_laya", "auroc", "brier_multi", "nll", "rps"]


def ece(confs, correct, n_bins=15, scheme="width"):
    """Expected Calibration Error. scheme='width' (igual ancho) o 'mass' (igual masa)."""
    if not confs:
        return 0.0
    pairs = list(zip(confs, correct))
    if scheme == "mass":
        pairs.sort(key=lambda t: t[0])
        chunks = [pairs[i * len(pairs) // n_bins:(i + 1) * len(pairs) // n_bins] for i in range(n_bins)]
    else:
        chunks = [[] for _ in range(n_bins)]
        for c, y in pairs:
            b = min(n_bins - 1, max(0, int(c * n_bins)))
            chunks[b].append((c, y))
    total, e = 0.0, 0.0
    for ch in chunks:
        if not ch:
            continue
        acc = sum(y for _, y in ch) / len(ch)
        conf = sum(c for c, _ in ch) / len(ch)
        e += (len(ch) / len(pairs)) * abs(acc - conf)
        total += len(ch)
    return e


def ece_laya(confs, correct, bins=15):
    """ECE con el binning EXACTO del arnés de Laya (`laya.common.ece_score`).

    Se implementa aquí para poder comparar contra el número publicado (0.213 en
    `laya-typed-decisions`) sin que la diferencia de binning contamine la comparación.
    Bordes `linspace(0, 1, bins+1)`; el primer bin incluye su borde inferior.
    """
    if not confs:
        return float("nan")
    e = 0.0
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        sel = [(c, y) for c, y in zip(confs, correct)
               if (c >= lo if i == 0 else c > lo) and c <= hi]
        if sel:
            mc = sum(c for c, _ in sel) / len(sel)
            ma = sum(y for _, y in sel) / len(sel)
            e += (len(sel) / len(confs)) * abs(mc - ma)
    return float(e)


def auroc(scores, labels):
    """AUROC con manejo de empates (Mann–Whitney U). labels: 1 = acierto."""
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return float("nan")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    r_pos = sum(ranks[i] for i in range(len(scores)) if labels[i] == 1)
    return (r_pos - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def brier_multi(probs, y):
    """Brier multiclase: media de Σ_k (p_ik − y_ik)²."""
    if not probs:
        return 0.0
    s = 0.0
    for p, yi in zip(probs, y):
        s += sum((p[k] - (1.0 if k == yi else 0.0)) ** 2 for k in range(len(p)))
    return s / len(probs)


def nll(probs, y):
    if not probs:
        return 0.0
    return -sum(math.log(max(p[yi], 1e-12)) for p, yi in zip(probs, y)) / len(probs)


def rps(p, y):
    """Ranked Probability Score para distribuciones ordinales (menor = mejor).

    El ecosistema lo usa para el primitivo `score` (RLCD resta el RPS a la regla de puntuación).
    """
    c = 0.0
    acc_p = 0.0
    for i, pi in enumerate(p):
        acc_p += pi
        acc_o = 1.0 if i >= y else 0.0
        c += (acc_p - acc_o) ** 2
    return c / max(1, len(p) - 1)
