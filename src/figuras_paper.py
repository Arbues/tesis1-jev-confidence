#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Figuras del paper (Tesis 1, Ruta 1).

Genera, desde los artefactos ya medidos (`results/crudos/`, `results/matrix/`), las figuras
que el paper necesita en sus puntos clave. Todo es **derivado**, nada se dibuja a mano:
si un número cambia en la matriz, la figura cambia con ella (regla D4).

Salida (vectorial, PDF para LaTeX + PNG para leer rápido):
    paper/figures/fig1_brecha.png/.pdf                  el objeto de la tesis, en una distribución
    paper/figures/fig2_directo_vs_mapa.png/.pdf         el titular (109x) por subconjunto
    paper/figures/fig3_delta_vs_mapa.png/.pdf           el número no viaja, el mapa sí (Prop. 1)
    paper/figures/fig4_por_par.png/.pdf                 la estructura está en el par (bimodal)
    paper/figures/fig5_por_cardinalidad.png/.pdf        dónde transfiere bien, por n
    paper/figures/fig6_ece_por_definicion.png/.pdf      el mismo dato, dos ECE (2.7x)
    paper/figures/fig7_accuracy_banking77.png/.pdf      Laya base vs Kev (control del ecosistema)

Uso:
    python src/figuras_paper.py                 # todas
    python src/figuras_paper.py --out paper/figures
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
import numpy as np  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = AQUI                      # este script vive en src/
RAIZ = os.path.dirname(SRC)
sys.path.insert(0, SRC)

from jev_conf_metrics.metricas import ece_laya  # noqa: E402

DEFS = ["pmax", "jev", "ent", "margin"]
GRIS = "0.35"
AZUL, NARANJA, ROJO, VERDE = "#3465a4", "#f57900", "#cc0000", "#4e9a06"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 9,
    "axes.titlesize": 10, "axes.labelsize": 9, "legend.fontsize": 8,
    "axes.grid": True, "grid.alpha": 0.25, "grid.linewidth": 0.5,
    "axes.spines.top": False, "axes.spines.right": False,
})


def _guardar(fig, out, nombre):
    """Escribe la figura en PNG y PDF (vectorial) y cierra.

    Los nombres usan guiones (no guiones bajos) para que `\\includegraphics` de LaTeX los
    tome sin problemas.
    """
    nombre = nombre.replace("_", "-")
    for ext in ("png", "pdf"):
        fig.savefig(os.path.join(out, f"{nombre}.{ext}"), bbox_inches="tight")
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
      · ece: {modelo|dataset: {"n":…, "pmax":ECE, "ent":ECE}} para el ECE por definición;
      · metas: {(modelo, dataset): meta} para accuracy.
    """
    brechas = []
    ece = {}
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
                clave = f"{r['model']}|{r['dataset']}"
                g = ece.setdefault(clave, {"n": 0, "pmax": [], "ent": []})
                g["n"] += 1
                g["pmax"].append((r["conf_pmax"], r["correct"]))
                g["ent"].append((r["conf_ent"], r["correct"]))
    for g in ece.values():
        g["ece_pmax"] = ece_laya([c for c, _ in g["pmax"]], [y for _, y in g["pmax"]])
        g["ece_ent"] = ece_laya([c for c, _ in g["ent"]], [y for _, y in g["ent"]])
    metas = {}
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.meta.json"))):
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        metas[(m["modelo"], m["dataset"])] = m
    return brechas, ece, metas


# ----------------------------------------------------------------------
#  Fig 1 — el objeto de la tesis
# ----------------------------------------------------------------------

def fig1_brecha(brechas, out):
    med = statistics.median(brechas)
    p90 = sorted(brechas)[int(0.9 * len(brechas))]
    mx = max(brechas)
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    ax.hist(brechas, bins=60, range=(0, 1), color=AZUL, alpha=0.85, edgecolor="white",
            linewidth=0.3)
    for x, etq, col in [(med, f"mediana = {med:.3f}", ROJO),
                        (p90, f"p90 = {p90:.3f}", NARANJA)]:
        ax.axvline(x, color=col, lw=1.6, ls="--")
        ax.text(x, ax.get_ylim()[1] * 0.92, " " + etq, color=col, rotation=90,
                va="top", ha="left", fontsize=8)
    ax.set_xlabel("separación entre la definición más alta y la más baja de la MISMA distribución")
    ax.set_ylabel("nº de decisiones")
    ax.set_title(f"El objeto de la tesis: el mismo dato, {len(brechas):,} decisiones, "
                 f"dos definiciones que discrepan\n(brecha máxima = {mx:.3f})".replace(",", "."))
    _guardar(fig, out, "fig1_brecha")
    return {"n": len(brechas), "mediana": med, "p90": p90, "max": mx}


# ----------------------------------------------------------------------
#  Fig 2 — el titular: directo vs mapa
# ----------------------------------------------------------------------

def _sin_empates(filas, umbral=0.05):
    out = []
    for r in filas:
        te = int(r["n_items_te"]) or 1
        if int(r["n_empates_tau"]) / te < umbral:
            out.append(r)
    return out


def fig2_directo_vs_mapa(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    subs = [
        ("todas las celdas\ncon mapa", con),
        ("sin empates\ndominantes", _sin_empates(con)),
        ("solo modelos\nentrenados", [r for r in con if not str(r["modelo"]).startswith("Qwen")]),
        ("solo n ≥ 3\n(Prop. 1)", [r for r in con if str(r["n"]) != "2"]),
    ]
    etiquetas, d_dir, d_map, fac = [], [], [], []
    for nombre, sub in subs:
        if not sub:
            continue
        d = sum(abs(_num(r["delta"])) for r in sub) / len(sub)
        m = sum(abs(_num(r["delta_mapa"])) for r in sub) / len(sub)
        etiquetas.append(f"{nombre}\n({len(sub)} celdas)")
        d_dir.append(d)
        d_map.append(m)
        fac.append(d / max(1e-9, m))
    x = np.arange(len(etiquetas))
    w = 0.38
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    b1 = ax.bar(x - w / 2, d_dir, w, label="porte DIRECTO (τ tal cual)", color=ROJO, alpha=0.9)
    b2 = ax.bar(x + w / 2, d_map, w, label="porte por MAPA (φ)", color=VERDE, alpha=0.9)
    for i, f in enumerate(fac):
        ax.text(x[i], max(d_dir[i], d_map[i]) * 1.06, f"{f:.0f}×", ha="center",
                fontsize=10, fontweight="bold", color="0.15")
    for b in list(b1) + list(b2):
        ax.annotate(f"{b.get_height():.4f}", (b.get_x() + b.get_width() / 2, b.get_height()),
                    textcoords="offset points", xytext=(0, 2), ha="center", fontsize=7, color=GRIS)
    ax.set_xticks(x, etiquetas)
    ax.set_ylabel("error absoluto medio  |Δ|")
    ax.set_ylim(0, max(d_dir) * 1.28)
    ax.legend(loc="upper right")
    ax.set_title("El número no viaja; el mapa sí: el porte directo se equivoca ~100× más\n"
                 "(nivel principal $raw$, q = 0.80)")
    _guardar(fig, out, "fig2_directo_vs_mapa")
    return {"celdas_con_mapa": len(con), "factores": [round(f, 1) for f in fac]}


# ----------------------------------------------------------------------
#  Fig 3 — Δ directo contra Δ con mapa
# ----------------------------------------------------------------------

def fig3_delta_vs_mapa(filas, out):
    sub = [r for r in filas if r["nivel"] == "raw" and abs(_num(r["q"]) - 0.8) < 1e-9
           and r["delta_mapa"] not in ("", None)]
    x = [_num(r["delta"]) for r in sub]
    y = [_num(r["delta_mapa"]) for r in sub]
    fig, ax = plt.subplots(figsize=(5.0, 4.6))
    ax.scatter(x, y, s=24, alpha=0.7, edgecolor="k", linewidth=0.3, color=AZUL)
    lim = max(0.05, max(abs(v) for v in x + y) * 1.12)
    ax.axhline(0, color="0.6", lw=0.8)
    ax.axvline(0, color="0.6", lw=0.8)
    ax.plot([-lim, lim], [-lim, lim], "--", color=GRIS, lw=0.8, label="y = x")
    ax.set_xlim(-lim, lim)
    ax.set_ylim(-lim, lim)
    ax.set_xlabel("Δ con porte DIRECTO (τ tal cual)")
    ax.set_ylabel("Δ con porte por MAPA (φ)")
    ax.legend(loc="upper left")
    ax.set_title("Proposición 1 en los datos: con el mapa el error\ncolapsa a cero; sin él se abre")
    _guardar(fig, out, "fig3_delta_vs_mapa")
    return {"celdas": len(sub)}


# ----------------------------------------------------------------------
#  Fig 4 — por par de definiciones (bimodal)
# ----------------------------------------------------------------------

def fig4_por_par(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    pares = {}
    for r in con:
        pares.setdefault((r["A"], r["B"]), []).append(abs(_num(r["delta"])))
    orden = sorted(pares.items(), key=lambda kv: statistics.median(kv[1]))
    etq = [f"{a} → {b}" for (a, b), _ in orden]
    med = [statistics.median(v) for _, v in orden]
    media = [sum(v) / len(v) for _, v in orden]
    colores = [ROJO if m > 0.3 else (NARANJA if m > 0.05 else VERDE) for m in med]
    yy = np.arange(len(etq))
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    ax.barh(yy, med, color=colores, alpha=0.9, label="|Δ| mediana")
    ax.plot(media, yy, "o", color="0.15", ms=4, label="|Δ| media")
    ax.set_yticks(yy, etq)
    ax.invert_yaxis()
    ax.set_xlabel("error del porte directo  |Δ|  (nivel $raw$)")
    ax.legend(loc="lower right")
    ax.set_title("El promedio engaña: la estructura está en el PAR de definiciones\n"
                 "(verde ≈ transfiere; rojo = falla en grande)")
    _guardar(fig, out, "fig4_por_par")
    return {f"{a}->{b}": round(statistics.median(v), 4) for (a, b), v in orden}


# ----------------------------------------------------------------------
#  Fig 5 — por cardinalidad
# ----------------------------------------------------------------------

def fig5_por_cardinalidad(filas, out):
    con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
    ns = sorted({int(r["n"]) for r in con})
    frac = []
    cel = []
    for n in ns:
        sub = [abs(_num(r["delta"])) for r in con if int(r["n"]) == n]
        cel.append(len(sub))
        frac.append(100 * sum(1 for x in sub if x < 0.01) / len(sub))
    fig, ax = plt.subplots(figsize=(6.2, 3.4))
    b = ax.bar([str(n) for n in ns], frac, color=[VERDE if f > 40 else ROJO for f in frac],
               alpha=0.9)
    for r, f, c in zip(b, frac, cel):
        ax.annotate(f"{f:.0f} %\n({c})", (r.get_x() + r.get_width() / 2, r.get_height()),
                    textcoords="offset points", xytext=(0, 3), ha="center", fontsize=7.5,
                    color=GRIS)
    ax.set_xlabel("cardinalidad n (nº de opciones)")
    ax.set_ylabel("% de celdas que transfieren bien (|Δ| < 0.01)")
    ax.set_ylim(0, 80)
    ax.set_title("El porte falla en todas las cardinalidades; solo remonta a n alto,\n"
                 "donde las definiciones tipo p_max convergen entre sí")
    _guardar(fig, out, "fig5_por_cardinalidad")
    return {str(n): round(f, 1) for n, f in zip(ns, frac)}


# ----------------------------------------------------------------------
#  Fig 6 — ECE por definición (el mismo dato, dos ECE)
# ----------------------------------------------------------------------

def fig6_ece(ece, out, clave="convaiinnovations/laya/typed-decisions|typed-decisions"):
    g = ece.get(clave)
    if not g:
        print(f"[figura] sin datos para {clave}: se omite fig6")
        return None
    vals = [g["ece_pmax"], g["ece_ent"]]
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    b = ax.bar(["concepto Jev/lite\n(p_max)", "Laya\n(entropía normalizada)"], vals,
               color=[AZUL, ROJO], alpha=0.9)
    for r, v in zip(b, vals):
        ax.annotate(f"{v:.3f}", (r.get_x() + r.get_width() / 2, r.get_height()),
                    textcoords="offset points", xytext=(0, 3), ha="center", fontweight="bold")
    ax.set_ylabel("ECE (binning exacto de Laya)")
    ax.set_ylim(0, max(vals) * 1.2)
    ax.set_title(f"El mismo modelo y los mismos datos:\ndos definiciones, un factor "
                 f"{max(vals)/min(vals):.1f}× en ECE\n(laya/typed-decisions, n = {g['n']})")
    _guardar(fig, out, "fig6_ece_por_definicion")
    return {"n": g["n"], "ece_pmax": g["ece_pmax"], "ece_ent": g["ece_ent"]}


# ----------------------------------------------------------------------
#  Fig 7 — accuracy en cardinalidad alta (Laya base vs Kev)
# ----------------------------------------------------------------------

def fig7_accuracy_banking77(metas, out):
    clave_laya = ("convaiinnovations/laya", "banking77")
    clave_kev = ("jaredpalmer/kev-0.8b", "banking77")
    if clave_laya not in metas or clave_kev not in metas:
        print("[figura] sin metas de banking77: se omite fig7")
        return None
    vals = [metas[clave_laya]["accuracy"], metas[clave_kev]["accuracy"]]
    fig, ax = plt.subplots(figsize=(4.4, 3.2))
    b = ax.bar(["Laya (base)\n421 M", "Kev-0.8B"], vals, color=[NARANJA, VERDE], alpha=0.9)
    for r, v in zip(b, vals):
        ax.annotate(f"{v:.3f}", (r.get_x() + r.get_width() / 2, r.get_height()),
                    textcoords="offset points", xytext=(0, 3), ha="center", fontweight="bold")
    ax.set_ylabel("accuracy")
    ax.set_ylim(0, 1.0)
    ax.set_title("El ecosistema sí entrena para cardinalidad alta\n(banking77, n = 77)")
    _guardar(fig, out, "fig7_accuracy_banking77")
    return {"laya": vals[0], "kev": vals[1]}


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
        "fig1_brecha": fig1_brecha(brechas, args.out),
        "fig2_directo_vs_mapa": fig2_directo_vs_mapa(filas, args.out),
        "fig3_delta_vs_mapa": fig3_delta_vs_mapa(filas, args.out),
        "fig4_por_par": fig4_por_par(filas, args.out),
        "fig5_por_cardinalidad": fig5_por_cardinalidad(filas, args.out),
        "fig6_ece": fig6_ece(ece, args.out),
        "fig7_accuracy": fig7_accuracy_banking77(metas, args.out),
    }
    print("\n[figuras] numeros calculados:")
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
