#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Paso 0 — go/no-go · Tesis 1, Ruta 1 (metrología del campo `confidence`).

Qué hace
--------
1. Descarga/verifica pesos abiertos (Laya 421M, Kev-0.8B) y registra versión + hash (D4).
2. Corre los primitivos `choice` / `score` / `noul` y verifica `output_tokens = 0`.
3. Reproduce un ECE publicado sobre `LocalLLaMA/typed-decisions` (card: 0.466 → 0.081 con refit;
   arXiv:2609.33843: 0.214 en el checkpoint tal cual).
4. Escribe los artefactos en `results/raw/` con versión + hash por fila.

Modos
-----
  python src/paso0_go_no_go.py --selftest        # valida la matemática (SOLO stdlib, corre en el t440)
  python src/paso0_go_no_go.py --inspect         # descubre la API real de Laya/Kev (red; sin GPU)
  python src/paso0_go_no_go.py --model laya --n 200
  python src/paso0_go_no_go.py --model kev --revision main

CÓMO CORRERLO
-------------
* El SELFTEST corre en cualquier máquina (el thinkpad-t440) porque usa solo la stdlib.
* El camino REAL (`--model ...`) exige GPU y red: córrelo en el **Acer Nitro** (RTX 4050) o el Mac Mini.
  Antes: `pip install -r src/requirements.txt` (en el Nitro).

D2: cero etiquetado propio — usa datasets ya etiquetados (typed-decisions, etc.).
"""

from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import math
import os
import random
import sys

# ======================================================================
#  1. DEFINICIONES DEL CAMPO `confidence`  (fieles al ecosistema; ver paper §3)
# ======================================================================

def conf_jev(p):
    """Jev 1.13: concentración, (n·pmax − 1)/(n − 1). NO es la probabilidad ganadora."""
    n = len(p)
    if n <= 1:
        return p[0] if p else 0.0
    return (n * max(p) - 1.0) / (n - 1.0)


def conf_ent(p):
    """Laya (choice/score): 1 − H(p)/log k  (entropía normalizada)."""
    n = len(p)
    if n <= 1:
        return 1.0
    h = -sum(pi * math.log(pi) for pi in p if pi > 0)
    return max(0.0, min(1.0, 1.0 - h / math.log(n)))


def conf_pmax(p):
    """Laya `answer_confidence` / jev-lite: la probabilidad ganadora."""
    return max(p)


def conf_margin(p):
    """Margen: p_(1) − p_(2)."""
    if len(p) < 2:
        return 1.0 if p else 0.0
    s = sorted(p, reverse=True)
    return s[0] - s[1]


def conf_noul(px):
    """Primitivo `noul` (binario): max(p, 1 − p)."""
    return max(px, 1.0 - px)


# nombre -> función sobre la distribución
CONFIDENCES = {
    "jev": conf_jev,
    "ent": conf_ent,       # Laya entropía
    "pmax": conf_pmax,
    "margin": conf_margin,
}


def all_confidences(p):
    """Calcula TODAS las definiciones sobre la misma distribución (el punto del trabajo)."""
    return {name: fn(p) for name, fn in CONFIDENCES.items()}


def order_equiv_affine_jev_pmax(n):
    """φ tal que C_jev = φ(C_max) con n fijo: φ(x) = (n·x − 1)/(n − 1). (Proposición 1.)"""
    return lambda x: (n * x - 1.0) / (n - 1.0)


# ======================================================================
#  2. MÉTRICAS  (stdlib)
# ======================================================================

def ece(confs, correct, n_bins=15, scheme="width"):
    """Expected Calibration Error. scheme='width' (igual ancho) o 'mass' (igual masa)."""
    if not confs:
        return 0.0
    pairs = list(zip(confs, correct))
    if scheme == "mass":
        pairs.sort(key=lambda t: t[0])
        chunks = [pairs[i * len(pairs) // n_bins:(i + 1) * len(pairs) // n_bins] for i in range(n_bins)]
    else:
        chunks = [[] for _ in range(n_bins)]
        for c, y in pairs:
            b = min(n_bins - 1, max(0, int(c * n_bins)))
            chunks[b].append((c, y))
    total, e = 0.0, 0.0
    for ch in chunks:
        if not ch:
            continue
        acc = sum(y for _, y in ch) / len(ch)
        conf = sum(c for c, _ in ch) / len(ch)
        e += (len(ch) / len(pairs)) * abs(acc - conf)
        total += len(ch)
    return e


def auroc(scores, labels):
    """AUROC con manejo de empates (Mann–Whitney U). labels: 1 = acierto."""
    pos = [s for s, y in zip(scores, labels) if y == 1]
    neg = [s for s, y in zip(scores, labels) if y == 0]
    if not pos or not neg:
        return float("nan")
    order = sorted(range(len(scores)), key=lambda i: scores[i])
    ranks = [0.0] * len(scores)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    r_pos = sum(ranks[i] for i in range(len(scores)) if labels[i] == 1)
    return (r_pos - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def brier_multi(probs, y):
    """Brier multiclase: media de Σ_k (p_ik − y_ik)²."""
    if not probs:
        return 0.0
    s = 0.0
    for p, yi in zip(probs, y):
        s += sum((p[k] - (1.0 if k == yi else 0.0)) ** 2 for k in range(len(p)))
    return s / len(probs)


def nll(probs, y):
    if not probs:
        return 0.0
    return -sum(math.log(max(p[yi], 1e-12)) for p, yi in zip(probs, y)) / len(probs)


# ======================================================================
#  3. VERSIONES Y HASHES  (D4)
# ======================================================================

def _sha256_file(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def model_revision_sha(model_id, revision=None):
    """Devuelve el SHA exacto del modelo en el Hub (para registrar la versión, D4)."""
    try:
        from huggingface_hub import HfApi
        info = HfApi().model_info(model_id, revision=revision)
        return info.sha
    except Exception as e:  # red o repo inexistente
        return f"UNKNOWN ({type(e).__name__}: {e})"


def record_versions(out_dir, entries):
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "paso0_versions.json")
    payload = {
        "fecha_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "maquina": os.uname().nodename if hasattr(os, "uname") else "unknown",
        "modelos": entries,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path


# ======================================================================
#  4. BACKENDS  (camino REAL — se finaliza en el Nitro; ver `--inspect`)
# ======================================================================

class BackendError(RuntimeError):
    pass


def _softmax(xs):
    m = max(xs)
    es = [math.exp(x - m) for x in xs]
    z = sum(es)
    return [e / z for e in es]


class LayaBackend:
    """Laya (convaiinnovations/laya, 421M) — PyPI `laya`.

    NOTA(API): la interfaz exacta del paquete `laya` (v0.3.20) debe confirmarse con
    `--inspect` en el Nitro. Aquí se deja el adaptador listo: solo hay que enchufar la
    llamada real que devuelve la distribución sobre las opciones en `probs()`.
    Adaptador genérico de respaldo: readout de logits de la última posición sobre los
    token-ids de cada opción (softmax restringido), que es la mecánica documentada de Jev/Laya.
    """

    def __init__(self, model_id="convaiinnovations/laya", revision=None, device=None):
        self.model_id = model_id
        self.revision = revision
        self.device = device
        self._ready = False

    def _lazy(self):
        if self._ready:
            return
        try:
            import laya  # noqa: F401  (PyPI: laya==0.3.20)
            self._laya = laya
        except Exception as e:
            raise BackendError(
                "No se pudo importar `laya`. En el Nitro: `pip install -r src/requirements.txt`.\n"
                "Luego corre `python src/paso0_go_no_go.py --inspect` para ver la API y completar este adaptador."
            ) from e
        self._ready = True

    def probs(self, question, options):
        """Devuelve la distribución sobre `options`. -> (list[float], meta)"""
        self._lazy()
        # TODO(API, 5 min en el Nitro tras --inspect): reemplazar por la llamada real, p.ej.
        #   out = self._laya.decide(question=question, options=options)   # <- nombre real por confirmar
        #   return list(out["probabilities"]), {"output_tokens": out.get("output_tokens", 0)}
        raise BackendError(
            "Adaptador Laya sin enchufar. Corre `--inspect` y completa Backend.probs() "
            "(la mecánica es readout de logits + softmax sobre las opciones)."
        )


class HFLogitBackend:
    """Backend genérico para LLMs causales (Kev = Qwen3.5/3.8, y otros).

    Readout de logits: se construye un prompt con las opciones etiquetadas y se leen los
    logits de la última posición para el token inicial de cada etiqueta, con softmax
    restringido a las opciones. `output_tokens = 0` porque NO se genera: solo se mira el logit.
    """

    def __init__(self, model_id="jaredpalmer/kev-0.8b", revision=None, device=None):
        self.model_id = model_id
        self.revision = revision
        self.device = device
        self._ready = False

    def _lazy(self):
        if self._ready:
            return
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except Exception as e:
            raise BackendError("Faltan torch/transformers: `pip install -r src/requirements.txt`.") from e
        self._torch = torch
        self.tok = AutoTokenizer.from_pretrained(self.model_id, revision=self.revision, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, revision=self.revision, trust_remote_code=True,
            torch_dtype="auto", device_map=self.device or "auto",
        ).eval()
        self._ready = True

    def probs(self, question, options):
        self._lazy()
        torch = self._torch
        # prompt con etiquetas (A, B, C, …) — el formato final se ajusta al model card en el Nitro.
        labels = [chr(ord("A") + i) for i in range(len(options))]
        prompt = f"{question}\n" + "\n".join(f"{l}. {o}" for l, o in zip(labels, options)) + "\nRespuesta:"
        ids = self.tok(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            logits = self.model(**ids).logits[0, -1]  # logits de la última posición (readout)
        opt_ids = [self.tok(" " + l, add_special_tokens=False)["input_ids"][0] for l in labels]
        probs = _softmax([float(logits[i]) for i in opt_ids])
        return probs, {"output_tokens": 0, "prompt_tokens": int(ids["input_ids"].shape[1])}


BACKENDS = {
    "laya": LayaBackend,
    "kev": HFLogitBackend,
}


# ======================================================================
#  5. PASO 0
# ======================================================================

def _synthetic_dataset(n=2000, seed=7, calibrated=True):
    """Dataset sintético para `--selftest`/`--mock`: repite la estructura (probs, y)."""
    rng = random.Random(seed)
    probs, y = [], []
    for _ in range(n):
        k = rng.randint(2, 6)
        raw = [rng.random() ** (1.0 if calibrated else 3.0) for _ in range(k)]
        s = sum(raw)
        p = [r / s for r in raw]
        probs.append(p)
        # etiqueta muestreada de p (calibrado por construcción) o argmax (sobre-confiado)
        if calibrated:
            r, acc = rng.random(), 0.0
            for i, pi in enumerate(p):
                acc += pi
                if r <= acc:
                    y.append(i)
                    break
            else:
                y.append(len(p) - 1)
        else:
            y.append(rng.randrange(k) if rng.random() > max(p) else max(range(k), key=lambda i: p[i]))
    return probs, y


def _step0_from_pairs(pairs, out_dir, model_id, revision, extra_meta=None):
    """pairs: list[(probs, y, output_tokens)]. Escribe mediciones crudas + resumen de ECE."""
    os.makedirs(out_dir, exist_ok=True)
    probs = [p for p, _, _ in pairs]
    ys = [y for _, y, _ in pairs]
    correct = [1 if (max(range(len(p)), key=lambda i: p[i]) == y) else 0 for p, y in zip(probs, ys)]
    out_tokens = [ot for _, _, ot in pairs]

    rows = []
    for (p, y, ot), c in zip(pairs, correct):
        row = {"probs": p, "y": y, "correct": c, "output_tokens": ot}
        row.update({f"conf_{k}": v for k, v in all_confidences(p).items()})
        rows.append(row)
    raw_path = os.path.join(out_dir, f"paso0_raw_{model_id.replace('/', '__')}.jsonl")
    with open(raw_path, "w", encoding="utf-8") as f:
        for r in rows:
            r["model"] = model_id
            r["model_revision"] = revision
            r["row_hash"] = hashlib.sha256(json.dumps(r, sort_keys=True).encode()).hexdigest()[:16]
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    summary = {"model": model_id, "revision": revision, "n": len(pairs),
               "output_tokens_total": sum(out_tokens),
               "accuracy": sum(correct) / len(correct) if correct else 0.0,
               "brier": brier_multi(probs, ys), "nll": nll(probs, ys)}
    for name in CONFIDENCES:
        cs = [r[f"conf_{name}"] for r in rows]
        summary[f"ece_{name}_width"] = ece(cs, correct, 15, "width")
        summary[f"ece_{name}_mass"] = ece(cs, correct, 15, "mass")
        summary[f"auroc_{name}"] = auroc(cs, correct)
    if extra_meta:
        summary.update(extra_meta)
    sum_path = os.path.join(out_dir, f"paso0_summary_{model_id.replace('/', '__')}.json")
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    return raw_path, sum_path, summary


def run_real(model_key, model_id, revision, n, out_dir):
    print(f"[paso0] modelos: cargando {model_id} (revision={revision}) …", flush=True)
    back = BACKENDS[model_key](model_id=model_id, revision=revision)

    # --- dataset real: `LocalLLaMA/typed-decisions` (Apache-2.0). Esquema a confirmar en el Nitro.
    try:
        from datasets import load_dataset
    except Exception as e:
        raise SystemExit("Falta `datasets`: pip install -r src/requirements.txt") from e
    ds = load_dataset("LocalLLaMA/typed-decisions", split="train")
    ds = ds.select(range(min(n, len(ds))))
    # TODO(Nitro): mapear los campos reales (question/options/answer) del dataset a (texto, opciones, índice).
    raise SystemExit(
        "Esqueleto listo. En el Nitro: (1) mapea los campos de typed-decisions, "
        "(2) completa Backend.probs(), (3) re-ejecuta. El pipeline, las métricas y los artefactos ya están hechos."
    )


def run_inspect():
    print("== API discovery (corre en el Nitro; sin GPU) ==")
    for mid in ("convaiinnovations/laya", "jaredpalmer/kev-0.8b"):
        print(f"\n--- {mid} ---")
        try:
            from huggingface_hub import HfApi
            info = HfApi().model_info(mid, files_metadata=True)
            print("sha:", info.sha)
            print("archivos:", [s.rfilename for s in (info.siblings or [])][:30])
        except Exception as e:
            print("  (no accesible:", type(e).__name__, e, ")")
    try:
        import laya
        print("\n== dir(laya) ==", [a for a in dir(laya) if not a.startswith("_")])
    except Exception as e:
        print("\n(laya no instalado:", type(e).__name__, ")")
    print("\nCon esto se completa `Backend.probs()` en src/paso0_go_no_go.py (5 minutos).")


# ======================================================================
#  6. SELFTEST — valida la matemática y las DOS proposiciones del marco teórico
# ======================================================================

def selftest():
    print("== SELFTEST (solo stdlib) ==")
    probs, ys = _synthetic_dataset(2000, seed=7, calibrated=True)
    correct = [1 if (max(range(len(p)), key=lambda i: p[i]) == y) else 0 for p, y in zip(probs, ys)]

    # --- todas las definiciones en [0,1]
    for p in probs:
        for k, v in all_confidences(p).items():
            assert 0.0 <= v <= 1.0 + 1e-9, (k, v, p)
    print("[ok] todas las definiciones caen en [0,1]")

    # --- Proposición 1: C_jev = φ(C_pmax), φ afín creciente  => transferencia EXACTA
    n0 = 3
    phi = order_equiv_affine_jev_pmax(n0)
    sample = [pp for pp in probs if len(pp) == n0][:500]
    for pp in sample:
        assert abs(conf_jev(pp) - phi(conf_pmax(pp))) < 1e-12
    print(f"[ok] Prop.1 verificada sobre {len(sample)} distribuciones n={n0}: C_jev = φ(C_pmax)")

    # --- Proposición 2: existen p, p' con mismo p_max y distinta entropía  => NO transferencia
    p_a = [0.6, 0.2, 0.2]
    p_b = [0.6, 0.4, 0.0]
    assert abs(max(p_a) - max(p_b)) < 1e-12 and abs(conf_ent(p_a) - conf_ent(p_b)) > 1e-6
    print(f"[ok] Prop.2: p_max igual (0.6), conf_ent distinto ({conf_ent(p_a):.3f} vs {conf_ent(p_b):.3f})")

    # --- Reproduce el ejemplo publicado: (0.0118, 0.4629, 0.5253)
    p_ex = [0.0118, 0.4629, 0.5253]
    print(f"[ejemplo publicado] Jev={conf_jev(p_ex):.3f} (0.288) · ent={conf_ent(p_ex):.3f} (0.320) "
          f"· pmax={conf_pmax(p_ex):.3f} (0.525)")

    # --- ECE, AUROC, Brier, NLL: rangos y coherencia
    cs = [conf_pmax(p) for p in probs]
    for name, val, lo, hi in [("ece_width", ece(cs, correct, 15, "width"), 0, 1),
                              ("ece_mass", ece(cs, correct, 15, "mass"), 0, 1),
                              ("auroc", auroc(cs, correct), 0, 1),
                              ("brier", brier_multi(probs, ys), 0, 2),
                              ("nll", nll(probs, ys), 0, 12)]:
        assert lo <= val <= hi, (name, val)
        print(f"[ok] {name} = {val:.4f}  (en rango)")

    # --- transferencia de umbral: el caso EXACTO (jev -> pmax) da cobertura idéntica
    #     C_jev = φ(C_pmax)  ⟺  C_jev ≥ τ ⟺ C_pmax ≥ φ⁻¹(τ)
    def coverage_tau(confs, tau):
        return sum(1 for c in confs if c >= tau) / len(confs)

    def phi_inv(x, n):
        return (x * (n - 1) + 1.0) / n

    c_jev = [conf_jev(p) for p in probs if len(p) == n0]
    c_pm = [conf_pmax(p) for p in probs if len(p) == n0]
    taus = sorted(c_jev)
    tau_jev = taus[int(0.2 * len(taus))]                 # umbral que da ~80% de cobertura en jev
    cov_jev = coverage_tau(c_jev, tau_jev)
    cov_pm = coverage_tau(c_pm, phi_inv(tau_jev, n0))    # el umbral espejo en pmax
    assert abs(cov_jev - cov_pm) < 1e-9, (cov_jev, cov_pm)
    print(f"[ok] transferencia EXACTA jev→pmax (n={n0}): cov={cov_jev:.4f} con τ_jev={tau_jev:.4f} "
          f"== cov={cov_pm:.4f} con φ⁻¹(τ)={phi_inv(tau_jev, n0):.4f}")

    # --- y el caso INCOMPATIBLE: entropía -> pmax, mismo τ, cobertura distinta (en general)
    taus_e = sorted(conf_ent(p) for p in probs if len(p) == n0)
    tau_e = taus_e[int(0.2 * len(taus_e))]
    cov_e_on_pm = coverage_tau(c_pm, tau_e)
    assert abs(cov_e_on_pm - 0.80) > 1e-3, cov_e_on_pm
    print(f"[ok] transferencia FALLIDA ent→pmax (n={n0}): τ_ent={tau_e:.3f} daría cobertura "
          f"{cov_e_on_pm:.3f} en pmax (≠ 0.80) — la matriz lo cuantifica")

    print("\nSELFTEST OK — la matemática del marco teórico es consistente.")
    return 0


# ======================================================================
#  7. CLI
# ======================================================================

def main(argv=None):
    ap = argparse.ArgumentParser(description="Paso 0 go/no-go — Tesis 1 Ruta 1")
    ap.add_argument("--model", choices=list(BACKENDS), help="modelo a correr (camino real; en el Nitro)")
    ap.add_argument("--model-id", default=None, help="override del id HF (por defecto el del backend)")
    ap.add_argument("--revision", default=None, help="revisión/sha del Hub (se registra, D4)")
    ap.add_argument("--n", type=int, default=200, help="nº de ítems a medir")
    ap.add_argument("--out", default="results/raw", help="carpeta de salida de artefactos")
    ap.add_argument("--selftest", action="store_true", help="valida la matemática (stdlib; corre sin GPU)")
    ap.add_argument("--mock", action="store_true", help="genera artefactos con datos sintéticos (sin GPU)")
    ap.add_argument("--inspect", action="store_true", help="descubre la API real de Laya/Kev (red; sin GPU)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if args.inspect:
        return run_inspect()
    if args.mock:
        probs, ys = _synthetic_dataset(args.n, seed=1, calibrated=False)
        pairs = [(p, y, 0) for p, y in zip(probs, ys)]
        mid = args.model_id or "mock/synthetic"
        raw, summ, s = _step0_from_pairs(pairs, args.out, mid, "mock",
                                         extra_meta={"nota": "datos sintéticos; NO son mediciones reales"})
        print(json.dumps(s, ensure_ascii=False, indent=2))
        print(f"\n[paso0] escritos: {raw}\n[paso0]           {summ}")
        return 0
    if args.model:
        defaults = {"laya": "convaiinnovations/laya", "kev": "jaredpalmer/kev-0.8b"}
        mid = args.model_id or defaults[args.model]
        rev = args.revision or model_revision_sha(mid)
        return run_real(args.model, mid, rev, args.n, args.out)

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
