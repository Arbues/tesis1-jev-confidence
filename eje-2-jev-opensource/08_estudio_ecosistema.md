# Ecosistema open-source de Jev — viabilidad, alcance y estado real

Estudio de campo · verificación con API de GitHub / Hugging Face / PyPI · corte 25-sep-2026

> **Nota (13-oct-2026):** las copias crudas de los READMEs de las implementaciones (`audit/jev-oss/`) se
> eliminaron del repo; son públicas en sus repositorios y las fuentes citadas aquí siguen en `FUENTES.md`.

---

## 0. Resumen ejecutivo

Cuando evaluamos Jev por primera vez lo descartamos con una razón simple: **no es open source**.
Esa razón **ya no se sostiene**. En los **seis días** posteriores al lanzamiento (18–24 sep 2026)
apareció un ecosistema completo de implementaciones abiertas: **152 repos** tocando el tema,
**367 entradas curadas** en un índice de la comunidad, **más de 20 modelos publicados** con pesos,
**2 datasets de entrenamiento abiertos** y **~30 arneses de evaluación independientes**.

El hallazgo que más importa, y que nadie ha reclamado:

> **El ecosistema abierto refutó empíricamente la premisa central de Jev.**
> TypeSafe vende que RLCD produce probabilidades calibradas. Todos los proyectos que implementaron
> RLCD y midieron con honestidad encontraron lo mismo: **el modelo sale sobre-confiado y hay que
> reajustar la temperatura sobre datos propios.** Jev no publica un solo ECE.

Eso convierte al tema en algo distinto de una comparación externa — es una pregunta sobre
**el objetivo de entrenamiento**, que es exactamente el tipo de aporte interno que buscas.

---

## 1. Qué es Jev, con precisión (la referencia cerrada)

**TypeSafe AI**, fundada por **Diogo Almeida** (co-inventor de RLHF). Jev salió el **18-sep-2026**.
Modelo actual: `jev-1.13.0`.

### 1.1 Los tres primitivos

| Primitivo | Pregunta | Devuelve | Límite |
|---|---|---|---|
| `choice` | ¿Cuál de estas N opciones? | opción + `probabilities` + `confidence` | ≤ 255 opciones |
| `score` | ¿Dónde en esta escala ordenada? | `score` fraccional + `legend` + `probabilities` + `confidence` | 2–10 niveles |
| `noul` | ¿Es verdad esto? | probabilidad 0.0–1.0 | — |

`confidence` en `choice`/`score` **no es** la probabilidad ganadora: mide qué tan concentrada está
la distribución. Fórmula publicada: `(n·p_max − 1)/(n − 1)`.

### 1.2 La mecánica real (lo verificado, no el marketing)

- **No genera texto.** Termina la inferencia con una **lectura** (`readout`) de los logits en la
  posición de cada etiqueta, y aplica softmax **solo sobre las etiquetas permitidas**.
  `usage.output_tokens = 0` no es redondeo: nunca se produjo un token.
- **Estado compartido, preguntas aisladas.** Todas las preguntas de una llamada se evalúan contra
  la misma codificación del estado, **en paralelo y sin verse entre sí**. Añadir preguntas casi no
  cambia la latencia. Consecuencia no obvia: **una pregunta y su negación pueden devolver 0.7 ambas** —
  no comparten una distribución conjunta.
- **Sin test-time compute.** Al no haber bucle de decodificación no hay forma de "pensar más".
  De ahí sus debilidades declaradas: aritmética, conteo, comparación de fechas, multi-hop, lectura literal.
- **Prompt congelado.** Mover un salto de línea mueve los logits, y con ellos los umbrales ya calibrados.

### 1.3 RLCD — el método que nadie puede inspeccionar

**Reinforcement Learning for Calibrated Decisions.** Lo que se sabe del análisis de implementaciones abiertas:

| Componente | Descripción |
|---|---|
| Exploración | Ruido **gaussiano de media cero** inyectado en los logits (proyectado a media cero para no distorsionar el softmax) |
| σ | Annealing de **1.0 → 0.3** durante el entrenamiento |
| Recompensa | **Reglas de puntuación estrictamente propias** (*strictly proper scoring rules*): `log score` (con suelo ≈ −9.21) **+ 0.75 × spherical score**; para `score` ordinal se resta el **Ranked Probability Score** |
| Ventaja | Media y desviación de la recompensa sobre el grupo de candidatos ruidosos (**estilo GRPO**) |
| Actualización | **REINFORCE con baseline de grupo**, sin cross-entropy supervisada |
| Después | Se ajusta una **temperatura** con red congelada, minimizando cross-entropy |

La propiedad que se busca: la recompensa esperada se maximiza **solo** si el modelo reporta sus
probabilidades verdaderas. En teoría, reportar honestamente es la única estrategia óptima.

**Lo que no existe:** ni paper, ni pérdida publicada, ni dataset, ni pesos de Jev.
TypeSafe **no ha publicado un solo número de calibración** (ni ECE, ni diagrama de fiabilidad
de su modelo) para una empresa cuyo producto central es la calibración.

### 1.4 La arquitectura (análisis especulativo, pero bien fundado)

**Archer Hume**, 17-sep-2026 — *"Jev's Architecture Unmasked"*, **10.000 llamadas a la API**
sondeando escalado de latencia, reordenamiento de preguntas y longitud de contexto. Siete principios:

1. Terminar la inferencia con una lectura (*readout*), no con generación
2. Compartir el estado, aislar las preguntas
3. Backbone **causal** (no bidireccional)
4. **Dejar que las opciones interactúen antes de elegir**
5. Entrenar la distribución, **calcular la confianza después**
6. Capacidad **dispersa** (probablemente MoE)
7. Programar las ramas como **batch**, no como conversación

Es la referencia arquitectónica que usa **Kev** para construirse. Marcado explícitamente como
especulativo por su autor.

---

## 2. El ecosistema: seis días de edad

Fechas de creación verificadas por API:

```
17-sep  archerhume: "Jev's Architecture Unmasked" · jaredpalmer/kev
18-sep  LANZAMIENTO DE JEV · NandhaKishorM/laya · bespokelabsai/nimble
19-sep  mizorewww/laya-mlx · mizorewww/laya-coreml · vagmi/jevlite
20-sep  frontier-infra/jebadiah-9b-v0
21-sep  fastjev · anyjev
22-sep  tinyjev · tydex
23-sep  chaoliangUNSW (HF) · logit-classifier
24-sep  laya-multilingual · frontier-infra/jebadiah-9b-v1 · laya v0.3.20
25-sep  kev (último push observado)
```

**Esto es una fiebre del oro de seis días.** Consecuencia metodológica crítica: buena parte de lo
publicado **no está probado**. El propio índice curado `awesome-jev` pone esta advertencia:

> *"Cuidado especial con los envíos en bloque del mismo día. Varios repositorios publicados juntos
> por un mismo autor, compartiendo un andamiaje y un historial de commits delgado, pueden satisfacer
> todas las reglas de inclusión y seguir sin estar probados. **El volumen no es evidencia de calidad.**"*

---

## 3. Taxonomía por rigor — lo que sobrevive a la inspección

### Tier A — Reproducciones con receta completa y pesos propios

Son las que valen. Implementan el método y publican tanto los pesos como cómo llegaron a ellos.

| Proyecto | Licencia | Base | Tamaño | Evidencia medida | Verificado |
|---|---|---|---|---|---|
| **Laya** `NandhaKishorM/laya` | Apache-2.0 | ModernBERT-large + cabeza propia | **421M** | in-task macro acc **0.838**, macro ECE **0.060**; routing 0.991/ECE 0.009; zero-shot 0.651/0.207 | ★**23.3k** repo · HF ♥3.447 |
| **Kev** `jaredpalmer/kev` | Apache-2.0 | Qwen3.5 / Qwen3.8 | 0.5B→**27B** (7 checkpoints) | kev-27B: **0.848 vs 0.857 de Jev** en fuentes nuevas; Brier 0.236 | ★**6.790** · HF ↓6.087 (4B) |
| **Nimble** `bespokelabsai/nimble` | (ver repo) | Qwen3.5-9B + LoRA | **9B** | **90.1%** acuerdo con etiquetas de referencia vs **66.4%** del base vs **93.2% de Jev** en 324 ejemplos retenidos | ★1.741 |
| **SemIf** (ex-OpenJev) `TheoLeeCJ/SemIf-OpenJev` | **MIT** | Qwen3.8-27B (puente EXL3) / Qwen3.5-4B | 4B / 27B | temperatura **por carga de trabajo** con **ECE fuera de muestra**; WANLI externo | ★**4.251** |

**Laya** es la implementación de RLCD de referencia: es la única que publica el bucle completo
(política → ruido gaussiano en logits → regla de puntuación propia → REINFORCE con baseline de grupo
→ ajuste de temperatura). Trae **notebook de fine-tuning en Kaggle con 2×T4 gratis** (~4 h).

**Kev** es la más honesta metodológicamente: *"No sabemos con qué se entrenó Jev, así que esto no es
una comparación controlada"*. Y su receta de fine-tuning es la más práctica:
**3 preguntas, 1.050 registros generados, 15 minutos en una H100 → Kev-4B de 67,7% a 73,6%.**
El 0.8B entrena con `--batch 1 --accum 8` en bf16 **en una GPU de 4 GB**.

**Nimble** es el aporte científico más limpio: publicó **2.676 ejemplos de entrenamiento y 324
retenidos**, y un arnés que corre **Nimble y Jev sobre los mismos registros** de 13 subconjuntos
públicos con etiquetas humanas. Declara explícitamente *"no destilamos de Jev"*. Construido en un día.

### Tier B — Adaptadores entrenados con medición honesta

| Proyecto | Base | Tamaño | Números clave |
|---|---|---|---|
| **Jeff-1** `GestaltLabs/Jeff-1` | Qwen3-4B-Instruct + LoRA | 4B | **9.730 filas humanas**: Jeff **0.8183** vs **Jev 0.8283**; ECE **0.0807** vs **0.0932** (Jev peor); Brier 0.2839 vs 0.2750 |
| **jev-lite** `vagmi/jev-lite` | Gemma 4 E4B + QLoRA NF4 | 8B (34,9M entrenables) | **ECE 0.019**; entrenado **1 h 40 min en una RTX 4090**; paradoja: servido en bf16 el ECE se **duplica** (0.036 → 0.069) |
| **jebadiah** `frontier-infra/jebadiah-9b-v0/v1` | Qwen3.5-9B + LoRA | 9B / 4B | 11.072 preguntas públicas, **1 época, 45 min en una H100**; hallazgo: la temperatura de `score` aprendida de targets del profesor **empeora** la calibración en rúbricas humanas |

**El caso `jebadiah` es el más interesante para tu tesis:** la temperatura de `score` fue aprendida
de **targets suaves del profesor** y transfiere a *typed-decisions* pero **no a rúbricas humanas**,
donde empeora la calibración. Eso es evidencia directa de que **el objetivo de entrenamiento optimiza
una cosa y la calibración en el mundo real es otra**. La v1 lo corrige — y el hecho de que haya que
corregirlo es el dato.

**`jev-lite`** encontró algo contraintuitivo y medido: **`p_max` gana a la entropía normalizada** como
estadístico de confianza (AUROC 0.816 vs peor ECE). La entropía normalizada —la primera opción obvia—
"lee un 0.85/0.08/0.07 decisivo como baja confianza" y manda el 45% del tráfico a revisión humana.
**Y Laya define `confidence` como 1 − entropía normalizada.** Dos implementaciones serias, dos
definiciones incompatibles del mismo campo — un umbral no transfiere entre ellas.

### Tier C — Lectura de logits sin entrenamiento (el "truco" puro)

| Proyecto | Qué es | Nota de honestidad |
|---|---|---|
| **open-jev** `daseinlabs/open-jev` (★110, MIT) | Una pasada sobre Gemma 3 4B local, MLX/PyTorch | *"las probabilidades zero-shot son verosimilitudes softmax del siguiente token, **no juicios calibrados**"* |
| **SemIf / fastjev** | Logits directos declarados | *"no reproduce la calibración de Jev"* |
| **AnyJev** (PyPI) | Convierte **cualquier** LLM en modelo tipo Jev, sin entrenar | Introduce niveles: `raw` / `L0` (debiasing sin etiquetas) / `L1` (temperatura con 100–500 etiquetas) |
| **logit-classifier** (PyPI) | Acepta el formato de Jev, **soporta imágenes** (Qwen3-VL-4B) | Sesgo de etiqueta aprendido como media móvil de las peticiones servidas |
| **tydex** (PyPI, MIT) | Envuelve OpenAI/Anthropic/Ollama; escala a humano | Bench: ECE de `choice` **0.350 → 0.023** con T=2.7 |
| **TinyJev** | Qwen3-0.6B + cabeza puntero, MLX/PyTorch | 596M, ~1,2 GB, corre en un M1 |
| **mini-jev**, **LitJev**, **ruling**, **jev-local**, **OpenDecision**, **poorjev**, **Verdict** (118M bi-encoder), **openJev-verdict-2.0** (151M), **von** (395M) | Varios | Ver §3.5 |

**AnyJev** merece atención especial: documenta el **sesgo de posición** con un ejemplo medible —
un `noul` de spam da **P(Sí) = 0.62** con el contenido y **0.70** con el contenido reemplazado por
`N/A`. Dividiendo por ese prior y renormalizando, el juicio **se invierte** a 0.41.

### Tier D — Excéntricos (útiles como señal de amplitud, no como base)

- **`jevlike-esp32`** — exporta un scorer como **firmware de ESP32**
- **`CUA-S1-FORMS`** — **706.048 parámetros, 2,8 MB**, puntúa FILL/CHECK/CLICK/SKIP
- **`minojev`** — **547k parámetros** para Choice (2–255), Boolean y Score
- **`NanoJev`** — 0,6B paralelo
- **`JoshuaSP/open-jev`** — **DiffusionGemma**, sin entrenamiento; replicó **las 408 preguntas
  guardadas de las rutas de ejecución públicas de Jev**; infiere en 2 pasos con canvas JSON
- **`jevbetter`** — encoder de n-gramas con hashing, rivaliza con redes neuronales
- **`Luce`** — describes la tarea en una frase, un profesor LLM escribe los datos, entrena LoRA + cabeza

### Tier E — Descartar o tratar con pinzas

| Proyecto | Problema |
|---|---|
| **`openjevpro`** (PyPI) | Licencia **PolyForm Noncommercial** — **no es open source**. Sus tablas se auto-reportan (100% en su propio arnés vs 80,56% de Jev): valor de evidencia nulo |
| **`vagmi/jevlite`** (repo GitHub) | **Sin licencia** — limita reuso y redistribución |
| Envíos en bloque | El warning de `awesome-jev` aplica; hay repos con más prosa que código |

---

## 4. El estado real de la calibración — la tabla que Jev no publica

Es el eje del asunto. Números verificados, cada uno con su fuente:

| Modelo | ECE | Contexto | Fuente |
|---|---|---|---|
| **Jev 1.13.0** | **no publicado** | — | TypeSafe no ha publicado ningún ECE |
| Laya (sin refit) | **0.466** | media | model card |
| Laya (con refit) | **0.081** | temperatura por (tipo, cardinalidad) | model card |
| Laya (in-task) | 0.060 | test sets propios | model card |
| Laya (zero-shot) | 0.207 | familias retenidas | model card |
| Bespoke-Nimble-9B | ajustada post-hoc | 22-sep | repo |
| Jeff-1 | 0.0807 | vs Jev 0.0932, mismas 9.730 filas | Gestalt |
| jev-lite | 0.019 | 4-bit NF4; 0.069 servido en bf16 | HF card |
| jebadiah-9b | temperatura de `score` **empeora** en rúbricas humanas | v1 lo corrige | HF card |
| tydex + gemma4:31b | 0.350 → 0.023 | T=2.7 | PyPI |
| AnyJev L1 sobre Qwen3-32B | 0.206 → **0.034** | T con 200 etiquetas | PyPI |
| Jev (reportado por terceros) | 0.144 | 2.000 decisiones | AnyJev bench |

**La lectura que importa:** en **todos** los proyectos que midieron con honestidad, la calibración
**no vino del método de entrenamiento** — vino de un **ajuste de temperatura post-hoc sobre datos
etiquetados propios**. Y en varios casos el ajuste que se aprendió del profesor **no transfirió**
a datos humanos reales.

Y hay un problema de **definición**, no solo de número: Laya define `confidence` como
`1 − entropía normalizada`; Jev usa `(n·p_max − 1)/(n − 1)`; `jev-lite` midió y eligió `p_max`;
`logit-classifier` aprende un prior. **Cuatro definiciones del mismo campo. Un umbral calibrado
en una no significa nada en otra.** Eso es metrología, no comparación.

---

## 5. El hueco: lo que NO está hecho

Contra esta evidencia, lo que sigue abierto y **nadie ha reclamado**:

1. **Por qué RLCD no basta.** Hay ~20 implementaciones de RLCD o de su forma, y **ninguna
   caracterización de por qué la calibración no emerge del objetivo**. La teoría existe en el papel
   (regla estrictamente propia ⇒ reportar honestamente es óptimo) y falla en la práctica. **El
   diagnóstico del desajuste entre el óptimo teórico y el comportamiento aprendido no está hecho.**
2. **La definición de `confidence` no está unificada ni estudiada.** Cuatro definiciones incompatibles,
   cero estudios de transferencia de umbrales entre ellas.
3. **El sesgo de posición y el sesgo de etiqueta** están documentados anecdóticamente (`Jev Does Not
   Play Dice`: cara 1 en 400 de 400 tiradas de un dado justo; AnyJev: 0.62 → 0.41 al debiasear)
   y **no cuantificados de forma sistemática**.
4. **Ground truth humano con acuerdo inter-anotador (kappa) no existe en ningún lado** del ecosistema.
   Todas las mediciones usan etiquetas de un solo anotador o etiquetas sintéticas.
5. **La descomposición del error** —¿cuánta descalibración viene del encoder, cuánta de la cabeza,
   cuánta del objetivo, cuánta de la cardinalidad de opciones?— no está hecha.
6. **La interacción entre el `noul` y su negación** (que ambos den 0.7) nunca se midió como propiedad
   matemática del modelo.

---

## 6. Viabilidad para una tesis

### 6.1 Lo que el ecosistema te regala

| Recurso | Qué es | Licencia |
|---|---|---|
| `LocalLLaMA/typed-decisions` | **2.000 decisiones / 4 flujos de trabajo** — el benchmark compartido | Apache-2.0 (↓9.620, ♥31) |
| `jaredpalmer/kev-suites` | Suites de evaluación congeladas | ↓1.487 |
| `bespokelabsai/nimble` | **2.676 train + 324 retenidos**, públicos | ver repo |
| `jaredpalmer/kev` | Pesos 0.5B→27B con temperatura ya ajustada | Apache-2.0 |
| `convaiinnovations/laya` | 3 checkpoints con notebook de fine-tuning (Kaggle 2×T4) | Apache-2.0 |
| `yibie/awesome-jev` | **367 entradas / 14 categorías** — índice curado con criterios explícitos | — |
| `Jevals.com` | Leaderboard independiente | CC-BY-4.0 |
| WANLI, Banking77, CLINC150, MedHallu | Datos externos con etiquetas humanas | varias |
| ~30 arneses de evaluación | `ASSAY-001`, `jev-ood-calibration`, `jev-acento`, `jev-orderby-bench`… | varias |

### 6.2 Lo que ya está pre-empteado (evitar)

Hay que ser honesto: el espacio de "medir la calibración de Jev" **ya está bastante ocupado**.
Existen auditorías **pre-registradas** (`ASSAY-001` con veredicto dividido en Banking77/CLINC150),
auditorías en **español sobre 3.200 ítems** (`jev-acento`), de **sesgo de posición**
(`Jev Does Not Play Dice`), de **inversiones de ranking** (`jev-orderby-bench`), de **OOD**
(`jev-ood-calibration`, 900 tickets generados por reglas), médico (`jev-medhallu-benchmark`,
1.000 ítems), y de **facturación por batching** (`jev-fanout-bench`, 2.976 llamadas).

**Lo que sigue libre es el "por qué", no el "cuánto".** Todas esas mediciones dicen *que* está
descalibrado. Ninguna explica *de dónde viene*, ni qué propiedad del objetivo lo causa.

### 6.3 El ángulo interno que sí queda libre

> **Caracterización del desajuste entre el objetivo RLCD y la calibración observada, con
> descomposición por componente (encoder / cabeza / objetivo / cardinalidad) y validación cruzada
> entre las definiciones de confianza.**

Es interno (mecanismo, matemática del objetivo, código), falsable, y el ecosistema te da los pesos,
los datos y los arneses. **Nadie lo ha hecho.**

### 6.4 Costo

**Cero dólares, y tu RTX 4050 alcanza.** Los modelos del Tier A/B son de 0.5B a 9B, y el 0.8B de Kev
entrena en **4 GB**. El 27B de Kev pide una H100 80 GB — pero es opcional, no necesario.
El fine-tuning de referencia son 15 minutos en una H100 o ~1,5 h en una 4090 para el 8B.

---

## 7. Veredicto

| Pregunta | Respuesta |
|---|---|
| ¿Hay suficiente material open-source para investigar? | **Sí, de sobra.** 20+ modelos con pesos, 2 datasets abiertos, ~30 arneses |
| ¿Es un tema virgen? | **No el "cuánto"**; **sí el "por qué"** |
| ¿Es aporte interno o comparación superficial? | **Puede ser interno** si atacas el objetivo de entrenamiento, no la tabla comparativa |
| ¿Es viable al costo? | **Sí: $0 y cabe en tu 4050** |
| ¿Cuál es el riesgo? | Que es una fiebre de oro de 6 días: mucho ruido, poco probado. Y que el "cuánto" ya está ocupado |
| ¿Es mejor o peor que la ruta JEPA? | **Es un tema distinto, no un reemplazo.** Ver §8 |

---

## 8. Cómo se relaciona con tu elección actual (JEPA)

Son **dos tesis distintas**, y la decisión es tuya:

| | **Ruta JEPA** (elegida) | **Ruta Jev-OSS** |
|---|---|---|
| Objeto | Modelos de mundo latentes (LeWM 15M) | Modelos de decisión tipo Jev (0.5B–9B) |
| Propiedad | *decision-metric alignment* | Calibración y su origen en el objetivo |
| Hueco | Cuándo el coste latente ordena bien los planes | Por qué RLCD no produce calibración |
| Madurez del campo | Investigación de años, comunidad académica | **6 días, fiebre del oro** |
| Riesgo de te adelanten | Medio (arxiv:2608.18746 es de agosto) | **Alto** (30 grupos midiendo ya) |
| Calidad de la evidencia disponible | Alta (papers con revisión) | **Baja** (auto-reportada, sin revisión) |
| Encaje "interno" | Sí (geometría del latente, objetivo) | Sí, si atacas el objetivo |
| Tipo de tesis | Medición → teoría (Taller) | Medición → teoría (Taller) |

**Mi lectura honesta:** Jev-OSS es más fácil de arrancar (los pesos y los datos están ahí, hoy) y
más fácil de publicar rápido; pero es un campo con 30 grupos midiendo en paralelo y evidencia de
baja calidad, donde el "cuánto" ya está ocupado. JEPA tiene un hueco más limpio, evidencia de mejor
calidad, y **el mismo tipo de contribución interna** que buscas.

**No te sugiero cambiar.** Te sugiero saber que esta puerta está abierta y que la premisa con la que
la cerramos ("no es open source") ya es falsa. Si en algún momento el eje λ de JEPA no da señal, esta
es la salida de emergencia más sólida que tienes.

---

## 9. Fuentes y artefactos verificados

**Verificado con API en esta sesión:** GitHub (`gh api`, 152 repos por 6 consultas + 10 repos
individuales), Hugging Face (modelos, datasets, 4 organizaciones), PyPI (9 paquetes).
Los README completos de 11 repos quedaron en `audit/jev-oss/`.

**Documentos clave del ecosistema:**
- `archerhume.com/posts/jevs-architecture-unmasked` — 10.000 llamadas, 7 principios
- `navinpai.github.io/decoding-jev/` — la mecánica de RLCD derivada de Laya, paso a paso
- `systemonemodels.org/guides/jev-architecture/` — qué se sabe y qué no
- `yibie/awesome-jev` — 367 entradas, 14 categorías, con criterios de inclusión honestos
- `developers.dev.to` (programmerraja) — "The Logit Trick", la implementación del readout explicada

**Advertencia metodológica:** buena parte de los números de este documento son
**auto-reportados por sus autores**. Solo los de Laya (model card), Kev (repo con arnés),
Nimble (datos publicados) y Jeff (comparación contra Jev en vivo sobre las mismas filas) tienen
suficiente trazabilidad para citarse. Todo lo demás es evidencia gris hasta que lo midas tú.
