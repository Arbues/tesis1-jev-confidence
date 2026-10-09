# -*- coding: utf-8 -*-
"""Transferencia de umbrales: la definición operativa de la matriz.

`paper/03_especificacion_confidence.md` §5, con dos erratas corregidas y documentadas
(ver `docs/erratas_especificacion.md`):

  E1. El paso 1 definía `τ_A` con `≤ 1 − q`; los pasos 3-4 usan cobertura objetivo `q`.
      Aquí: `cobertura(τ) = #{i : C(i) ≥ τ}/N`, decreciente en τ, y
            `τ_A(q) = min{ τ : cobertura(τ) ≤ q }`.
  E2. El paso 2 prescribe portar el número **tal cual** (`τ_B := τ_A`), pero §5 espera
      `Δ = 0` dentro de una clase de equivalencia. Las dos cosas no pueden ser ciertas a la
      vez: `jev` y `pmax` viven en escalas afines distintas, así que el número NO transfiere
      ni dentro de la clase. Se reportan los DOS portes:
        · `delta`       — porte directo, `τ` tal cual (lo que practica el ecosistema). Es la
                          métrica principal de la matriz.
        · `delta_mapa`  — porte con el mapa φ explícito, solo cuando existe (misma clase y
                          misma cardinalidad). Verifica la Proposición 1 (Δ = 0).
"""
from __future__ import annotations

import hashlib
import random

__all__ = [
    "cobertura", "precision", "umbral_para_cobertura", "celda", "fold_de",
    "bootstrap_delta", "bh_fdr",
]


def cobertura(confs, tau):
    """Fracción de ítems con `C ≥ τ`. Decreciente en τ."""
    return sum(1 for c in confs if c >= tau) / len(confs) if confs else 0.0


def precision(confs, correct, tau):
    """Acierto medio entre los ítems seleccionados (`C ≥ τ`)."""
    sel = [c for c, a in zip(confs, correct) if c >= tau]
    return (sum(sel) / len(sel)) if sel else float("nan")


def umbral_para_cobertura(confs, q):
    """Menor τ observado cuya cobertura cae a `≤ q`, y nº de ítems empatados en ese τ."""
    vals = sorted(set(confs))
    for tau in vals:
        if cobertura(confs, tau) <= q:
            return tau, sum(1 for c in confs if c == tau)
    return vals[-1], sum(1 for c in confs if c == vals[-1])


def celda(conf_a_cal, conf_b_cal, conf_a_te, conf_b_te, correct_te, q, mapa=None):
    """Una celda (A → B): τ_A ajustado en calibración y aplicado a B en prueba.

    `mapa`: función estrictamente creciente de la escala de A a la de B (p. ej. `phi_inv`
    para A=`jev`, B=`pmax`). Si es None, la celda solo reporta el porte directo.
    """
    tau, emp = umbral_para_cobertura(conf_a_cal, q)
    cov_b = cobertura(conf_b_te, tau)
    out = {
        "tau": tau,
        "n_empates_tau": emp,
        "cobertura_A_te": cobertura(conf_a_te, tau),
        "cobertura_B": cov_b,
        "delta": q - cov_b,
        "precision_A": precision(conf_a_te, correct_te, tau),
        "precision_B": precision(conf_b_te, correct_te, tau),
    }
    if mapa is not None:
        tau_b = mapa(tau)
        cov_bm = cobertura(conf_b_te, tau_b)
        out["tau_B_mapa"] = tau_b
        out["cobertura_B_mapa"] = cov_bm
        out["delta_mapa"] = q - cov_bm
    return out


def fold_de(item_id, k=5, seed=20261008):
    """Asignación determinista de fold por hash del id (cross-fitting reproducible)."""
    h = hashlib.sha256(f"{seed}:{item_id}".encode()).hexdigest()
    return int(h, 16) % k


def bootstrap_delta(conf_b_te, correct_te, tau, q, B=2000, seed=20261008):
    """IC 95 % y p bilateral por bootstrap de ítems. El umbral τ NO se re-ajusta."""
    rng = random.Random(seed)
    n = len(conf_b_te)
    if n == 0:
        return {"delta_media": float("nan"), "ic95_lo": float("nan"),
                "ic95_hi": float("nan"), "p": float("nan")}
    deltas = []
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        deltas.append(q - cobertura([conf_b_te[i] for i in idx], tau))
    deltas.sort()
    lo, hi = deltas[int(0.025 * B)], deltas[int(0.975 * B) - 1]
    p = 2 * min(sum(1 for d in deltas if d <= 0), sum(1 for d in deltas if d >= 0)) / B
    return {"delta_media": sum(deltas) / B, "ic95_lo": lo, "ic95_hi": hi, "p": min(1.0, p)}


def bh_fdr(pvals, alpha=0.05):
    """Benjamini–Hochberg: devuelve (rechaza, q_valor) en el orden de entrada."""
    m = len(pvals)
    if m == 0:
        return [], []
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank, i in enumerate(reversed(order), start=1):
        k = m - rank + 1
        val = min(prev, pvals[i] * m / k)
        q[i] = val
        prev = val
    return [qi <= alpha for qi in q], q
