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
  python src/paso0_go_no_go.py --selftest              # valida la matemática (SOLO stdlib, corre en el t440)
  python src/paso0_go_no_go.py --inspect               # descubre la API real de Laya/Kev (red; sin GPU)
  python src/paso0_go_no_go.py --model laya --n 100    # paso 0 real: Laya 421M sobre typed-decisions
  python src/paso0_go_no_go.py --model kev             # Kev servido en http://127.0.0.1:8008
  python src/paso0_go_no_go.py --model raw             # control: LLM crudo (readout de logits)

Entorno (uv; ver src/README.md):
  uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python -r src/requirements.txt

CÓMO CORRERLO
-------------
* El SELFTEST corre en cualquier máquina (el thinkpad-t440) porque usa solo la stdlib.
* El camino REAL (`--model ...`) exige GPU y red: córrelo en el **Acer Nitro** (RTX 4050) o el Mac Mini.
* `--subfolder`: `typed-decisions` (por defecto), `multilingual`, o `none` para el checkpoint inglés.

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


def ece_laya(confs, correct, bins=15):
    """ECE con el binning EXACTO del arnés de Laya (`laya.common.ece_score`).

    Se implementa aquí para poder comparar contra el número publicado (0.213 en
    `laya-typed-decisions`) sin que la diferencia de binning contamine la comparación.
    Bordes `linspace(0, 1, bins+1)`; el primer bin incluye su borde inferior.
    """
    if not confs:
        return float("nan")
    e = 0.0
    for i in range(bins):
        lo, hi = i / bins, (i + 1) / bins
        sel = [(c, y) for c, y in zip(confs, correct)
               if (c >= lo if i == 0 else c > lo) and c <= hi]
        if sel:
            mc = sum(c for c, _ in sel) / len(sel)
            ma = sum(y for _, y in sel) / len(sel)
            e += (len(sel) / len(confs)) * abs(mc - ma)
    return float(e)


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


def dataset_revision_sha(dataset_id, revision=None):
    """SHA del dataset en el Hub (los datasets usan `dataset_info`, no `model_info`)."""
    try:
        from huggingface_hub import HfApi
        info = HfApi().dataset_info(dataset_id, revision=revision)
        return info.sha
    except Exception as e:
        return f"UNKNOWN ({type(e).__name__}: {e})"


def record_versions(out_dir, entries):
    """Acumula versiones/hashes en `paso0_versions.json` (una entrada por modelo, D4).

    Se fusiona con lo ya escrito: cada corrida añade o reemplaza SU entrada y conserva las demás.
    """
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "paso0_versions.json")
    prev = {}
    if os.path.exists(path):
        try:
            with open(path, encoding="utf-8") as f:
                prev = json.load(f).get("modelos", {})
                if isinstance(prev, list):  # formato antiguo (lista): se descarta
                    prev = {}
        except Exception:
            prev = {}
    for e in entries:
        key = f"{e.get('backend')}:{e.get('model_id') or e.get('base_url')}:{e.get('subfolder')}"
        prev[key] = e
    payload = {
        "fecha_utc": _dt.datetime.now(_dt.timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "maquina": os.uname().nodename if hasattr(os, "uname") else "unknown",
        "modelos": prev,
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
    """Laya real — paquete `laya` (PyPI, Apache-2.0), API confirmada con `--inspect`.

        agent = laya.load("convaiinnovations/laya", subfolder="typed-decisions", device="cuda")
        out   = agent.predict(state, questions)          # payload `system_one`

    Forma del payload (verificada el 08-oct-2026 con laya 0.4.1):

        out["answers"][q]["type"]                 -> "choice" | "score" | "noul"
        out["answers"][q]["probabilities"]        -> {etiqueta: p}   (choice y score)
        out["answers"][q]["noul"]                 -> P(true)         (noul NO trae probabilities)
        out["answers"][q]["confidence"]           -> 1 - H(p)/log k  (entropía normalizada)
        out["answers"][q]["answer_confidence"]    -> max(p)
        out["answers"][q]["action"]["act_probability"] -> cabeza `act` (sin señal útil)
        out["usage"]["output_tokens"]             -> 0  (no genera texto)

    Las tres definiciones conviven en la MISMA respuesta: ese es el objeto de la Ruta 1.
    """

    def __init__(self, model_id="convaiinnovations/laya", subfolder="typed-decisions",
                 revision=None, device=None):
        self.model_id = model_id
        self.subfolder = subfolder
        self.revision = revision
        self.device = device
        self._ready = False

    def load(self):
        if self._ready:
            return
        try:
            import laya
        except Exception as e:
            raise BackendError(
                "No se pudo importar `laya`. Instálalo en el venv: `uv pip install laya`."
            ) from e
        kwargs = {}
        if self.subfolder:
            kwargs["subfolder"] = self.subfolder
        if self.revision:
            kwargs["revision"] = self.revision
        if self.device:
            kwargs["device"] = self.device
        self._agent = laya.load(self.model_id, **kwargs)
        self._laya = laya
        self._ready = True

    @property
    def info(self):
        self.load()
        cfg = getattr(self._agent, "cfg", {}) or {}
        return {
            "backend": "laya",
            "model_id": self.model_id,
            "subfolder": self.subfolder,
            "revision": getattr(self._agent, "revision", None) or self.revision,
            "hf_sha": model_revision_sha(self.model_id, self.revision),
            "device": str(getattr(self._agent, "device", self.device)),
            "cfg_model_name": cfg.get("model_name"),
            "temperature": cfg.get("temperature"),
            "temperature_by_options": cfg.get("temperature_by_options"),
            "fine_tuned": cfg.get("fine_tuned"),
        }

    def predict(self, state, questions):
        self.load()
        return self._agent.predict(state, questions)


class KevHTTPBackend:
    """Kev servido localmente (mismo contrato que la API System One de TypeSafe).

    Kev NO se carga con transformers: es un adaptador LoRA + una cabeza *pointer* sobre
    Qwen3.5-0.8B-Base, y se sirve desde su propio repositorio:

        git clone https://github.com/jaredpalmer/kev.git && cd kev
        uv sync --extra serve
        uv run --extra serve python -m kev.serve --run jaredpalmer/kev-0.8b --port 8008

    Este backend solo habla HTTP con ese servidor (stdlib, sin dependencias extra).
    """

    def __init__(self, base_url="http://127.0.0.1:8008", model="kev-latest", timeout=120,
                 repo_path=None):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.repo_path = repo_path or os.environ.get("KEV_REPO", os.path.expanduser("~/kev-serve"))

    def _repo_commit(self):
        """Commit del repo `kev` que sirve el modelo (D4: versión + hash por fila)."""
        try:
            import subprocess
            out = subprocess.run(["git", "-C", self.repo_path, "rev-parse", "HEAD"],
                                 capture_output=True, text=True, timeout=10)
            return out.stdout.strip() or None
        except Exception:
            return None

    @property
    def info(self):
        return {"backend": "kev-http", "base_url": self.base_url, "model": self.model,
                "model_id": "jaredpalmer/kev-0.8b",
                "hf_sha": model_revision_sha("jaredpalmer/kev-0.8b"),
                "repo_commit": self._repo_commit()}

    def predict(self, state, questions):
        import urllib.request
        body = json.dumps({"state": state, "questions": questions}).encode()
        req = urllib.request.Request(
            self.base_url + "/v1/systemone", data=body,
            headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            raise BackendError(
                f"No se pudo hablar con el servidor de Kev en {self.base_url} ({type(e).__name__}: {e}).\n"
                "Arráncalo con: uv run --extra serve python -m kev.serve --run jaredpalmer/kev-0.8b --port 8008"
            ) from e


class HFLogitBackend:
    """Control: LLM causal CRUDO (sin entrenar) con readout de logits sobre las etiquetas.

    NO sirve para Kev-0.8B (que usa cabeza pointer, no logits de etiqueta). Es el control
    "LLM crudo" del diseño de medición: la definición de `confidence` sin entrenamiento.
    """

    def __init__(self, model_id="Qwen/Qwen3.5-0.8B-Base", revision=None, device=None):
        self.model_id = model_id
        self.revision = revision
        self.device = device
        self._ready = False

    def load(self):
        if self._ready:
            return
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except Exception as e:
            raise BackendError("Faltan torch/transformers.") from e
        self._torch = torch
        self.tok = AutoTokenizer.from_pretrained(self.model_id, revision=self.revision,
                                                 trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, revision=self.revision, trust_remote_code=True,
            torch_dtype="auto", device_map=self.device or "auto",
        ).eval()
        self._ready = True

    @property
    def info(self):
        return {"backend": "hf-logit", "model_id": self.model_id}

    def predict(self, state, questions):
        self.load()
        torch = self._torch
        answers = {}
        for qname, q in questions.items():
            opts = list(q["criteria"]) if isinstance(q.get("criteria"), dict) else list(q.get("criteria", []))
            labels = [chr(ord("A") + i) for i in range(len(opts))]
            prompt = (f"{state}\n{q.get('instructions', qname)}\n"
                      + "\n".join(f"{l}. {o}" for l, o in zip(labels, opts)) + "\nRespuesta:")
            ids = self.tok(prompt, return_tensors="pt").to(self.model.device)
            with torch.no_grad():
                logits = self.model(**ids).logits[0, -1]
            opt_ids = [self.tok(" " + l, add_special_tokens=False)["input_ids"][0] for l in labels]
            probs = _softmax([float(logits[i]) for i in opt_ids])
            answers[qname] = {"type": q.get("type"), "probabilities": dict(zip(opts, probs))}
        return {"model": self.model_id, "answers": answers,
                "usage": {"output_tokens": 0}}


BACKENDS = {
    "laya": LayaBackend,
    "kev": KevHTTPBackend,
    "raw": HFLogitBackend,
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


def _normalize_answer(answer):
    """Convierte una respuesta del payload `system_one` en (labels, probs).

    `choice`/`score` traen `probabilities` (dict etiqueta -> p). `noul` NO: trae
    `noul` = P(true), así que se reconstruye [1-p, p] con las etiquetas [false, true].
    """
    if not isinstance(answer, dict):
        return None
    probs = answer.get("probabilities")
    if isinstance(probs, dict) and probs:
        labels = [str(k) for k in probs]
        return labels, [float(probs[k]) for k in labels]
    if answer.get("type") == "noul" and "noul" in answer:
        ptrue = float(answer["noul"])
        return ["false", "true"], [1.0 - ptrue, ptrue]
    return None


def _gold_dist(gold_q, labels):
    """Distribución del PROFESOR alineada a `labels`, o None si no está disponible.

    El ecosistema publica sus métricas contra la distribución completa del profesor, no contra
    la etiqueta: `soft accuracy` = Σ p_modelo·p_profesor y `Brier` = Σ (p_modelo − p_profesor)².
    Se replican las dos aquí para poder comparar contra los números publicados (D4).
    """
    gp = gold_q.get("probabilities")
    if isinstance(gp, dict) and gp:
        keys = [str(k) for k in gp]
        if keys == list(labels):
            return [float(gp[k]) for k in keys]
        if set(keys) == set(labels):
            return [float(gp[l]) for l in labels]
        return None
    if gold_q.get("type") == "noul" and "noul" in gold_q:
        ptrue = float(gold_q["noul"])
        return [1.0 - ptrue, ptrue] if list(labels) == ["false", "true"] else None
    return None


def _summarize(rows, scope):
    """Métricas de un conjunto de filas (una fila = un ítem de una pregunta)."""
    if not rows:
        return {"scope": scope, "n": 0}
    probs = [r["probs"] for r in rows]
    ys = [r["y"] for r in rows]
    correct = [r["correct"] for r in rows]
    out = {
        "scope": scope,
        "n": len(rows),
        "accuracy": sum(correct) / len(correct),
        "soft_accuracy": sum(r["probs"][r["y"]] for r in rows) / len(rows),
        "brier": brier_multi(probs, ys),
        "nll": nll(probs, ys),
        "output_tokens_total": sum(r["output_tokens"] for r in rows),
        "output_tokens_max": max(r["output_tokens"] for r in rows),
    }
    score_rows = [r for r in rows if r["type"] == "score" and r.get("gold_score") is not None]
    if score_rows:
        out["score_mae"] = sum(abs(r["gold_score"] - r["pred_score"]) for r in score_rows) / len(score_rows)
        out["n_score"] = len(score_rows)
    # --- métricas contra la distribución del PROFESOR (las que publica Laya) ---
    te = [(r["probs"], r["gold_probs"]) for r in rows if r.get("gold_probs")]
    if te:
        out["n_con_profesor"] = len(te)
        out["soft_accuracy_teacher"] = sum(sum(a * b for a, b in zip(p, g)) for p, g in te) / len(te)
        out["brier_teacher"] = sum(sum((a - b) ** 2 for a, b in zip(p, g)) for p, g in te) / len(te)
    # --- Brier binario sobre la confianza reportada (conf vs acierto) ---
    if all(r.get("answer_confidence") is not None for r in rows):
        out["brier_conf_binary"] = sum((r["answer_confidence"] - r["correct"]) ** 2 for r in rows) / len(rows)
    for name in CONFIDENCES:
        cs = [r[f"conf_{name}"] for r in rows]
        out[f"ece_{name}_laya"] = ece_laya(cs, correct, 15)
        out[f"ece_{name}_width"] = ece(cs, correct, 15, "width")
        out[f"ece_{name}_mass"] = ece(cs, correct, 15, "mass")
        out[f"auroc_{name}"] = auroc(cs, correct)
    # --- las definiciones tal cual las reporta el modelo en sus campos ---
    # (puede faltar en algunos tipos de pregunta: Kev no emite `confidence` en `noul`)
    ac = [(r["answer_confidence"], r["correct"]) for r in rows
          if r.get("answer_confidence") is not None]
    if ac:
        out["n_answer_confidence"] = len(ac)
        out["ece_answer_confidence_laya"] = ece_laya([a for a, _ in ac], [c for _, c in ac], 15)
        out["auroc_answer_confidence"] = auroc([a for a, _ in ac], [c for _, c in ac])
    cf = [(r["confidence_laya"], r["correct"]) for r in rows if r.get("confidence_laya") is not None]
    if cf:
        out["n_confidence_reported"] = len(cf)
        out["ece_confidence_reported_laya"] = ece_laya([a for a, _ in cf], [c for _, c in cf], 15)
        out["auroc_confidence_reported"] = auroc([a for a, _ in cf], [c for _, c in cf])
    return out


def _load_cases(configs, split, n_per_config):
    """Carga `LocalLLaMA/typed-decisions`: (state, questions, gold) por caso."""
    try:
        from datasets import load_dataset
    except Exception as e:
        raise SystemExit("Falta `datasets`: `uv pip install datasets`") from e
    cases = []
    for cfg in configs:
        ds = load_dataset("LocalLLaMA/typed-decisions", cfg, split=split)
        for i in range(min(n_per_config, len(ds))):
            row = ds[i]
            try:
                state = json.loads(row["state"])
            except Exception:
                state = row["state"]
            cases.append({
                "id": row["id"], "workflow": row["workflow"], "config": cfg,
                "state": state,
                "questions": json.loads(row["questions"]),
                "gold": json.loads(row["gold"]),
            })
    return cases


def run_real(backend, backend_key, n, out_dir, configs, split):
    """Paso 0 real: corre el modelo sobre typed-decisions y escribe los artefactos."""
    print(f"[paso0] backend={backend_key} · configs={configs} · split={split} · n/config={n}", flush=True)
    info = backend.info
    print("[paso0] backend info:", json.dumps(info, ensure_ascii=False, default=str), flush=True)

    cases = _load_cases(configs, split, n)
    print(f"[paso0] {len(cases)} casos, "
          f"{sum(len(c['gold']) for c in cases)} decisiones", flush=True)

    rows, skipped, usage_tot = [], 0, {}
    for i, c in enumerate(cases, 1):
        payload = backend.predict(c["state"], c["questions"])
        usage = payload.get("usage") or {}
        for k, v in usage.items():
            if isinstance(v, (int, float)):
                usage_tot[k] = usage_tot.get(k, 0) + int(v)
        answers = payload.get("answers") or {}
        for qname, gold_q in c["gold"].items():
            ans = answers.get(qname) or {}
            dist = _normalize_answer(ans)
            gold_label = str(gold_q.get("label"))
            if dist is None:
                skipped += 1
                continue
            labels, p = dist
            if gold_label not in labels:
                skipped += 1
                continue
            y = labels.index(gold_label)
            correct = 1 if max(range(len(p)), key=lambda j: p[j]) == y else 0
            row = {
                "id": c["id"], "workflow": c["workflow"], "config": c["config"],
                "question": qname, "type": ans.get("type"),
                "labels": labels, "probs": p, "gold_label": gold_label, "y": y,
                "correct": correct,
                "output_tokens": int(usage.get("output_tokens", 0) or 0),
                "answer_confidence": ans.get("answer_confidence"),
                "confidence_laya": ans.get("confidence"),
                "act_probability": (ans.get("action") or {}).get("act_probability"),
                "gold_score": gold_q.get("score"),
                "pred_score": ans.get("score"),
                "gold_probs": _gold_dist(gold_q, labels),
                "n_options": len(p),
            }
            row.update({f"conf_{k}": v for k, v in all_confidences(p).items()})
            rows.append(row)
        if i % 25 == 0 or i == len(cases):
            print(f"  [{i}/{len(cases)}] filas={len(rows)} saltadas={skipped}", flush=True)

    if not rows:
        raise SystemExit("[paso0] no se produjo ninguna fila: revisa el mapeo del dataset")

    os.makedirs(out_dir, exist_ok=True)
    sub = info.get("subfolder") or "english"
    tag = f"{backend_key}_{info.get('model') or sub if backend_key == 'kev' else sub}"
    raw_path = os.path.join(out_dir, f"paso0_raw_{tag}.jsonl")
    with open(raw_path, "w", encoding="utf-8") as f:
        for r in rows:
            r["backend"] = backend_key
            r["model"] = info.get("model_id", info.get("model"))
            r["model_revision"] = info.get("revision")
            r["row_hash"] = hashlib.sha256(
                json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()[:16]
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")

    summary = {
        "backend": backend_key, "backend_info": info,
        "dataset": "LocalLLaMA/typed-decisions", "configs": configs, "split": split,
        "dataset_sha": dataset_revision_sha("LocalLLaMA/typed-decisions"),
        "n_cases": len(cases), "n_rows": len(rows), "n_skipped": skipped,
        "usage_total": usage_tot,
        "output_tokens_ok": all(r["output_tokens"] == 0 for r in rows),
        "global": _summarize(rows, "global"),
        "by_question": {q: _summarize([r for r in rows if r["question"] == q], q)
                        for q in sorted({r["question"] for r in rows})},
        "by_config": {c: _summarize([r for r in rows if r["config"] == c], c)
                      for c in sorted({r["config"] for r in rows})},
    }
    sum_path = os.path.join(out_dir, f"paso0_summary_{tag}.json")
    with open(sum_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2, default=str)

    record_versions(out_dir, [{"backend": backend_key, **info,
                               "dataset_sha": summary["dataset_sha"]}])
    print("\n" + json.dumps(summary["global"], ensure_ascii=False, indent=2, default=str))
    print(f"\n[paso0] escritos:\n  {raw_path}\n  {sum_path}")
    print(f"[paso0] output_tokens == 0 en todas las filas: {summary['output_tokens_ok']}")
    return 0


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

    # --- T6 / Proposición 3: con n=2 las CINCO definiciones ordenan igual => transferencia exacta
    def _rank(confs):
        order = sorted(range(len(confs)), key=lambda i: confs[i])
        r = [0] * len(confs)
        for pos, idx in enumerate(order):
            r[idx] = pos
        return r

    pis = [0.5 + 0.5 * i / 999 for i in range(1000)]
    p2 = [[x, 1.0 - x] for x in pis]
    defs2 = {
        "pmax": [conf_pmax(p) for p in p2],
        "jev": [conf_jev(p) for p in p2],
        "ent": [conf_ent(p) for p in p2],
        "mar": [conf_margin(p) for p in p2],
        "noul": [conf_noul(x) for x in pis],
    }
    base = _rank(defs2["pmax"])
    for k, v in defs2.items():
        assert _rank(v) == base, k
    print("[ok] T6/Prop.3 (n=2): las 5 definiciones ordenan idéntico -> transferencia EXACTA")

    # --- T8: `noul` simétrico y nunca por debajo de 0.5
    for x in pis:
        assert abs(conf_noul(x) - conf_noul(1.0 - x)) < 1e-12
        assert conf_noul(x) >= 0.5 - 1e-12
    print("[ok] T8: C_noul simétrico (C(π)=C(1−π)) y >= 0.5")

    print("\nSELFTEST OK — la matemática del marco teórico es consistente.")
    return 0


# ======================================================================
#  7. CLI
# ======================================================================

def build_backend(args):
    """Construye el backend según los argumentos de la CLI."""
    device = args.device
    if device is None:
        try:
            import torch
            device = "cuda" if torch.cuda.is_available() else "cpu"
        except Exception:
            device = "cpu"
    if args.model == "laya":
        sub = None if args.subfolder in ("none", "", "english") else args.subfolder
        return LayaBackend(model_id=args.model_id or "convaiinnovations/laya",
                           subfolder=sub, revision=args.revision, device=device), "laya"
    if args.model == "kev":
        return KevHTTPBackend(base_url=args.base_url), "kev"
    if args.model == "raw":
        return HFLogitBackend(model_id=args.model_id or "Qwen/Qwen3.5-0.8B-Base",
                              revision=args.revision, device=device), "raw"
    raise SystemExit(f"backend desconocido: {args.model}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Paso 0 go/no-go — Tesis 1 Ruta 1")
    ap.add_argument("--model", choices=list(BACKENDS), help="backend a correr (laya | kev | raw)")
    ap.add_argument("--model-id", default=None, help="override del id HF")
    ap.add_argument("--subfolder", default="typed-decisions",
                    help="checkpoint de Laya: typed-decisions | multilingual | none (english)")
    ap.add_argument("--revision", default=None, help="revisión/sha del Hub (se registra, D4)")
    ap.add_argument("--device", default=None, help="cuda | cpu | mps (por defecto: autodetecta)")
    ap.add_argument("--base-url", default="http://127.0.0.1:8008", help="servidor de Kev (backend kev)")
    ap.add_argument("--split", default="test", help="split de typed-decisions: test | train")
    ap.add_argument("--configs", default="agent_trace_observability,customer_service,"
                                         "invoice_processing,security_incidents",
                    help="configs de typed-decisions (separadas por coma) o 'all'")
    ap.add_argument("--n", type=int, default=200, help="nº de casos (filas del dataset) por config")
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
        configs = args.configs.split(",") if args.configs != "all" else [
            "agent_trace_observability", "customer_service", "invoice_processing", "security_incidents"]
        backend, key = build_backend(args)
        return run_real(backend, key, args.n, args.out, configs, args.split)

    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
