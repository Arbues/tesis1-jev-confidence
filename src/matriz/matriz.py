#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construye la MATRIZ de transferencia de umbrales desde `results/crudos/*.jsonl`.

CPU puro: no toca la GPU ni los pesos (por eso puede correr también en el t440).
Toda la matemática viene de `jev_conf_metrics`; aquí solo se orquesta.

Diseño (ver `paper/00_plan_del_paper.md` §10 y `docs/erratas_especificacion.md`):
  · Cross-fitting K=5 con semilla fija: el umbral se ajusta en 4 folds y se evalúa en el que
    queda; cada ítem pasa por prueba exactamente una vez.
  · Coberturas objetivo q = 0.80 (principal), 0.50 y 0.95 (sensibilidad).
  · Dos portes por celda: `delta` (directo, τ tal cual) y `delta_mapa` (con el mapa φ, solo
    cuando existe: misma clase de equivalencia y misma cardinalidad).
  · Niveles AnyJev: `raw` (principal), `L0` (debiasing sin etiquetas) y `L1` (temperatura,
    ajustada SIEMPRE dentro del fold de calibración: nada de fuga).
  · Bootstrap de ítems (B=2000) + Benjamini–Hochberg sobre todas las celdas.

Uso:
    python src/matriz/matriz.py --crudos results/crudos --out results/matrix
    python src/matriz/matriz.py --solo "convaiinnovations/laya|sst5"   # una sola celda de grupo
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(SRC)
sys.path.insert(0, SRC)

from jev_conf_metrics.definiciones import (  # noqa: E402
    CONFIDENCES, aplicar_l0, aplicar_l1, order_equiv_affine_jev_pmax,
    phi_inv, prior_por_desplazamiento_ciclico,
)
from jev_conf_metrics.transferencia import (  # noqa: E402
    bh_fdr, bootstrap_delta, celda, fold_de,
)

DEFS = ["pmax", "jev", "ent", "margin"]
NIVELES = ["raw", "L0", "L1"]
QS = [0.80, 0.50, 0.95]
K = 5

CABECERA = ["modelo", "dataset", "n", "nivel", "q", "A", "B", "n_items", "n_items_te",
            "cobertura_B", "delta", "delta_mapa", "precision_A", "precision_B",
            "tau_media", "n_empates_tau", "ic95_lo", "ic95_hi", "p", "q_fdr", "rechaza"]


# ======================================================================
#  Mapas cerrados entre definiciones
# ======================================================================

def _ent_binaria(p):
    """H(p) para una distribución de dos opciones."""
    h = 0.0
    for x in (p, 1.0 - p):
        if x > 0:
            h -= x * math.log(x)
    return h


def _ent2(pmax):
    """`ent` como función de `pmax` cuando n=2 (Proposición 3)."""
    return 1.0 - _ent_binaria(pmax) / math.log(2)


def _inv(f, y, lo=0.5, hi=1.0, iters=200):
    """Inversa numérica por bisección (las funciones son estrictamente crecientes)."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        if f(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _a_pmax(definicion, n):
    """Devuelve la función valor_de_la_definicion -> pmax (solo existe si es inyectiva)."""
    if definicion == "pmax":
        return lambda t: t
    if definicion == "jev":
        return lambda t: phi_inv(t, n)
    if n == 2:
        if definicion == "ent":
            return lambda t: _inv(_ent2, t)
        if definicion == "margin":
            return lambda t: (t + 1.0) / 2.0
    return None


def _desde_pmax(definicion, n):
    """Devuelve la función pmax -> valor de la definición."""
    if definicion == "pmax":
        return lambda x: x
    if definicion == "jev":
        return order_equiv_affine_jev_pmax(n)
    if n == 2:
        if definicion == "ent":
            return _ent2
        if definicion == "margin":
            return lambda x: 2.0 * x - 1.0
    return None


def mapa_entre(A, B, n):
    """Mapa cerrado y estrictamente creciente de la escala de A a la de B, o None.

    Existe si A y B están en la misma clase de equivalencia Y a cardinalidad fija:
      · {pmax, jev} para cualquier n (Proposición 1);
      · todas las definiciones cuando n = 2 (Proposición 3).
    """
    if A == B:
        return None
    fa, fb = _a_pmax(A, n), _desde_pmax(B, n)
    if fa is None or fb is None:
        return None
    return lambda t: fb(fa(t))


# ======================================================================
#  Niveles AnyJev
# ======================================================================

def ajustar_temperatura(probs, ys, rejilla=(0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0)):
    """T que minimiza la NLL en el conjunto dado. Se ajusta SOLO con calibración."""
    mejor, mejor_nll = 1.0, float("inf")
    for T in rejilla:
        nll = 0.0
        for p, y in zip(probs, ys):
            q = aplicar_l1(p, T)
            nll -= math.log(max(q[y], 1e-12))
        nll /= max(1, len(probs))
        if nll < mejor_nll:
            mejor, mejor_nll = T, nll
    return mejor


def _confs(probs, nivel, cal_probs, cal_ys, n):
    """Todas las definiciones para un conjunto, en el nivel pedido.

    L0 y L1 se AJUSTAN con `cal_probs`/`cal_ys` (nunca con el conjunto de prueba).
    """
    if nivel == "raw":
        transformadas = probs
    elif nivel == "L0":
        b = prior_por_desplazamiento_ciclico(cal_probs, n)
        transformadas = [aplicar_l0(p, b) for p in probs]
    elif nivel == "L1":
        T = ajustar_temperatura(cal_probs, cal_ys)
        transformadas = [aplicar_l1(p, T) for p in probs]
    else:
        raise ValueError(f"nivel desconocido: {nivel}")
    return {d: [CONFIDENCES[d](p) for p in transformadas] for d in DEFS}


# ======================================================================
#  Lectura de crudos
# ======================================================================

def cargar_crudos(crudos_dir, solo=None):
    """{(modelo, dataset): [filas]} desde los .jsonl (ignora los `_*.jsonl` de log)."""
    grupos = {}
    for path in sorted(glob.glob(os.path.join(crudos_dir, "*.jsonl"))):
        if os.path.basename(path).startswith("_"):
            continue
        with open(path, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                r = json.loads(linea)
                clave = (r["model"], r["dataset"])
                if solo and f"{clave[0]}|{clave[1]}" != solo:
                    continue
                grupos.setdefault(clave, []).append(r)
    return grupos


# ======================================================================
#  La matriz
# ======================================================================

def medir_grupo(filas, nivel, q, B_boot=2000, k=K):
    """Celdas de un grupo (modelo × dataset × cardinalidad) para un nivel y un q."""
    n = filas[0]["n_options"]
    filas = [r for r in filas if r["n_options"] == n]
    por_fold = {f: [] for f in range(k)}
    for r in filas:
        por_fold[fold_de(r["id"])].append(r)

    celdas = {}
    for fold in range(k):
        te = por_fold[fold]
        cal = [r for f2 in range(k) if f2 != fold for r in por_fold[f2]]
        if not cal or not te:
            continue
        cal_probs = [r["probs"] for r in cal]
        cal_ys = [r["y"] for r in cal]
        conf_cal = _confs(cal_probs, nivel, cal_probs, cal_ys, n)
        conf_te = _confs([r["probs"] for r in te], nivel, cal_probs, cal_ys, n)
        correct_te = [r["correct"] for r in te]

        for A in DEFS:
            for Bx in DEFS:
                if A == Bx:
                    continue
                mapa = mapa_entre(A, Bx, n)
                c = celda(conf_cal[A], conf_cal[Bx], conf_te[A], conf_te[Bx], correct_te, q, mapa=mapa)
                acum = celdas.setdefault((A, Bx), {
                    "tau": [], "cov": [], "delta": [], "prec_A": [], "prec_B": [],
                    "delta_mapa": [], "emp": [], "items": [], "n_te": 0})
                acum["tau"].append(c["tau"])
                acum["cov"].append(c["cobertura_B"])
                acum["delta"].append(c["delta"])
                acum["prec_A"].append(c["precision_A"])
                acum["prec_B"].append(c["precision_B"])
                acum["emp"].append(c["n_empates_tau"])
                if "delta_mapa" in c:
                    acum["delta_mapa"].append(c["delta_mapa"])
                # pares (conf_B, acierto) con su τ, para el bootstrap
                acum["items"].extend([(cb, a, c["tau"]) for cb, a in zip(conf_te[Bx], correct_te)])
                acum["n_te"] += len(te)

    salida = []
    for (A, Bx), acum in celdas.items():
        if not acum["delta"]:
            continue
        delta_medio = sum(acum["delta"]) / len(acum["delta"])
        # bootstrap sobre la unión de los conjuntos de prueba, con el τ de cada fold
        ic = bootstrap_items(acum["items"], q, B=B_boot)
        salida.append({
            "n": n, "nivel": nivel, "q": q, "A": A, "B": Bx,
            "n_items": len(filas), "n_items_te": acum["n_te"],
            "cobertura_B": sum(acum["cov"]) / len(acum["cov"]),
            "delta": delta_medio,
            "delta_mapa": (sum(acum["delta_mapa"]) / len(acum["delta_mapa"])
                           if acum["delta_mapa"] else None),
            "precision_A": _media(acum["prec_A"]), "precision_B": _media(acum["prec_B"]),
            "tau_media": _media(acum["tau"]),
            "n_empates_tau": int(_media(acum["emp"])),
            **ic,
        })
    return salida


def bootstrap_items(items, q, B=2000, seed=20261008, chunk=250):
    """Bootstrap de ítems VECTORIZADO (numpy, por trozos para no inflar la RAM).

    `items` = [(conf_B, acierto, tau), ...] con el tau del fold de cada ítem. El umbral NO se
    re-ajusta dentro del bootstrap. Devuelve IC 95 % y p bilateral.
    """
    import numpy as np
    if not items:
        return {"ic95_lo": float("nan"), "ic95_hi": float("nan"), "p": float("nan")}
    cb = np.asarray([x[0] for x in items], dtype=np.float64)
    tau = np.asarray([x[2] for x in items], dtype=np.float64)
    m = cb.size
    rng = np.random.default_rng(seed)
    deltas = np.empty(B, dtype=np.float64)
    for ini in range(0, B, chunk):
        fin = min(B, ini + chunk)
        idx = rng.integers(0, m, size=(fin - ini, m))
        deltas[ini:fin] = q - (cb[idx] >= tau[idx]).mean(axis=1)
    deltas.sort()
    p = 2.0 * min(int((deltas <= 0).sum()), int((deltas >= 0).sum())) / B
    return {"ic95_lo": float(deltas[int(0.025 * B)]),
            "ic95_hi": float(deltas[int(0.975 * B) - 1]),
            "p": min(1.0, float(p))}


def _media(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and math.isnan(x))]
    return sum(xs) / len(xs) if xs else float("nan")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Matriz de transferencia de umbrales (CPU)")
    ap.add_argument("--crudos", default=os.path.join(RAIZ, "results", "crudos"))
    ap.add_argument("--out", default=os.path.join(RAIZ, "results", "matrix"))
    ap.add_argument("--niveles", default=",".join(NIVELES))
    ap.add_argument("--qs", default=",".join(str(q) for q in QS))
    ap.add_argument("--solo", default=None, help='filtro "modelo|dataset"')
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--min-items", type=int, default=40,
                    help="mínimo de ítems por (grupo, cardinalidad) para entrar en la matriz")
    args = ap.parse_args(argv)

    niveles = [x for x in args.niveles.split(",") if x]
    qs = [float(x) for x in args.qs.split(",") if x]
    grupos = cargar_crudos(args.crudos, args.solo)
    if not grupos:
        raise SystemExit(f"[matriz] no hay crudos en {args.crudos}")

    filas_salida = []
    for (modelo, dataset), filas in sorted(grupos.items()):
        card = sorted({r["n_options"] for r in filas})
        for n in card:
            sub = [r for r in filas if r["n_options"] == n]
            if len(sub) < args.min_items:
                print(f"[matriz] {modelo} × {dataset} n={n}: solo {len(sub)} ítems, se omite")
                continue
            for nivel in niveles:
                for q in qs:
                    for c in medir_grupo(sub, nivel, q, B_boot=args.bootstrap):
                        c.update({"modelo": modelo, "dataset": dataset})
                        filas_salida.append(c)
            print(f"[matriz] {modelo} × {dataset} n={n}: {len(sub)} ítems ok", flush=True)

    if not filas_salida:
        raise SystemExit("[matriz] no se produjo ninguna celda")

    # FDR sobre el conjunto principal (nivel raw, q principal) y se propaga a las demás
    pvals = [c["p"] for c in filas_salida]
    ok = [p if not math.isnan(p) else 1.0 for p in pvals]
    rechaza, qvals = bh_fdr(ok, alpha=0.05)
    for c, rej, qv in zip(filas_salida, rechaza, qvals):
        c["q_fdr"] = qv
        c["rechaza"] = rej

    os.makedirs(args.out, exist_ok=True)
    ruta = os.path.join(args.out, "matriz_transferencia.csv")
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CABECERA)
        w.writeheader()
        for c in filas_salida:
            w.writerow({k: ("" if c.get(k) is None else
                            (round(c[k], 6) if isinstance(c.get(k), float) else c.get(k)))
                        for k in CABECERA})
    print(f"\n[matriz] {len(filas_salida)} celdas -> {ruta}")

    resumen = {
        "n_celdas": len(filas_salida),
        "modelos": sorted({c["modelo"] for c in filas_salida}),
        "datasets": sorted({c["dataset"] for c in filas_salida}),
        "cardinalidades": sorted({c["n"] for c in filas_salida}),
        "niveles": niveles, "qs": qs, "K": K, "bootstrap": args.bootstrap,
    }
    with open(os.path.join(args.out, "resumen.json"), "w", encoding="utf-8") as f:
        json.dump(resumen, f, ensure_ascii=False, indent=2)
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
