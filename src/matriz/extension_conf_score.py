#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Resultados de la definición EXT-1 (`conf_score`, MAD_unif) sobre los crudos YA medidos.

**Extensión declarada**, posterior al pre-registro `10.5281/zenodo.23266795` (19-oct-2026).
No re-mide nada, no toca las filas crudas ni `matriz_transferencia.csv`: lee `probs` de
`results/crudos/*sst5.jsonl`, calcula la quinta definición y escribe un informe aparte.

Salidas (todo regenerable, ningún número escrito a mano):
    results/matrix/extension_conf_score.csv
    results/matrix/EXTENSION_CONF_SCORE.md

Uso:
    .venv/bin/python src/matriz/extension_conf_score.py
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import statistics
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from src.jev_conf_metrics.definiciones import CONFIDENCES, conf_score  # noqa: E402
from src.jev_conf_metrics.metricas import ece  # noqa: E402

SELLADAS = ["pmax", "jev", "ent", "margin"]
TODAS = SELLADAS + ["score"]
DATASET = "sst5"          # único dataset con orden natural de niveles (5 niveles ordinales)


def _f(x, nd=3):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return "—" if v != v else f"{v:.{nd}f}"


def cargar(ruta):
    """Devuelve las confianzas (5 definiciones) y la corrección de cada fila del .jsonl."""
    filas = []
    with open(ruta, encoding="utf-8") as f:
        for linea in f:
            r = json.loads(linea)
            p = r.get("probs")
            if not p or len(p) < 2:
                continue
            confs = {n: fn(p) for n, fn in CONFIDENCES.items()}
            confs["score"] = conf_score(p)
            filas.append((confs, int(r.get("correct") or 0), r.get("model") or "?"))
    return filas


def resumen_grupo(filas):
    out = {"n": len(filas)}
    for d in TODAS:
        vals = [c[d] for c, _, _ in filas]
        out[f"mediana_{d}"] = statistics.median(vals)
        out[f"ece_{d}"] = ece(vals, [y for _, y, _ in filas], n_bins=15)
    brecha4 = [max(c[d] for d in SELLADAS) - min(c[d] for d in SELLADAS) for c, _, _ in filas]
    brecha5 = [max(c[d] for d in TODAS) - min(c[d] for d in TODAS) for c, _, _ in filas]
    for nombre, v in (("brecha4", brecha4), ("brecha5", brecha5)):
        v_ord = sorted(v)
        out[f"mediana_{nombre}"] = statistics.median(v)
        out[f"p90_{nombre}"] = v_ord[min(len(v_ord) - 1, int(round(0.9 * (len(v_ord) - 1))))]
        out[f"max_{nombre}"] = max(v)
    for d in SELLADAS:
        out[f"delta_medio_score_vs_{d}"] = statistics.fmean(
            abs(c["score"] - c[d]) for c, _, _ in filas)
    out["pct_score_max"] = 100.0 * sum(
        1 for c, _, _ in filas if c["score"] >= max(c[d] for d in SELLADAS)) / len(filas)
    out["pct_score_min"] = 100.0 * sum(
        1 for c, _, _ in filas if c["score"] <= min(c[d] for d in SELLADAS)) / len(filas)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--crudos", default=os.path.join(RAIZ, "results", "crudos"))
    ap.add_argument("--out", default=os.path.join(RAIZ, "results", "matrix"))
    args = ap.parse_args()

    grupos = {}
    for ruta in sorted(glob.glob(os.path.join(args.crudos, f"*{DATASET}.jsonl"))):
        filas = cargar(ruta)
        if not filas:
            continue
        modelo = filas[0][2]
        grupos[modelo] = resumen_grupo(filas)

    if not grupos:
        raise SystemExit(f"no hay crudos de `{DATASET}` en {args.crudos}")

    # ---------------- CSV ----------------
    cols = ["modelo", "n"] + [f"mediana_{d}" for d in TODAS] + [f"ece_{d}" for d in TODAS] + [
        "mediana_brecha4", "mediana_brecha5", "p90_brecha5", "max_brecha5",
        "delta_medio_score_vs_pmax", "delta_medio_score_vs_jev",
        "delta_medio_score_vs_ent", "delta_medio_score_vs_margin",
        "pct_score_max", "pct_score_min",
    ]
    csv_out = os.path.join(args.out, "extension_conf_score.csv")
    with open(csv_out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for modelo, r in sorted(grupos.items()):
            w.writerow({c: (modelo if c == "modelo" else r[c]) for c in cols})

    # ---------------- Informe ----------------
    total = sum(r["n"] for r in grupos.values())
    todas = []
    for ruta in sorted(glob.glob(os.path.join(args.crudos, f"*{DATASET}.jsonl"))):
        todas.extend(cargar(ruta))
    glob_ = resumen_grupo(todas)

    L = []
    L.append("# Extensión declarada — `conf_score` (MAD_unif), quinta definición del campo\n")
    L.append("> **Estatus:** extensión **posterior** al pre-registro `10.5281/zenodo.23266795` "
             "(19-oct-2026).\n> No modifica el nivel `raw` sellado, ni las filas crudas, ni "
             "`matriz_transferencia.csv`: se calcula\n> como post-proceso sobre `results/crudos/` y se "
             "publica en este informe aparte.\n")
    L.append("## 0. Qué se mide y qué no\n")
    L.append("| | |\n|---|---|")
    L.append(f"| Definición nueva | `confidence = max(0, 1 − Σᵢ pᵢ·\\|i − m\\| / MAD_unif)`, "
             f"`MAD_unif = (1/n)·Σᵢ \\|i − (n−1)/2\\|` |")
    L.append("| Origen | documentación oficial de TypeSafe (`docs.typesafe.ai/confidence`), "
             "verificada en vivo el 12-oct-2026 |")
    L.append(f"| Alcance | `{DATASET}` (5 niveles ordinales), 5 configuraciones de modelo, "
             f"**{total} decisiones** |")
    L.append("| Excluidos | `wanli`, `banking77`, `clinc150`, `typed-decisions`: sus etiquetas son "
             "**nominales**; la fórmula exige un orden y no se inventa la escala |")
    L.append("| No hace | no recalcula la matriz de transferencia, no re-mide con modelos, "
             "no toca el pre-registro |\n")

    L.append("## 1. ECE por definición (misma corrida, mismas 5 confianzas sobre la misma distribución)\n")
    L.append("| modelo | n | " + " | ".join(TODAS) + " |")
    L.append("|---|---|" + "---|" * len(TODAS))
    for modelo, r in sorted(grupos.items()):
        L.append(f"| `{modelo}` | {r['n']} | " + " | ".join(_f(r[f'ece_{d}']) for d in TODAS) + " |")
    L.append(f"| **global** | {glob_['n']} | " + " | ".join(_f(glob_[f'ece_{d}']) for d in TODAS) + " |\n")

    L.append("## 2. La quinta definición frente a las cuatro selladas (misma distribución)\n")
    L.append("| modelo | mediana `score` | Δ medio vs `pmax` | vs `jev` | vs `ent` | vs `margin` | "
             "% filas con `score` = máximo | % con `score` = mínimo |")
    L.append("|---|---|---|---|---|---|---|---|")
    for modelo, r in sorted(grupos.items()):
        L.append(f"| `{modelo}` | {_f(r['mediana_score'])} | "
                 f"{_f(r['delta_medio_score_vs_pmax'])} | {_f(r['delta_medio_score_vs_jev'])} | "
                 f"{_f(r['delta_medio_score_vs_ent'])} | {_f(r['delta_medio_score_vs_margin'])} | "
                 f"{_f(r['pct_score_max'], 1)} | {_f(r['pct_score_min'], 1)} |")
    L.append(f"| **global** | {_f(glob_['mediana_score'])} | "
             f"{_f(glob_['delta_medio_score_vs_pmax'])} | {_f(glob_['delta_medio_score_vs_jev'])} | "
             f"{_f(glob_['delta_medio_score_vs_ent'])} | {_f(glob_['delta_medio_score_vs_margin'])} | "
             f"{_f(glob_['pct_score_max'], 1)} | {_f(glob_['pct_score_min'], 1)} |\n")

    L.append("## 3. La brecha, con y sin la quinta definición\n")
    L.append("| subconjunto | mediana (4) | mediana (5) | p90 (5) | máx (5) |")
    L.append("|---|---|---|---|---|")
    L.append(f"| global | {_f(glob_['mediana_brecha4'])} | {_f(glob_['mediana_brecha5'])} | "
             f"{_f(glob_['p90_brecha5'])} | {_f(glob_['max_brecha5'])} |")
    for modelo, r in sorted(grupos.items()):
        L.append(f"| `{modelo}` | {_f(r['mediana_brecha4'])} | {_f(r['mediana_brecha5'])} | "
                 f"{_f(r['p90_brecha5'])} | {_f(r['max_brecha5'])} |")
    L.append("")
    L.append("### Cómo leerlo\n")
    L.append("1. Añadir una quinta definición **solo puede ampliar** la brecha de cada fila "
             "(el máximo sube o el mínimo baja); la columna `mediana (5)` es el número a citar si "
             "el texto describe el campo con cinco definiciones.")
    L.append("2. `conf_score` **no es** una versión de `conf_jev`: mide la dispersión alrededor del "
             "nivel modal, no la concentración en el máximo. Dos distribuciones con el mismo "
             "`p_max` dan valores distintos (`test_sensible_a_la_distancia_y_no_solo_al_maximo`).")
    L.append("3. Su ECE en esta corrida es la columna `score` de la tabla 1: comparable 1:1 con las "
             "otras cuatro porque se calcula sobre la misma corrida y la misma etiqueta de "
             "corrección.")
    L.append("4. La fórmula exige orden. Sobre un dataset nominal el índice `i` no significa nada: "
             "por eso la extensión se limita a `sst5` y se declara así en el paper.\n")
    L.append("## 4. Regeneración\n")
    L.append("```bash\n.venv/bin/python src/matriz/extension_conf_score.py\n```\n")
    L.append(f"Fuente: `results/crudos/*{DATASET}.jsonl` · semilla y folds del pre-registro intactos.\n")

    md_out = os.path.join(args.out, "EXTENSION_CONF_SCORE.md")
    with open(md_out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    print(f"OK  {csv_out}")
    print(f"OK  {md_out}")
    print(f"n = {total} decisiones · {len(grupos)} grupos · brecha mediana (4) = "
          f"{glob_['mediana_brecha4']:.4f} → (5) = {glob_['mediana_brecha5']:.4f}")
    print("ECE global: " + " · ".join(f"{d} {glob_[f'ece_{d}']:.3f}" for d in TODAS))


if __name__ == "__main__":
    main()
