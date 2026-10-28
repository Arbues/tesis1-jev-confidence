#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Auditoría: recalcular desde los artefactos TODO número que aparece en las figuras."""
import csv, glob, json, os, statistics, sys

RAIZ = "/home/arbues/paper-tesis1"
sys.path.insert(0, os.path.join(RAIZ, "src"))
from jev_conf_metrics.metricas import ece_laya

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return float("nan")

# ---------- 1. brecha (fig1 / Figura 2) ----------
brechas, ece, n_filas = [], {}, 0
for p in sorted(glob.glob(os.path.join(RAIZ, "results/crudos/*.jsonl"))):
    if os.path.basename(p).startswith("_"):
        continue
    with open(p, encoding="utf-8") as f:
        for linea in f:
            r = json.loads(linea)
            vals = [r.get(f"conf_{d}") for d in ("pmax", "jev", "ent", "margin")]
            if any(v is None for v in vals):
                continue
            n_filas += 1
            brechas.append(max(vals) - min(vals))
            k = f"{r['model']}|{r['dataset']}"
            g = ece.setdefault(k, {"n": 0, "pmax": [], "ent": []})
            g["n"] += 1
            g["pmax"].append((r["conf_pmax"], r["correct"]))
            g["ent"].append((r["conf_ent"], r["correct"]))

sb = sorted(brechas)
print("== FIG1 (Figura 2) ==")
print("n filas:", n_filas, "| n brechas:", len(brechas))
print("mediana %.4f  p90 %.4f  max %.4f" % (statistics.median(sb), sb[int(0.9 * len(sb))], sb[-1]))
print("masa exactamente en 0:", sum(1 for v in brechas if v == 0), "(%.1f%%)" % (100 * sum(1 for v in brechas if v == 0) / len(brechas)))

# ---------- 2. ECE (fig6 / Figura 8) ----------
print("\n== FIG6 (Figura 8) ECE laya-typed-decisions ==")
k = "convaiinnovations/laya/typed-decisions|typed-decisions"
g = ece[k]
ep = ece_laya([c for c, _ in g["pmax"]], [y for _, y in g["pmax"]])
ee = ece_laya([c for c, _ in g["ent"]], [y for _, y in g["ent"]])
print("n=%d  ECE pmax %.4f  ECE ent %.4f  factor %.2fx" % (g["n"], ep, ee, ee / ep))

# ---------- 3. matriz ----------
filas = list(csv.DictReader(open(os.path.join(RAIZ, "results/matrix/matriz_transferencia.csv"), encoding="utf-8")))
print("\n== matriz: filas totales", len(filas), "==")
con = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
print("celdas raw con mapa (todas las q):", len(con))
print("niveles:", sorted({r["nivel"] for r in filas}), "| q:", sorted({r["q"] for r in filas}))

def sin_empates(fs, u=0.05):
    return [r for r in fs if int(r["n_empates_tau"]) / (int(r["n_items_te"]) or 1) < u]

print("\n== FIG2 (Figura 3) ==")
subs = [("todas", con), ("sin empates", sin_empates(con)),
        ("sin control Qwen", [r for r in con if not str(r["modelo"]).startswith("Qwen")]),
        ("n>=3", [r for r in con if str(r["n"]) != "2"]),
        ("n=2", [r for r in con if str(r["n"]) == "2"])]
for nom, s in subs:
    d = sum(abs(num(r["delta"])) for r in s) / len(s)
    m = sum(abs(num(r["delta_mapa"])) for r in s) / len(s)
    print(f"  {nom:16s} n={len(s):4d}  dir={d:.4f}  mapa={m:.4f}  factor={d/m:.1f}x")

print("\n== FIG3/Figura 4 (scatter q=0.8) ==")
s3 = [r for r in con if abs(num(r["q"]) - 0.8) < 1e-9]
print("  celdas:", len(s3))
xs = [num(r["delta"]) for r in s3]; ys = [num(r["delta_mapa"]) for r in s3]
print("  Δdir rango: %.3f..%.3f | Δmapa rango: %.3f..%.3f" % (min(xs), max(xs), min(ys), max(ys)))
print("  |Δmapa|<0.01 en:", sum(1 for y in ys if abs(y) < 0.01), "/", len(ys))
print("  corr(dir,mapa): %.3f" % statistics.correlation(xs, ys))
print("  puntos en (0,0) exacto:", sum(1 for x, y in zip(xs, ys) if x == 0 and y == 0))

print("\n== FIG4/Figura 5 (por par) ==")
pares = {}
for r in con:
    pares.setdefault((r["A"], r["B"]), []).append(abs(num(r["delta"])))
for (a, b), v in sorted(pares.items(), key=lambda kv: statistics.median(kv[1])):
    print(f"  {a:>6s}->{b:<6s} n={len(v):3d} med={statistics.median(v):.4f} media={sum(v)/len(v):.4f}")

print("\n== FIG5/Figura 6 (cardinalidad) ==")
ns = sorted({int(r["n"]) for r in con})
for n in ns:
    v = [abs(num(r["delta"])) for r in con if int(r["n"]) == n]
    print(f"  n={n:4d} celdas={len(v):3d}  %<0.01={100*sum(1 for x in v if x<0.01)/len(v):5.1f}  med={statistics.median(v):.4f}")

print("\n== FIG7/Figura 1 (accuracy banking77) ==")
for p in sorted(glob.glob(os.path.join(RAIZ, "results/crudos/*.meta.json"))):
    m = json.load(open(p, encoding="utf-8"))
    if m["dataset"] == "banking77":
        print("  %-42s acc=%.4f n=%s" % (m["modelo"], m["accuracy"], m.get("n_items")))
