# Paso 0 — informe go/no-go (Tesis 1, Ruta 1)

*Generado automáticamente desde `results/raw/` por `src/paso0_informe.py` · 08-oct-2026*

---

## 0. Veredicto: **GO**

Los tres criterios del paso 0 (`11_ruta1_metrologia_confidence.md` §10) se cumplen:

1. **Los tres primitivos corren** en modelos de pesos abiertos sobre `typed-decisions` (`choice`, `score`, `noul`), con la distribución completa por pregunta.
2. **`output_tokens = 0`** en Laya (todas las filas, los tres checkpoints) — y se descubre que **Kev reporta ese mismo campo con otro significado** (§3).
3. **Se reproduce un número publicado**: cinco métricas de Laya, en los tres checkpoints (§1).

| | |
|---|---|
| Máquina | `Arbues-AxeNitro` (WSL2) · **RTX 4050 Laptop 6 GB** |
| Python / torch | 3.12.14 · torch 2.14.1+**cu126** (el build cu130 de PyPI no arranca con el driver 556.19) |
| Datos | `LocalLLaMA/typed-decisions`, split `test` = 400 casos / **2 000 decisiones** (4 flujos × 100 casos) |
| Costo | **$0** (D5): pesos y datasets abiertos, nada de nube |

### Versiones y hashes (D4)

| modelo | revisión / sha | device |
|---|---|---|
| `kev` | `bf75a6a8848ea6960ff2ed108d9ed44c2941174f` · repo `kev` @ `5e42a7a0` | — |
| `english` | `7b928d828b7b0e022f929d9bd2e44165aa270148` | cuda |
| `multilingual` | `7b928d828b7b0e022f929d9bd2e44165aa270148` | cuda |
| `typed-decisions` | `7b928d828b7b0e022f929d9bd2e44165aa270148` | cuda |

## 1. Reproducción de los números publicados

Números de Laya **auto-reportados** (README del modelo, tabla *typed-decisions, measured on all three checkpoints*) frente a lo **medido aquí** sobre las mismas 2 000 decisiones.

| métrica | `laya-typed-decisions` | `laya` (english) | `laya-multilingual` |
|---|---|---|---|
| accuracy | 0.766 → **0.7685** (Δ +0.0025) | 0.362 → **0.3595** (Δ -0.0025) | 0.342 → **0.3515** (Δ +0.0095) |
| soft accuracy (vs profesor) | 0.471 → **0.4707** (Δ -0.0003) | 0.332 → **0.3313** (Δ -0.0007) | 0.326 → **0.3280** (Δ +0.0020) |
| Brier (vs profesor) | 0.062 → **0.0615** (Δ -0.0005) | 0.316 → **0.3157** (Δ -0.0003) | 0.439 → **0.4627** (Δ +0.0237) |
| ECE (answer_confidence) | 0.213 → **0.2157** (Δ +0.0027) | 0.175 → **0.1766** (Δ +0.0016) | 0.285 → **0.3175** (Δ +0.0325) |
| score MAE | 0.242 → **0.2424** (Δ +0.0004) | 0.694 → **0.6947** (Δ +0.0007) | 0.687 → **0.7605** (Δ +0.0735) |

El checkpoint afinado sobre el benchmark (`laya-typed-decisions`) reproduce las cinco métricas con **|Δ| ≤ 0.003**; el inglés, con |Δ| ≤ 0.003 en las cinco. La discrepancia mayor está en `laya-multilingual` (ECE Δ +0.033, score MAE Δ +0.074): es el checkpoint que **no trae temperaturas ajustadas** (`temperature = [1.0, 1.0, 1.0]`, `temperature_by_options = {}` en `paso0_versions.json`), así que la comparación no es contra el mismo artefacto. Queda documentado, no corregido.

> Convención descubierta y verificada: las métricas que publica Laya se calculan **contra la distribución completa del profesor**, no contra la etiqueta — `soft accuracy` = Σ p_modelo·p_profesor (0.4707 medido vs 0.471 publicado) y `Brier` = Σ (p_modelo − p_profesor)² (0.0615 vs 0.062). El ECE sí se calcula sobre `answer_confidence` = `max(p)`, con 15 bins de igual ancho (`laya.common.ece_score`, replicado en `ece_laya()`).

## 2. El objeto de la Ruta 1, ya visible en el paso 0

La **misma corrida**, las **mismas 2 000 decisiones**, el **mismo modelo**: el ECE cambia por completo según qué definición de `confidence` se use. Esto es exactamente lo que la matriz de transferencia va a cuantificar de forma sistemática.

| checkpoint | `p_max` | **Jev** `(n·p−1)/(n−1)` | **entropía** `1−H/log k` | margen `p₁−p₂` |
|---|---|---|---|---|
| `typed-decisions` | 0.2157 | 0.4256 | 0.5766 | 0.5109 |
| `english` | 0.1766 | 0.1661 | 0.2301 | 0.1941 |
| `multilingual` | 0.3175 | 0.2551 | 0.2118 | 0.2436 |
| `kev` | 0.0610 | 0.2283 | 0.3627 | 0.2739 |

En `laya-typed-decisions` el ECE va de **0.216** (con `p_max`) a **0.577** (con la entropía normalizada): un factor **2.7×** sobre el mismo dato. Cualquier umbral de «actúo o escalo» fijado sobre una de las dos no significa lo mismo sobre la otra.

Discriminación (AUROC vs acierto), que **no** es calibración:

| checkpoint | AUROC `p_max` | AUROC Jev | AUROC entropía | AUROC margen |
|---|---|---|---|---|
| `typed-decisions` | 0.7552 | 0.7167 | 0.6344 | 0.7739 |
| `english` | 0.5826 | 0.5003 | 0.4785 | 0.5245 |
| `multilingual` | 0.5904 | 0.5688 | 0.5504 | 0.5869 |
| `kev` | 0.6756 | 0.6763 | 0.6730 | 0.6634 |

## 3. Kev: el mismo campo, otra definición (y otro `output_tokens`)

`jaredpalmer/kev-0.8b` no se carga con `transformers`: es un adaptador LoRA + cabeza *pointer* sobre `Qwen/Qwen3.5-0.8B-Base`, servido por su propio repositorio. Se corrió contra ese servidor (`kev/api.py`, commit `5e42a7a0`).

**a) `choice_confidence` de Kev ES la fórmula de Jev.** En `kev/api.py:127-130`:

```python
def choice_confidence(p):
    """(p_max - 1/K) / (1 - 1/K): 0 at uniform, 1 at certainty."""
    K = len(p)
    return 1.0 if K == 1 else (max(_normalize(p)) - 1 / K) / (1 - 1 / K)
```
Algebraicamente `(p_max − 1/K)/(1 − 1/K) = (K·p_max − 1)/(K − 1)`, que es **exactamente** la fórmula publicada de Jev. Verificado numéricamente para K ∈ {2,3,4,7,12}: idénticas. El ecosistema las tenía registradas como definiciones distintas. Consecuencia directa de la Proposición 1: **este par transfiere el umbral de forma exacta** (misma cobertura, a `n` fijo).

**b) `score_confidence` de Kev es una tercera familia.** `max(0, 1 − E|nivel − moda| / D)` — dispersión ordinal, ni `p_max` ni entropía. Kev declara en el código que ambas fórmulas *espejan el adaptador de referencia de TypeSafe* (`system-one-adapter 0.2.1`).

**c) `noul` no lleva `confidence`** — igual que en Jev. Confirmado en la corrida: 400 de las 2 000 filas de Kev no tienen ese campo.

**d) `output_tokens` significa otra cosa.** `kev/api.py:163-165`:

```python
def output_tokens(tok, answers: dict) -> int:
    """Billing-style figure: tokens of the serialised answers. Not a measure of generation (there is none)."""
    return len(tok(json.dumps(answers), add_special_tokens=False).input_ids)
```
Medido: `output_tokens` total **869,310** (máx 480 por llamada) en las mismas 2 000 decisiones donde Laya reporta **0** en todas las filas. **El mismo campo, tres significados**: Jev y Laya = 0 (no hay generación); Kev = recuento de tokens de la respuesta serializada. Esto es metrología del campo, no un fallo de Kev.

Resultados de Kev sobre las mismas 2 000 decisiones:

| métrica | valor |
|---|---|
| accuracy | 0.4595 |
| soft accuracy (vs profesor) | 0.3733 |
| Brier (vs profesor) | 0.1958 |
| ECE (`p_max`) | 0.0610 |
| ECE (Jev) | 0.2283 |
| ECE (entropía) | 0.3627 |
| ECE (`confidence` reportada) | 0.2330 |
| score MAE | 0.6265 |

## 4. Artefactos y cómo regenerarlos

| artefacto | ruta |
|---|---|
| `paso0_raw_kev_kev-latest.jsonl` | `results/raw/` |
| `paso0_raw_laya_english.jsonl` | `results/raw/` |
| `paso0_raw_laya_multilingual.jsonl` | `results/raw/` |
| `paso0_raw_laya_typed-decisions.jsonl` | `results/raw/` |
| `paso0_summary_kev_kev-latest.json` | `results/raw/` |
| `paso0_summary_laya_english.json` | `results/raw/` |
| `paso0_summary_laya_multilingual.json` | `results/raw/` |
| `paso0_summary_laya_typed-decisions.json` | `results/raw/` |
| `paso0_versions.json` | `results/raw/` |

```bash
# entorno (uv; el torch de PyPI es cu130 y el driver del Nitro es 556.19 = CUDA 12.5)
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r src/requirements.txt
uv pip install --python .venv/bin/python "torch==2.14.1+cu126" \
    --index-url https://download.pytorch.org/whl/cu126
# Laya (los tres checkpoints)
for s in typed-decisions none multilingual; do
  .venv/bin/python src/paso0_go_no_go.py --model laya --subfolder $s --split test --n 100 --out results/raw
done
# Kev (servidor aparte; ver src/README.md)
.venv/bin/python src/paso0_go_no_go.py --model kev --split test --n 100 --out results/raw
# regenerar ESTE informe
.venv/bin/python src/paso0_informe.py
```

Cada fila de `results/raw/paso0_raw_*.jsonl` lleva `model`, `model_revision` y `row_hash` (D4); lleva además **las cuatro definiciones de `confidence` calculadas sobre la misma distribución** (`conf_jev`, `conf_ent`, `conf_pmax`, `conf_margin`) más los campos crudos del modelo (`answer_confidence`, `confidence_laya`, `act_probability`).

## 5. Pendiente

- **Nimble / SemIf / Jeff-1 / jev-lite** (los otros pares entrenables) — mismo pipeline, otros pesos.
- **Mac Mini**: los 4B–9B en 4-bit que no entran en 6 GB.
- **Pre-registro con DOI** antes de la medición principal (lo único que necesita al autor).
- `laya-multilingual` sin temperaturas: decidir si entra en la matriz con esa salvedad o con las temperaturas reajustadas (y declararlo).

