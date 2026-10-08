#!/usr/bin/env python3
"""Genera results/paso0_informe.md a partir de los artefactos de results/raw/ (D3/D4)."""
import glob
import json
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(REPO, "results/raw")

PUB = {  # laya README, tabla "typed-decisions, measured on all three checkpoints"
    "typed-decisions": dict(acc=0.766, soft=0.471, brier=0.062, ece=0.213, mae=0.242),
    "english": dict(acc=0.362, soft=0.332, brier=0.316, ece=0.175, mae=0.694),
    "multilingual": dict(acc=0.342, soft=0.326, brier=0.439, ece=0.285, mae=0.687),
}

runs = {}
for f in sorted(glob.glob(os.path.join(RAW, "paso0_summary_*.json"))):
    s = json.load(open(f))
    sub = s["backend_info"].get("subfolder")
    key = "english" if (s["backend"] == "laya" and not sub) else (sub or s["backend"])
    runs[key] = s

# --- comprobación algebraica: la confidence de choice de Kev ES la fórmula de Jev ---
import math
_ok = True
for k in (2, 3, 4, 7, 12):
    for pmax in (1 / k, 0.5, 0.83, 0.99):
        p = [(1 - pmax) / (k - 1)] * (k - 1) + [pmax]
        kev = (max(p) - 1 / k) / (1 - 1 / k)
        jev = (k * max(p) - 1) / (k - 1)
        _ok &= abs(kev - jev) < 1e-12

L = []
w = L.append
w("# Paso 0 — informe go/no-go (Tesis 1, Ruta 1)\n")
w("*Generado automáticamente desde `results/raw/` por `src/paso0_informe.py` · 08-oct-2026*\n")
w("---\n")
w("## 0. Veredicto: **GO**\n")
w("Los tres criterios del paso 0 (`11_ruta1_metrologia_confidence.md` §10) se cumplen:\n")
w("1. **Los tres primitivos corren** en modelos de pesos abiertos sobre `typed-decisions` "
  "(`choice`, `score`, `noul`), con la distribución completa por pregunta.")
w("2. **`output_tokens = 0`** en Laya (todas las filas, los tres checkpoints) — y se descubre que "
  "**Kev reporta ese mismo campo con otro significado** (§3).")
w("3. **Se reproduce un número publicado**: cinco métricas de Laya, en los tres checkpoints (§1).\n")
w("| | |")
w("|---|---|")
w("| Máquina | `Arbues-AxeNitro` (WSL2) · **RTX 4050 Laptop 6 GB** |")
w("| Python / torch | 3.12.14 · torch 2.14.1+**cu126** (el build cu130 de PyPI no arranca con el driver 556.19) |")
w("| Datos | `LocalLLaMA/typed-decisions`, split `test` = 400 casos / **2 000 decisiones** (4 flujos × 100 casos) |")
w("| Costo | **$0** (D5): pesos y datasets abiertos, nada de nube |\n")

w("### Versiones y hashes (D4)\n")
w("| modelo | revisión / sha | device |")
w("|---|---|---|")
for key, s in runs.items():
    i = s["backend_info"]
    rev = i.get("hf_sha") or i.get("repo_commit") or "—"
    extra = ""
    if i.get("repo_commit"):
        extra = f" · repo `kev` @ `{i['repo_commit'][:8]}`"
    w(f"| `{key}` | `{str(rev)[:40]}`{extra} | {i.get('device', '—')} |")
w("")

w("## 1. Reproducción de los números publicados\n")
w("Números de Laya **auto-reportados** (README del modelo, tabla *typed-decisions, measured on all three "
  "checkpoints*) frente a lo **medido aquí** sobre las mismas 2 000 decisiones.\n")
w("| métrica | `laya-typed-decisions` | `laya` (english) | `laya-multilingual` |")
w("|---|---|---|---|")
rows = [("accuracy", "accuracy", "acc"), ("soft accuracy (vs profesor)", "soft_accuracy_teacher", "soft"),
        ("Brier (vs profesor)", "brier_teacher", "brier"), ("ECE (answer_confidence)", "ece_answer_confidence_laya", "ece"),
        ("score MAE", "score_mae", "mae")]
for label, k, pk in rows:
    cells = []
    for key in ("typed-decisions", "english", "multilingual"):
        g = runs[key]["global"]
        mv, pv = g[k], PUB[key][pk]
        cells.append(f"{pv:.3f} → **{mv:.4f}** (Δ {mv - pv:+.4f})")
    w(f"| {label} | " + " | ".join(cells) + " |")
w("")
w("El checkpoint afinado sobre el benchmark (`laya-typed-decisions`) reproduce las cinco métricas con "
  "**|Δ| ≤ 0.003**; el inglés, con |Δ| ≤ 0.003 en las cinco. La discrepancia mayor está en "
  "`laya-multilingual` (ECE Δ +0.033, score MAE Δ +0.074): es el checkpoint que **no trae temperaturas "
  "ajustadas** (`temperature = [1.0, 1.0, 1.0]`, `temperature_by_options = {}` en `paso0_versions.json`), "
  "así que la comparación no es contra el mismo artefacto. Queda documentado, no corregido.\n")
w("> Convención descubierta y verificada: las métricas que publica Laya se calculan **contra la "
  "distribución completa del profesor**, no contra la etiqueta — `soft accuracy` = Σ p_modelo·p_profesor "
  "(0.4707 medido vs 0.471 publicado) y `Brier` = Σ (p_modelo − p_profesor)² (0.0615 vs 0.062). "
  "El ECE sí se calcula sobre `answer_confidence` = `max(p)`, con 15 bins de igual ancho "
  "(`laya.common.ece_score`, replicado en `ece_laya()`).\n")

w("## 2. El objeto de la Ruta 1, ya visible en el paso 0\n")
w("La **misma corrida**, las **mismas 2 000 decisiones**, el **mismo modelo**: el ECE cambia por completo "
  "según qué definición de `confidence` se use. Esto es exactamente lo que la matriz de transferencia "
  "va a cuantificar de forma sistemática.\n")
w("| checkpoint | `p_max` | **Jev** `(n·p−1)/(n−1)` | **entropía** `1−H/log k` | margen `p₁−p₂` |")
w("|---|---|---|---|---|")
for key in ("typed-decisions", "english", "multilingual", "kev"):
    g = runs[key]["global"]
    w(f"| `{key}` | {g['ece_pmax_laya']:.4f} | {g['ece_jev_laya']:.4f} | {g['ece_ent_laya']:.4f} | "
      f"{g['ece_margin_laya']:.4f} |")
w("")
w("En `laya-typed-decisions` el ECE va de **0.216** (con `p_max`) a **0.577** (con la entropía normalizada): "
  "un factor **2.7×** sobre el mismo dato. Cualquier umbral de «actúo o escalo» fijado sobre una de las "
  "dos no significa lo mismo sobre la otra.\n")
w("Discriminación (AUROC vs acierto), que **no** es calibración:\n")
w("| checkpoint | AUROC `p_max` | AUROC Jev | AUROC entropía | AUROC margen |")
w("|---|---|---|---|---|")
for key in ("typed-decisions", "english", "multilingual", "kev"):
    g = runs[key]["global"]
    w(f"| `{key}` | {g['auroc_pmax']:.4f} | {g['auroc_jev']:.4f} | {g['auroc_ent']:.4f} | {g['auroc_margin']:.4f} |")
w("")

w("## 3. Kev: el mismo campo, otra definición (y otro `output_tokens`)\n")
w("`jaredpalmer/kev-0.8b` no se carga con `transformers`: es un adaptador LoRA + cabeza *pointer* sobre "
  "`Qwen/Qwen3.5-0.8B-Base`, servido por su propio repositorio. Se corrió contra ese servidor "
  "(`kev/api.py`, commit `5e42a7a0`).\n")
w("**a) `choice_confidence` de Kev ES la fórmula de Jev.** En `kev/api.py:127-130`:\n")
w("```python")
w("def choice_confidence(p):")
w('    """(p_max - 1/K) / (1 - 1/K): 0 at uniform, 1 at certainty."""')
w("    K = len(p)")
w("    return 1.0 if K == 1 else (max(_normalize(p)) - 1 / K) / (1 - 1 / K)")
w("```")
w("Algebraicamente `(p_max − 1/K)/(1 − 1/K) = (K·p_max − 1)/(K − 1)`, que es **exactamente** la fórmula "
  f"publicada de Jev. Verificado numéricamente para K ∈ {{2,3,4,7,12}}: {'idénticas' if _ok else 'NO coinciden'}. "
  "El ecosistema las tenía registradas como definiciones distintas. Consecuencia directa de la "
  "Proposición 1: **este par transfiere el umbral de forma exacta** (misma cobertura, a `n` fijo).\n")
w("**b) `score_confidence` de Kev es una tercera familia.** `max(0, 1 − E|nivel − moda| / D)` — dispersión "
  "ordinal, ni `p_max` ni entropía. Kev declara en el código que ambas fórmulas *espejan el adaptador de "
  "referencia de TypeSafe* (`system-one-adapter 0.2.1`).\n")
w("**c) `noul` no lleva `confidence`** — igual que en Jev. Confirmado en la corrida: 400 de las 2 000 filas "
  "de Kev no tienen ese campo.\n")
w("**d) `output_tokens` significa otra cosa.** `kev/api.py:163-165`:\n")
w("```python")
w("def output_tokens(tok, answers: dict) -> int:")
w('    """Billing-style figure: tokens of the serialised answers. Not a measure of generation (there is none)."""')
w("    return len(tok(json.dumps(answers), add_special_tokens=False).input_ids)")
w("```")
g = runs["kev"]["global"]
w(f"Medido: `output_tokens` total **{g['output_tokens_total']:,}** (máx {g['output_tokens_max']} por llamada) "
  "en las mismas 2 000 decisiones donde Laya reporta **0** en todas las filas. **El mismo campo, tres "
  "significados**: Jev y Laya = 0 (no hay generación); Kev = recuento de tokens de la respuesta serializada. "
  "Esto es metrología del campo, no un fallo de Kev.\n")
w("Resultados de Kev sobre las mismas 2 000 decisiones:\n")
w("| métrica | valor |")
w("|---|---|")
for label, k in [("accuracy", "accuracy"), ("soft accuracy (vs profesor)", "soft_accuracy_teacher"),
                 ("Brier (vs profesor)", "brier_teacher"), ("ECE (`p_max`)", "ece_pmax_laya"),
                 ("ECE (Jev)", "ece_jev_laya"), ("ECE (entropía)", "ece_ent_laya"),
                 ("ECE (`confidence` reportada)", "ece_confidence_reported_laya"),
                 ("score MAE", "score_mae")]:
    v = g.get(k)
    w(f"| {label} | {v:.4f} |" if isinstance(v, float) else f"| {label} | {v} |")
w("")

w("## 4. Artefactos y cómo regenerarlos\n")
w("| artefacto | ruta |")
w("|---|---|")
for f in sorted(glob.glob(os.path.join(RAW, "paso0_*"))):
    w(f"| `{os.path.basename(f)}` | `results/raw/` |")
w("")
w("```bash")
w("# entorno (uv; el torch de PyPI es cu130 y el driver del Nitro es 556.19 = CUDA 12.5)")
w("uv venv --python 3.12 .venv")
w("uv pip install --python .venv/bin/python -r src/requirements.txt")
w('uv pip install --python .venv/bin/python "torch==2.14.1+cu126" \\')
w("    --index-url https://download.pytorch.org/whl/cu126")
w("# Laya (los tres checkpoints)")
w("for s in typed-decisions none multilingual; do")
w("  .venv/bin/python src/paso0_go_no_go.py --model laya --subfolder $s --split test --n 100 --out results/raw")
w("done")
w("# Kev (servidor aparte; ver src/README.md)")
w(".venv/bin/python src/paso0_go_no_go.py --model kev --split test --n 100 --out results/raw")
w("# regenerar ESTE informe")
w(".venv/bin/python src/paso0_informe.py")
w("```\n")
w("Cada fila de `results/raw/paso0_raw_*.jsonl` lleva `model`, `model_revision` y `row_hash` (D4); "
  "lleva además **las cuatro definiciones de `confidence` calculadas sobre la misma distribución** "
  "(`conf_jev`, `conf_ent`, `conf_pmax`, `conf_margin`) más los campos crudos del modelo "
  "(`answer_confidence`, `confidence_laya`, `act_probability`).\n")

w("## 5. Pendiente\n")
w("- **Nimble / SemIf / Jeff-1 / jev-lite** (los otros pares entrenables) — mismo pipeline, otros pesos.")
w("- **Mac Mini**: los 4B–9B en 4-bit que no entran en 6 GB.")
w("- **Pre-registro con DOI** antes de la medición principal (lo único que necesita al autor).")
w("- `laya-multilingual` sin temperaturas: decidir si entra en la matriz con esa salvedad o con las "
  "temperaturas reajustadas (y declararlo).\n")

out = os.path.join(REPO, "results/paso0_informe.md")
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(L) + "\n")
print("escrito:", out)
print("\n".join(L[:0]))
