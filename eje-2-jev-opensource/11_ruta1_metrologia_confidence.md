# Tesis 1 — RUTA 1: Metrología y transferencia del campo `confidence`

**Documento principal vigente** · eje 2 (Jev, Laya y el ecosistema de modelos de decisión) · 04-oct-2026
Sustituye como *propuesta a ejecutar* a `10_tres_rutas_tesis1.md` (que queda como registro de la elección).

> **Título (definitivo, 10-oct-2026):** *Metrología y transferencia del campo `confidence` en modelos de
> decisión de pesos abiertos tipo Jev.*
> **English:** *Metrology and Threshold Transfer of the `confidence` Field in Open-Weight Jev-Type
> Decision Models.*
> Regla de estilo: sin dos puntos, sin subtítulo, sin signos de interrogación. El título se fija al cerrar
> la especificación.

---

## 0. Estado y decisión

- **Ruta elegida (04-oct-2026): RUTA 1.** Razón: es la única que sigue abierta como *instrumento*, es un
  artefacto puro (D1), no exige anotación manual (D2), y su matemática cabe entera en el marco teórico.
- **Equipos disponibles:** Mac Mini (Apple Silicon) y Acer Nitro con **RTX 4050 Laptop 6 GB**. El servidor
  `thinkpad-t440` **no tiene GPU**: solo orquesta. Nada de nube (D5).
- **Sondeo del 04-oct-2026 (ver §9):** las rutas 2 y 3 del documento anterior quedaron casi ocupadas
  (RLCD y cartografía). La metrología de `confidence` sigue libre como **tabla sistemática**, aunque la
  *afirmación* "los umbrales no transfieren" ya circula en anécdotas. Por eso el aporte se define como
  **el instrumento que lo cuantifica**, no como el hallazgo.

---

## 1. El problema (por qué es un problema real)

En el ecosistema tipo Jev, **el mismo campo `confidence` significa cosas distintas según quién lo emite**,
y todas se usan para lo mismo: fijar un umbral y decidir "actúo o escalo a un humano". Un umbral
calibrado sobre una definición **no significa nada** sobre otra, pero el ecosistema los porta entre
modelos como si fueran intercambiables.

Evidencia medida (cada cifra con su fuente — regla D4):

| Implementación | Definición de `confidence` | Fuente |
|---|---|---|
| **Jev 1.13** | `(n·p_max − 1)/(n − 1)` — concentración, **no** la probabilidad ganadora | docs TypeSafe; fórmula medida to-a-to en 30 tickets por rohitghumare.com |
| **Laya** (`choice`, `score`) | `1 − H(p)/log k` (entropía normalizada) | laya.studio/glossary/entropy-based-confidence |
| **Laya** (`noul`) | `max(p, 1 − p)` | laya.studio/docs/jev-migration |
| **Laya** `answer_confidence` | `p_max` (la probabilidad del ganador) | rohitghumare.com (medido) |
| **Laya** `action.act_probability` | cabeza aprendida sobre (p_max, margen, entropía, nº opciones) | laya.studio/learn/act-escalate-routing (**sin señal útil: AUROC 0.30; se usa `confidence`, AUROC 0.77**) |
| **jev-lite** | `p_max` — **gana** a la entropía normalizada (AUROC 0.816) | FUENTES.md §3 |
| **AnyJev** | niveles `raw` / `L0` (debiasing sin etiquetas) / `L1` (temperatura con etiquetas) | MarkTechPost / PyPI anyjev |
| **logit-classifier** | prior de etiqueta aprendido como media móvil | FUENTES.md §4 |
| **open-decision-ai** | `confidence` propia (ECE 0.045 en `choice`) | PyPI open-decision-ai |

**Lo que está medido hoy:** una distribución de 3 opciones `(0.0118, 0.4629, 0.5253)` da, a la vez,
`0.288` (formula de Jev), `0.3199` (entropía de Laya) y `0.5253` (p_max) — tres números del mismo dato,
y hasta `0.24` de diferencia entre los dos primeros. Un blog lo midió sobre **30 tickets**; un paper
pre-registrado lo midió **dentro de una sola definición** (`q = p_max`) sobre un modelo; **la matriz
sistemática entre definiciones × modelos × datasets no existe**.

---

## 2. El artefacto final

> **Especificación + librería + arnés de conformidad del campo `confidence`, y la MATRIZ de
> transferencia de umbrales** medida sobre modelos de pesos abiertos, más el dataset de mediciones crudas
> y el script que lo regenera todo.

No es un paper que "descubre" que la calibración no se porta: es **el instrumento con el que se mide**.
El patrón es Guo et al. (2017) para el eje de calibración: no descubrieron que las redes modernas están
des-calibradas — dieron la métrica y la corrección que todo el campo cita. Aquí, quien afirme que los
umbrales no transfieren tendrá que **citar la matriz**, no reemplazarla.

---

## 3. Entregables

1. **Especificación formal** de cada definición como función de la distribución devuelta y de la
   cardinalidad `n` (con dominio y rango: p.ej. `noul` nunca baja de 0.5; la entropía normalizada de un
   `choice` de 4 opciones a 0.5 ya es una distribución picuda).
2. **Librería `jev-conf-metrics`** (MIT o Apache-2.0) que implementa todas las definiciones, con
   **tests de conformidad** contra salidas publicadas (precedente: el arnés `jev-verify` recomputa las
   identidades de confianza de Jev contra repos públicos).
3. **Matriz de transferencia de umbrales**: para cada par (definición origen A → definición destino B),
   cada modelo y cada dataset, el umbral `τ_A` que da una cobertura objetivo (p.ej. 80 %) y la
   **cobertura y precisión REALES** que produce al aplicarlo con B. Es la tabla que convierte "los
   umbrales no son comparables" en **una cifra por celda**.
4. **Dataset de mediciones crudas**: una fila por (modelo × dataset × ítem) con la distribución devuelta,
   la etiqueta, el acierto, y todas las definiciones de `confidence` calculadas en paralelo.
5. **Script regenerador** (`make matrix`) + figura de la matriz (§7).
6. **Pre-registro con DOI** antes de correr la medición principal.

---

## 4. Diseño de la medición (automática, cero etiquetado propio)

### 4.1 Modelos (pesos abiertos, ≤ 6 GB — cuantizar a 4 bits si hace falta)
Laya base 421M · Laya-typed-decisions 421M · Laya-multilingual 322M · Kev 0.5B / 0.8B · Nimble-9B (LoRA,
cuantizado) · Jeff-1 (Qwen3-4B) · jev-lite (Gemma 4 E4B) · tinyjev 596M · chaoliangUNSW Jev-Style 2B ·
open-decision-150m · **y un control "LLM crudo a nivel L0/L1" con AnyJev** (Qwen3-8B), para tener la
definición *sin entrenar*. Los 4B/9B solo si el 4-bit los mete en 6 GB; si no, se corren en el Mac Mini
con memoria unificada.

### 4.2 Datasets (ya etiquetados — D2: cero anotación)
`LocalLLaMA/typed-decisions` (2.000 decisiones / 4 flujos, Apache-2.0 — el benchmark compartido) ·
`jaredpalmer/kev-suites` · `alisawuffles/WANLI` (CC-BY-4.0) · Banking77 · CLINC150 · MedHallu (1.000) ·
AG News · SST-5 · DAIR Emotion (los tres últimos los usan los benches del ecosistema, para comparabilidad).

### 4.3 Procedimiento
1. Para cada modelo: leer la **distribución completa** sobre las opciones (no solo el ganador).
2. Calcular **todas** las definiciones de `confidence` (§1) a partir de esa misma distribución.
3. Métricas por (modelo × dataset): accuracy, Brier, NLL, **ECE** (bins de igual ancho **y** de igual
   masa), y **AUROC de cada definición vs. el acierto** (discriminación, que es distinta de calibración).
4. **Transferencia de umbral:** en el conjunto de calibración, hallar en A el `τ_A` que da 80 % de
   cobertura; aplicarlo tal cual a B en el conjunto de prueba; medir cobertura y precisión resultantes.
   Repetir también **entre datasets** (τ ajustado en A, aplicado en B) — es el eje donde `jebadiah` mostró
   que la calibración no viaja.
5. Agregar con **bootstrap** (IC 95 %), corregir comparaciones múltiples con **FDR**.

---

## 5. Por qué sobrevive al hueco

- El "*cuánto*" (que está des-calibrado) y el "*por qué*" (RLCD no basta) ya están ocupados. **El
  instrumento de metrología, no.**
- La afirmación cualitativa "los umbrales no transfieren" ya circula (30 tickets, un blog) → eso **refuerza**
  la ruta: el campo necesita justamente la tabla sistemática que fije la magnitud por modelo y dataset.
- Aunque otro publique el mismo hallazgo, la matriz y la librería siguen siendo la referencia.

---

## 6. Reparto de trabajo

| | Tarea |
|---|---|
| **Agente (automático)** | descarga de pesos, cacheo, inferencia, cálculo de todas las definiciones, ECE/Brier/AUROC, construcción de la matriz, bootstrap + FDR, figuras, BibTeX, pre-registro, librería y sus tests |
| **Autor (manual)** | definir el alcance de la especificación (qué definiciones entran, qué cobertura objetivo) y **redactar**. **Cero etiquetado, cero anotación, cero kappa** |

---

## 7. Cómputo y costo

- **Costo monetario: $0.** Todo con pesos abiertos y datasets públicos.
- **Dónde corre:** RTX 4050 6 GB para los modelos pequeños (Laya 421M, Kev 0.8B, tinyjev) con encoder
  congelable y features cacheadas; **Mac Mini** (memoria unificada) para los 4B–9B en 4-bit. El
  `thinkpad-t440` **solo orquesta** (no tiene GPU).
- **Cuello real:** horas de inferencia, no dinero. Es la ruta de **menor** costo de cómputo de las tres.
- **Figura central:** la matriz de transferencia como *heatmap* (filas = definición origen, columnas =
  definición destino), con la caída de cobertura anotada por celda.

---

## 8. Riesgo y mitigación

| Riesgo | Mitigación |
|---|---|
| Que ya exista la matriz | Verificado el 04-oct-2026: no existe. Solo anécdotas y medición intra-definición |
| Que el ecosistema mute (152 repos en 6 días) | La ventana del **corpus ya no es el objeto**; la ruta vive de modelos con **pesos versionados y hasheados**. Se fija versión + hash por fila |
| Modelos > 6 GB | 4-bit, cacheo de features, o Mac Mini; se documenta qué modelo corrió dónde |
| Pre-registro tardío | Se escribe **antes** de la corrida principal; cobertura objetivo y definiciones se congelan |

---

## 9. Marco teórico — lo que hay que dominar (y estudiar)

Sin esto no se entiende lo que se mide ni se puede redactar el marco. Ordenado por dependencia.

| # | Tema | Qué hay que entender | Fuente ancla |
|---|---|---|---|
| 1 | **Calibración** | Qué significa que un 0.8 acierte el 80 %; **diagrama de fiabilidad**; diferencia entre *discriminación* (AUROC) y *calibración* (ECE) | Guo et al., *On Calibration of Modern Neural Networks* (2017) |
| 2 | **Métricas de calibración** | ECE (bins de igual ancho vs. igual masa), MCE, Brier, NLL; por qué el binning cambia el número | Naeini et al. (2015); Brier (1950) |
| 3 | **Reglas de puntuación propias** (*strictly proper*) | log, Brier, spherical, **RPS** para ordinal; **por qué el óptimo es reportar la probabilidad verdadera** (la premisa teórica de RLCD) | Gneiting & Raftery (2007); Good (1952); Epstein (1969) |
| 4 | **Estadísticos de confianza** | `p_max`, margen, entropía `H`, entropía normalizada `H/log k`; relación y **escala distinta** de cada uno | glossario laya.studio; medidos en jev-lite |
| 5 | **Predicción selectiva y umbrales** | cobertura, accuracy-on-answered, curvas *risk–coverage*, AURC, abstención; fórmula de coste `p > 1 − C_esc/C_err` | Chow (1970); Geifman & El-Yaniv (2017); Jitkrittum et al. (2023) |
| 6 | **Calibración post-hoc** | temperature scaling, Platt, isotonic; **por qué la regla de selección por NLL falla fuera de muestra** | Guo et al. (2017); Zadrozny & Elkan (2002); arXiv:2609.33843 |
| 7 | **Conformal prediction** | cobertura libre de distribución, conjuntos de predicción, abstención con garantía | Vovk et al.; Angelopoulos & Bates (2021) |
| 8 | **El objeto: modelo de decisión tipo Jev** | *readout* de logits, primitivos `choice`/`score`/`noul`, `output_tokens = 0`, **sin distribución conjunta**, `confidence` = concentración | docs TypeSafe; archerhume; navinpai |
| 9 | **RLCD** | ruido gaussiano en logits, regla propia, REINFORCE con baseline, temperatura post-hoc; y el análisis de que el término RL ≈ gradiente de CE suavizada → sobre-confianza | note.com/wayne_chang; navinpai; zyvop (LakoreAI) |
| 10 | **Estadística de evaluación** | bootstrap e IC, pre-registro, corrección **FDR**, tamaño de muestra | arXiv:2609.33843; estándar de la psicometría/ML |

**Lectura mínima para arrancar (3 fuentes):** Guo 2017 (calibración) · Gneiting & Raftery 2007 (reglas
propias) · arXiv:2609.33843 (el estado del arte más cercano a tu medición).

---

## 10. Paso 0 — go/no-go (medio día) · ✅ **HECHO: GO (08-oct-2026)**

Resultado en **`results/paso0_informe.md`** (regenerable con `src/paso0_informe.py`); mediciones crudas en
`results/raw/`. Resumen:

1. ✅ Descargados y corridos **Laya** (los tres checkpoints, `convaiinnovations/laya`) y **Kev-0.8B**
   (`jaredpalmer/kev-0.8b`, servido desde su repo) sobre las **2.000 decisiones** de `typed-decisions`.
2. ✅ **`output_tokens = 0`** verificado en todas las filas de Laya. **Kev reporta ese mismo campo con otro
   significado** (*billing-style*: tokens de la respuesta serializada) → hallazgo de metrología.
3. ✅ **Reproducido el número publicado:** las 5 métricas del README de Laya en los tres checkpoints, con
   **|Δ| ≤ 0.003** en `laya-typed-decisions` (ECE 0.213→**0.2157**, accuracy 0.766→**0.7685**).
4. ✅ Versiones y hashes en `results/raw/paso0_versions.json` (sha del Hub por modelo + commit del repo de Kev).

Hallazgo adicional: la **`choice_confidence` de Kev es algebraicamente la fórmula de Jev**
(`(K·p_max−1)/(K−1)`) → por la Proposición 1, ese par **transfiere el umbral de forma exacta**.

- **Ejecutado en el Acer Nitro (RTX 4050)**, nunca en el `thinkpad-t440` (sin GPU).

---

## 11. Plan de pasos

| # | Paso | Responsable |
|---|---|---|
| 0 | Paso 0 go/no-go (arriba) | agente |
| 1 | Congelar la lista de **definiciones** y de **datasets**, y la cobertura objetivo | autor (alcance) |
| 2 | Especificación formal de cada definición | agente (redacción técnica: autor) |
| 3 | Librería `jev-conf-metrics` + tests de conformidad | agente |
| 4 | Pipeline de medición (pesos abiertos + datasets ya etiquetados) | agente |
| 5 | Matriz + dataset de mediciones crudas (versión + hash por fila) | agente |
| 6 | **Pre-registro con DOI** | agente |
| 7 | Medición principal | agente |
| 8 | Fijar el título definitivo y redactar | autor |
| 9 | (Línea paralela) estudio del objetivo RLCD para el **Taller** | — |

---

## 12. Fuentes

**Metrología y calibración:** Guo et al. 2017 (temperature scaling, ECE) · Naeini et al. 2015 (ECE) ·
Brier 1950 · Gneiting & Raftery 2007 (reglas propias) · Good 1952 (spherical) · Epstein 1969 (RPS) ·
Chow 1970 (reject option) · Geifman & El-Yaniv 2017 (selective nets) · Jitkrittum et al. 2023 (deferral) ·
Angelopoulos & Bates 2021 (conformal).

**El ecosistema (eje 2):** docs TypeSafe `docs.typesafe.ai/primitives/choice` · `typesafe.ai/blog/introducing-system-one-models-and-jev` ·
archerhume.com/posts/jevs-architecture-unmasked · `navinpai.github.io/decoding-jev/` · note.com/wayne_chang (reconstrucción de RLCD) ·
`laya.studio/glossary/entropy-based-confidence` y `laya.studio/docs/jev-migration` · rohitghumare.com (medición de la fórmula de Jev sobre 30 tickets) ·
`github.com/NandhaKishorM/laya` + `convaiinnovations/laya` (421M) · `jaredpalmer/kev` (+ kev-0.8b) · `bespokelabsai/nimble` ·
`TheoLeeCJ/SemIf-OpenJev` · `GestaltLabs/Jeff-1` · `vagmi/jev-lite` · `frontier-infra/jebadiah-9b-v0/v1` · AnyJev (Nokia) ·
`open-decision-ai` (PyPI) · `yibie/awesome-jev`.

**Cierres de septiembre (contexto, para no repetirlos):** arXiv:2609.38850 (por qué RLCD no calibra) ·
zhung (Lê Đức Minh, 26-sep-2026) + `github.com/LakoreAI/sev` (reproducción y ablación de RLCD) ·
arXiv:2609.33209 (negación/coherencia) · arXiv:2609.26758 (sesgo nombre↔definición) · arXiv:2609.26550 (JEV-as-a-Judge) ·
arXiv:2609.33843 (reproducción pre-registrada de Laya: sub-confianza, transferencia fallida del umbral) ·
arXiv:2609.30216 (*Jev in the Wild*, cartografía del ecosistema).

**Datasets:** `LocalLLaMA/typed-decisions` · `jaredpalmer/kev-suites` · `alisawuffles/WANLI` · Banking77 · CLINC150 · MedHallu · AG News · SST-5 · DAIR Emotion.
