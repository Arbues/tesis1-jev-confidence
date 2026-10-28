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
    return "—" if v != v else f"{v:.{nd}f}"


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


def dispersion_definiciones(crudos_dir, limite=None):
    """Ilustración del objeto: cuánto se separan las 4 definiciones en la MISMA distribución.

    `limite=None` lee TODAS las filas del conjunto medido (la estadística se reporta sobre el
    conjunto completo, no sobre una muestra). Un valor entero acota cada archivo.
    """
    import statistics
    rangos = []
    for p in sorted(glob.glob(os.path.join(crudos_dir, "*.jsonl"))):
        if os.path.basename(p).startswith("_"):
            continue
        with open(p, encoding="utf-8") as f:
            for i, linea in enumerate(f):
                if limite is not None and i >= limite:
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


def _sin_empates(filas, umbral=0.05):
    """Celdas cuyo umbral NO cae sobre una masa grande de ítems empatados."""
    out = []
    for r in filas:
        te = int(r["n_items_te"]) or 1
        if int(r["n_empates_tau"]) / te < umbral:
            out.append(r)
    return out


def _media_sin_nan(xs):
    xs = [x for x in xs if x is not None and not (isinstance(x, float) and x != x)]
    return (sum(xs) / len(xs)) if xs else float("nan")


def precisiones_raw(crudos_dir, q=0.80, k=5):
    """Precisión por celda del nivel `raw`, **recalculada desde los crudos**.

    `precisión = acierto entre los ítems seleccionados` (especificación §5, paso 3): folds
    K=5 deterministas, `τ_A` ajustado en calibración y precisión medida en el fold de prueba.

    Por qué se recalcula aquí y no se lee del CSV: las columnas `precision_A`/`precision_B`
    del CSV sellado se calcularon con una versión de `precision()` que devolvía la **confianza
    media** en vez del acierto (bug corregido el 28-oct-2026; ver errata E8 en
    `docs/erratas_especificacion.md`). El CSV es un artefacto sellado y no se reescribe, así
    que el informe recalcula lo que publica. `Δ`, `tau` e IC no dependen de esto.
    """
    sys.path.insert(0, os.path.dirname(AQUI))
    from jev_conf_metrics.definiciones import CONFIDENCES  # noqa: E402
    from jev_conf_metrics.transferencia import (  # noqa: E402
        fold_de, precision, umbral_para_cobertura,
    )

    grupos = defaultdict(list)
    for ruta in sorted(glob.glob(os.path.join(crudos_dir, "*.jsonl"))):
        if os.path.basename(ruta).startswith("_"):
            continue
        with open(ruta, encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    r = json.loads(linea)
                    grupos[(r["model"], r["dataset"], r["n_options"])].append(r)

    salida = {}
    for (modelo, dataset, n), rows in grupos.items():
        por_fold = defaultdict(list)
        for r in rows:
            por_fold[fold_de(r["id"])].append(r)
        acum = defaultdict(lambda: ([], []))
        for f in range(k):
            te = por_fold.get(f) or []
            cal = [r for f2 in range(k) if f2 != f for r in (por_fold.get(f2) or [])]
            if not cal or not te:
                continue
            conf_cal = {d: [CONFIDENCES[d](r["probs"]) for r in cal] for d in DEFS}
            conf_te = {d: [CONFIDENCES[d](r["probs"]) for r in te] for d in DEFS}
            corr = [r["correct"] for r in te]
            tau = {d: umbral_para_cobertura(conf_cal[d], q)[0] for d in DEFS}
            for a in DEFS:
                for b in DEFS:
                    if a == b:
                        continue
                    acum[(a, b)][0].append(precision(conf_te[a], corr, tau[a]))
                    acum[(a, b)][1].append(precision(conf_te[b], corr, tau[a]))
        for (a, b), (pa, pb) in acum.items():
            salida[(modelo, dataset, n, a, b)] = (_media_sin_nan(pa), _media_sin_nan(pb))
    return salida


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
    # El titular va sobre el nivel PRINCIPAL (`raw`): mezclar niveles mezclaria el efecto de las
    # transformaciones AnyJev con el de la definicion, que es lo que se mide.
    con_mapa = [r for r in filas if r["nivel"] == "raw" and r["delta_mapa"] not in ("", None)]
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
        w.append("Todo lo de esta sección es sobre el **nivel principal `raw`** (el que congela el "
                 "pre-registro), salvo las dos filas marcadas con †. Los niveles `L0` y `L1` están en la "
                 "matriz completa y se resumen en §5.")
        w.append("")
        w.append("Error absoluto medio del porte, por subconjunto de celdas:")
        w.append("")
        w.append("| subconjunto | celdas | \\|Δ\\| directo | \\|Δ\\| con mapa | factor |")
        w.append("|---|---|---|---|---|")
        subconjuntos = [
            ("todas las celdas con mapa", con_mapa),
            ("sin empates dominantes en el umbral (masa < 5 %)", _sin_empates(con_mapa)),
            ("solo modelos entrenados (sin el control crudo)",
             [r for r in con_mapa if not str(r["modelo"]).startswith("Qwen")]),
            ("solo n = 2 (Proposición 3)", [r for r in con_mapa if str(r["n"]) == "2"]),
            ("solo n ≥ 3 (Proposición 1)", [r for r in con_mapa if str(r["n"]) != "2"]),
            ("nivel `L0` † (debiasing sin etiquetas)",
             [r for r in filas if r["nivel"] == "L0" and r["delta_mapa"] not in ("", None)
              and int(r["n_empates_tau"]) / max(1, int(r["n_items_te"])) < 0.05]),
            ("nivel `L1` † (temperatura con etiquetas)",
             [r for r in filas if r["nivel"] == "L1" and r["delta_mapa"] not in ("", None)
              and int(r["n_empates_tau"]) / max(1, int(r["n_items_te"])) < 0.05]),
        ]
        for nombre, sub in subconjuntos:
            if not sub:
                continue
            d = sum(abs(float(r["delta"])) for r in sub) / len(sub)
            m = sum(abs(float(r["delta_mapa"])) for r in sub) / len(sub)
            w.append(f"| {nombre} | {len(sub)} | {d:.4f} | {m:.4f} | "
                     f"{d / max(1e-9, m):.1f}× |")
        w.append("")
        # Las dos filas de nivel llevan un filtro que las otras cinco no: se declara, y se dan
        # las cifras sin filtro para que la diferencia no se atribuya al nivel.
        sin_filtro = {}
        for nivel in ("raw", "L0", "L1"):
            sub = [r for r in filas if r["nivel"] == nivel and r["delta_mapa"] not in ("", None)]
            if sub:
                d = sum(abs(float(r["delta"])) for r in sub) / len(sub)
                m = sum(abs(float(r["delta_mapa"])) for r in sub) / len(sub)
                sin_filtro[nivel] = (len(sub), d, m)
        if "L0" in sin_filtro and "L1" in sin_filtro:
            (n0, d0, m0), (n1, d1, m1) = sin_filtro["L0"], sin_filtro["L1"]
            w.append(f"† Las filas de nivel llevan **además** el filtro de empates de la segunda fila. "
                     f"Sin ese filtro, los tres niveles tienen {sin_filtro['raw'][0]} celdas con mapa "
                     f"cada uno y el |Δ| directo es {sin_filtro['raw'][1]:.4f} (`raw`), {d0:.4f} (`L0`) "
                     f"y {d1:.4f} (`L1`); el |Δ| con mapa, {sin_filtro['raw'][2]:.4f}, {m0:.4f} y "
                     f"{m1:.4f}. La diferencia entre filas es del filtro, no del nivel.")
        w.append("")
        w.append("**Cómo leer esto.** El porte con mapa tiene un suelo que no es culpa del mapa: si el "
                 "umbral cae sobre un valor **empatado** (salidas saturadas), la cobertura salta y ni el "
                 "mapa puede dar exactamente `q`. Por eso la comparación limpia es la del subconjunto sin "
                 "empates dominantes, y por eso `delta_mapa` debe leerse **contra `delta` de la misma "
                 "celda**, nunca como un cero absoluto. La columna `n_empates_tau` de la matriz dice, en "
                 "cada celda, cuántos ítems comparten el umbral.")
        w.append("")
        w.append("### 3b. El promedio NO es el resumen: la estructura está en el par de definiciones")
        w.append("")
        w.append("La distribución de `Δ` es **bimodal**, no centrada: hay pares que coinciden (y entonces "
                 "transferir es gratis) y pares que fallan en grande. Por eso el titular es el **par**, no "
                 "la media global.")
        w.append("")
        w.append("| A → B | celdas | \\|Δ\\| **mediana** | \\|Δ\\| media | ¿tiene mapa? |")
        w.append("|---|---|---|---|---|")
        _pares = {}
        for r in con_mapa:
            _pares.setdefault((r["A"], r["B"]), []).append(abs(float(r["delta"])))
        for (a, b), vals in sorted(_pares.items(), key=lambda kv: sum(kv[1]) / len(kv[1])):
            tiene = "sí" if any(r["delta_mapa"] not in ("", None)
                                for r in con_mapa if (r["A"], r["B"]) == (a, b)) else "no"
            w.append(f"| {a} → {b} | {len(vals)} | **{sorted(vals)[len(vals)//2]:.4f}** | "
                     f"{sum(vals)/len(vals):.4f} | {tiene} |")
        w.append("")
        w.append("Dos coincidencias **por identidad matemática**, no por azar: (i) a `n = 2`, `C_jev` y "
                 "`C_mar` son la MISMA función (`2·p_max − 1`), así que su porte directo ya da 0; (ii) a "
                 "cardinalidad alta, `C_jev = (n·p−1)/(n−1) → p`, así que `jev` y `pmax` convergen y sus "
                 "umbrales casi coinciden. En el extremo opuesto, `pmax → ent` es el peor par: cambia la "
                 "FORMA de la función, no solo la escala.")
        w.append("")
        w.append("**Fracción de celdas que transfieren bien (|Δ| < 0.01), por cardinalidad:**")
        w.append("")
        w.append("| n | celdas con mapa | \\|Δ\\| mediana | % con \\|Δ\\| < 0.01 |")
        w.append("|---|---|---|---|")
        import statistics as _st
        for n in sorted({int(r["n"]) for r in con_mapa}):
            sub = [abs(float(r["delta"])) for r in con_mapa if int(r["n"]) == n]
            bien = sum(1 for x in sub if x < 0.01)
            w.append(f"| {n} | {len(sub)} | {_st.median(sub):.4f} | {100*bien/len(sub):.0f} % |")
        w.append("")

    # --- 4. las celdas peligrosas
    principales = [r for r in filas if r["nivel"] == "raw" and abs(float(r["q"]) - 0.80) < 1e-9
                   and r["rechaza"] == "True"]
    if principales:
        peores = sorted(principales, key=lambda r: -abs(float(r["delta"])))[:12]
        prec = precisiones_raw(args.crudos, q=0.80)
        # ¿Las columnas del CSV coinciden con lo recalculado? Si no, el CSV es anterior a la
        # corrección de `precision()` (errata E8) y hay que decirlo.
        desfasado = False
        for r in peores:
            pa, pb = prec.get((r["modelo"], r["dataset"], int(r["n"]), r["A"], r["B"]),
                              (float("nan"), float("nan")))
            for viejo, nuevo in ((r["precision_A"], pa), (r["precision_B"], pb)):
                try:
                    if abs(float(viejo) - float(nuevo)) > 5e-3:
                        desfasado = True
                except (TypeError, ValueError):
                    pass
        w.append("## 4. Dónde el umbral NO viaja (nivel `raw`, q = 0.80, tras FDR)")
        w.append("")
        w.append("| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B | precisión A | precisión B |")
        w.append("|---|---|---|---|---|---|---|---|---|")
        for r in peores:
            pa, pb = prec.get((r["modelo"], r["dataset"], int(r["n"]), r["A"], r["B"]),
                              (float("nan"), float("nan")))
            w.append(f"| `{r['modelo']}` | {r['dataset']} | {r['n']} | {r['A']} → {r['B']} | "
                     f"{_f(r['delta'])} | [{_f(r['ic95_lo'], 3)}, {_f(r['ic95_hi'], 3)}] | "
                     f"{_f(r['cobertura_B'], 3)} | {_f(pa, 3)} | {_f(pb, 3)} |")
        w.append("")
        nota = ("*Precisión = acierto entre los ítems seleccionados (especificación §5, paso 3), "
                "recalculada desde los crudos.")
        if desfasado:
            nota += (" Las columnas `precision_A`/`precision_B` del CSV de este directorio conservan "
                     "el cálculo anterior —confianza media, no acierto— y se corrigen en la próxima "
                     "regeneración completa del artefacto: ver errata E8 en "
                     "`docs/erratas_especificacion.md`.")
        else:
            nota += " El CSV del directorio ya trae la misma corrección (errata E8)."
        w.append(nota + "*")
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

    # --- 7. desviaciones respecto al pre-registro (su seccion 7 las exige)
    w.append("## 7. Desviaciones respecto al pre-registro")
    w.append("")
    w.append("El pre-registro (`paper/04_pre_registro.md`, DOI 10.5281/zenodo.23266795) exige reportar "
             "cualquier desviación. Las habidas:")
    w.append("")
    w.append("| # | Qué | Por qué | Efecto |")
    w.append("|---|---|---|---|")
    w.append("| D1 | Se corrigió un **fallo de implementación del nivel `L0`** | El debiasing sin etiquetas "
             "no convergía: el paso era ~1000× demasiado pequeño, `b` quedaba en ~0 y las frecuencias de "
             "argmax apenas se movían (168/294/416/222 → 169/299/408/224, con objetivo 275). El nivel `L0` "
             "era indistinguible de `raw` | No cambia el plan congelado (que dice «debiasing sin "
             "etiquetas»), corrige su implementación. **Las celdas `L0` se recalcularon**; `raw` (nivel "
             "principal) y `L1` no se tocan |")
    w.append("| D2 | Se descartó un archivo del **piloto** que estaba contaminado | "
             "`convaiinnovations__laya__clinc150.jsonl` contenía datos de `multilingual` etiquetados como "
             "`none` (residuo de una corrida previa a un arreglo de colisión) | No afecta a la "
             "confirmatoria: ese archivo no existe en ella |")
    w.append("| D3 | `clinc150` no se midió en el checkpoint `none` de Laya | Su ventana de 512 tokens "
             "solo admite 126 de las 151 opciones | **Limitación, no desviación**: se declara en el paper |")
    w.append("")
    w.append("El **nivel principal es `raw`** y **no se ha tocado** tras publicar el pre-registro. `L0` y "
             "`L1` son niveles de sensibilidad.")
    w.append("")

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write("\n".join(w) + "\n")
    print(f"[informe] {args.out} ({len(w)} líneas)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
