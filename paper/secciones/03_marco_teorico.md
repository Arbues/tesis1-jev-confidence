# §3. Marco teórico (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 3 · 04-oct-2026*
*Versión orientada al paper; las notas de estudio ampliadas están en `paper/01_marco_teorico.md`.*

---

## 3.1. Notación

Sea una pregunta con `n` opciones etiquetadas (`n` = cardinalidad; `choice` admite hasta 255, `score` entre 2
y 10). El modelo devuelve una distribución `p = (p_1, …, p_n)` sobre las opciones, con `p_i ≥ 0` y
`Σ_i p_i = 1`, y la etiqueta correcta es `y ∈ {1…n}`. Escribimos `p_max = max_i p_i` y `ŷ = argmax_i p_i`; el
acierto es `a = 1[ŷ = y]`. Con `H(p) = −Σ_i p_i log p_i` denotamos la entropía de Shannon (log natural o
base 2, indistinto mientras se normalice).

## 3.2. El campo `confidence` como función de la distribución

Cada implementación define `confidence` como una función distinta de `p` (y de `n`):

- **Concentración de Jev:** `C_Jev(p) = (n·p_max − 1)/(n − 1)`.
- **Entropía normalizada de Laya:** `C_ent(p) = 1 − H(p)/log n`.
- **Probabilidad ganadora (`p_max`):** `C_max(p) = p_max` (Laya `answer_confidence`, `jev-lite`).
- **Margen:** `C_mar(p) = p_(1) − p_(2)` (la mayor menos la segunda mayor).
- **`noul` (binario):** `C_noul = max(p, 1 − p)`.

Para una misma `p`, estas funciones toman valores distintos (Tabla 3.1). Esta es la fuente de la
incompatibilidad de umbrales: el umbral es un punto en el **rango** de una función, y los rangos no coinciden.

| `p` (n = 3) | `C_Jev` | `C_ent` | `C_max` | `C_mar` |
|---|---|---|---|---|
| `(0.0118, 0.4629, 0.5253)` | 0.288 | 0.320 | 0.525 | 0.062 |

*Tabla 3.1. La misma distribución, cuatro definiciones, cuatro números.*

## 3.3. Calibración frente a discriminación

La **calibración** pregunta si el número es *creíble*: `P(ŷ = y | C = c) = c` para todo `c`. La
**discriminación** pregunta si el número *ordena bien*: si los aciertos reciben valores de `C` más altos que
los errores. Se mide con AUROC(`C`, `a`). Un modelo puede discriminar bien y estar des-calibrado, y dos
definiciones pueden discriminar idéntico y calibrar distinto: por eso el trabajo reporta **ambas**. El ECE
(Error de Calibración Esperado) con `M` bins `B_m` es

`ECE = Σ_m (|B_m| / N) · |acc(B_m) − conf(B_m)|`,

y se calcula en dos esquemas —bins de **igual ancho** y de **igual masa**— porque el número cambia entre
ellos \cite{naeini2015,guo2017}. Como métricas de error probabilístico se usan la **Brier** multiclase
`Brier = (1/N) Σ_i Σ_k (p_ik − y_ik)²` \cite{brier1950} y la **NLL** `−(1/N) Σ_i log p_i(y_i)`.

## 3.4. Equivalencia en orden y transferencia exacta (proposición)

El punto teórico del trabajo es que la incompatibilidad **no** es uniforme: algunas definiciones están
relacionadas por una transformación monótona —y entonces el umbral transfiere **exacto**— y otras no lo están.

> **Proposición 1 (equivalencia en orden).** Sea `n` fijo. La definición de Jev es afín y estrictamente
> creciente en `p_max`: `C_Jev = α·p_max + β` con `α = n/(n−1) > 0` y `β = −1/(n−1)`. En consecuencia,
> `C_Jev` y `C_max` son **equivalentes en orden**: existe `φ` estrictamente creciente con `C_Jev = φ(C_max)`.
> Un umbral `τ` sobre `C_Jev` induce el mismo conjunto de aciertos–abstenciones que el umbral
> `φ(τ)` sobre `C_max`; la cobertura es idéntica.

> **Proposición 2 (no equivalencia con la entropía).** Para `n ≥ 3` existen distribuciones `p, p'` con
> `p_max = p'_max` y `H(p) ≠ H(p')`. Por tanto `C_ent` **no** es función de `p_max` solo, y en general **no**
> existe `φ` monótona con `C_ent = φ(C_max)`. Un umbral no transfiere en general entre una definición tipo
> `p_max` y una tipo entropía.

**Consecuencia.** Las definiciones se parten en **clases de equivalencia en orden** (transferencia exacta,
Proposición 1) y **pares incompatibles** (transferencia fallida, Proposición 2). La magnitud del fallo —que la
teoría acota pero no fija numéricamente— es lo que la **matriz de transferencia** mide.

## 3.5. Transferencia de umbrales (definición formal)

Dados un origen `A`, un destino `B`, una cobertura objetivo `q ∈ (0,1)` y un conjunto de calibración:

1. Hallar `τ_A` tal que `cobertura_A(τ_A) = q` (la fracción de ítems con `C_A ≥ τ_A` iguala `q`).
2. Aplicarlo **tal cual** al destino: `τ_B := τ_A`.
3. Medir en el conjunto de prueba `cobertura_B(τ_A)` y `precisión_B(τ_A)`.

La **degradación** `Δ = q − cobertura_B(τ_A)` es la celda de la matriz. Se repite por modelo y por dataset
(también **entre** datasets: `τ` ajustado en `A`, aplicado en `B`), el eje donde \cite{jebadiah} observó que
la calibración no viaja y \cite{arXiv2609.33843} lo cuantificó dentro de la definición `p_max`.

## 3.6. Predicción selectiva: el umbral como política

Con probabilidad de acierto `p`, coste de error `C_err` y coste de escalar `C_esc`, actuar conviene si
`(1−p)·C_err < C_esc`, es decir `p > 1 − C_esc/C_err` \cite{chow1970}. Esta frontera **presupone** que `p`
es una probabilidad calibrada. Cuando el umbral se elige como cuantil de una `confidence` mal especificada,
la política efectiva deja de ser la óptima para el coste real: la métrica de la matriz es, en el fondo, la
pérdida de utilidad del despliegue.

## 3.7. Nota sobre RLCD

RLCD (ruido gaussiano de media cero en los logits, regla estrictamente propia, REINFORCE con baseline de
grupo, temperatura post-hoc) es el mecanismo que produce estas `confidence`. La teoría garantiza que reportar
honestamente es el óptimo bajo una regla propia \cite{gneiting2007}; el análisis de septiembre de 2026 muestra
que, en la práctica, el término RL equivale al gradiente de una cross-entropy suavizada con ruido, de modo que
la inferencia sin ruido sale **sobre-confiada** \cite{arXiv2609.38850,lakoreai2026}. Esto explica **por qué**
hace falta medir la calibración, pero no es el objeto de este trabajo: aquí no se propone un objetivo de
entrenamiento, se construye el instrumento que mide su resultado.
