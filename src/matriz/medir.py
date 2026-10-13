#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mide UN modelo sobre UN dataset y escribe `results/crudos/<modelo>__<dataset>.jsonl`.

Una fila por (modelo × dataset × ítem): la distribución COMPLETA devuelta, la etiqueta, el
acierto y las cuatro definiciones de `confidence` calculadas sobre la misma distribución (D4).

Los backends se importan de `src/paso0_go_no_go.py` (ya verificados contra los números
publicados de Laya): aquí NO se reimplementa la inferencia, solo se orquesta.

Modos
-----
  python src/matriz/medir.py --listar                       # qué adaptadores hay (sin GPU)
  python src/matriz/medir.py --dataset sst5 --inspeccionar  # carga 3 casos y los imprime
  python src/matriz/medir.py --model laya --subfolder none --dataset sst5 --limite 300
  python src/matriz/medir.py --model kev --dataset typed-decisions   # servidor en :8008
  python src/matriz/medir.py --model raw --model-id GestaltLabs/Jeff-1 --dataset wanli

Regla de recursos (autor, 08-oct-2026): si la RAM disponible baja de 1 GB, el guard aborta.
Un modelo en VRAM a la vez; el servidor de Kev se levanta solo para su bloque.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(AQUI)
RAIZ = os.path.dirname(SRC)
sys.path.insert(0, SRC)
sys.path.insert(0, AQUI)

from jev_conf_metrics.definiciones import all_confidences  # noqa: E402
from jev_conf_metrics.recursos import exigir_recursos, liberar  # noqa: E402

from adaptadores import AdaptadorNoDisponible, cargar, listar  # noqa: E402

# VRAM que necesita reservar ESTE proceso antes de cargar, en MiB.
# `kev` va por HTTP contra su propio servidor: el modelo ya está residente allí, así que este
# proceso no reserva nada (pedir 5 GB libres hacía que el guard abortara con el servidor vivo).
VRAM_ESTIMADA = {"laya": 1600, "kev": 0, "raw": 2600, "hf": 2600, "typesafe": 0}


def _backend(args):
    """Construye el backend reutilizando `build_backend` del paso 0 (no se duplica)."""
    from paso0_go_no_go import build_backend

    class _A:
        pass

    a = _A()
    a.model = "raw" if args.model == "hf" else args.model
    a.model_id = args.model_id
    a.subfolder = args.subfolder
    a.revision = args.revision
    a.device = args.device
    a.base_url = args.base_url
    a.presupuesto_usd = getattr(args, "presupuesto_usd", None)
    return build_backend(a)


def _fila(caso, qname, ans, gold_q):
    """Convierte una respuesta del backend en una fila del dataset de mediciones crudas.

    Tolera los DOS convenios de etiquetas del ecosistema: el modelo puede devolver los nombres
    de las opciones (control crudo) o índices `"0".."n-1"` con el mapa en `legend` (Laya en
    `score`). Se busca la etiqueta de oro en los nombres y, si no está, en las claves.
    """
    from paso0_go_no_go import _gold_dist, _normalize_answer, etiquetas_de

    dist = _normalize_answer(ans)
    if dist is None:
        return None
    claves, p = dist
    nombres = etiquetas_de(ans, claves)
    gold_label = str(gold_q.get("label"))
    if gold_label in nombres:
        labels = nombres
    elif gold_label in claves:
        labels = claves
    else:
        return None
    y = labels.index(gold_label)
    fila = {
        "id": caso["id"], "config": caso.get("config"), "workflow": caso.get("workflow"),
        "question": qname, "type": ans.get("type"),
        "labels": labels, "probs": p, "gold_label": gold_label, "y": y,
        "n_options": len(p),
        "correct": 1 if max(range(len(p)), key=lambda j: p[j]) == y else 0,
        "output_tokens": int((ans.get("usage") or {}).get("output_tokens", 0) or 0),
        # lo que el modelo REPORTA en su propio campo (auto-reportado; D4)
        "answer_confidence": ans.get("answer_confidence"),
        "confidence_reported": ans.get("confidence"),
        "act_probability": (ans.get("action") or {}).get("act_probability"),
        "gold_score": gold_q.get("score"), "pred_score": ans.get("score"),
        "gold_probs": _gold_dist(gold_q, labels),
    }
    fila.update({f"conf_{k}": v for k, v in all_confidences(p).items()})
    return fila


def nombre_de_modelo(info, backend_key=""):
    """Nombre del modelo que se registra en cada fila.

    Los tres checkpoints de Laya comparten `model_id`, así que sin el subfolder se pisarían
    entre sí en disco (fallo real detectado el 08-oct-2026: solo sobrevivía el último en
    escribirse). Se cualifica con el subfolder.
    """
    modelo = info.get("model_id") or info.get("model") or backend_key
    sub = info.get("subfolder")
    return f"{modelo}/{sub}" if sub else str(modelo)


def etiqueta_de(modelo, dataset, sufijo=""):
    """Nombre base de los artefactos de una corrida: `<modelo>__<dataset>`."""
    return f"{str(modelo).replace('/', '__')}__{dataset}{sufijo}"


def medir(backend, backend_key, dataset, limite, out_dir, info, sufijo=""):
    casos = cargar(dataset, limite=limite)
    if not casos:
        raise SystemExit(f"[medir] el adaptador {dataset} no devolvió casos")
    print(f"[medir] {len(casos)} casos de {dataset}", flush=True)

    filas, saltadas = [], 0
    t0 = time.time()
    for i, caso in enumerate(casos, 1):
        payload = backend.predict(caso["state"], caso["questions"])
        respuestas = payload.get("answers") or {}
        for qname, gold_q in caso["gold"].items():
            fila = _fila(caso, qname, respuestas.get(qname) or {}, gold_q)
            if fila is None:
                saltadas += 1
                continue
            filas.append(fila)
        if i % 25 == 0 or i == len(casos):
            vel = i / max(1e-9, time.time() - t0)
            print(f"  [{i}/{len(casos)}] filas={len(filas)} saltadas={saltadas} "
                  f"({vel:.1f} casos/s)", flush=True)

    if not filas:
        raise SystemExit(f"[medir] 0 filas para {dataset}: revisa el mapeo del adaptador")

    modelo = nombre_de_modelo(info, backend_key)
    etiqueta = etiqueta_de(modelo, dataset, sufijo)
    os.makedirs(out_dir, exist_ok=True)
    ruta = os.path.join(out_dir, f"{etiqueta}.jsonl")
    with open(ruta, "w", encoding="utf-8") as f:
        for r in filas:
            r["model"] = modelo
            r["model_revision"] = info.get("revision")
            r["dataset"] = dataset
            r["backend"] = backend_key
            r["row_hash"] = hashlib.sha256(
                json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()[:16]
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

    meta = {
        "modelo": modelo, "backend": backend_key, "dataset": dataset,
        "n_filas": len(filas), "n_saltadas": saltadas, "n_casos": len(casos),
        "backend_info": info,
        "cardinalidades": sorted({r["n_options"] for r in filas}),
        "accuracy": sum(r["correct"] for r in filas) / len(filas),
        "output_tokens_total": sum(r["output_tokens"] for r in filas),
        "ruta": os.path.relpath(ruta, RAIZ),
    }
    with open(os.path.join(out_dir, f"{etiqueta}.meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2, default=str)
    print(f"[medir] escrito {meta['ruta']} ({len(filas)} filas, "
          f"accuracy={meta['accuracy']:.4f}, n={meta['cardinalidades']})", flush=True)
    return meta


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mide un modelo sobre un dataset (matriz de transferencia)")
    ap.add_argument("--model", choices=["laya", "kev", "raw", "hf", "typesafe"], help="backend")
    ap.add_argument("--model-id", default=None, help="id HF (para --model raw/hf)")
    ap.add_argument("--subfolder", default="none", help="checkpoint de Laya")
    ap.add_argument("--revision", default=None, help="revisión/sha del Hub (se registra, D4)")
    ap.add_argument("--device", default=None, help="cuda | cpu | mps")
    ap.add_argument("--base-url", default="http://127.0.0.1:8008", help="servidor de Kev")
    ap.add_argument("--dataset", default=None, help="adaptador de dataset")
    ap.add_argument("--limite", type=int, default=400, help="nº máximo de casos")
    ap.add_argument("--presupuesto-usd", type=float, default=None,
                    help="tope de gasto con el backend typesafe (abraza la corrida al superarlo)")
    ap.add_argument("--out", default=os.path.join(RAIZ, "results", "crudos"))
    ap.add_argument("--listar", action="store_true", help="lista los adaptadores y sale")
    ap.add_argument("--inspeccionar", action="store_true", help="carga 3 casos y los imprime")
    args = ap.parse_args(argv)

    if args.listar:
        print("adaptadores:", ", ".join(listar()))
        return 0

    if args.inspeccionar:
        if not args.dataset:
            raise SystemExit("--inspeccionar necesita --dataset")
        try:
            casos = cargar(args.dataset, limite=3)
        except AdaptadorNoDisponible as e:
            print(f"[adaptador] NO DISPONIBLE: {e}")
            return 1
        print(f"{len(casos)} casos de {args.dataset}")
        c = casos[0]
        print("  id:", c["id"], "| config:", c.get("config"))
        print("  state:", c["state"][:200].replace("\n", " ⏎ "))
        for qn, q in c["questions"].items():
            print(f"  question {qn}: type={q.get('type')} n_opciones={len(q.get('criteria', []))}")
            print("    opciones[:6]:", q.get("criteria", [])[:6])
            print("    instructions:", str(q.get("instructions"))[:120])
        print("  gold:", c["gold"])
        return 0

    if not args.model or not args.dataset:
        ap.print_help()
        return 0

    exigir_recursos(vram_necesaria_mb=VRAM_ESTIMADA.get(args.model, 2000),
                    etiqueta=f" antes de cargar {args.model}")
    backend, key = _backend(args)
    info = backend.info
    print("[medir] backend:", json.dumps(info, ensure_ascii=False, default=str), flush=True)
    try:
        medir(backend, key, args.dataset, args.limite, args.out, info)
    finally:
        liberar(backend)
    return 0


if __name__ == "__main__":
    sys.exit(main())
