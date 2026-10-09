#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera `results/matrix/RESUMEN_MATRIZ.md` a partir de la matriz y de los crudos.

Todos los números salen de los artefactos; ninguno se escribe a mano (misma disciplina que
`src/paso0_informe.py`). Es el documento que lee el redactor del paper en el t440.
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))
DEFS = ["pmax", "jev", "ent", "margin"]


def _f(x, nd=4):
    try:
        v = float(x)
    except (TypeError, ValueError):
        return "—"
    return "nan" if v != v else f"{v:.{nd}f}"


def leer_csv(ruta):
    with open(ruta, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def leer_metas(crudos_dir):
    metas = {}
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.meta.json"))):
        with open(p, encoding="utf-8") as f:
            m = json.load(f)
        metas[(m["modelo"], m["dataset"])] = m
    return metas


def dispersion_definiciones(crudos_dir, limite=2000):
    """Ilustración del objeto: cuánto se separan las 4 definiciones en la MISMA distribución."""
    import statistics
    rangos = []
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.jsonl"))):
        if os.path.basename(p).startswith("_"):
            continue
        with open(p, encoding="utf-8") as f:
            for i, linea in enumerate(f):
                if i >= limite:
                    break
                r = json.loads(linea)
                vals = [r.get(f"conf_{d}") for d in DEFS]
                if any(v is None for v in vals):
                    continue
                rangos.append(max(vals) - min(vals))
    if not rangos:
        return None
    return {"n": len(rangos), "mediana": statistics.median(rangos),
            "p90": sorted(rangos)[int(0.9 * len(rangos))], "max": max(rangos)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Informe legible de la matriz")
    ap.add_argument("--matriz", default=os.path.join(RAIZ, "results", "matrix",
                                                     "matriz_transferencia.csv"))
    ap.add_argument("--crudos", default=os.path.join(RAIZ, "results", "crudos"))
    ap.add_argument("--out", default=os.path.join(RAIZ, "results", "matrix", "RESUMEN_MATRIZ.md"))
    args = ap.parse_args(argv)

    if not os.path.exists(args.matriz):
        raise SystemExit(f"[informe] no existe {args.matriz}")
    filas = leer_csv(args.matriz)
    metas = leer_metas(args.crudos)
    resumen = {}
    rres = os.path.join(os.path.dirname(args.matriz), "resumen.json")
    if os.path.exists(rres):
        with open(rres, encoding="utf-8") as f:
            resumen = json.load(f)

    w = []
    w.append("# Matriz de transferencia de umbrales — resumen")
    w.append("")
    w.append(f"*Generado por `src/matriz/informe_matriz.py` desde `{os.path.relpath(args.matriz, RAIZ)}` "
             f"({len(filas)} celdas). No editar a mano: se regenera.*")
    w.append("")
    w.append("## 0. Qué mide esto")
    w.append("")
    w.append("Para cada par de definiciones `confidence` (A origen → B destino), cada modelo y cada "
             "dataset: se ajusta en calibración el umbral `τ_A` que da la cobertura objetivo `q`, se "
             "aplica **tal cual** a la definición B en prueba y se mide la cobertura real. "
             "`Δ(A→B) = q − cobertura_B`. Cero si el umbral viaja; grande si no.")
    w.append("")
    w.append("Dos portes por celda: **`delta`** (directo, lo que hace el ecosistema) y "
             "**`delta_mapa`** (con el mapa cerrado φ, cuando existe: misma clase y misma "
             "cardinalidad). Ver `docs/erratas_especificacion.md`.")
    w.append("")
    if resumen:
        w.append(f"Parámetros: `K={resumen.get('K')}` cross-fitting · "
                 f"`q={resumen.get('qs')}` · bootstrap `B={resumen.get('bootstrap')}` · "
                 f"niveles `{resumen.get('niveles')}` · BH-FDR α=0.05.")
        w.append("")

    # --- 1. grupos medidos
    w.append("## 1. Qué se midió")
    w.append("")
    w.append("| modelo | dataset | n | ítems | accuracy | tokens de salida |")
    w.append("|---|---|---|---|---|---|")
    for (modelo, ds), m in sorted(metas.items()):
        w.append(f"| `{modelo}` | {ds} | {m.get('cardinalidades')} | {m.get('n_filas')} | "
                 f"{_f(m.get('accuracy'))} | {m.get('output_tokens_total')} |")
    w.append("")

    # --- 2. el objeto
    disp = dispersion_definiciones(args.crudos)
    if disp:
        w.append("## 2. El objeto de la tesis, en una cifra")
        w.append("")
        w.append(f"Sobre **{disp['n']} distribuciones** medidas (una fila = una decisión), la "
                 f"diferencia entre la definición de `confidence` más alta y la más baja de la "
                 f"**misma** distribución tiene mediana **{disp['mediana']:.3f}**, percentil 90 "
                 f"**{disp['p90']:.3f}** y máximo **{disp['max']:.3f}**.")
        w.append("")

    # --- 3. Proposición 1 en los datos
    con_mapa = [r for r in filas if r["delta_mapa"] not in ("", None)]
    if con_mapa:
        peores = sorted(con_mapa, key=lambda r: -abs(float(r["delta_mapa"])))[:8]
        w.append("## 3. Proposición 1 en los datos (¿el mapa conserva la cobertura?)")
        w.append("")
        w.append(f"{len(con_mapa)} celdas tienen mapa cerrado (misma clase de equivalencia y misma "
                 f"cardinalidad). Las 8 con mayor desviación:")
        w.append("")
        w.append("| modelo | dataset | n | q | A → B | Δ directo | Δ con mapa |")
        w.append("|---|---|---|---|---|---|---|")
        for r in peores:
            w.append(f"| `{r['modelo']}` | {r['dataset']} | {r['n']} | {r['q']} | "
                     f"{r['A']} → {r['B']} | {_f(r['delta'])} | {_f(r['delta_mapa'])} |")
        w.append("")
        media_directo = sum(abs(float(r["delta"])) for r in con_mapa) / len(con_mapa)
        media_mapa = sum(abs(float(r["delta_mapa"])) for r in con_mapa) / len(con_mapa)
        w.append(f"Error absoluto medio del porte: **{media_directo:.4f}** directo contra "
                 f"**{media_mapa:.4f}** con mapa (factor {media_directo / max(1e-9, media_mapa):.1f}×).")
        w.append("")

    # --- 4. las celdas peligrosas
    principales = [r for r in filas if r["nivel"] == "raw" and abs(float(r["q"]) - 0.80) < 1e-9
                   and r["rechaza"] == "True"]
    if principales:
        peores = sorted(principales, key=lambda r: -abs(float(r["delta"])))[:12]
        w.append("## 4. Dónde el umbral NO viaja (nivel `raw`, q = 0.80, tras FDR)")
        w.append("")
        w.append("| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B | precisión A | precisión B |")
        w.append("|---|---|---|---|---|---|---|---|---|")
        for r in peores:
            w.append(f"| `{r['modelo']}` | {r['dataset']} | {r['n']} | {r['A']} → {r['B']} | "
                     f"{_f(r['delta'])} | [{_f(r['ic95_lo'], 3)}, {_f(r['ic95_hi'], 3)}] | "
                     f"{_f(r['cobertura_B'], 3)} | {_f(r['precision_A'], 3)} | {_f(r['precision_B'], 3)} |")
        w.append("")

    # --- 5. efecto de la cardinalidad
    w.append("## 5. Efecto de la cardinalidad n")
    w.append("")
    w.append("| n | celdas | \\|Δ\\| medio | celdas con FDR | dataset de ejemplo |")
    w.append("|---|---|---|---|---|")
    por_n = defaultdict(list)
    for r in filas:
        if r["nivel"] == "raw" and abs(float(r["q"]) - 0.80) < 1e-9:
            por_n[int(r["n"])].append(r)
    for n in sorted(por_n):
        celdas = por_n[n]
        medio = sum(abs(float(r["delta"])) for r in celdas) / len(celdas)
        sig = sum(1 for r in celdas if r["rechaza"] == "True")
        w.append(f"| {n} | {len(celdas)} | {medio:.4f} | {sig} | {celdas[0]['dataset']} |")
    w.append("")

    # --- 6. trazabilidad
    w.append("## 6. Trazabilidad (D4)")
    w.append("")
    w.append("| artefacto | qué contiene |")
    w.append("|---|---|")
    w.append("| `results/crudos/*.jsonl` | una fila por (modelo × dataset × ítem): distribución "
             "completa, etiqueta, acierto, las 4 definiciones y `row_hash` |")
    w.append("| `results/crudos/*.meta.json` | modelo, revisión del Hub, cardinalidades, accuracy |")
    w.append("| `results/matrix/matriz_transferencia.csv` | las celdas (A→B) × modelo × dataset × n × q × nivel |")
    w.append("| `results/matrix/resumen.json` | parámetros de la corrida (K, q, bootstrap, niveles) |")
    w.append("| `results/matrix/heatmap_*.png/pdf` | la figura central |")
    w.append("| `results/raw/paso0_*` | la reproducción del paso 0 (5 métricas publicadas, |Δ| ≤ 0.003) |")
    w.append("")
    w.append("Columna **medido aquí / auto-reportado**: en los crudos, `conf_*` son **medidos aquí** "
             "(calculados sobre la distribución devuelta) y `answer_confidence` / "
             "`confidence_reported` / `act_probability` son **auto-reportados** por el modelo. Las "
             "cifras de ECE de la tabla de calibración del ecosistema son **auto-reportadas** y no "
             "se usan en la matriz.")
    w.append("")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(w) + "\n")
    print(f"[informe] {args.out} ({len(w)} líneas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
