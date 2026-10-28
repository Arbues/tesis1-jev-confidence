# Matriz de transferencia de umbrales — resumen

*Generado por `src/matriz/informe_matriz.py` desde `results/matrix_pagado/matriz_transferencia.csv` (2880 celdas). No editar a mano: se regenera.*

## 0. Qué mide esto

Para cada par de definiciones `confidence` (A origen → B destino), cada modelo y cada dataset: se ajusta en calibración el umbral `τ_A` que da la cobertura objetivo `q`, se aplica **tal cual** a la definición B en prueba y se mide la cobertura real. `Δ(A→B) = q − cobertura_B`. Cero si el umbral viaja; grande si no.

Dos portes por celda: **`delta`** (directo, lo que hace el ecosistema) y **`delta_mapa`** (con el mapa cerrado φ, cuando existe: misma clase y misma cardinalidad). Ver `docs/erratas_especificacion.md`.

Parámetros: `K=5` cross-fitting · `q=[0.8, 0.5, 0.95]` · bootstrap `B=2000` · niveles `['raw', 'L1']` · BH-FDR α=0.05.

## 1. Qué se midió

| modelo | dataset | n | ítems | accuracy | tokens de salida |
|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | [77] | 3076 | 0.0156 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | clinc150 | [151] | 3100 | 0.0387 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | [5] | 1101 | 0.2116 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | [2, 4, 5] | 2000 | 0.4860 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | wanli | [3] | 5000 | 0.3598 | 0 |
| `convaiinnovations/laya` | banking77 | [77] | 3076 | 0.3765 | 0 |
| `convaiinnovations/laya` | sst5 | [5] | 1101 | 0.3451 | 0 |
| `convaiinnovations/laya` | typed-decisions | [2, 4, 5] | 2000 | 0.3595 | 0 |
| `convaiinnovations/laya` | wanli | [3] | 5000 | 0.6178 | 0 |
| `convaiinnovations/laya/multilingual` | banking77 | [77] | 3076 | 0.3560 | 0 |
| `convaiinnovations/laya/multilingual` | clinc150 | [151] | 3100 | 0.6274 | 0 |
| `convaiinnovations/laya/multilingual` | sst5 | [5] | 1101 | 0.2489 | 0 |
| `convaiinnovations/laya/multilingual` | typed-decisions | [2, 4, 5] | 2000 | 0.3515 | 0 |
| `convaiinnovations/laya/multilingual` | wanli | [3] | 5000 | 0.5750 | 0 |
| `convaiinnovations/laya/typed-decisions` | banking77 | [77] | 3076 | 0.3781 | 0 |
| `convaiinnovations/laya/typed-decisions` | clinc150 | [151] | 3100 | 0.4732 | 0 |
| `convaiinnovations/laya/typed-decisions` | sst5 | [5] | 1101 | 0.4505 | 0 |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | [2, 4, 5] | 2000 | 0.7685 | 0 |
| `convaiinnovations/laya/typed-decisions` | wanli | [3] | 5000 | 0.6190 | 0 |
| `jaredpalmer/kev-0.8b` | banking77 | [77] | 3076 | 0.8134 | 0 |
| `jaredpalmer/kev-0.8b` | sst5 | [5] | 1101 | 0.4995 | 0 |
| `jaredpalmer/kev-0.8b` | typed-decisions | [2, 4, 5] | 2000 | 0.4595 | 0 |
| `jaredpalmer/kev-0.8b` | wanli | [3] | 5000 | 0.5954 | 0 |
| `typesafe-ai/jev` | banking77 | [77] | 3076 | 0.7962 | 2547728 |
| `typesafe-ai/jev` | clinc150 | [151] | 3100 | 0.9006 | 4034486 |
| `typesafe-ai/jev` | sst5 | [5] | 1101 | 0.5413 | 19818 |
| `typesafe-ai/jev` | typed-decisions | [2, 4, 5] | 2000 | 0.7330 | 270290 |
| `typesafe-ai/jev` | wanli | [3] | 5000 | 0.7538 | 220650 |

## 2. El objeto de la tesis, en una cifra

Sobre **79462 distribuciones** medidas (una fila = una decisión), la diferencia entre la definición de `confidence` más alta y la más baja de la **misma** distribución tiene mediana **0.273**, percentil 90 **0.435** y máximo **0.848**.

## 3. Proposición 1 en los datos (¿el mapa conserva la cobertura?)

420 celdas tienen mapa cerrado (misma clase de equivalencia y misma cardinalidad). Las 8 con mayor desviación:

| modelo | dataset | n | q | A → B | Δ directo | Δ con mapa |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | pmax → margin | 0.5000 | 0.2090 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | jev → margin | 0.2090 | 0.2090 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | pmax → jev | 0.5000 | 0.1288 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | pmax → ent | 0.5000 | 0.1288 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | jev → pmax | -0.5000 | 0.1288 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | jev → ent | 0.5000 | 0.1288 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | ent → pmax | -0.5000 | 0.1288 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | ent → jev | -0.4448 | 0.1288 |

Todo lo de esta sección es sobre el **nivel principal `raw`** (el que congela el pre-registro), salvo las dos filas marcadas con †. Los niveles `L0` y `L1` están en la matriz completa y se resumen en §5.

Error absoluto medio del porte, por subconjunto de celdas:

| subconjunto | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| todas las celdas con mapa | 420 | 0.2392 | 0.0124 | 19.3× |
| sin empates dominantes en el umbral (masa < 5 %) | 380 | 0.2242 | 0.0037 | 61.2× |
| solo modelos entrenados (sin el control crudo) | 348 | 0.2175 | 0.0043 | 50.6× |
| solo n = 2 (Proposición 3) | 216 | 0.2959 | 0.0209 | 14.1× |
| solo n ≥ 3 (Proposición 1) | 204 | 0.1791 | 0.0034 | 52.6× |
| nivel `L1` † (temperatura con etiquetas) | 380 | 0.2792 | 0.0039 | 72.3× |


**Cómo leer esto.** El porte con mapa tiene un suelo que no es culpa del mapa: si el umbral cae sobre un valor **empatado** (salidas saturadas), la cobertura salta y ni el mapa puede dar exactamente `q`. Por eso la comparación limpia es la del subconjunto sin empates dominantes, y por eso `delta_mapa` debe leerse **contra `delta` de la misma celda**, nunca como un cero absoluto. La columna `n_empates_tau` de la matriz dice, en cada celda, cuántos ítems comparten el umbral.

### 3b. El promedio NO es el resumen: la estructura está en el par de definiciones

La distribución de `Δ` es **bimodal**, no centrada: hay pares que coinciden (y entonces transferir es gratis) y pares que fallan en grande. Por eso el titular es el **par**, no la media global.

| A → B | celdas | \|Δ\| **mediana** | \|Δ\| media | ¿tiene mapa? |
|---|---|---|---|---|
| margin → jev | 18 | **0.0032** | 0.0236 | sí |
| jev → margin | 18 | **0.0032** | 0.0272 | sí |
| jev → pmax | 120 | **0.0674** | 0.1443 | sí |
| ent → jev | 18 | **0.1837** | 0.1840 | sí |
| ent → margin | 18 | **0.1837** | 0.1840 | sí |
| margin → pmax | 18 | **0.2000** | 0.2281 | sí |
| ent → pmax | 18 | **0.2000** | 0.2434 | sí |
| pmax → jev | 120 | **0.2199** | 0.2698 | sí |
| margin → ent | 18 | **0.3474** | 0.3743 | sí |
| jev → ent | 18 | **0.3474** | 0.3745 | sí |
| pmax → margin | 18 | **0.5183** | 0.5025 | sí |
| pmax → ent | 18 | **0.7667** | 0.6783 | sí |

Dos coincidencias **por identidad matemática**, no por azar: (i) a `n = 2`, `C_jev` y `C_mar` son la MISMA función (`2·p_max − 1`), así que su porte directo ya da 0; (ii) a cardinalidad alta, `C_jev = (n·p−1)/(n−1) → p`, así que `jev` y `pmax` convergen y sus umbrales casi coinciden. En el extremo opuesto, `pmax → ent` es el peor par: cambia la FORMA de la función, no solo la escala.

**Fracción de celdas que transfieren bien (|Δ| < 0.01), por cardinalidad:**

| n | celdas con mapa | \|Δ\| mediana | % con \|Δ\| < 0.01 |
|---|---|---|---|
| 2 | 216 | 0.2259 | 12 % |
| 3 | 36 | 0.1247 | 0 % |
| 4 | 36 | 0.3304 | 0 % |
| 5 | 72 | 0.1969 | 0 % |
| 77 | 36 | 0.0060 | 64 % |
| 151 | 24 | 0.0127 | 46 % |

## 4. Dónde el umbral NO viaja (nivel `raw`, q = 0.80, tras FDR)

| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B | precisión A | precisión B |
|---|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.018 | — |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.213 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → jev | 0.8000 | [0.800, 0.800] | 0.000 | 0.646 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.646 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.646 | — |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.925 | — |
| `jaredpalmer/kev-0.8b` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.534 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | pmax → margin | 0.7997 | [0.799, 0.800] | 0.000 | 0.018 | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → jev | 0.7997 | [0.799, 0.800] | 0.000 | 0.018 | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | jev → margin | 0.7993 | [0.798, 0.800] | 0.001 | 0.018 | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → pmax | 0.7990 | [0.798, 0.800] | 0.001 | 0.018 | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → margin | 0.7974 | [0.794, 0.800] | 0.003 | 0.213 | 0.667 |

*Precisión = acierto entre los ítems seleccionados (especificación §5, paso 3), recalculada desde los crudos. El CSV del directorio ya trae la misma corrección (errata E8).*

## 5. Efecto de la cardinalidad n

| n | celdas | \|Δ\| medio | celdas con FDR | dataset de ejemplo |
|---|---|---|---|---|
| 2 | 72 | 0.2976 | 62 | typed-decisions |
| 3 | 72 | 0.1880 | 71 | wanli |
| 4 | 72 | 0.2982 | 72 | typed-decisions |
| 5 | 144 | 0.2480 | 140 | sst5 |
| 77 | 72 | 0.1522 | 62 | banking77 |
| 151 | 48 | 0.1726 | 43 | clinc150 |

## 6. Trazabilidad (D4)

| artefacto | qué contiene |
|---|---|
| `results/crudos/*.jsonl` | una fila por (modelo × dataset × ítem): distribución completa, etiqueta, acierto, las 4 definiciones y `row_hash` |
| `results/crudos/*.meta.json` | modelo, revisión del Hub, cardinalidades, accuracy |
| `results/matrix/matriz_transferencia.csv` | las celdas (A→B) × modelo × dataset × n × q × nivel |
| `results/matrix/resumen.json` | parámetros de la corrida (K, q, bootstrap, niveles) |
| `results/matrix/heatmap_*.png/pdf` | la figura central |
| `results/raw/paso0_*` | la reproducción del paso 0 (5 métricas publicadas, |Δ| ≤ 0.003) |

Columna **medido aquí / auto-reportado**: en los crudos, `conf_*` son **medidos aquí** (calculados sobre la distribución devuelta) y `answer_confidence` / `confidence_reported` / `act_probability` son **auto-reportados** por el modelo. Las cifras de ECE de la tabla de calibración del ecosistema son **auto-reportadas** y no se usan en la matriz.

## 7. Desviaciones respecto al pre-registro

El pre-registro (`paper/04_pre_registro.md`, DOI 10.5281/zenodo.23266795) exige reportar cualquier desviación. Las habidas:

| # | Qué | Por qué | Efecto |
|---|---|---|---|
| D1 | Se corrigió un **fallo de implementación del nivel `L0`** | El debiasing sin etiquetas no convergía: el paso era ~1000× demasiado pequeño, `b` quedaba en ~0 y las frecuencias de argmax apenas se movían (168/294/416/222 → 169/299/408/224, con objetivo 275). El nivel `L0` era indistinguible de `raw` | No cambia el plan congelado (que dice «debiasing sin etiquetas»), corrige su implementación. **Las celdas `L0` se recalcularon**; `raw` (nivel principal) y `L1` no se tocan |
| D2 | Se descartó un archivo del **piloto** que estaba contaminado | `convaiinnovations__laya__clinc150.jsonl` contenía datos de `multilingual` etiquetados como `none` (residuo de una corrida previa a un arreglo de colisión) | No afecta a la confirmatoria: ese archivo no existe en ella |
| D3 | `clinc150` no se midió en el checkpoint `none` de Laya | Su ventana de 512 tokens solo admite 126 de las 151 opciones | **Limitación, no desviación**: se declara en el paper |

El **nivel principal es `raw`** y **no se ha tocado** tras publicar el pre-registro. `L0` y `L1` son niveles de sensibilidad.

