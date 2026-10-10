# §3. Marco teórico (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 3 · 08-oct-2026*
*Versión orientada al paper; las notas de estudio ampliadas están en `paper/01_marco_teorico.md` y la
especificación congelada en `paper/03_especificacion_confidence.md`.*

---

## 3.1. Notación

Sea una pregunta con `n` opciones etiquetadas (`n` es la cardinalidad; el primitivo `choice` admite hasta 255
y `score` entre 2 y 10). El modelo devuelve una distribución `p = (p_1, …, p_n)` sobre las opciones, con
`p_i ≥ 0` y `Σ_i p_i = 1`, y la etiqueta correcta es `y ∈ {1…n}`. Escribimos `p_max = max_i p_i`,
`ŷ = argmax_i p_i`, y el acierto `a = 1[ŷ = y]`. Con `H(p) = −Σ_i p_i log p_i` denotamos la entropía de
Shannon (el logaritmo es indistinto mientras se normalice). Ordenamos las probabilidades de mayor a menor:
`p_(1) ≥ p_(2) ≥ … ≥ p_(n)`, de modo que `p_(1) = p_max`.

## 3.2. El campo `confidence` como función de la distribución

Cada implementación define `confidence` como una función distinta de `p` y de `n`:

| definición | fórmula | dominio | quién la usa |
|---|---|---|---|
| concentración de Jev | `C_Jev(p) = (n·p_max − 1)/(n − 1)` | `[0, 1]` | Jev, Kev |
| entropía normalizada | `C_ent(p) = 1 − H(p)/log n` | `[0, 1]` | Laya (choice, score) |
| probabilidad ganadora | `C_max(p) = p_max` | `[1/n, 1]` | jev-lite, `answer_confidence` |
| margen | `C_mar(p) = p_(1) − p_(2)` | `[0, 1]` | derivados |
| `noul` (binario) | `C_noul(p) = max(p, 1 − p)` | `[1/2, 1]` | Laya (`noul`) |

Para una misma `p`, estas funciones toman valores distintos. Esta es la fuente de la incompatibilidad de
umbrales: el umbral es un punto en el **rango** de una función, y los rangos no coinciden.

| `p` (n = 3) | `C_Jev` | `C_ent` | `C_max` | `C_mar` |
|---|---|---|---|---|
| `(0.0118, 0.4629, 0.5253)` | 0.288 | 0.320 | 0.525 | 0.062 |

*Tabla 3.1. La misma distribución, cuatro definiciones, cuatro números.*

## 3.3. Calibración frente a discriminación

La **calibración** pregunta si el número es *creíble*: `P(ŷ = y | C = c) = c` para todo `c`. La
**discriminación** pregunta si el número *ordena bien*: si los aciertos reciben valores de `C` más altos que
los errores, y se mide con AUROC(`C`, `a`). Un modelo puede discriminar bien y estar des-calibrado, y dos
definiciones pueden discriminar idéntico y calibrar distinto: por eso el trabajo reporta **ambas**. El ECE
(Error de Calibración Esperado) con `M` bins `B_m` es

`ECE = Σ_m (|B_m| / N) · |acc(B_m) − conf(B_m)|`,

y se calcula en dos esquemas, bins de **igual ancho** y de **igual masa**, porque el número cambia entre
ellos \cite{naeini2015,guo2017}. Como métricas de error probabilístico se usan la **Brier** multiclase
`Brier = (1/N) Σ_i Σ_k (p_ik − y_ik)²` \cite{brier1950} y la **NLL** `−(1/N) Σ_i log p_i(y_i)`.

## 3.4. Equivalencia en orden y transferencia exacta

El punto teórico del trabajo es que la incompatibilidad **no** es uniforme: algunas definiciones están
relacionadas por una transformación monótona, y entonces el umbral transfiere **exacto**; otras no lo están.
Lo fijamos en tres proposiciones (demostraciones y comprobación numérica en
`paper/03_especificacion_confidence.md`).

> **Proposición 1 (equivalencia en orden).** Sea `n` fijo. La definición de Jev es afín y estrictamente
> creciente en `p_max`: `C_Jev = α·p_max + β` con `α = n/(n−1) > 0` y `β = −1/(n−1)`. En consecuencia,
> `C_Jev` y `C_max` son **equivalentes en orden**: existe `φ` estrictamente creciente con `C_Jev = φ(C_max)`.
> Un umbral `τ` sobre `C_Jev` induce el mismo conjunto de actuaciones y abstenciones que el umbral
> `φ⁻¹(τ)` sobre `C_max`, y la cobertura es idéntica.

> **Proposición 2 (no equivalencia con la entropía).** Para `n ≥ 3` existen distribuciones `p, p'` con
> `p_max = p'_max` y `H(p) ≠ H(p')`. Por tanto `C_ent` **no** es función de `p_max` solo, y en general **no**
> existe `φ` monótona con `C_ent = φ(C_max)`. El umbral no transfiere entre una definición tipo `p_max` y una
> tipo entropía.

> **Proposición 3 (degeneración en `n = 2`).** Con `n = 2`, `C_Jev = 2·p_max − 1 = C_mar`, esto es, la
> definición de Jev y el margen son la **misma** función; y `C_ent`, con `H` función de un solo parámetro, es
> también una transformación estrictamente monótona de `p_max`. Por tanto en `n = 2` **todas** las
> definiciones son equivalentes en orden, y la incompatibilidad de umbrales es un fenómeno exclusivo de
> `n ≥ 3` con distribuciones dispersas.

**Consecuencia: el fallo tiene dos capas.** Si dos definiciones son equivalentes en orden pero viven en
escalas distintas (por ejemplo `C_Jev` y `C_max`), el **número** no viaja aunque el **mapa** sí: existe
traducción exacta `φ⁻¹`. Si además pertenecen a **clases** distintas (por ejemplo `p_max` y la entropía), no
existe ni número ni mapa, y el porte directo es una extrapolación inválida. Esta distinción, entre la capa
de **escala** y la capa de **forma**, es la que explica por qué el resultado no se puede resumir con un
promedio y se documenta en `docs/erratas_especificacion.md`.

## 3.5. Transferencia de umbrales (definición formal)

Dados un origen `A`, un destino `B`, una cobertura objetivo `q ∈ (0, 1)` y un conjunto de calibración:

1. Hallar `τ_A` tal que `cobertura_A(τ_A) = q`, con `cobertura_A(τ) = #{C_A ≥ τ}/N` (el menor umbral
   observado que no supera la cobertura objetivo).
2. Portarlo al destino de una de dos maneras:
   - **porte directo:** `τ_B := τ_A`, que es lo que practica el ecosistema;
   - **porte con mapa:** `τ_B := ψ(τ_A)`, con `ψ` el mapa cerrado `A→B`, que **solo existe** dentro de una
     clase de equivalencia y a cardinalidad fija (por ejemplo `ψ = φ⁻¹` para `jev → pmax`).
3. Medir en el conjunto de prueba la cobertura efectiva `cobertura_B(τ_A)` y la precisión.

La **degradación** `Δ(A→B) = q − cobertura_B(τ_A)` es la celda de la matriz. Se repite por modelo, por
dataset y por cardinalidad. El mismo procedimiento se puede aplicar **entre datasets** (umbral ajustado en
un dataset `A` y aplicado en otro `B`), que es el eje donde \cite{jebadiah} observó que la calibración no
viaja y \cite{arXiv2609.33843} lo cuantificó dentro de la definición `p_max`. Este trabajo recorre el eje
distinto, el de las definiciones.

## 3.6. Predicción selectiva: el umbral como política

Con probabilidad de acierto `p`, coste de error `C_err` y coste de escalar `C_esc`, actuar conviene si
`(1−p)·C_err < C_esc`, es decir `p > 1 − C_esc/C_err` \cite{chow1970}. Esta frontera **presupone** que `p`
es una probabilidad calibrada. Cuando el umbral se elige como cuantil de una `confidence` mal especificada,
la política efectiva deja de ser la óptima para el coste real: la métrica de la matriz es, en el fondo, la
pérdida de utilidad del despliegue.

## 3.7. Nota sobre RLCD

RLCD (ruido gaussiano de media cero en los logits, regla estrictamente propia, REINFORCE con baseline de
grupo, temperatura post-hoc) es el mecanismo que produce estas `confidence`. La teoría garantiza que reportar
honestamente es el óptimo bajo una regla propia \cite{gneiting2007}; el análisis de septiembre de 2026
muestra que, en la práctica, el término RL equivale al gradiente de una cross-entropy suavizada con ruido, de
modo que la inferencia sin ruido sale **sobre-confiada** \cite{arXiv2609.38850,lakoreai2026}. Esto explica
**por qué** hace falta medir la calibración, pero no es el objeto de este trabajo: aquí no se propone un
objetivo de entrenamiento, se construye el instrumento que mide su resultado.
