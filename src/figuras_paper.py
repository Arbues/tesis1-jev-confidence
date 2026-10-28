#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figuras del paper (Tesis 1, Ruta 1).

Genera las **ocho** figuras del paper desde los artefactos ya medidos (`results/crudos/` y
`results/matrix/`). Todo es derivado: si un número cambia en la matriz, la figura cambia con ella (D4).

Reglas de dibujo (ver `docs/plan-edicion-textual.md` §1b):

  R1  se dibuja **a la medida final**: 3.45 in (una columna IEEE, 253 pt) o 7.1 in (dos columnas, 516 pt),
      con fuente 7 pt. Nada de dibujar a 6.5 in y dejar que LaTeX lo encoja a 5 pt.
  R2  **sin título dentro de la imagen**: el mensaje va en el `caption`.
  R3  cada figura se cita en el texto con `ref` (eso es del `.tex`, no de este script).

Salida en `paper/figures/` (PDF vectorial + PNG para leer rápido):

    fig1-accuracy-banking77   accuracy de las 5 configuraciones en banking77 (n=77)      1 col
    fig2-brecha               distribución de la brecha entre definiciones (65 185)      1 col
    fig3-directo-vs-mapa      |Δ| medio directo vs con mapa, por subconjunto             1 col
    fig4-cdf-delta            CDF pareada de |Δ| en las celdas con mapa cerrado          1 col
    fig5-por-par              |Δ| por par de definiciones (12 pares)                     1 col
    fig6-por-cardinalidad     |Δ| mediana por cardinalidad, escala log + IQR             1 col
    fig7-heatmap-banking77    mapa de calor de 5 paneles 4x4                            2 col
    fig8-ece-por-definicion   ECE de las 4 definiciones en los 23 grupos                 2 col

Uso:
    .venv/bin/python src/figuras_paper.py              # todas, a paper/figures
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import statistics
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = AQUI
RAIZ = os.path.dirname(SRC)
sys.path.insert(0, SRC)

from jev_conf_metrics.metricas import ece_laya  # noqa: E402
from matriz.figura import heatmap_paper  # noqa: E402

DEFS = ["pmax", "jev", "ent", "margin"]
GRIS = "0.35"
AZUL, NARANJA, ROJO, VERDE = "#3465a4", "#f57900", "#cc0000", "#4e9a06"
ANCHO = 3.45     # una columna IEEEtran (253 pt)
ANCHO2 = 7.10    # dos columnas (516 pt)

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 300, "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "legend.fontsize": 6.5, "legend.frameon": False,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.4,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    # Fuentes Type 1/TrueType en el PDF, no Type 3: IEEE PDF eXpress rechaza las Type 3 que
    # matplotlib emite por defecto (verificado el 28-oct-2026 con `pdffonts`).
    "pdf.fonttype": 42, "ps.fonttype": 42,
})


def _guardar(fig, out, nombre, rect=None):
    """Escribe PNG y PDF vectorial, y cierra. Sin títulos internos (R2).

    Sin `bbox_inches="tight"`: la página del PDF debe medir exactamente `figsize`, para que
    `\\includegraphics[width=\\columnwidth]` la imprima a escala ~1:1 (regla R1).

    `rect` reserva una franja para una leyenda que va fuera de los ejes (p. ej. la de la Fig. 5);
    sin él, `tight_layout` no la ve y LaTeX recorta la última entrada.
    """
    if rect is None:
        fig.tight_layout()
    else:
        fig.tight_layout(rect=rect)
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(out, f"{nombre}.{ext}"))
    plt.close(fig)
    print(f"[figura] {nombre}.png/.pdf")


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")


def recorrer_crudos(crudos_dir):
    """Una sola pasada por los 65.185 registros.

    Devuelve:
      · brechas: max(def) − min(def) por decisión (el objeto de la tesis);
      · ece: {(modelo, dataset): {"n": …, "pmax": …, "jev": …, "ent": …, "margin": …}};
      · metas: {(modelo, dataset): meta} para accuracy.
    """
    brechas = []
    acumulado = {}
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.jsonl"))):
        if os.path.basename(p).startswith("_"):
            continue
        with open(p, encoding="utf-8") as f:
            for linea in f:
                r = json.loads(linea)
                vals = [r.get(f"conf_{d}") for d in DEFS]
                if any(v is None for v in vals):
                    continue
                brechas.append(max(vals) - min(vals))
                clave = (r["model"], r["dataset"])
                g = acumulado.setdefault(clave, {"n": 0, **{d: [] for d in DEFS}})
                g["n"] += 1
                for d in DEFS:
                    g[d].append((r[f"conf_{d}"], r["correct"]))
    ece = {}
    for clave, g in acumulado.items():
        ece[clave] = {"n": g["n"]}
        for d in DEFS:
            ece[clave][d] = ece_laya([c for c, _ in g[d]], [y for _, y in g[d]])
    metas = {}
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.meta.json"))):
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        metas[(m["modelo"], m["dataset"])] = m
    return brechas, ece, metas


# ----------------------------------------------------------------------
#  Fig 1 — accuracy: las cinco configuraciones en cardinalidad alta
# ----------------------------------------------------------------------

def fig1_accuracy(metas, out):
    clave = [("Qwen/Qwen3.5-0.8B-Base", "Qwen 0.8B (control)"),
             ("convaiinnovations/laya/multilingual", "Laya multilingual"),
             ("convaiinnovations/laya", "Laya base"),
             ("convaiinnovations/laya/typed-decisions", "Laya typed-decisions"),
             ("jaredpalmer/kev-0.8b", "Kev-0.8B")]
    datos = [(etq, metas[(m, "banking77")]["accuracy"]) for m, etq in clave
             if (m, "banking77") in metas]
    if len(datos) < 2:
        print("[figura] sin metas de banking77: se omite fig1")
        return None
    yy = np.arange(len(datos))
    fig, ax = plt.subplots(figsize=(ANCHO, 2.05))
    colores = [GRIS if e.startswith("Qwen") else (VERDE if e.startswith("Kev") else AZUL)
               for e, _ in datos]
    ax.barh(yy, [v for _, v in datos], color=colores, alpha=0.9, height=0.62)
    for i, (_, v) in enumerate(datos):
        ax.text(v + 0.012, i, f"{v:.3f}", va="center", fontsize=6.5, color="0.2")
    azar = 1.0 / 77
    ax.axvline(azar, color=ROJO, lw=1.0, ls=":")
    ax.text(azar + 0.012, len(datos) - 0.4, f"azar 1/77 = {azar:.3f}",
            color=ROJO, fontsize=6, va="top")
    ax.set_yticks(yy, [e for e, _ in datos])
    ax.invert_yaxis()
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("accuracy en banking77 (n = 77)")
    ax.grid(axis="y", visible=False)
    _guardar(fig, out, "fig1-accuracy-banking77")
    return {"accuracy": {e: round(v, 4) for e, v in datos},
            "factor_kev_vs_laya_base": round(datos[-1][1] / dict(datos)["Laya base"], 2)}


# ----------------------------------------------------------------------
#  Fig 2 — la brecha: el objeto de la tesis
# ----------------------------------------------------------------------

def fig2_brecha(brechas, out):
    med = statistics.median(brechas)
    p90 = sorted(brechas)[int(0.9 * len(brechas))]
    mx = max(brechas)
    ceros = sum(1 for v in brechas if v == 0)
    fig, ax = plt.subplots(figsize=(ANCHO, 2.3))
    ax.hist(brechas, bins=60, range=(0, 1), color=AZUL, alpha=0.85,
            edgecolor="white", linewidth=0.25)
    tope = ax.get_ylim()[1]
    for x, etq, col, dy in [(med, f"mediana {med:.3f}", ROJO, 0.94),
                            (p90, f"p90 {p90:.3f}", NARANJA, 0.80)]:
        ax.axvline(x, color=col, lw=1.1, ls="--")
        ax.text(x + 0.012, tope * dy, etq, color=col, fontsize=6.5, va="top")
    ax.annotate(f"{ceros} filas saturadas\n(las 4 definiciones valen 1)",
                xy=(0.01, tope * 0.55), xytext=(0.17, tope * 0.66),
                fontsize=6, color="0.25",
                arrowprops=dict(arrowstyle="->", lw=0.6, color="0.35"))
    ax.set_xlabel("separación entre la definición más alta\ny la más baja de la MISMA distribución")
    ax.set_ylabel("nº de decisiones")
    ax.set_xlim(0, 1)
    _guardar(fig, out, "fig2-brecha")
    return {"n": len(brechas), "mediana": round(med, 4), "p90": round(p90, 4),
            "max": round(mx, 4), "filas_saturadas": ceros}


# ----------------------------------------------------------------------
#  Fig 3 — el titular: directo vs mapa
# ----------------------------------------------------------------------

def _sin_empates(filas, umbral=0.05):
    return [r for r in filas
            if int(r["n_empates_tau"]) / (int(r["n_items_te"]) or 1) < umbral]


def fig3_directo_vs_mapa(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    subs = [("todas\ncon mapa", con),
            ("sin empates\ndominantes", _sin_empates(con)),
            ("solo modelos\nentrenados", [r for r in con if not str(r["modelo"]).startswith("Qwen")]),
            ("solo n >= 3", [r for r in con if str(r["n"]) != "2"])]
    etq, d_dir, d_map, fac = [], [], [], []
    for nombre, sub in subs:
        if not sub:
            continue
        d = sum(abs(_num(r["delta"])) for r in sub) / len(sub)
        m = sum(abs(_num(r["delta_mapa"])) for r in sub) / len(sub)
        etq.append(f"{nombre}\n({len(sub)})")
        d_dir.append(d)
        d_map.append(m)
        fac.append(d / max(1e-9, m))
    x = np.arange(len(etq))
    w = 0.38
    fig, ax = plt.subplots(figsize=(ANCHO, 2.45))
    b1 = ax.bar(x - w / 2, d_dir, w, label="porte directo (tau tal cual)", color=ROJO, alpha=0.9)
    b2 = ax.bar(x + w / 2, d_map, w, label="porte con mapa", color=VERDE, alpha=0.9)
    for i, f in enumerate(fac):
        ax.text(x[i], max(d_dir[i], d_map[i]) * 1.04, f"{f:.0f}x", ha="center",
                fontsize=7, color="0.15")
    ax.set_xticks(x, etq)
    ax.set_ylabel("error absoluto medio |Δ|")
    ax.set_ylim(0, max(d_dir) * 1.24)
    ax.legend(loc="upper right", handlelength=1.2, borderaxespad=0.1)
    ax.grid(axis="x", visible=False)
    _guardar(fig, out, "fig3-directo-vs-mapa")
    return {"celdas": len(con), "factor": [round(f, 1) for f in fac],
            "directo": [round(v, 4) for v in d_dir], "mapa": [round(v, 4) for v in d_map]}


# ----------------------------------------------------------------------
#  Fig 4 — CDF pareada de |Δ| (sustituye al scatter sobre la diagonal)
# ----------------------------------------------------------------------

def fig4_cdf_delta(filas, out):
    sub = [r for r in filas if r["nivel"] == "raw" and abs(_num(r["q"]) - 0.8) < 1e-9
           and r["delta_mapa"] not in ("", None)]
    if not sub:
        print("[figura] sin celdas con mapa para q=0.8: se omite fig4")
        return None
    xd = sorted(abs(_num(r["delta"])) for r in sub)
    xm = sorted(abs(_num(r["delta_mapa"])) for r in sub)
    n = len(sub)

    def cdf(v):
        return np.arange(1, len(v) + 1) / len(v)

    fig, ax = plt.subplots(figsize=(ANCHO, 2.35))
    ax.step(xd, cdf(xd), where="post", color=ROJO, lw=1.2, label="porte directo")
    ax.step(xm, cdf(xm), where="post", color=VERDE, lw=1.2, label="porte con mapa")
    ax.axvline(0.01, color="0.4", lw=0.8, ls=":")
    frac_map = sum(1 for v in xm if v < 0.01) / n
    frac_dir = sum(1 for v in xd if v < 0.01) / n
    ax.text(0.014, 0.04, "|Δ| = 0.01", fontsize=6, color="0.35")
    ax.text(0.42, 0.36, f"|Δ| < 0.01:\n con mapa {frac_map:.0%}\n directo {frac_dir:.0%}",
            fontsize=6.2, color="0.15", ha="left", va="top",
            bbox=dict(facecolor="white", edgecolor="0.75", linewidth=0.4, pad=1.6))
    ax.set_xlabel("|Δ| de la celda (fracción de cobertura perdida)")
    ax.set_ylabel("fracción de celdas <= |Δ|")
    ax.set_xlim(0, 0.85)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right", handlelength=1.2, borderaxespad=0.2)
    _guardar(fig, out, "fig4-cdf-delta")
    return {"celdas": n, "q": 0.8, "pct_mapa_bajo_001": round(100 * frac_map, 1),
            "pct_directo_bajo_001": round(100 * frac_dir, 1)}


# ----------------------------------------------------------------------
#  Fig 5 — la estructura está en el par
# ----------------------------------------------------------------------

def fig5_por_par(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    pares = {}
    for r in con:
        pares.setdefault((r["A"], r["B"]), []).append(abs(_num(r["delta"])))
    orden = sorted(pares.items(), key=lambda kv: statistics.median(kv[1]))
    etq = [f"{a} -> {b}  ({len(v)})" for (a, b), v in orden]
    med = [statistics.median(v) for _, v in orden]
    media = [sum(v) / len(v) for _, v in orden]
    colores = [ROJO if m > 0.30 else (NARANJA if m > 0.05 else VERDE) for m in med]
    yy = np.arange(len(etq))
    fig, ax = plt.subplots(figsize=(ANCHO, 3.4))
    ax.barh(yy, med, color=colores, alpha=0.9, height=0.66, label="|Δ| mediana")
    ax.plot(media, yy, "o", color="0.15", ms=2.6, label="|Δ| media")
    ax.set_yticks(yy, etq)
    ax.invert_yaxis()
    ax.set_xlabel("error del porte directo |Δ|")
    ax.set_xlim(0, max(max(media), max(med)) * 1.10)
    manejos = [
        Patch(facecolor=VERDE, label="≤ 0.05"),
        Patch(facecolor=NARANJA, label="0.05–0.30"),
        Patch(facecolor=ROJO, label="> 0.30"),
        Line2D([], [], marker="o", ls="", color="0.15", ms=3, label="|Δ| media"),
    ]
    ax.legend(handles=manejos, loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2,
              handlelength=1.1, columnspacing=0.9, fontsize=6)
    ax.grid(axis="y", visible=False)
    _guardar(fig, out, "fig5-por-par", rect=(0, 0.16, 1, 1))
    return {f"{a}->{b}": round(statistics.median(v), 4) for (a, b), v in orden}


# ----------------------------------------------------------------------
#  Fig 6 — cardinalidad: patrón no monótono, escala log + IQR
# ----------------------------------------------------------------------

def fig6_por_cardinalidad(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    ns = sorted({int(r["n"]) for r in con})
    med, iqr_lo, iqr_hi, cel = [], [], [], []
    for n in ns:
        v = sorted(abs(_num(r["delta"])) for r in con if int(r["n"]) == n)
        m = statistics.median(v)
        cel.append(len(v))
        med.append(m)
        iqr_lo.append(max(0.0, m - v[int(0.25 * len(v))]))
        iqr_hi.append(max(0.0, v[int(0.75 * len(v))] - m))
    fig, ax = plt.subplots(figsize=(ANCHO, 2.4))
    ax.errorbar(ns, med, yerr=[iqr_lo, iqr_hi], fmt="o-", ms=3.4, lw=1.0, capsize=2.2,
                color=AZUL, ecolor="0.6", elinewidth=0.7, label="mediana e IQR")
    for n, m, c in zip(ns, med, cel):
        ax.annotate(f"{m:.3f}\n({c})", (n, m), textcoords="offset points", xytext=(0, 7),
                    ha="center", fontsize=5.6, color=GRIS)
    ax.set_xscale("log")
    ax.set_xticks(ns, [str(n) for n in ns])
    ax.minorticks_off()
    ax.set_yscale("log")
    ax.set_xlabel("cardinalidad n (nº de opciones, escala log)")
    ax.set_ylabel("|Δ| (escala log)")
    ax.set_ylim(1e-3, 1.0)
    ax.legend(loc="lower left", handlelength=1.2, borderaxespad=0.1)
    _guardar(fig, out, "fig6-por-cardinalidad")
    return {str(n): {"celdas": c, "mediana": round(m, 4)} for n, m, c in zip(ns, med, cel)}


# ----------------------------------------------------------------------
#  Fig 8 — ECE por definición en los 23 grupos
# ----------------------------------------------------------------------

FAMILIAS = {"Qwen (control)": "0.45", "laya": AZUL, "laya/multilingual": "#117a65",
            "laya/typed-decisions": NARANJA, "kev-0.8b": VERDE}


def _familia(modelo):
    if modelo.startswith("Qwen"):
        return "Qwen (control)"
    if modelo.endswith("/laya"):
        return "laya"
    if modelo.endswith("multilingual"):
        return "laya/multilingual"
    if modelo.endswith("typed-decisions"):
        return "laya/typed-decisions"
    if modelo.endswith("kev-0.8b"):
        return "kev-0.8b"
    return "laya"


def fig8_ece(ece, out):
    if not ece:
        print("[figura] sin ECE: se omite fig8")
        return None
    grupos = sorted(ece, key=lambda k: statistics.median([ece[k][d] for d in DEFS]))
    xs = np.arange(len(DEFS))
    fig, ax = plt.subplots(figsize=(ANCHO2, 2.9))
    mejor, peor, spreads = {}, {}, []
    for k in grupos:
        vals = [ece[k][d] for d in DEFS]
        col = FAMILIAS.get(_familia(k[0]), AZUL)
        ax.plot(xs, vals, "-", color=col, alpha=0.55, lw=0.8, zorder=2)
        ax.scatter(xs, vals, s=6, color=col, alpha=0.55, zorder=2, linewidths=0)
        i_min, i_max = int(np.argmin(vals)), int(np.argmax(vals))
        ax.scatter(xs[i_min], vals[i_min], s=34, facecolor="white", edgecolor=col,
                   linewidth=1.0, zorder=4)
        mejor[DEFS[i_min]] = mejor.get(DEFS[i_min], 0) + 1
        peor[DEFS[i_max]] = peor.get(DEFS[i_max], 0) + 1
        spreads.append(vals[i_max] - vals[i_min])
    ax.set_xticks(xs, DEFS)
    ax.set_xlim(-0.28, len(DEFS) - 0.72)
    ax.set_ylabel("ECE (binning exacto de Laya)")
    ax.set_xlabel("definición de confidence")
    ax.grid(axis="x", visible=False)
    manejos = [Line2D([], [], color=c, lw=1.6, label=f) for f, c in FAMILIAS.items()]
    manejos.append(Line2D([], [], marker="o", ls="", mfc="white", mec="0.3",
                              ms=4.5, label="mínimo del grupo"))
    ax.legend(handles=manejos, loc="upper left", ncol=3, handlelength=1.4,
              columnspacing=1.0, borderaxespad=0.2)
    _guardar(fig, out, "fig8-ece-por-definicion")
    return {"grupos": len(grupos),
            "spread_mediana": round(statistics.median(spreads), 3),
            "spread_max": round(max(spreads), 3),
            "mejor": mejor, "peor": peor}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Figuras del paper (derivadas de los artefactos)")
    ap.add_argument("--crudos", default=os.path.join(RAIZ, "results", "crudos"))
    ap.add_argument("--matriz", default=os.path.join(RAIZ, "results", "matrix",
                                                     "matriz_transferencia.csv"))
    ap.add_argument("--out", default=os.path.join(RAIZ, "paper", "figures"))
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)

    print("[figuras] leyendo crudos (una pasada)...")
    brechas, ece, metas = recorrer_crudos(args.crudos)
    filas = leer_csv(args.matriz)

    res = {
        "fig1_accuracy": fig1_accuracy(metas, args.out),
        "fig2_brecha": fig2_brecha(brechas, args.out),
        "fig3_directo_vs_mapa": fig3_directo_vs_mapa(filas, args.out),
        "fig4_cdf_delta": fig4_cdf_delta(filas, args.out),
        "fig5_por_par": fig5_por_par(filas, args.out),
        "fig6_cardinalidad": fig6_por_cardinalidad(filas, args.out),
        "fig7_heatmap": heatmap_paper(filas, os.path.join(args.out, "fig7-heatmap-banking77"),
                                      dataset="banking77", nivel="raw", q=0.8),
        "fig8_ece": fig8_ece(ece, args.out),
    }
    print("\n[figuras] numeros calculados:")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
