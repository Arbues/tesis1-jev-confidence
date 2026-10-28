#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ECE por definición en los 23 grupos — dato de la nueva Fig. 8 (ver docs/plan-edicion-textual.md §6).

Recalcula el ECE con el binning exacto de Laya sobre las filas crudas ya medidas (post-proceso, sin GPU):
no re-mide nada, solo re-tabulá lo que está en `results/crudos/*.jsonl`.

Uso:  .venv/bin/python docs/auditoria-ece-por-grupo.py
"""
import collections
import glob
import json
import os
import statistics
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "src"))
from jev_conf_metrics.metricas import ece_laya  # noqa: E402

DEFS = ("pmax", "jev", "ent", "margin")


def main():
    grupos = collections.defaultdict(lambda: collections.defaultdict(list))
    for p in sorted(glob.glob(os.path.join(RAIZ, "results/crudos/*.jsonl"))):
        if os.path.basename(p).startswith("_"):
            continue
        with open(p, encoding="utf-8") as f:
            for linea in f:
                r = json.loads(linea)
                if any(r.get(f"conf_{d}") is None for d in DEFS):
                    continue
                k = (r["model"].split("/")[-1], r["dataset"])
                for d in DEFS:
                    grupos[k][d].append((r[f"conf_{d}"], r["correct"]))

    print(f"{'grupo':30s} {'n':>6s} {'pmax':>7s} {'jev':>7s} {'ent':>7s} {'margin':>7s}  spread  mejor")
    filas = []
    for k in sorted(grupos, key=lambda x: (x[1], x[0])):
        e = {d: ece_laya([c for c, _ in grupos[k][d]], [y for _, y in grupos[k][d]]) for d in DEFS}
        mn, mx = min(e, key=e.get), max(e, key=e.get)
        filas.append((k, e, mn, mx))
        print(f"{k[0][:16] + '|' + k[1]:30s} {len(grupos[k]['pmax']):6d} "
              f"{e['pmax']:7.3f} {e['jev']:7.3f} {e['ent']:7.3f} {e['margin']:7.3f}  "
              f"{e[mx] - e[mn]:6.3f}  {mn}")

    print(f"\ngrupos: {len(filas)}")
    spreads = [f[1][f[3]] - f[1][f[2]] for f in filas]
    print("spread (max − min entre definiciones): mediana %.3f · min %.3f · max %.3f"
          % (statistics.median(spreads), min(spreads), max(spreads)))
    print("definición que MINIMIZA el ECE:", collections.Counter(f[2] for f in filas))
    print("definición que MAXIMIZA el ECE:", collections.Counter(f[3] for f in filas))
    return 0


if __name__ == "__main__":
    sys.exit(main())
