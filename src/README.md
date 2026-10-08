# src/ — código (se trabaja en el Acer Nitro)

## `paso0_go_no_go.py` — verificación go/no-go de la Ruta 1

Modos, en orden de uso:

| Comando | Dónde | Qué hace |
|---|---|---|
| `python3 src/paso0_go_no_go.py --selftest` | **cualquier máquina** | Valida la matemática del marco teórico (solo stdlib): las definiciones de `confidence`, ECE/AUROC/Brier/NLL y las **dos proposiciones** (equivalencia en orden jev↔pmax = transferencia exacta; no-transferencia con la entropía) |
| `python3 src/paso0_go_no_go.py --inspect` | Nitro (con red) | Descubre la **API real** de Laya/Kev y el sha de cada modelo |
| `python3 src/paso0_go_no_go.py --model laya --n 100` | **Nitro / Mac Mini** | Paso 0 real: Laya sobre `typed-decisions`, escribe artefactos en `results/raw/` |
| `python3 src/paso0_go_no_go.py --model kev` | Nitro | Igual, contra un servidor de Kev en `http://127.0.0.1:8008` |
| `python3 src/paso0_go_no_go.py --model raw` | Nitro | Control: LLM crudo con readout de logits (sin entrenar) |
| `python3 src/paso0_go_no_go.py --mock` | cualquiera | Artefactos con datos sintéticos (marcados como NO reales) |

Flags útiles: `--subfolder {typed-decisions,multilingual,none}` (checkpoint de Laya), `--split {test,train}`,
`--configs a,b,c|all`, `--n` (casos por config), `--out`, `--device {cuda,cpu}`.

## Puesta en marcha en el Nitro (RTX 4050) — con `uv`

```bash
git clone git@github.com:Arbues/tesis1-jev-confidence.git && cd tesis1-jev-confidence
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r src/requirements.txt
# GPU: el torch de PyPI se compila contra CUDA 13 y el driver del Nitro es 556.19 (CUDA 12.5):
uv pip install --python .venv/bin/python "torch==2.14.1+cu126" \
    --index-url https://download.pytorch.org/whl/cu126
.venv/bin/python src/paso0_go_no_go.py --selftest          # debe imprimir: SELFTEST OK
.venv/bin/python src/paso0_go_no_go.py --model laya --n 100
```

## API real de Laya (verificada el 08-oct-2026, `laya` 0.4.1)

```python
import laya
agent = laya.load("convaiinnovations/laya", subfolder="typed-decisions", device="cuda")
out = agent.predict(state, questions)        # payload `system_one`
out["answers"]["<q>"]["probabilities"]       # {etiqueta: p}  (choice y score)
out["answers"]["<q>"]["noul"]                # P(true)        (noul NO trae `probabilities`)
out["answers"]["<q>"]["confidence"]          # 1 − H(p)/log k  (entropía normalizada)
out["answers"]["<q>"]["answer_confidence"]   # max(p)
out["answers"]["<q>"]["action"]["act_probability"]
out["usage"]["output_tokens"]                # 0  ← no genera texto
```

Tres definiciones distintas de `confidence` viven en **la misma respuesta**: ese es el objeto de la Ruta 1.

## Qué queda por enchufar

- **Kev**: no se carga con `transformers` (es LoRA + cabeza *pointer* sobre `Qwen/Qwen3.5-0.8B-Base`).
  Se sirve desde su repo y el backend `kev` solo habla HTTP con él:
  ```bash
  git clone https://github.com/jaredpalmer/kev.git && cd kev
  uv sync --extra serve
  uv run --extra serve python -m kev.serve --run jaredpalmer/kev-0.8b --port 8008
  ```

## Reglas

- Datos y pesos **no se versionan** (ver `.gitignore`).
- Cada fila de `results/raw/*.jsonl` lleva `model`, `model_revision` y `row_hash` (D4).
- Las métricas se reportan **con la convención declarada**: `ece_*_laya` replica el binning de Laya
  (`laya.common.ece_score`); `brier_teacher` y `soft_accuracy_teacher` replican las suyas
  (contra la distribución completa del profesor).
- Corre esto en el **Nitro** o el **Mac Mini**, nunca en el `thinkpad-t440` (sin GPU).
