# §5. Resultados (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 5 · 08-oct-2026*
*Todas las cifras salen de `results/matrix/matriz_transferencia.csv` y `results/matrix/RESUMEN_MATRIZ.md`,
que se regeneran con los comandos de §4.5. La corrida confirmatoria está declarada en el pre-registro.*

---

## 5.1. Qué se midió

23 grupos, 65.185 decisiones, 3.564 celdas. El detalle por modelo y dataset:

| modelo | dataset | n | ítems | accuracy | tokens de salida |
|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | 3.076 | 0.0156 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | clinc150 | 151 | 3.100 | 0.0387 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | 1.101 | 0.2116 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2, 4, 5 | 2.000 | 0.4860 | 0 |
| `Qwen/Qwen3.5-0.8B-Base` | wanli | 3 | 5.000 | 0.3598 | 0 |
| `convaiinnovations/laya` | banking77 | 77 | 3.076 | 0.3765 | 0 |
| `convaiinnovations/laya` | sst5 | 5 | 1.101 | 0.3451 | 0 |
| `convaiinnovations/laya` | typed-decisions | 2, 4, 5 | 2.000 | 0.3595 | 0 |
| `convaiinnovations/laya` | wanli | 3 | 5.000 | 0.6178 | 0 |
| `convaiinnovations/laya/multilingual` | banking77 | 77 | 3.076 | 0.3560 | 0 |
| `convaiinnovations/laya/multilingual` | clinc150 | 151 | 3.100 | 0.6274 | 0 |
| `convaiinnovations/laya/multilingual` | sst5 | 5 | 1.101 | 0.2489 | 0 |
| `convaiinnovations/laya/multilingual` | typed-decisions | 2, 4, 5 | 2.000 | 0.3515 | 0 |
| `convaiinnovations/laya/multilingual` | wanli | 3 | 5.000 | 0.5750 | 0 |
| `convaiinnovations/laya/typed-decisions` | banking77 | 77 | 3.076 | 0.3781 | 0 |
| `convaiinnovations/laya/typed-decisions` | clinc150 | 151 | 3.100 | 0.4732 | 0 |
| `convaiinnovations/laya/typed-decisions` | sst5 | 5 | 1.101 | 0.4505 | 0 |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | 2, 4, 5 | 2.000 | 0.7685 | 0 |
| `convaiinnovations/laya/typed-decisions` | wanli | 3 | 5.000 | 0.6190 | 0 |
| `jaredpalmer/kev-0.8b` | banking77 | 77 | 3.076 | 0.8134 | 0 |
| `jaredpalmer/kev-0.8b` | sst5 | 5 | 1.101 | 0.4995 | 0 |
| `jaredpalmer/kev-0.8b` | typed-decisions | 2, 4, 5 | 2.000 | 0.4595 | 0 |
| `jaredpalmer/kev-0.8b` | wanli | 3 | 5.000 | 0.5954 | 0 |

Un dato aparte que el ecosistema no reporta: en cardinalidad alta, **Kev-0.8B saca 0.813 de accuracy en
`banking77` (n = 77) frente a 0.377 del checkpoint base de Laya**. El ecosistema sí entrena para muchos
opciones; no todos los modelos por igual.

## 5.2. El objeto de la tesis, en una cifra

Sobre las **65.185** distribuciones medidas (una fila por decisión), la diferencia entre la definición de
`confidence` más alta y la más baja de la **misma** distribución tiene:

| estadístico | valor |
|---|---|
| mediana | **0.288** |
| percentil 90 | **0.434** |
| máximo | **0.848** |

Es decir: en el caso típico, dos implementaciones del mismo campo discrepan en casi tres décimas sobre el
mismo dato, y el peor caso llega a 0.85. Cualquier umbral fijado sobre una de las dos no significa lo mismo
sobre la otra.

## 5.3. El número no viaja; el mapa sí

De las 3.564 celdas, **1.044 tienen mapa cerrado** entre definiciones (misma clase de equivalencia y misma
cardinalidad), que son las únicas donde tiene sentido comparar el porte directo contra el porte con mapa. El
error absoluto medio:

| subconjunto | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| todas las celdas con mapa | 1.044 | 0.2721 | 0.0105 | 25.9× |
| **sin empates dominantes en el umbral** | **948** | **0.2577** | **0.0025** | **104.5×** |
| solo modelos entrenados (sin control crudo) | 828 | 0.2466 | 0.0022 | 113.9× |
| solo n = 2 (Proposición 3) | 540 | 0.3136 | 0.0182 | 17.2× |
| solo n ≥ 3 (Proposición 1) | 504 | 0.2276 | 0.0023 | 100.0× |

El porte directo se equivoca **del orden de cien veces más** que el porte con mapa. El matiz de la tercera
columna lo explica §5.4.

**Cómo leer la tabla.** El porte con mapa tiene un suelo que no es culpa del mapa: si el umbral cae sobre un
valor **empatado** en muchas salidas (modelos saturados), la cobertura salta y ni el mapa puede dar `q`
exacto. Por eso la comparación limpia es la del subconjunto sin empates dominantes (masa por debajo del 5 %),
y por eso `delta_mapa` debe leerse contra `delta` de la **misma** celda, nunca como un cero absoluto. La
columna `n_empates_tau` de la matriz declara, en cada celda, cuántos ítems comparten el umbral.

## 5.4. El promedio no es el resumen: la estructura está en el par

La distribución de `Δ` es **bimodal**: hay pares de definiciones que coinciden y pares que fallan en grande.
El titular es el par, no la media global.

| A → B | celdas | \|Δ\| mediana | \|Δ\| media | ¿mapa? |
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

Dos de las coincidencias son **identidades matemáticas**, no azar: (i) a `n = 2`, `C_Jev` y `C_mar` son la
**misma** función (`2·p_max − 1`), así que su porte directo ya da casi cero; (ii) a cardinalidad alta,
`C_Jev = (n·p − 1)/(n − 1) → p`, así que `jev` y `pmax` convergen y sus umbrales casi coinciden. En el
extremo opuesto, `pmax → ent` es el peor par: no cambia la escala, cambia la **forma** de la función.

Fracción de celdas que transfieren bien (`|Δ| < 0.01`), por cardinalidad:

| n | celdas con mapa | \|Δ\| mediana | % con \|Δ\| < 0.01 |
|---|---|---|---|
| 2 | 540 | 0.2288 | 14 % |
| 3 | 90 | 0.1980 | 0 % |
| 4 | 90 | 0.4018 | 0 % |
| 5 | 180 | 0.2081 | 0 % |
| 77 | 90 | 0.0068 | 57 % |
| 151 | 54 | 0.0131 | 41 % |

## 5.5. Efecto de la cardinalidad

| n | celdas | \|Δ\| medio | celdas con FDR | dataset de ejemplo |
|---|---|---|---|---|
| 2 | 60 | 0.3042 | 52 | typed-decisions |
| 3 | 60 | 0.2011 | 60 | wanli |
| 4 | 60 | 0.3240 | 60 | typed-decisions |
| 5 | 120 | 0.2664 | 119 | sst5 |
| 77 | 60 | 0.1638 | 52 | banking77 |
| 151 | 36 | 0.2140 | 32 | clinc150 |

El porte falla en todas las cardinalidades, pero con dos matices ya visibles en §5.4: a `n` bajo el daño es
grande y sistemático, mientras que a cardinalidad alta (`n ≥ 77`) las definiciones tipo `p_max` convergen
entre sí y una parte de las celdas transfiere bien. La Proposición 3 predice que con `n = 2` todas las
definiciones deberían ser equivalentes en orden; en los datos eso se cumple **dentro del par `jev ↔ margin`**
(misma función) y no en el resto, porque el porte directo cruza escalas distintas aunque el orden sea el
mismo. Es la distinción entre el número y el mapa.

## 5.6. Dónde el umbral no viaja (nivel `raw`, q = 0.80, tras FDR)

| modelo | dataset | n | A → B | Δ | IC95 % | cobertura B |
|---|---|---|---|---|---|---|
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → margin | 0.8000 | [0.800, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → jev | 0.8000 | [0.800, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | typed-decisions | 2 | pmax → margin | 0.8000 | [0.800, 0.800] | 0.000 |
| `convaiinnovations/laya/typed-decisions` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 |
| `jaredpalmer/kev-0.8b` | typed-decisions | 2 | pmax → ent | 0.8000 | [0.800, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | pmax → margin | 0.7997 | [0.799, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → jev | 0.7997 | [0.799, 0.800] | 0.000 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | jev → margin | 0.7993 | [0.798, 0.800] | 0.001 |
| `Qwen/Qwen3.5-0.8B-Base` | banking77 | 77 | ent → pmax | 0.7990 | [0.798, 0.800] | 0.001 |
| `Qwen/Qwen3.5-0.8B-Base` | sst5 | 5 | pmax → margin | 0.7974 | [0.794, 0.800] | 0.003 |

La lectura es directa: hay celdas en las que portar el umbral **pierde toda la cobertura**. Quien calibra al
80 % con una definición y despliega con otra puede terminar actuando en el 0 % de los casos (o en todos), sin
ningún aviso del modelo.

## 5.7. Hallazgos de metrología del paso 0 (contexto)

La corrida de verificación sobre `typed-decisions` dejó, además, dos resultados que no estaban en la
literatura del ecosistema y que son parte del instrumento:

1. **La `choice_confidence` de Kev es la fórmula de Jev.** `(p_max − 1/K)/(1 − 1/K) ≡ (K·p_max − 1)/(K − 1)`,
   verificado numéricamente para `K ∈ {2,3,4,7,12}`. Estaban registradas como definiciones distintas; por la
   Proposición 1, ese par transfiere el umbral de forma exacta.
2. **El campo `output_tokens` tiene tres significados.** Jev y Laya lo reportan como 0 (no hay generación);
   Kev lo usa como recuento de tokens de la respuesta serializada (869.310 en las mismas 2.000 decisiones).
   Es metrología del propio campo, no un fallo de Kev.

Y sobre la misma corrida, el ECE cambia por completo según la definición: en `laya-typed-decisions` va de
**0.216** con `p_max` a **0.577** con la entropía normalizada, un factor **2.7×** sobre el mismo dato.
