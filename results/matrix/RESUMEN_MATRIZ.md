# Matriz de transferencia de umbrales — resumen

*Generado por `src/matriz/informe_matriz.py` desde `results/matrix/matriz_transferencia.csv` (3672 celdas). No editar a mano: se regenera.*

## 0. Qué mide esto

Para cada par de definiciones `confidence` (A origen → B destino), cada modelo y cada dataset: se ajusta en calibración el umbral `τ_A` que da la cobertura objetivo `q`, se aplica **tal cual** a la definición B en prueba y se mide la cobertura real. `Δ(A→B) = q − cobertura_B`. Cero si el umbral viaja; grande si no.

Dos portes por celda: **`delta`** (directo, lo que hace el ecosistema) y **`delta_mapa`** (con el mapa cerrado φ, cuando existe: misma clase y misma cardinalidad). Ver `docs/erratas_especificacion.md`.

Parámetros: `K=5` cross-fitting · `q=[0.8, 0.5, 0.95]` · bootstrap `B=2000` · niveles `['raw', 'L0', 'L1']` · BH-FDR α=0.05.

## 1. Qué se midió

| modelo | dataset | n | ítems | accuracy | tokens de salida |
|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | [77] | 400 | 0.0200 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | clinc150 | [151] | 400 | 0.0400 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | [5] | 400 | 0.2475 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | [2, 4, 5] | 2000 | 0.4860 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | wanli | [3] | 400 | 0.4925 | 0 |
| `convaiinnovations/laya` | banking77 | [77] | 400 | 0.3575 | 0 |
| `convaiinnovations/laya` | clinc150 | [151] | 400 | 0.6325 | 0 |
| `convaiinnovations/laya` | sst5 | [5] | 400 | 0.3400 | 0 |
| `convaiinnovations/laya` | typed-decisions | [2, 4, 5] | 2000 | 0.3595 | 0 |
| `convaiinnovations/laya` | wanli | [3] | 400 | 0.6600 | 0 |
| `convaiinnovations/laya/multilingual` | banking77 | [77] | 400 | 0.3850 | 0 |
| `convaiinnovations/laya/multilingual` | clinc150 | [151] | 400 | 0.6325 | 0 |
| `convaiinnovations/laya/multilingual` | sst5 | [5] | 400 | 0.2425 | 0 |
| `convaiinnovations/laya/multilingual` | typed-decisions | [2, 4, 5] | 2000 | 0.3515 | 0 |
| `convaiinnovations/laya/multilingual` | wanli | [3] | 400 | 0.6275 | 0 |
| `convaiinnovations/laya/typed-decisions` | banking77 | [77] | 400 | 0.3700 | 0 |
| `convaiinnovations/laya/typed-decisions` | clinc150 | [151] | 400 | 0.4700 | 0 |
| `convaiinnovations/laya/typed-decisions` | sst5 | [5] | 400 | 0.4350 | 0 |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | [2, 4, 5] | 2000 | 0.7685 | 0 |
| `convaiinnovations/laya/typed-decisions` | wanli | [3] | 400 | 0.6650 | 0 |
| `jaredpalmer/kev-0.8b` | banking77 | [77] | 400 | 0.8200 | 0 |
| `jaredpalmer/kev-0.8b` | sst5 | [5] | 400 | 0.4250 | 0 |
| `jaredpalmer/kev-0.8b` | typed-decisions | [2, 4, 5] | 2000 | 0.4595 | 0 |
| `jaredpalmer/kev-0.8b` | wanli | [3] | 400 | 0.6175 | 0 |

## 2. El objeto de la tesis, en una cifra

Sobre **17600 distribuciones** medidas (una fila = una decisión), la diferencia entre la definición de `confidence` más alta y la más baja de la **misma** distribución tiene mediana **0.321**, percentil 90 **0.531** y máximo **0.848**.

## 3. Proposición 1 en los datos (¿el mapa conserva la cobertura?)

1062 celdas tienen mapa cerrado (misma clase de equivalencia y misma cardinalidad). Las 8 con mayor desviación:

| modelo | dataset | n | q | A → B | Δ directo | Δ con mapa |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | pmax → margin | 0.5000 | 0.2090 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | jev → margin | 0.2090 | 0.2090 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.8 | margin → pmax | -0.2000 | 0.2078 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.8 | margin → jev | 0.2078 | 0.2078 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.8 | margin → ent | 0.7916 | 0.2078 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.8 | pmax → margin | 0.8000 | 0.1719 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.8 | jev → margin | 0.1719 | 0.1719 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | 0.5 | pmax → margin | 0.5000 | 0.1419 |

Error absoluto medio del porte, por subconjunto de celdas:

| subconjunto | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| todas las celdas con mapa | 1062 | 0.2679 | 0.0115 | 23.2× |
| sin empates dominantes en el umbral (masa < 5 %) | 966 | 0.2534 | 0.0037 | 67.6× |
| solo modelos entrenados (sin el control crudo) | 846 | 0.2415 | 0.0033 | 72.4× |
| solo n = 2 (Proposición 3) | 540 | 0.3136 | 0.0182 | 17.2× |
| solo n ≥ 3 (Proposición 1) | 522 | 0.2206 | 0.0047 | 47.4× |

**Cómo leer esto.** El porte con mapa tiene un suelo que no es culpa del mapa: si el umbral cae sobre un valor **empatado** (salidas saturadas), la cobertura salta y ni el mapa puede dar exactamente `q`. Por eso la comparación limpia es la del subconjunto sin empates dominantes, y por eso `delta_mapa` debe leerse **contra `delta` de la misma celda**, nunca como un cero absoluto. La columna `n_empates_tau` de la matriz dice, en cada celda, cuántos ítems comparten el umbral.

## 4. Dónde el umbral NO viaja (nivel `raw`, q = 0.80, tras FDR)

| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B | precisión A | precisión B |
|---|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | pmax → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.204 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | jev → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.194 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → pmax | 0.8000 | [0.800, 0.800] | 0.000 | 0.338 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → jev | 0.8000 | [0.800, 0.800] | 0.000 | 0.338 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.338 | — |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.313 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → jev | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.701 | — |
| `jaredpalmer/kev-0.8b` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.667 | — |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → margin | 0.7978 | [0.792, 0.800] | 0.002 | 0.313 | 0.265 |

## 5. Efecto de la cardinalidad n

| n | celdas | \|Δ\| medio | celdas con FDR | dataset de ejemplo |
|---|---|---|---|---|
| 2 | 60 | 0.3042 | 52 | typed-decisions |
| 3 | 60 | 0.1919 | 54 | wanli |
| 4 | 60 | 0.3240 | 60 | typed-decisions |
| 5 | 120 | 0.2661 | 117 | sst5 |
| 77 | 60 | 0.1614 | 49 | banking77 |
| 151 | 48 | 0.1777 | 42 | clinc150 |

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

