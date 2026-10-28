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

*Nota sobre la última columna.* El adaptador de la corrida confirmatoria no propaga `output_tokens`: vale 0 en
las 65.185 filas, también para Kev. El único recuento medido de ese campo en pesos abiertos es el del paso 0
(Kev: 869.310 en las mismas 2.000 decisiones, §5.7).

Un dato aparte que el ecosistema no reporta: en cardinalidad alta, Kev-0.8B obtiene 0.813 de accuracy en
`banking77` (n = 77) frente a 0.377 del checkpoint base de Laya, un factor de 2.2. Las cinco configuraciones
medidas cubren el rango completo: del 0.016 del control sin entrenamiento al 0.813 de Kev-0.8B.

![Accuracy en cardinalidad alta (banking77, n = 77)](../figures/fig1-accuracy-banking77.pdf)
*Accuracy en banking77 (n = 77) de las cinco configuraciones medidas. La línea punteada marca el azar (1/77 = 0.013); el control sin entrenamiento cae sobre ella.*

## 5.2. Brecha entre definiciones sobre las 65.185 distribuciones

Sobre las 65.185 distribuciones medidas (una fila por decisión), la diferencia entre la definición de
`confidence` más alta y la más baja de la misma distribución tiene:

| estadístico | valor |
|---|---|
| mediana | **0.288** |
| percentil 90 | **0.434** |
| máximo | **0.848** |

En el caso típico, dos implementaciones del mismo campo discrepan en casi tres décimas sobre el
mismo dato, y el peor caso llega a 0.85. Cualquier umbral fijado sobre una de las dos no significa lo mismo
sobre la otra.

![Distribución de la brecha entre definiciones](../figures/fig2-brecha.pdf)
*Distribución de la brecha entre la definición más alta y la más baja de cada distribución, sobre las 65.185 decisiones medidas (mediana 0.288, p90 0.434, máximo 0.848). El pico en cero son las 2.167 filas saturadas, en las que las cuatro definiciones valen 1.*

## 5.3. Porte directo frente a porte con mapa cerrado

El resultado principal corresponde al nivel `raw`, que es el que congela el pre-registro. En él, de las 3.564
celdas, 348 tienen mapa cerrado entre definiciones (misma clase de equivalencia y misma cardinalidad;
1.044 si se cuentan los tres niveles), que son las únicas donde tiene sentido comparar el porte directo
contra el porte con mapa. El error absoluto medio:

| subconjunto | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| todas las celdas con mapa | 348 | 0.2528 | 0.0123 | 20.5× |
| **sin empates dominantes en el umbral** | **312** | **0.2337** | **0.0021** | **109.2×** |
| solo modelos entrenados (sin control crudo) | 276 | 0.2289 | 0.0020 | 112.8× |
| solo n = 2 (Proposición 3) | 180 | 0.3006 | 0.0218 | 13.8× |
| solo n ≥ 3 (Proposición 1) | 168 | 0.2015 | 0.0021 | 95.8× |
| nivel `L0` † (debiasing sin etiquetas) | 324 | 0.2190 | 0.0059 | 37.1× |
| nivel `L1` † (temperatura con etiquetas) | 312 | 0.3022 | 0.0024 | 126.0× |

† Las dos filas de nivel llevan **además** el filtro de empates de la fila «sin empates dominantes», que las
otras cinco no llevan. Sin ese filtro los tres niveles tienen 348 celdas con mapa cada uno, y el |Δ| directo es
0.2528 (`raw`), 0.2312 (`L0`) y 0.3145 (`L1`) —el |Δ| con mapa, 0.0123, 0.0096 y 0.0136—: la diferencia entre
filas es del filtro, no del nivel.

El porte directo se equivoca del orden de cien veces más que el porte con mapa. El matiz de la tercera
columna lo explica §5.4.

![Error del porte directo frente al porte con mapa](../figures/fig3-directo-vs-mapa.pdf)
*|Δ| medio del porte directo (τ tal cual) y del porte con mapa cerrado, por subconjunto de celdas del nivel raw con las tres q. Entre paréntesis, la cantidad de celdas; sobre cada par, la razón entre ambas barras. Las celdas sin empates dominantes son la comparación limpia (0.2337 frente a 0.0021, 109×).*

**Cómo leer la tabla.** El porte con mapa tiene un suelo que no es culpa del mapa: si el umbral cae sobre un
valor empatado en muchas salidas (modelos saturados), la cobertura salta y ni el mapa puede dar `q`
exacto. Por eso la comparación limpia es la del subconjunto sin empates dominantes (masa por debajo del 5 %),
y por eso `delta_mapa` debe leerse contra `delta` de la misma celda, nunca como un cero absoluto. La
columna `n_empates_tau` de la matriz declara, en cada celda, cuántos ítems comparten el umbral.

![CDF de |Δ| con mapa cerrado (nivel raw, q = 0.80)](../figures/fig4-cdf-delta.pdf)
*Función de distribución empírica de |Δ| en las 116 celdas con mapa cerrado del nivel raw con q = 0.80. La línea vertical marca |Δ| = 0.01: por debajo quedan el 84 % de las celdas con porte con mapa y el 14 % con porte directo.*

## 5.4. Caída de cobertura por par de definiciones

La distribución de `Δ` es bimodal: hay pares de definiciones que coinciden y pares que fallan en grande.
Por eso la unidad de análisis es el par y no la media global.

| A → B | celdas | \|Δ\| mediana | \|Δ\| media | ¿mapa? |
|---|---|---|---|---|
| margin → jev | 15 | **0.0023** | 0.0250 | sí |
| jev → margin | 15 | **0.0023** | 0.0293 | sí |
| jev → pmax | 99 | **0.0759** | 0.1568 | sí |
| ent → jev | 15 | **0.1837** | 0.1898 | sí |
| ent → margin | 15 | **0.1837** | 0.1898 | sí |
| margin → pmax | 15 | **0.2000** | 0.2253 | sí |
| ent → pmax | 15 | **0.2000** | 0.2421 | sí |
| pmax → jev | 99 | **0.2574** | 0.2973 | sí |
| margin → ent | 15 | **0.3474** | 0.3855 | sí |
| jev → ent | 15 | **0.3474** | 0.3857 | sí |
| pmax → margin | 15 | **0.5262** | 0.5154 | sí |
| pmax → ent | 15 | **0.7667** | 0.6787 | sí |

Dos de las coincidencias son identidades matemáticas, no azar: (i) a `n = 2`, `C_Jev` y `C_mar` son la
misma función (`2·p_max − 1`), así que su porte directo ya da casi cero; (ii) a cardinalidad alta,
`C_Jev = (n·p − 1)/(n − 1) → p`, así que `jev` y `pmax` convergen y sus umbrales casi coinciden. En el
extremo opuesto, `pmax → ent` es el peor par: no cambia la escala, cambia la forma de la función.

![Error del porte directo por par de definiciones](../figures/fig5-por-par.pdf)
*|Δ| mediana (barra) y media (punto) por par de definiciones del nivel raw, ordenadas por la mediana; entre paréntesis, la cantidad de celdas. El color separa los tres regímenes (≤ 0.05, 0.05–0.30, > 0.30). Los extremos son margin↔jev (0.0023) y pmax→ent (0.7667).*

Fracción de celdas que transfieren bien (`|Δ| < 0.01`), por cardinalidad (nivel `raw`):

| n | celdas con mapa | \|Δ\| mediana | % con \|Δ\| < 0.01 |
|---|---|---|---|
| 2 | 180 | 0.2141 | 14 % |
| 3 | 30 | 0.1775 | 0 % |
| 4 | 30 | 0.4085 | 0 % |
| 5 | 60 | 0.2000 | 0 % |
| 77 | 30 | 0.0058 | 63 % |
| 151 | 18 | 0.0127 | 44 % |

![Transferencia por cardinalidad](../figures/fig6-por-cardinalidad.pdf)
*|Δ| mediana por cardinalidad en escala logarítmica, con el rango intercuartílico y la cantidad de celdas entre paréntesis (nivel raw, las tres q). El patrón no es monótono: 0.214, 0.178, 0.409 y 0.200 para n ≤ 5, y 0.006 y 0.013 para n ≥ 77.*

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
definiciones deberían ser equivalentes en orden; en los datos eso se cumple dentro del par `jev ↔ margin`
(misma función) y no en el resto, porque el porte directo cruza escalas distintas aunque el orden sea el
mismo. Es la distinción entre el número y el mapa.

## 5.6. Celdas sin transferencia tras FDR (nivel `raw`, q = 0.80)

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

Hay celdas en las que portar el umbral pierde toda la cobertura. Quien calibra al
80 % con una definición y despliega con otra puede terminar actuando en el 0 % de los casos (o en todos), sin
ningún aviso del modelo.

![Heatmap de la matriz (banking77, n = 77)](../figures/fig7-heatmap-banking77.pdf)
*Δ = q − cobertura_B al portar τ sin mapa en banking77 (n = 77, nivel raw, q = 0.80): filas de definición origen, columnas de definición destino y escala de color compartida entre los cinco paneles; la diagonal no aplica. En el control Qwen, usar ent como origen pierde toda la cobertura (Δ = +0.80) sea cual sea el destino, y lo inverso ocurre con margin (Δ = −0.20, sobre-cobertura).*

## 5.7. Hallazgos de metrología del paso 0 (contexto)

La corrida de verificación sobre `typed-decisions` dejó, además, dos resultados que no estaban en la
literatura del ecosistema y que son parte del instrumento:

1. **La `choice_confidence` de Kev es la fórmula de Jev.** `(p_max − 1/K)/(1 − 1/K) ≡ (K·p_max − 1)/(K − 1)`,
   verificado numéricamente para `K ∈ {2,3,4,7,12}`. Estaban registradas como definiciones distintas; por la
   Proposición 1, ese par transfiere el umbral de forma exacta.
2. **El campo `output_tokens` tiene tres significados.** En el **paso 0** —la corrida de verificación, no la
   confirmatoria— Laya lo reporta como 0 (no hay generación) y Kev como recuento de tokens de la respuesta
   serializada (869.310 en las mismas 2.000 decisiones); es metrología del propio campo, no un fallo de Kev. La
   corrida confirmatoria no propaga el campo: vale 0 en las 65.185 filas (nota de la tabla de §5.1). Y el
   contador de la API de TypeSafe **sí está medido**, y tampoco es 0: 7.092.972 tokens en el brazo pagado
   (§5.8.2). Ninguna lectura de ese campo, por sí sola, distingue un modelo de decisión de uno generativo.

Y sobre la misma corrida, el ECE depende de la definición: en `laya-typed-decisions` va de 0.216 con `p_max`
a 0.577 con la entropía normalizada, un factor 2.7 sobre el mismo dato. El patrón no es local: sobre los 23
grupos, la diferencia entre la mejor y la peor definición tiene mediana 0.124 y llega a 0.361, y la definición
mejor calibrada cambia de grupo en grupo (`pmax` en 7, `margin` en 6, `ent` en 6 y `jev` en 4), con la entropía
normalizada como la peor en 13 de los 23 (Fig. 8).

![ECE por definición](../figures/fig8-ece-por-definicion.pdf)
*ECE de las cuatro definiciones en los 23 grupos medidos, calculado sobre las mismas filas crudas. El círculo hueco marca la definición con menor ECE de cada grupo: cambia de grupo en grupo y ninguna definición es la mejor calibrada en todos.*

## 5.8. Extensiones declaradas (posteriores al pre-registro)

Las cifras de §5.1–§5.7 están selladas por el pre-registro `10.5281/zenodo.23266795`: 23 grupos, 65.185
decisiones, 3.564 celdas. Las dos mediciones de esta subsección son posteriores a ese pre-registro y se
declaran aparte para no moverlas: no recalculan la matriz sellada ni las filas crudas, se calculan como
post-proceso sobre datos ya medidos o sobre un brazo nuevo, y llevan su fecha.

### 5.8.1. Quinta definición del campo: `conf_score` (distancia al nivel modal)

La documentación de TypeSafe define para la primitiva `score` una `confidence` que no estaba entre las cuatro
definiciones selladas:

```
confidence = max(0, 1 − Σᵢ pᵢ·|i − m| / MAD_unif),   MAD_unif = (1/n)·Σᵢ |i − (n−1)/2|
```

No es una variante de `conf_jev`: `conf_jev` mide concentración en el máximo; `conf_score` mide
dispersión alrededor del nivel modal. Dos distribuciones con el mismo `p_max` dan valores distintos. Y es
ordinal: exige que los niveles tengan orden y distancia, así que solo se mide donde el orden existe.

| | |
|---|---|
| Alcance | `sst5` (5 niveles ordinales), 5 configuraciones, **5.505 decisiones** |
| Brecha (misma distribución) | mediana **0.272** con 4 definiciones → **0.290** con 5 (p90 0.411, máx 0.581) |
| ECE global (misma corrida) | `p_max` 0.204 · `jev` 0.184 · `ent` 0.199 · `margin` 0.237 · **`score` 0.241** |
| Verificación en vivo | el API real devuelve esta fórmula en las filas `score` (máx \|Δ\| 0.0050 en 800 filas) |

**Por qué solo `sst5`.** En `banking77` (77), `clinc150` (151) y `typed-decisions` (2, 4, 5) las etiquetas son
nominales: el índice `i` no significa nada y usarlo sería añadir un supuesto, no medir. En `wanli` (3) el orden
es discutible. Se declara el límite en lugar de inventar la escala.

**El hallazgo que añade.** La quinta definición no tiene un sesgo estable: es la más baja de las cinco en el
70.3 % de las filas del control crudo Qwen y la más alta en el 92.6 % de las de Laya-multilingual. El
signo de la discrepancia depende del modelo, no de la definición — que es exactamente el objeto de la tesis,
ahora con una definición más en la lista.

### 5.8.2. Brazo pagado: el modelo detrás del campo

Hasta aquí todo se midió sobre pesos abiertos. El servicio real de TypeSafe (`jev-1.13.0`, una petición por
ítem) se midió sobre los mismos cinco datasets y se publica como brazo aparte: 14.277 decisiones, gasto
USD 0.79, con `probabilities` y `confidence` redondeadas a 0.01 por el servicio.

| dataset | n | ítems | accuracy | tokens de salida |
|---|---|---|---|---|
| `banking77` | 77 | 3.076 | 0.796 | 2.547.728 |
| `clinc150` | 151 | 3.100 | 0.901 | 4.034.486 |
| `sst5` | 5 | 1.101 | 0.541 | 19.818 |
| `typed-decisions` | 2, 4, 5 | 2.000 | 0.733 | 270.290 |
| `wanli` | 3 | 5.000 | 0.754 | 220.650 |

Dos observaciones de metrología del propio campo. (i) El contador `output_tokens` no es cero en el servicio
(7.092.972 en total), a diferencia de la corrida confirmatoria de pesos abiertos, donde el adaptador no propaga
el campo y vale 0 en las 65.185 filas (§5.7): el campo `tokens de salida` no distingue por sí solo un modelo de
decisión de uno generativo; esa lectura solo vale donde se controla la implementación.
(ii) La confianza que el servicio devuelve coincide con la definición que la especificación le asigna a cada
primitiva: `conf_score` en las filas `score` (máx |Δ| 0.0050 sobre 800 filas) y `conf_jev` en las de `choice`
(600 filas). La especificación describe el servicio real, no una reconstrucción.

Sumado a los brazos abiertos, el conjunto tiene 79.462 decisiones y una brecha mediana de 0.273
(p90 0.435) — el mismo orden que la cifra sellada de 0.288, ahora con seis modelos.

**El porte del umbral con la rejilla de 0.01.** Error absoluto medio del porte sobre las celdas con mapa cerrado
(nivel `raw`, las tres `q`; 420 celdas):

| modelo | celdas | \|Δ\| directo | \|Δ\| con mapa | factor | empate medio de τ |
|---|---|---|---|---|---|
| `typesafe-ai/jev` | 72 | 0.1735 | **0.0130** | 13.4× | 2.5 % |
| `convaiinnovations/laya/multilingual` | 72 | **0.1315** | 0.0018 | 75.1× | 0.1 % |
| `convaiinnovations/laya` | 66 | 0.2581 | 0.0028 | 91.7× | 0.1 % |
| `convaiinnovations/laya/typed-decisions` | 72 | 0.2515 | 0.0014 | 174.4× | 0.1 % |
| `jaredpalmer/kev-0.8b` | 66 | 0.2813 | 0.0022 | 128.5× | 0.1 % |
| `Qwen/Qwen3.5-0.8B-Base` (control) | 72 | 0.3441 | 0.0517 | 6.7× | 5.0 % |
| **global** | 420 | 0.2392 | 0.0124 | 19.3× | — |

El resultado se lee en dos partes, y la segunda corrige la intuición. (i) El porte directo de Jev (0.1735) es de
los mejores, pero no el mejor: el checkpoint `laya/multilingual` transfiere mejor (0.1315) sin ser el modelo
de referencia del campo. Comparar |Δ| directo entre modelos mezcla dos causas —la definición y la calidad del
modelo— y por eso la unidad de análisis de este trabajo es el par de definiciones (§5.4), no el modelo. (ii) El porte con
mapa de Jev es 4.6 a 9.3 veces el de los checkpoints abiertos (0.0130 frente a 0.0014–0.0028) y su factor
directo/mapa es 13.4×, un orden de magnitud menor que el de ellos (75–174×). La causa está medida: la rejilla
de 0.01 reasigna masa a valores empatados y 2.5 % de los ítems de prueba de Jev comparten el umbral, frente a
0.1 % en los cuatro checkpoints abiertos **entrenados** (25×), con 4 de 72 celdas por encima del 5 % de empate
frente a 0 en ellos; el control crudo se sale de esa comparación por su saturación (5.0 % de empate y 36 de 72
celdas, el extremo opuesto al de los checkpoints entrenados). El mapa cerrado sigue siendo válido
(Proposición 1); lo que la rejilla degrada es la resolución del umbral, no la equivalencia entre definiciones.

*Fuentes: `results/matrix/EXTENSION_CONF_SCORE.md` (+ `.csv`) y `results/matrix_pagado/RESUMEN_MATRIZ_PAGADO.md`.
Se regeneran con `src/matriz/extension_conf_score.py` y `src/matriz/correr_matriz_pagado.sh`. Ninguna de estas dos
extensiones modifica el nivel `raw` sellado, ni las 3.564 celdas, ni las 65.185 filas crudas de §5.1.*
