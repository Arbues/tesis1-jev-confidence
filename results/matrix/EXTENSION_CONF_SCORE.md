# Extensión declarada — `conf_score` (MAD_unif), quinta definición del campo

> **Estatus:** extensión **posterior** al pre-registro `10.5281/zenodo.23266795` (19-oct-2026).
> No modifica el nivel `raw` sellado, ni las filas crudas, ni `matriz_transferencia.csv`: se calcula
> como post-proceso sobre `results/crudos/` y se publica en este informe aparte.

## 0. Qué se mide y qué no

| | |
|---|---|
| Definición nueva | `confidence = max(0, 1 − Σᵢ pᵢ·\|i − m\| / MAD_unif)`, `MAD_unif = (1/n)·Σᵢ \|i − (n−1)/2\|` |
| Origen | documentación oficial de TypeSafe (`docs.typesafe.ai/confidence`), verificada en vivo el 12-oct-2026 |
| Alcance | `sst5` (5 niveles ordinales), 5 configuraciones de modelo, **5505 decisiones** |
| Excluidos | `wanli`, `banking77`, `clinc150`, `typed-decisions`: sus etiquetas son **nominales**; la fórmula exige un orden y no se inventa la escala |
| No hace | no recalcula la matriz de transferencia, no re-mide con modelos, no toca el pre-registro |

## 1. ECE por definición (misma corrida, mismas 5 confianzas sobre la misma distribución)

| modelo | n | pmax | jev | ent | margin | score |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | 1101 | 0.087 | 0.089 | 0.171 | 0.143 | 0.173 |
| `convaiinnovations/laya` | 1101 | 0.264 | 0.176 | 0.088 | 0.150 | 0.275 |
| `convaiinnovations/laya/multilingual` | 1101 | 0.588 | 0.547 | 0.488 | 0.464 | 0.606 |
| `convaiinnovations/laya/typed-decisions` | 1101 | 0.061 | 0.156 | 0.225 | 0.292 | 0.088 |
| `jaredpalmer/kev-0.8b` | 1101 | 0.088 | 0.059 | 0.117 | 0.209 | 0.103 |
| **global** | 5505 | 0.204 | 0.184 | 0.199 | 0.237 | 0.241 |

## 2. La quinta definición frente a las cuatro selladas (misma distribución)

| modelo | mediana `score` | Δ medio vs `pmax` | vs `jev` | vs `ent` | vs `margin` | % filas con `score` = máximo | % con `score` = mínimo |
|---|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | 0.000 | 0.258 | 0.099 | 0.057 | 0.078 | 0.0 | 70.3 |
| `convaiinnovations/laya` | 0.622 | 0.049 | 0.108 | 0.192 | 0.259 | 66.2 | 1.5 |
| `convaiinnovations/laya/multilingual` | 0.900 | 0.028 | 0.064 | 0.121 | 0.169 | 92.6 | 0.6 |
| `convaiinnovations/laya/typed-decisions` | 0.401 | 0.081 | 0.108 | 0.177 | 0.236 | 35.1 | 5.3 |
| `jaredpalmer/kev-0.8b` | 0.599 | 0.036 | 0.118 | 0.211 | 0.293 | 71.9 | 0.0 |
| **global** | 0.544 | 0.090 | 0.100 | 0.151 | 0.207 | 53.2 | 15.5 |

## 3. La brecha, con y sin la quinta definición

| subconjunto | mediana (4) | mediana (5) | p90 (5) | máx (5) |
|---|---|---|---|---|
| global | 0.272 | 0.290 | 0.411 | 0.581 |
| `Qwen/Qwen3.5-0.8B-Base` | 0.258 | 0.280 | 0.355 | 0.450 |
| `convaiinnovations/laya` | 0.288 | 0.303 | 0.432 | 0.564 |
| `convaiinnovations/laya/multilingual` | 0.137 | 0.153 | 0.427 | 0.581 |
| `convaiinnovations/laya/typed-decisions` | 0.298 | 0.307 | 0.394 | 0.504 |
| `jaredpalmer/kev-0.8b` | 0.296 | 0.308 | 0.440 | 0.559 |

### Cómo leerlo

1. Añadir una quinta definición **solo puede ampliar** la brecha de cada fila (el máximo sube o el mínimo baja); la columna `mediana (5)` es el número a citar si el texto describe el campo con cinco definiciones.
2. `conf_score` **no es** una versión de `conf_jev`: mide la dispersión alrededor del nivel modal, no la concentración en el máximo. Dos distribuciones con el mismo `p_max` dan valores distintos (`test_sensible_a_la_distancia_y_no_solo_al_maximo`).
3. Su ECE en esta corrida es la columna `score` de la tabla 1: comparable 1:1 con las otras cuatro porque se calcula sobre la misma corrida y la misma etiqueta de corrección.
4. La fórmula exige orden. Sobre un dataset nominal el índice `i` no significa nada: por eso la extensión se limita a `sst5` y se declara así en el paper.

## 4. Regeneración

```bash
.venv/bin/python src/matriz/extension_conf_score.py
```

Fuente: `results/crudos/*sst5.jsonl` · semilla y folds del pre-registro intactos.
