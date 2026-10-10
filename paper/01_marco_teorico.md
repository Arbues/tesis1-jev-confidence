# Marco teórico — base para el paper (Tesis 1, Ruta 1)

*Metrología y transferencia del campo `confidence` en modelos de decisión tipo Jev · 04-oct-2026*

Este documento es la **base teórica** del paper. Cubre, en orden de dependencia, todo lo que hay que
dominar y citar. Cada tema indica su fuente ancla (claves de `paper/02_referencias.bib`).

> **Versión operativa:** la que rige la matriz y el paper es `paper/03_especificacion_confidence.md` (con sus
> erratas en `docs/erratas_especificacion.md`); el borrador del paper está en
> `paper/secciones/03_marco_teorico.md`.

---

## 1. Notación

- `k` (o `n`): número de opciones etiquetadas de una pregunta (`choice` hasta 255; `score` 2–10).
- `p = (p_1, …, p_k)`: distribución devuelta sobre las opciones, `Σ p_i = 1`, `p_i ≥ 0`.
- `p_max = max_i p_i`; `y ∈ {1…k}`: etiqueta correcta; `ŷ = argmax p`.
- `a = 1[ŷ = y]`: acierto. `C`: el campo `confidence` **tal como lo emite cada implementación**.
- Dos "definiciones" `C_A`, `C_B` son **equivalentes en orden** si existe `φ` estrictamente creciente con
  `C_B = φ(C_A)`; entonces un umbral transfiere de forma exacta **aplicando el mapa** (`τ_B = φ⁻¹(τ_A)`), no
  copiando el número.

---

## 2. Qué es calibrar

Un modelo está **calibrado** si, de las veces que dice "0.8", acierta el 80 %. Formalmente, para un
predictor probabilístico `p` sobre clases:
`P(ŷ = y | p_max = c) = c` para todo `c ∈ [0,1]` (calibración de confianza / *confidence calibration*).
La **discriminación** (capacidad de ordenar aciertos por confianza) es **otra cosa** y se mide con AUROC;
un modelo puede discriminar bien y estar mal calibrado (fuente: `guo2017`).
El **diagrama de fiabilidad** (accuracy vs confidence por cubos) es la visualización estándar.

Referencias: `guo2017`, `niculescu2005`.

---

## 3. Métricas de calibración y de error probabilístico

- **ECE** (Expected Calibration Error): particiona `[0,1]` en `M` bins, `ECE = Σ_m (|B_m|/N) · |acc(B_m) − conf(B_m)|`.
  Variante **igual masa** (*adaptive/quantile ECE*) cuando los bins tienen el mismo número de muestras —importante
  cuando las probabilidades se amontonan cerca de 0/1. Fuente: `naeini2015`, `guo2017`.
- **MCE**: el máximo de los gaps por bin.
- **Brier** (multiclase): `Brier = (1/N) Σ_i Σ_k (p_{ik} − y_{ik})²`. Fuente: `brier1950`.
- **NLL / log-loss**: `NLL = −(1/N) Σ_i log p_i(y_i)`.
- **Nota clave:** ECE cambia con el esquema de bins (igual ancho vs igual masa); por eso hay que **reportar el
  esquema**. El ecosistema reporta ECE sin decir el esquema → parte de la heterogeneidad de la tabla.

Referencias: `naeini2015`, `guo2017`, `brier1950`.

---

## 4. Reglas de puntuación estrictamente propias

Una regla de puntuación `S(P, y)` es **propia** si el forecaster maximiza la puntuación esperada reportando su
distribución verdadera, y **estrictamente propia** si el óptimo es único. Es la base teórica de RLCD: la
recompensa de Jev (log + 0.75·spherical, con RPS para ordinal) es estrictamente propia, así que **en teoría
reportar honestamente es la única estrategia óptima** (fuente: `gneiting2007`).

Ejemplos (categóricas):
- **Log score:** `S_log = log p(y)`.
- **Spherical / quadratic (Brier):** `S_sph = p(y) / ‖p‖₂`, `S_quad` = Brier.
- **RPS (Ranked Probability Score)** para variables **ordinales** (`score`): suma de `(CDF_pronóstico − CDF_obs)²`;
  penaliza por distancia, no por etiqueta equivocada (fuente: `epstein1969`).

Referencias: `gneiting2007`, `good1952`, `epstein1969`, `brier1950`.

---

## 5. Estadísticos de confianza — y la definición de cada implementación

El punto del paper. La misma distribución `p` produce **varios números** según quién calcule `confidence`:

| Implementación | Definición | Tipo |
|---|---|---|
| **Jev 1.13** | `C_Jev = (n·p_max − 1)/(n − 1)` | afín en `p_max` |
| **Laya** (`choice`/`score`) | `C_Laya = 1 − H(p)/log k`, con `H(p) = −Σ p_i log p_i` | entropía normalizada |
| **Laya** (`noul`) | `C = max(p, 1−p)` | orden-estadístico (k=2) |
| **Laya** `answer_confidence` | `C = p_max` | `p_max` |
| **Laya** `action.act_probability` | cabeza aprendida sobre (`p_max`, margen, entropía, `n`) | aprendido (sin señal útil: AUROC 0.30) |
| **jev-lite** | `C = p_max` (gana a la entropía, AUROC 0.816) | `p_max` |
| **AnyJev** | niveles `raw` / `L0` / `L1` | crudo / corregido |
| **logit-classifier** | prior de etiqueta aprendido | aprendido |
| **open-decision-ai** | `confidence` propia (ECE 0.045 en choice) | mixto |

También: `margen = p_(1) − p_(2)` (segundo estadístico más usado).

### Proposición (núcleo interno del paper)

**P1.** Para `n` fijo, `C_Jev = (n·p_max − 1)/(n − 1)` es una función **estrictamente creciente y afín** de
`p_max`. En consecuencia, `C_Jev` y `p_max` son **equivalentes en orden**: el umbral que da cobertura `q` con
`C_Jev` da exactamente la misma cobertura con `p_max` (bajo el mismo `n`).

**P2.** La **entropía normalizada** `1 − H/log k` **no** es función de `p_max` solo: para `k ≥ 3` existen dos
distribuciones con el mismo `p_max` y distinta `H`. Por tanto, **en general un umbral NO transfiere** entre
una definición tipo `p_max` y una tipo entropía.

**Consecuencia:** las definiciones se parten en **clases de equivalencia en orden** (transferencia exacta) y
**pares peligrosos** (transferencia fallida). La **matriz de transferencia** mide la magnitud del fallo.

> Ejemplo motivador (medido en el ecosistema, `rohitghumare`): la distribución `(0.0118, 0.4629, 0.5253)`
> da `0.288` (Jev), `0.3199` (Laya entropía) y `0.5253` (`p_max`) — tres números del mismo dato.

Referencias: `rohitghumare`, `layastudio`, `jev2026docs`.

---

## 6. Transferencia de umbrales (definición formal)

Para un origen `A`, destino `B`, cobertura objetivo `q`, y conjunto de calibración:
1. Hallar `τ_A` con `cobertura_A(τ_A) = q`.
2. Aplicarlo tal cual a `B`: `τ_B := τ_A`.
3. Medir en el conjunto de prueba: `cobertura_B(τ_A)` y `accuracy-on-answered_B(τ_A)`.
La **degradación** `Δ = cobertura_A(τ_A) − cobertura_B(τ_A)` es la celda de la matriz. Se repite también
**entre datasets** (`τ` ajustado en dataset A, aplicado en B), donde `jebadiah` mostró que la calibración no
viaja.

Referencias: `jebadiah`, `arXiv2609.33843`.

---

## 7. Predicción selectiva y umbrales de abstención

Cuando el modelo decide "actúo o escalo": con probabilidad de acierto `p`, coste de error `C_err` y coste de
escalar `C_esc`, conviene actuar si `(1−p)·C_err < C_esc`, i.e. `p > 1 − C_esc/C_err`. Curvas
**risk–coverage** y **AURC** resumen el compromiso acierto/cobertura. La fórmula de coste da el umbral
**si las probabilidades están calibradas** — que es justo lo que falla.

Referencias: `chow1970`, `geifman2017`, `jitkrittum2023`.

---

## 8. Calibración post-hoc

- **Temperature scaling**: `p̂ = softmax(z/T)`, `T>0` óptimo por NLL en validación; no cambia la clase predicha.
  Fuente: `guo2017`.
- **Platt scaling** (sigmoide en logits) y **isotonic regression** (monótona no paramétrica). Fuente: `platt1999`, `zadrozny2002`.
- **Por qué elegir por NLL puede fallar fuera de muestra**: reglas expresivas (isotonic) ganan en la partición
  de ajuste y **no generalizan**; verificado en `arXiv2609.33843`.

Referencias: `guo2017`, `platt1999`, `zadrozny2002`, `arXiv2609.33843`.

---

## 9. Conformal prediction (cobertura sin supuestos)

Construye conjuntos de predicción con **garantía de cobertura** `≥ 1−α` libre de distribución, a partir de un
conjunto de calibración; y de ahí una **abstención** con tasa de error controlada. Alternativa a calibrar
`confidence` directamente; útil para la barrera de abstención.

Referencias: `vovk2005`, `angelopoulos2021`.

---

## 10. El objeto: el modelo de decisión tipo Jev

**Jev (TypeSafe System One, `jev-1.13.0`).** Primitivos: `choice` (≤255 opciones; devuelve opción +
`probabilities` + `confidence`), `score` (2–10 niveles ordinales; + `legend`), `noul` (0.0–1.0; **sin**
`confidence`). Mecánica: **no genera texto**; termina con *readout* de logits en la posición de cada etiqueta
y softmax **solo sobre las etiquetas permitidas** → `output_tokens = 0` **por construcción**. Estado
compartido y preguntas aisladas → **no hay distribución conjunta**. TypeSafe **no publica** ECE, pérdida ni pesos.

**Laya** (`NandhaKishorM/laya`, Apache-2.0, 421M = ModernBERT-large + cabeza que puntúa un token `[MASK]`).
Única implementación que publica el bucle RLCD completo; encoder congelable → features cacheadas.

Referencias: `jev2026docs`, `jev2026blog`, `archerhume`, `navinpai`, `layaRepo`, `layamultilingual`.

---

## 11. RLCD — y su análisis cerrado

Ruido gaussiano de media cero en los logits (σ 1.0 → 0.3) + regla **estrictamente propia** + REINFORCE con
baseline de grupo (estilo GRPO) + temperatura post-hoc. **Análisis cerrado (26-sep-2026):** el término RL
equivale al gradiente de la cross-entropy **suavizada con ruido** (identidad con el **lema de Stein**); como
el óptimo suavizado se reporta sin ruido, **la inferencia sale sobre-confiada**; la única palanca real fue el
**presupuesto de tokens de opción**.

Referencias: `navinpai`, `waynechang`, `arXiv2609.38850`, `lakoreai2026`.

---

## 12. Estadística de la evaluación

- **Bootstrap** para intervalos de confianza de ECE/Brier/cobertura (no paramétrico).
- **Pre-registro** de la cobertura objetivo, las definiciones y los datasets **antes** de la corrida principal.
- **Corrección por comparaciones múltiples (FDR)** al probar muchos pares de definiciones (como hace `arXiv2609.33843`).
- **Tamaño de muestra**: 200–240 casos fue insuficiente para estabilizar la selección de calibrador en
  `arXiv2609.33843` → dimensionar los conjuntos.

Referencias: `arXiv2609.33843`, `efron1993`.

---

## 13. Mapa de lecturas (orden de estudio)

1. `guo2017` — calibración y temperature scaling (base).
2. `gneiting2007` — reglas propias (base teórica de RLCD).
3. `arXiv2609.33843` — el estado del arte más cercano a nuestra medición.
4. `naeini2015` (ECE) → `chow1970`/`geifman2017` (selectiva) → `angelopoulos2021` (conformal).
5. `arXiv2609.38850` + `lakoreai2026` (por qué RLCD no calibra) y `rohitghumare`/`layastudio` (las definiciones).

---

*Fuentes detalladas en `paper/02_referencias.bib` y en `eje-2-jev-opensource/FUENTES.md`.*
