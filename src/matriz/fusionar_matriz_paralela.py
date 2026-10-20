#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fusiona los CSV parciales de la matriz paralela y **recalcula el FDR global**.

Por qué existe: `matriz.py` calcula `q_fdr` con Benjamini–Hochberg sobre **todas** las celdas de
la corrida. Si se parte el trabajo por grupos, cada parte corrige solo su subconjunto y los
q-valores quedan mal (se detectó el 20-oct-2026: 293 filas distintas y 1 `rechaza` distinto al
comparar la corrida serie contra la paralela). Este script reproduce el paso final de
`matriz.py` (líneas 319-335) sobre el conjunto ya fusionado: mismo `bh_fdr`, mismo redondeo a 6.

Uso:
    python src/matriz/fusionar_matriz_paralela.py results/matrix_pagado/partes \
           results/matrix_pagado/matriz_transferencia.csv
"""
from __future__ import annotations

import csv
import glob
import math
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)

from src.jev_conf_metrics.transferencia import bh_fdr  # noqa: E402


def main(partes_dir, destino):
    filas, cabecera = [], None
    for d in sorted(glob.glob(os.path.join(partes_dir, "*"))):
        if not os.path.isdir(d):
            continue
        ruta = os.path.join(d, "matriz_transferencia.csv")
        if not os.path.exists(ruta):
            continue
        with open(ruta, encoding="utf-8") as f:
            r = csv.DictReader(f)
            cabecera = cabecera or r.fieldnames
            filas.extend(list(r))
    if not filas:
        raise SystemExit(f"[merge] no hay partes en {partes_dir}")

    # --- FDR global, idéntico a matriz.py ---
    pvals = []
    for c in filas:
        try:
            p = float(c.get("p") or "nan")
        except ValueError:
            p = float("nan")
        pvals.append(p)
    ok = [p if not math.isnan(p) else 1.0 for p in pvals]
    rechaza, qvals = bh_fdr(ok, alpha=0.05)
    for c, rej, qv in zip(filas, rechaza, qvals):
        c["q_fdr"] = round(qv, 6)
        c["rechaza"] = rej

    with open(destino, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cabecera)
        w.writeheader()
        for c in filas:
            w.writerow({k: ("" if c.get(k) is None else c[k]) for k in cabecera})
    print(f"[merge] {len(filas)} filas, {len(set(c.get('rechaza') for c in filas))} valores de rechaza -> {destino}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
