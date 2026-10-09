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

## `jev_conf_metrics/` — la librería (entregable 2)

```python
from jev_conf_metrics import all_confidences, celda, umbral_para_cobertura, exigir_recursos
```

| Módulo | Qué trae |
|---|---|
| `definiciones` | DEF-1…DEF-5 (`conf_jev`, `conf_ent`, `conf_pmax`, `conf_margin`, `conf_noul`), `CONFIDENCES`, las transformaciones AnyJev `aplicar_l0` / `aplicar_l1` y los mapas `order_equiv_affine_jev_pmax` / `phi_inv` |
| `metricas` | `ece` (ancho y masa), `ece_laya` (binning exacto de Laya), `auroc`, `brier_multi`, `nll`, `rps` |
| `transferencia` | `cobertura`, `umbral_para_cobertura`, `celda` (con `delta` y `delta_mapa`), `fold_de` (cross-fitting), `bootstrap_delta`, `bh_fdr` |
| `recursos` | `exigir_recursos` / `liberar`: **aborta si la RAM disponible baja de 1 GB** |

## `matriz/` — el pipeline de la matriz (entregable 3)

| Comando | Qué hace |
|---|---|
| `python src/matriz/medir.py --listar` | lista los adaptadores de dataset (sin GPU) |
| `python src/matriz/medir.py --dataset sst5 --inspeccionar` | carga 3 casos y muestra su estructura |
| `python src/matriz/medir.py --model laya --subfolder none --dataset sst5 --limite 400` | mide → `results/crudos/<modelo>__<dataset>.jsonl` |
| `bash src/matriz/correr_nucleo.sh [laya\|raw]` | el bloque completo, **un modelo en VRAM a la vez** |
| `bash src/matriz/correr_kev.sh` | levanta el servidor de Kev, mide y lo mata (libera 4.8 GB) |
| `python src/matriz/matriz.py` | **CPU puro**: la matriz desde los crudos (K=5, q, bootstrap, FDR) |
| `python src/matriz/figura.py` | los *heatmaps* (escala de color compartida) |
| `python src/matriz/informe_matriz.py` | `results/matrix/RESUMEN_MATRIZ.md` |

Regla de recursos: un modelo a la vez, `exigir_recursos` antes de cargar, `liberar` después. Si la RAM
disponible baja de **1 GB**, se para todo.

## Qué queda por enchufar

- **Kev**: ya está. No se carga con `transformers` (es LoRA + cabeza *pointer* sobre
  `Qwen/Qwen3.5-0.8B-Base`): se sirve desde su repo y el backend `kev` solo habla HTTP con él.
  ```bash
  git clone https://github.com/jaredpalmer/kev.git && cd kev
  uv sync --extra serve
  uv run --extra serve python -m kev.serve --run jaredpalmer/kev-0.8b --port 8008
  ```
- **Modelos 4B–9B** (Jeff-1, SemIf, jev-lite, Nimble): no caben en 6 GB; van al Mac Mini o en 4-bit.

## Reglas

- Datos y pesos **no se versionan** (ver `.gitignore`).
- Cada fila de `results/raw/*.jsonl` lleva `model`, `model_revision` y `row_hash` (D4).
- Las métricas se reportan **con la convención declarada**: `ece_*_laya` replica el binning de Laya
  (`laya.common.ece_score`); `brier_teacher` y `soft_accuracy_teacher` replican las suyas
  (contra la distribución completa del profesor).
- Corre esto en el **Nitro** o el **Mac Mini**, nunca en el `thinkpad-t440` (sin GPU).
