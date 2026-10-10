# Matriz de transferencia de umbrales — resumen

*Generado por `src/matriz/informe_matriz.py` desde `results/matrix/matriz_transferencia.csv` (3564 celdas). No editar a mano: se regenera.*

## 0. Qué mide esto

Para cada par de definiciones `confidence` (A origen → B destino), cada modelo y cada dataset: se ajusta en calibración el umbral `τ_A` que da la cobertura objetivo `q`, se aplica **tal cual** a la definición B en prueba y se mide la cobertura real. `Δ(A→B) = q − cobertura_B`. Cero si el umbral viaja; grande si no.

Dos portes por celda: **`delta`** (directo, lo que hace el ecosistema) y **`delta_mapa`** (con el mapa cerrado φ, cuando existe: misma clase y misma cardinalidad). Ver `docs/erratas_especificacion.md`.

Parámetros: `K=5` cross-fitting · `q=[0.8, 0.5, 0.95]` · bootstrap `B=2000` · niveles `['raw', 'L0', 'L1']` · BH-FDR α=0.05.

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

## 2. El objeto de la tesis, en una cifra

Sobre **65185 distribuciones** medidas (una fila = una decisión), la diferencia entre la definición de `confidence` más alta y la más baja de la **misma** distribución tiene mediana **0.288**, percentil 90 **0.434** y máximo **0.848**.

## 3. Proposición 1 en los datos (¿el mapa conserva la cobertura?)

1044 celdas tienen mapa cerrado (misma clase de equivalencia y misma cardinalidad). Las 8 con mayor desviación:

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
| todas las celdas con mapa | 1044 | 0.2721 | 0.0105 | 25.9× |
| sin empates dominantes en el umbral (masa < 5 %) | 948 | 0.2577 | 0.0025 | 104.5× |
| solo modelos entrenados (sin el control crudo) | 828 | 0.2466 | 0.0022 | 113.9× |
| solo n = 2 (Proposición 3) | 540 | 0.3136 | 0.0182 | 17.2× |
| solo n ≥ 3 (Proposición 1) | 504 | 0.2276 | 0.0023 | 100.0× |

**Cómo leer esto.** El porte con mapa tiene un suelo que no es culpa del mapa: si el umbral cae sobre un valor **empatado** (salidas saturadas), la cobertura salta y ni el mapa puede dar exactamente `q`. Por eso la comparación limpia es la del subconjunto sin empates dominantes, y por eso `delta_mapa` debe leerse **contra `delta` de la misma celda**, nunca como un cero absoluto. La columna `n_empates_tau` de la matriz dice, en cada celda, cuántos ítems comparten el umbral.

### 3b. El promedio NO es el resumen: la estructura está en el par de definiciones

La distribución de `Δ` es **bimodal**, no centrada: hay pares que coinciden (y entonces transferir es gratis) y pares que fallan en grande. Por eso el titular es el **par**, no la media global.

| A → B | celdas | \|Δ\| **mediana** | \|Δ\| media | ¿tiene mapa? |
|---|---|---|---|---|
| margin → jev | 45 | **0.0023** | 0.0224 | sí |
| jev → margin | 45 | **0.0024** | 0.0245 | sí |
| jev → pmax | 297 | **0.0799** | 0.1675 | sí |
| ent → jev | 45 | **0.1837** | 0.1974 | sí |
| ent → margin | 45 | **0.1837** | 0.1974 | sí |
| margin → pmax | 45 | **0.2000** | 0.2336 | sí |
| ent → pmax | 45 | **0.2000** | 0.2447 | sí |
| pmax → jev | 297 | **0.3131** | 0.3388 | sí |
| margin → ent | 45 | **0.3817** | 0.4041 | sí |
| jev → ent | 45 | **0.3817** | 0.4042 | sí |
| pmax → margin | 45 | **0.5277** | 0.5590 | sí |
| pmax → ent | 45 | **0.7667** | 0.6834 | sí |

Dos coincidencias **por identidad matemática**, no por azar: (i) a `n = 2`, `C_jev` y `C_mar` son la MISMA función (`2·p_max − 1`), así que su porte directo ya da 0; (ii) a cardinalidad alta, `C_jev = (n·p−1)/(n−1) → p`, así que `jev` y `pmax` convergen y sus umbrales casi coinciden. En el extremo opuesto, `pmax → ent` es el peor par: cambia la FORMA de la función, no solo la escala.

**Fracción de celdas que transfieren bien (|Δ| < 0.01), por cardinalidad:**

| n | celdas con mapa | \|Δ\| mediana | % con \|Δ\| < 0.01 |
|---|---|---|---|
| 2 | 540 | 0.2288 | 14 % |
| 3 | 90 | 0.1980 | 0 % |
| 4 | 90 | 0.4018 | 0 % |
| 5 | 180 | 0.2081 | 0 % |
| 77 | 90 | 0.0068 | 57 % |
| 151 | 54 | 0.0131 | 41 % |

## 4. Dónde el umbral NO viaja (nivel `raw`, q = 0.80, tras FDR)

| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B | precisión A | precisión B |
|---|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.339 | — |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.311 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → jev | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → margin | 0.8000 | [0.800, 0.800] | 0.000 | 0.592 | — |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.701 | — |
| `jaredpalmer/kev-0.8b` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 | 0.667 | — |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | pmax → margin | 0.7997 | [0.799, 0.800] | 0.000 | 0.204 | 0.235 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → jev | 0.7997 | [0.799, 0.800] | 0.000 | 0.339 | 0.340 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | jev → margin | 0.7993 | [0.798, 0.800] | 0.001 | 0.194 | 0.207 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → pmax | 0.7990 | [0.798, 0.800] | 0.001 | 0.339 | 0.330 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → margin | 0.7974 | [0.794, 0.800] | 0.003 | 0.311 | 0.291 |

## 5. Efecto de la cardinalidad n

| n | celdas | \|Δ\| medio | celdas con FDR | dataset de ejemplo |
|---|---|---|---|---|
| 2 | 60 | 0.3042 | 52 | typed-decisions |
| 3 | 60 | 0.2011 | 60 | wanli |
| 4 | 60 | 0.3240 | 60 | typed-decisions |
| 5 | 120 | 0.2664 | 119 | sst5 |
| 77 | 60 | 0.1638 | 52 | banking77 |
| 151 | 36 | 0.2140 | 32 | clinc150 |

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

