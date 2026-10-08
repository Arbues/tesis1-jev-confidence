# Especificación formal de las definiciones de `confidence`

*Tesis 1 · Ruta 1 · entregable 1 · 04-oct-2026*
*Documento normativo: fija, para cada definición, su forma, dominio, rango, monotonía y clase de
equivalencia en orden. Es la base de la librería `jev-conf-metrics` y de sus tests de conformidad.*

---

## 0. Alcance

Se especifican las definiciones de `confidence` **en uso dentro del ecosistema open-source tipo Jev** (2026).
Cada definición se da como **función explícita** de la distribución devuelta y de la cardinalidad `n`. Las
definiciones **no analíticas** (cabezas aprendidas y posts-procesos con parámetros ajustados) se especifican
como transformaciones o como funciones opacas, con su dominio y las métricas que sí son medibles.

Marcas de estado: **[A]** = analítica (función cerrada) · **[T]** = transformación aplicada antes de otra
definición · **[O]** = opaca (aprendida), solo rango y medición.

---

## 1. El objeto y sus primitivas

Un **modelo de decisión** recibe una pregunta y un conjunto cerrado de opciones y termina la inferencia con un
*readout* de logits: **no genera texto**, luego `output_tokens = 0`. Tres primitivas:

| Primitiva | Entrada | Salida | n |
|---|---|---|---|
| `choice` | pregunta + opciones etiquetadas | opción + `probabilities` + `confidence` | 2 … 255 |
| `score` | pregunta + niveles ordinales (con `legend`) | nivel + probabilidades + `confidence` | 2 … 10 |
| `noul` | pregunta binaria | un valor en `[0,1]` (en TypeSafe, **sin** campo `confidence`) | 2 |

**Asimetría de partida (importante):** la fórmula de Jev se observa en `choice`/`score`; el `noul` de TypeSafe
no expone `confidence`. Laya **sí** define una `confidence` para `noul` (`max(π, 1−π)`). Por eso `noul` se
especifica como primitiva binaria y su "confianza" como una definición **distinta** (DEF-3), no como la de Jev.

---

## 2. Notación

- `n ∈ ℕ, n ≥ 2`: cardinalidad (nº de opciones o de niveles).
- `Δ_n = { p ∈ [0,1]^n : Σ_{i=1}^n p_i = 1 }`: el símplex de probabilidad (dominio común).
- `p_max = max_i p_i`; `p_(1) ≥ p_(2) ≥ …` : estadísticos de orden.
- `H(p) = −Σ_i p_i ln p_i`: entropía de Shannon (min `0`, max `ln n`, en `Δ_n`).
- `π ∈ [0,1]`: el valor escalar que devuelve `noul`.
- `𝕀[·]`: indicador. `ŷ = argmax p`; acierto `a = 𝕀[ŷ = y]`.

---

## 3. Definiciones

### DEF-1 — Concentración de Jev **[A]**

> `C_Jev(p) = (n·p_max − 1) / (n − 1)`

| Propiedad | Valor |
|---|---|
| Fuente | docs TypeSafe (`docs.typesafe.ai/primitives/choice`); fórmula reconstruida en vivo (30 tickets, rohitghumare) |
| Dominio | `Δ_n`, `n ≥ 2` |
| Rango | `[0, 1]` — exacto: `p_max = 1/n ⇒ 0`, `p_max = 1 ⇒ 1` |
| Monotonía | **estrictamente creciente y afín** en `p_max`, a `n` fijo: `C_Jev = α·p_max + β`, `α = n/(n−1) > 0`, `β = −1/(n−1)` |
| Extremos | `p` uniforme ⇒ `0`; `p` one-hot ⇒ `1` |
| Caso `n = 2` | `C_Jev = 2·p_max − 1` |
| Naturaleza | **no** es `p_max`; es la *concentración* normalizada (cuánto excede el ganador al azar) |
| Clase de equivalencia | `{C_max, C_Jev}` a `n` fijo (ver §4) |

### DEF-2 — Entropía normalizada de Laya **[A]**

> `C_ent(p) = 1 − H(p) / ln n`

| Propiedad | Valor |
|---|---|
| Fuente | `laya.studio/glossary/entropy-based-confidence`; implementada en `NandhaKishorM/laya` para `choice`/`score` |
| Dominio | `Δ_n`, `n ≥ 2` |
| Rango | `[0, 1]` — uniforme ⇒ `0`; one-hot ⇒ `1` |
| Monotonía | creciente en el *orden de concentración* de `p`; **no** es función de `p_max` solo para `n ≥ 3` |
| Naturaleza | función de **toda** la distribución; mide **dispersión**, no la probabilidad ganadora |
| Caso `n = 2` | `C_ent = 1 − H/ln 2`, estrictamente creciente en `p_max` ⇒ equivalente a las demás (§4) |
| Clase de equivalencia | sola, para `n ≥ 3` |

### DEF-3 — `noul` de Laya **[A]**

> `C_noul(π) = max(π, 1 − π)`,  `π ∈ [0,1]`

| Propiedad | Valor |
|---|---|
| Fuente | `laya.studio/docs/jev-migration` |
| Dominio | `[0,1]` (primitiva binaria; equivale a `Δ_2` con `p_max = max(π,1−π)`) |
| Rango | `[0.5, 1]` — **nunca baja de 0.5** |
| Monotonía | creciente en `|π − 0.5|`; estrictamente creciente en `p_max` |
| Relación | **idéntica a `C_max` en `n = 2`**: `max(π,1−π) = p_max` |
| Nota | TypeSafe **no** emite `confidence` en `noul`; esta definición es de Laya |

### DEF-4 — Probabilidad ganadora (`p_max`) **[A]**

> `C_max(p) = p_max`

| Propiedad | Valor |
|---|---|
| Fuentes | Laya `answer_confidence` (medido); `vagmi/jev-lite` |
| Dominio | `Δ_n`, `n ≥ 2` |
| Rango | `[1/n, 1]` |
| Monotonía | estrictamente creciente en `p_max` (identidad) |
| Clase de equivalencia | `{C_max, C_Jev}` a `n` fijo |

### DEF-5 — Margen **[A]**

> `C_mar(p) = p_(1) − p_(2)`

| Propiedad | Valor |
|---|---|
| Fuente | estadístico estándar; usado como entrada de la cabeza `act_probability` (Laya) |
| Dominio | `Δ_n`, `n ≥ 3` (para `n = 2`, `C_mar = 2·p_max − 1`) |
| Rango | `[0, 1]` |
| Monotonía | **no monótona en `p_max`**: depende de `p_(2)` |
| Caso `n = 2` | equivalente al resto (§4) |

### DEF-6 — `action.act_probability` de Laya **[O]**

> `C_act(p) = f_θ( p_max, C_mar, H(p), n )` — cabeza aprendida, `θ` no publicado

| Propiedad | Valor |
|---|---|
| Fuente | `laya.studio/learn/act-escalate-routing` |
| Dominio / rango | `Δ_n → [0,1]` |
| Analizabilidad | ninguna (opaca). **No** tiene clase de equivalencia en orden |
| Medición reportada | AUROC **0.30** vs. acierto → **sin señal útil**; el propio ecosistema usa `confidence` (AUROC 0.77) |
| Implicación | se conserva en el catálogo por completitud; para la matriz se trata como **no transferible** |

### DEF-7 — Recalibraciones de AnyJev **[T]**

Transformaciones que se aplican a `p` **antes** de una definición de las de arriba:

- **`L0` (debiasing sin etiquetas):** `p' = Proj_{Δ_n}( p − b )`, donde `b` es un prior estimado por
  marginalización por desplazamiento cíclico. **No** usa etiquetas (compatible con D2).
- **`L1` (temperatura con etiquetas):** `p' = softmax( log p / T )`, `T` ajustado sobre 100–500 etiquetas
  **de un dataset ya etiquetado** (sin anotación humana nueva — compatible con D2).
- Nivel **`raw`**: la definición sin transformar.

Después de `L0`/`L1` se recalcula la definición elegida (DEF-1…DEF-5) sobre `p'`.

### DEF-8 — `confidence` de open-decision-ai **[O]**

Modelo propio de ~50 M; `C ∈ [0,1]`, ECE reportado `0.045` en `choice`. Opaca: se cataloga y se mide, no se
descompone.

---

## 4. Relaciones formales entre definiciones

### 4.1. Equivalencia en orden

> **Definición.** `C_A` y `C_B` son **equivalentes en orden** (sobre un dominio `D`) si existe
> `φ: range(C_A) → range(C_B)` **estrictamente creciente** con `C_B = φ(C_A)` en `D`.

Consecuencia operativa: si son equivalentes en orden, **un umbral transfiere de forma exacta** (mismo conjunto
de ítems por encima del umbral, restringido a `D`); si no, puede reordenar y la transferencia falla.

### 4.2. Proposición 1 (Jev ↔ `p_max`)

Con `n` fijo, `C_Jev = φ(C_max)` con `φ(x) = (n·x − 1)/(n − 1)`, estrictamente creciente y afín.
**⇒ `{C_max, C_Jev}` es una clase de equivalencia en orden a `n` fijo**, con `φ` explícita y su inversa
`φ⁻¹(y) = (y·(n−1) + 1)/n`. La transferencia de umbral entre ellas es **exacta**.

> **Ojo (frontera de la proposición):** `φ` **depende de `n`**. Dos definiciones equivalentes a un `n` dado
> **no** lo son entre cardinalidades distintas: el mismo `τ` sobre `C_Jev` con `n = 2` y con `n = 5` no
> selecciona el mismo conjunto. La incompatibilidad reaparece **al cruzar `n`**.

### 4.3. Proposición 2 (entropía ⊀ `p_max`, `n ≥ 3`)

Para `n ≥ 3` existen `p, p' ∈ Δ_n` con `p_max = p'_max` y `H(p) ≠ H(p')` (p. ej. `p = (0.6,0.2,0.2)` y
`p' = (0.6,0.4,0.0)`). Por tanto `C_ent` **no** es función de `p_max`, y **no** existe `φ` estricta con
`C_ent = φ(C_max)`. **⇒ `C_ent` forma clase propia**; la transferencia `C_max ↔ C_ent` es, en general,
**falible** y su magnitud la fija la matriz.

### 4.4. Proposición 3 (el fenómeno es de `n ≥ 3`)

Para `n = 2` la distribución tiene **un solo grado de libertad** `p_max ∈ [1/2, 1]`, y sobre él **todas** las
definiciones son estrictamente monótonas:

`C_max = p_max`, `C_Jev = 2p_max − 1`, `C_noul = p_max`, `C_mar = 2p_max − 1`,
`C_ent = 1 − H(p_max)/ln 2`.

**⇒ con `n = 2`, todas las definiciones son equivalentes en orden y la transferencia de umbral es exacta.**
La incompatibilidad de umbrales es un fenómeno **exclusivo de `n ≥ 3`** (y del cruce entre cardinalidades,
Proposición 1). Este es el enunciado que da forma a toda la matriz.

### 4.5. Tabla de clases de equivalencia (a `n` fijo)

| `n` | Clases de equivalencia en orden | Transferencia |
|---|---|---|
| `n = 2` | **una sola clase**: `{C_max, C_Jev, C_noul, C_mar, C_ent}` | **exacta** entre todas |
| `n ≥ 3` | `{C_max, C_Jev}` · `{C_ent}` · `{C_mar}` | exacta dentro de la primera; **falible** entre clases |
| entre `n` | `C_max`/`C_Jev` cambian de mapa (`φ` depende de `n`) | **falible** al cruzar cardinalidades |

---

## 5. Transferencia de umbral (definición operativa de la matriz)

Dados origen `A`, destino `B`, cobertura objetivo `q ∈ (0,1)` y conjunto de calibración `S_cal`:

1. `τ_A = min { τ : (1/|S_cal|)·Σ_{i∈S_cal} 𝕀[C_A(i) ≥ τ] ≤ 1 − q }` (umbral que deja cobertura `q`).
2. Aplicar `τ_B := τ_A` **tal cual** (sin re-ajuste) al destino.
3. En prueba `S_te`: `cobertura_B = (1/|S_te|)·Σ 𝕀[C_B ≥ τ_A]`;
   `precisión_B = (1/|S_te|)·Σ 𝕀[C_B ≥ τ_A]·a_i / cobertura_B`.

**Celda de la matriz:** `Δ(A→B) = q − cobertura_B`, con `precisión_B` al lado. Por Proposición 1, las celdas
dentro de una clase de equivalencia (y todo `n = 2`) deben salir `Δ = 0` salvo ruido de empates; las celdas
entre clases (`pmax ↔ ent`, `pmax ↔ margen`, cruces de `n`) son las informativas.

---

## 6. Tests de conformidad de la librería (`jev-conf-metrics`)

Cada definición se acompaña de estas aserciones (semilla fija, `Δ_n` muestreado + casos exactos):

| Test | Aserción |
|---|---|
| T1 rango | para todo `p ∈ Δ_n`: `C(p) ∈ [rango]` (Jev/pmax/ent/mar: `[0,1]`; noul: `[0.5,1]`) |
| T2 extremos | uniforme ⇒ `C_Jev=C_ent=0`; one-hot ⇒ `C_Jev=C_ent=C_max=1` |
| T3 monotonía | `C_Jev` y `C_max` crecientes en `p_max`; `C_ent` NO determinada por `p_max` (`n≥3`) |
| T4 Prop.1 | `|C_Jev(p) − φ(C_max(p))| < 1e−12` para `n` fijo; y transferencia de umbral exacta (`Δ=0`) |
| T5 Prop.2 | existen `p,p'` con `p_max` igual y `C_ent` distinto (par explícito `(0.6,0.2,0.2)` vs `(0.6,0.4,0)`) |
| T6 Prop.3 | `n=2`: transferencia exacta entre **todas** las definiciones |
| T7 referencia publicada | `p=(0.0118,0.4629,0.5253)` ⇒ `C_Jev=0.288`, `C_ent≈0.320`, `C_max=0.525` |
| T8 simetría `noul` | `C_noul(π) = C_noul(1−π)` y `C_noul ≥ 0.5` |

*(T4–T8 ya están implementados y verificados en `src/paso0_go_no_go.py --selftest`.)*

---

## 7. Decisiones congeladas (04-oct-2026)

El alcance se **congeló** conforme a D1–D5 (el autor delegó su resolución; el detalle completo está en
`paper/00_plan_del_paper.md` §10).

| # | Decisión | Resuelto |
|---|---|---|
| A1 | `act_probability` (DEF-6) | **Solo catálogo** (opaca, AUROC 0.30 → sin señal). Fuera de la matriz |
| A2 | Mixtas (DEF-7 L1, DEF-8) | `AnyJev L0/L1` **entran** (compatibles con D2). `open-decision-ai` (DEF-8): solo catálogo |
| A3 | Cardinalidades | Reporte **por `n`**; se destaca el salto `n=2 → n≥3` (Proposición 3) |
| A4 | Cobertura objetivo `q` | principal **0.80**; sensibilidad **0.50** y **0.95** |

---

## 8. Fuentes

docs TypeSafe (`docs.typesafe.ai/primitives/choice`, `…/score`, `…/noul`) ·
`laya.studio/glossary/entropy-based-confidence` · `laya.studio/docs/jev-migration` ·
`laya.studio/learn/act-escalate-routing` · `rohitghumare.com` (fórmula de Jev medida) ·
`vagmi/jev-lite` · `PyPI anyjev` · `PyPI open-decision-ai` · `NandhaKishorM/laya` ·
arXiv:2609.33843 (medición intra-definición de `q = p_max`). Claves BibTeX en `paper/02_referencias.bib`.
