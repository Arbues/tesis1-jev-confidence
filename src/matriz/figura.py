#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figura central: el *heatmap* de la matriz de transferencia.

Lee `results/matrix/matriz_transferencia.csv` y escribe, por dataset, una rejilla de
paneles (uno por modelo) con filas = definición origen y columnas = destino, color = `delta`.

Sin display (`Agg`): corre igual en el t440.
"""
from __future__ import annotations

import argparse
import csv
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DEFS = ["pmax", "jev", "ent", "margin"]


def leer(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def _matriz_delta(cel, n):
    """Matriz 4x4 de Δ (filas = origen A, columnas = destino B). NaN si no aplica."""
    M = np.full((len(DEFS), len(DEFS)), np.nan)
    for r in cel:
        if int(r["n"]) != n or r["A"] not in DEFS or r["B"] not in DEFS or r["A"] == r["B"]:
            continue
        M[DEFS.index(r["A"]), DEFS.index(r["B"])] = _num(r["delta"])
    return M


def heatmap_por_dataset(filas, out_dir, nivel="raw", q=0.8):
    """Una figura por (dataset, cardinalidad), con la ESCALA DE COLOR COMPARTIDA entre paneles.

    Escala compartida = un mismo color significa el mismo Δ en todos los paneles. Con escalas
    por panel la comparacion visual entre modelos es falsa (defecto detectado el 08-oct-2026).
    """
    datasets = sorted({r["dataset"] for r in filas})
    for ds in datasets:
        sub = [r for r in filas if r["dataset"] == ds and r["nivel"] == nivel
               and abs(float(r["q"]) - q) < 1e-9]
        if not sub:
            continue
        for n in sorted({int(r["n"]) for r in sub}):
            modelos = sorted({r["modelo"] for r in sub if int(r["n"]) == n})
            matrices = {m: _matriz_delta([r for r in sub if r["modelo"] == m], n) for m in modelos}
            if all(np.all(np.isnan(M)) for M in matrices.values()):
                continue
            vmax = max(float(np.nanmax(np.abs(M))) for M in matrices.values()
                       if not np.all(np.isnan(M)))
            vmax = max(vmax, 1e-6)
            fig, axes = plt.subplots(1, len(modelos), figsize=(4.2 * len(modelos), 4.6),
                                     squeeze=False)
            for j, modelo in enumerate(modelos):
                ax = axes[0][j]
                M = matrices[modelo]
                cmap = plt.get_cmap("RdBu_r").copy()
                cmap.set_bad("0.88")
                im = ax.imshow(np.ma.masked_invalid(M), cmap=cmap, vmin=-vmax, vmax=vmax)
                ax.set_xticks(range(len(DEFS)), DEFS, fontsize=9)
                ax.set_yticks(range(len(DEFS)), DEFS, fontsize=9)
                ax.set_xlabel("destino (B)", fontsize=9)
                if j == 0:
                    ax.set_ylabel("origen (A)", fontsize=9)
                ax.set_title(modelo.split("/")[-1] if "/" in modelo else modelo, fontsize=9)
                for a in range(len(DEFS)):
                    for b in range(len(DEFS)):
                        if np.isnan(M[a, b]):
                            ax.text(b, a, "n/a" if a != b else "\u2014", ha="center",
                                    va="center", fontsize=7, color="0.45")
                            continue
                        color = "white" if abs(M[a, b]) > 0.6 * vmax else "black"
                        ax.text(b, a, f"{M[a, b]:+.2f}", ha="center", va="center",
                                fontsize=8, color=color)
                cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
                cb.set_label("\u0394 (q \u2212 cobertura B)", fontsize=8)
            fig.suptitle(f"Transferencia de umbral \u2014 {ds}, n={n} (nivel {nivel}, q={q})\n"
                         f"\u0394 = q \u2212 cobertura_B al portar \u03c4 tal cual "
                         f"\u00b7 escala de color COMPARTIDA", fontsize=11)
            fig.tight_layout(rect=(0, 0, 1, 0.90))
            nombre = f"heatmap_{ds}_n{n}_{nivel}_q{int(q*100)}"
            for ext in ("png", "pdf"):
                fig.savefig(os.path.join(out_dir, f"{nombre}.{ext}"), dpi=150)
            plt.close(fig)
            print(f"[figura] {nombre}.png/pdf ({len(modelos)} paneles)")


def figura_mapa(filas, out_dir, nivel="raw", q=0.8):
    """Δ directo contra Δ con mapa: el número no viaja, el mapa sí (Proposición 1)."""
    sub = [r for r in filas if r["nivel"] == nivel and abs(float(r["q"]) - q) < 1e-9
           and r["delta_mapa"] not in ("", None)]
    if not sub:
        print("[figura] sin celdas con mapa: se omite la figura del mapa")
        return
    x = [_num(r["delta"]) for r in sub]
    y = [_num(r["delta_mapa"]) for r in sub]
    fig, ax = plt.subplots(figsize=(6.4, 5.6))
    ax.scatter(x, y, s=28, alpha=0.75, edgecolor="k", linewidth=0.3)
    lim = max(0.05, max(abs(v) for v in x + y) * 1.15)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.6", lw=0.8)
    ax.plot([-lim, lim], [-lim, lim], "--", color="0.7", lw=0.8)
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("Δ con porte DIRECTO (τ tal cual)")
    ax.set_ylabel("Δ con porte por MAPA (φ)")
    ax.set_title("Proposición 1 en los datos: el mapa conserva la cobertura,\nel número no")
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(out_dir, f"delta_vs_delta_mapa_{nivel}_q{int(q*100)}.{ext}"), dpi=150)
    plt.close(fig)
    print(f"[figura] delta_vs_delta_mapa_{nivel}_q{int(q*100)}.png/pdf ({len(sub)} celdas)")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Figuras de la matriz de transferencia")
    ap.add_argument("--matriz", default=os.path.join(RAIZ, "results", "matrix",
                                                     "matriz_transferencia.csv"))
    ap.add_argument("--out", default=os.path.join(RAIZ, "results", "matrix"))
    ap.add_argument("--nivel", default="raw")
    ap.add_argument("--q", type=float, default=0.80)
    args = ap.parse_args(argv)

    if not os.path.exists(args.matriz):
        raise SystemExit(f"[figura] no existe {args.matriz}: corre antes src/matriz/matriz.py")
    filas = leer(args.matriz)
    os.makedirs(args.out, exist_ok=True)
    heatmap_por_dataset(filas, args.out, args.nivel, args.q)
    figura_mapa(filas, args.out, args.nivel, args.q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
