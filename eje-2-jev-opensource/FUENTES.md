# EJE 2 — Ecosistema open-source tipo Jev: inventario completo de fuentes

> ## ✅ ESTE ES EL EJE ELEGIDO (01-OCT-2026)
> **Tema definitivo de Tesis 1: Jev, Laya y el ecosistema de modelos de decisión.** Las rutas
> propuestas están en `eje-2-jev-opensource/10_tres_rutas_tesis1.md`.
>
> **Advertencia que condiciona el diseño (leer antes de §5):** 5 de los 6 huecos de §5 fueron
> ocupados **entre el 12 y el 30 de septiembre de 2026**, varios con pre-registro y DOI. El **"cuánto"
> y buena parte del "por qué" ya están reclamados**; por eso el resultado de Tesis 1 no puede ser un
> hallazgo, tiene que ser un artefacto. Verificación en vivo contra arXiv — ver `README.md` §7-bis:
>
> | Hueco de §5 | Quién lo ocupó |
> |---|---|
> | 1. Por qué RLCD no produce calibración | arXiv:2609.38850 (OpenJev-RLCD) + reproducción del término RL (lema de Stein) |
> | 2. Definiciones de `confidence` / transferencia de umbrales | Estudio pre-registrado UCLA (rejilla 0.01; 0.77–0.95 entre datasets) |
> | 3. Sesgo de posición y de etiqueta | arXiv:2609.26758 (flip 70.4 pp, AUC 93.8%→23.2%) + arXiv:2609.26550 |
> | 4. Ground truth humano con kappa | **NADIE — único hueco superviviente** (es anotación manual) |
> | 5. Descomposición del error por componente | Parcialmente: reproducción independiente aisló presupuesto de tokens vs pérdida |
> | 6. Coherencia / negación como propiedad matemática | **arXiv:2609.33209** (480 pares; s+n=1 falla 0.064; las tres mono-etiqueta suman 1.14) |
>
> **Consecuencia:** el eje 2 no es una Tesis 1 defendible hoy. Lo único abierto (kappa humano) exige
> anotación manual, que el autor excluyó por regla. El eje elegido es el **eje 1 → ruta 1**.

Alternativa / salida de emergencia · verificación HTTP de las 49 fuentes del eje · corte 25-sep-2026

---

## 0. Nota de lectura

**49 fuentes verificadas, 48 con HTTP 200.** La única que no responde (Medium, 403) es el enlace
original del usuario y su contenido ya fue extraído en su momento: el 403 es muro anti-bot, no
enlace muerto.

Todas las cifras de estrellas, descargas y licencias de este documento vienen de la **API** de
GitHub / Hugging Face / PyPI consultada en esta sesión, no de snippets de búsqueda.

**Advertencia transversal:** casi todos los números de rendimiento son **auto-reportados**. Los
únicos con trazabilidad suficiente para citar son Laya (model card), Kev (repo con arnés),
Nimble (datos publicados) y Jeff (comparación contra Jev en vivo sobre las mismas 9.730 filas).

---

## 1. La referencia cerrada (lo que se quiere imitar)

| Fuente | Qué es | Verificado |
|---|---|---|
| [typesafe.ai/blog/introducing-system-one-models-and-jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) | **El anuncio oficial.** 18-sep-2026. Los tres primitivos, la afirmación de calibración, RLCD nombrado por primera vez | ✅ 200 |
| [docs.typesafe.ai/primitives/choice](https://docs.typesafe.ai/primitives/choice) | Documentación oficial de los primitivos. `state`, `questions`, límites (255 opciones, 2–10 niveles) | ✅ 200 |
| [medium.com/…/what-is-jev-ai](https://medium.com/data-science-in-your-pocket/what-is-jev-ai-b8294d980001) | **El enlace que trajiste.** La lectura divulgativa que inició todo | ⚠️ 403 (muro anti-bot; contenido ya extraído) |
| [jevtypesafeai.com/what-is-jev](https://www.jevtypesafeai.com/what-is-jev) | Explicación de terceros, más ordenada que la oficial | ✅ 200 |
| [langchain.com/blog/building-a-harness-with-jev](https://www.langchain.com/blog/building-a-harness-with-jev) | Integración oficial `TypeSafeClassifier`, `AutoModeMiddleware`. Cómo se usa en un agente real | ✅ 200 |

**Precio y límites declarados:** $0.042 por millón de tokens de entrada, **coste de salida cero**
(nunca se generan tokens), latencia 70–500 ms, ventana ~64K compartida entre estado y preguntas.

---

## 2. Los análisis independientes de la arquitectura

Son las fuentes que **reconstruyeron el mecanismo** desde fuera. Sin ellas el ecosistema no existiría.

| Fuente | Qué aporta | Verificado |
|---|---|---|
| [archerhume.com/posts/jevs-architecture-unmasked](https://archerhume.com/posts/jevs-architecture-unmasked) | **El análisis más importante.** 10.000 llamadas a la API sondeando escalado de latencia y reordenamiento de preguntas. **Siete principios de diseño** (readout, estado compartido, backbone causal, opciones que interactúan, entrenar la distribución y calcular la confianza después, capacidad dispersa/MoE, batchear ramas). **Kev se construye sobre este documento** | ✅ 200 |
| [navinpai.github.io/decoding-jev/](https://navinpai.github.io/decoding-jev/) | **La mejor derivación matemática de RLCD.** Explica los marcadores `[MASK]` de Laya, por qué la calibración *no* requiere RL, la mecánica de REINFORCE con baseline, y la distinción entre σ (exploración) y T (temperatura) | ✅ 200 |
| [systemonemodels.org/guides/jev-architecture/](https://systemonemodels.org/guides/jev-architecture/) | Qué se sabe y qué no, con honestidad explícita. Las tres hipótesis arquitectónicas en competencia | ✅ 200 |
| [dev.to/programmerraja — *The Logit Trick*](https://dev.to/programmerraja/how-jev-works-the-logit-trick-behind-typesafes-system-one-model-4lpd) | **La implementación del readout, paso a paso.** Prompts que se cortan a mitad de la respuesta, softmax restringido, el `noul` de 9 bins del 1 al 9, caché KV compartida entre preguntas | ✅ 200 |
| [dev.to/stalwartcoder — *Jev is Not a Small LLM*](https://dev.to/stalwartcoder/jev-is-not-a-small-llm-a-technical-guide-to-system-one-models-25m2) | **La única medición externa publicada de la calibración de Jev.** Diagrama de fiabilidad, ECE por cubo, y el hallazgo de que Jev trata SHOULD como un "sí débil" (median 0.33) — la brecha de calibración es en realidad un **desacuerdo sobre la pregunta** | ✅ 200 |
| [kb.ekarisky.com/ai-agents/jev/architecture/](https://kb.ekarisky.com/ai-agents/jev/architecture/) | Tablas comparativas RLHF / RLVR / RLCD, y los tres niveles de calibración (`raw` / `L0` / `L1`) | ✅ 200 |
| [flaviocopes.com/jev/](https://flaviocopes.com/jev/) | El patrón de **enrutamiento de intención** con el código en TypeScript. La mejor ilustración del caso de uso real | ✅ 200 |
| [note.com/wayne_chang — informe de RLCD](https://note.com/wayne_chang/n/n151303c2041a) | **Reconstrucción detallada de RLCD**: regla de puntuación logarítmica con suelo −9.21, spherical score, RPS para ordinal, ruido gaussiano, annealing σ 1.0→0.3, GRPO-style con 8 candidatos | ✅ 200 |
| [jevals.com](https://jevals.com) | **Leaderboard independiente.** Hace a Jev y a seis LLMs las mismas preguntas Noul/Choice/Score y califica | ✅ 200 |

---

## 3. Tier A — Reproducciones serias (pesos propios + receta)

### Laya — la implementación de RLCD de referencia

| Fuente | Dato verificado |
|---|---|
| [github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | ★**23.327** · 2.016 forks · **Apache-2.0** · creado 18-sep-2026, push 24-sep |
| [huggingface.co/convaiinnovations/laya](https://huggingface.co/convaiinnovations/laya) | ♥**3.447** · Apache-2.0 · 421M (ModernBERT-large 395M + cabeza propia) |
| [laya-multilingual](https://huggingface.co/convaiinnovations/laya-multilingual) | ♥253 · mmBERT-base · 322M · 1024 tokens (hasta 8.192) · 100+ idiomas |
| [laya-typed-decisions](https://huggingface.co/convaiinnovations/laya-typed-decisions) | ♥— · 421M · fine-tuned sobre el split de entrenamiento del benchmark |
| [laya.convaiinnovations.com](https://laya.convaiinnovations.com/) | La comparativa contra Jev: **32.8 ms vs 236–276 ms**; 7.2 ms/pregunta batcheado. Afirma superar el techo del profesor (0.766 vs 0.735) |
| [PyPI: laya](https://pypi.org/project/laya/) | v0.3.20 · 28 releases · 18→24 sep |
| [arXiv:2503.23303](https://arxiv.org/abs/2503.23303) | **El predecesor**: *SalesRLAgent: A Reinforcement Learning Approach for Real-Time Sales Conversion Prediction and Optimization* · Nandakishor M · 30-mar-2025. PPO sobre representaciones de secuencia, conversión 0.0–1.0 |

**Números medidos en su model card:** in-task macro accuracy **0.838** / macro ECE **0.060**;
zero-shot **0.651** / **0.207**; intent routing **0.991** / ECE **0.009**; moderación 0.967/0.061;
emoción 0.906/0.018; triaje 0.732/0.017.

**Y el dato clave:** *"Ships over-confident: refitting one temperature per (question type, option
count) moves mean ECE **0.466 → 0.081**. Do this on your own data before trusting the probabilities."*

**Límites que declara:** zero-shot typed-decisions **0.362** (random 0.318, mayoría 0.461);
ordinal `score` el más débil (SST-5 0.372); solo inglés el checkpoint base; **khmer 0.000 de
precisión con 0.952 de confianza**; `confidence` = **1 − entropía normalizada**, *no* la fórmula de Jev.

### Kev — la familia entrenable, con la metodología más honesta

| Fuente | Dato verificado |
|---|---|
| [github.com/jaredpalmer/kev](https://github.com/jaredpalmer/kev) | ★**6.790** · **Apache-2.0** · 17→25 sep · *"Jev-like family of decision models built on top of Qwen3.5/3.8 you can train and run on a Mac"* |
| [jaredpalmer/kev-4b](https://huggingface.co/jaredpalmer/kev-4b) | ↓**6.087** · ♥45 |
| [jaredpalmer/kev-0.8b](https://huggingface.co/jaredpalmer/kev-0.8b) | ↓4.308 · ♥19 · **entrena en 4 GB de VRAM** |
| [jaredpalmer/kev-9b](https://huggingface.co/jaredpalmer/kev-9b) | ↓1.455 · ♥41 |
| [jaredpalmer/kev-27b](https://huggingface.co/jaredpalmer/kev-27b) | ↓0 · ♥4 · pide B200/H200/H100 80 GB |
| [jaredpalmer/kev-suites](https://huggingface.co/datasets/jaredpalmer/kev-suites) | ↓1.487 · suites de evaluación congeladas |

**Números:** kev-27B **0.848 vs 0.857 de Jev** en fuentes nuevas; Kev-4B y 9B a menos de cuatro
puntos. **Honestidad explícita:** *"No sabemos con qué se entrenó Jev, así que esto no es una
comparación controlada."* Incluye un control de **contexto mezclado** y reporta accuracy + Brier +
calibración **por tipo de pregunta**.

**La receta de fine-tuning más útil del ecosistema:** ejemplo de soporte, 3 preguntas, 1.050
registros generados, **15 minutos en una H100** → Kev-4B de **67,7% a 73,6%**. Trae una skill de
agente (`kev-finetune`) y una app de Modal.

### Nimble — el aporte científico más limpio

| Fuente | Dato verificado |
|---|---|
| [github.com/bespokelabsai/nimble](https://github.com/bespokelabsai/nimble) | ★**1.741** · creado 18-sep-2026 · *"Data, Model, Recipe for an open Jev"* |
| [bespokelabs/Bespoke-Nimble-9B](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B) | LoRA sobre Qwen3.5-9B |

**Números:** en **324 ejemplos retenidos**, Nimble coincide con **90,1%** de las etiquetas de
referencia, contra **66,4%** de su modelo base y **93,2% de Jev 1.13.0**.
**Publicó 2.676 ejemplos de entrenamiento + 324 retenidos.** Arnés que corre **Nimble y Jev sobre
los mismos registros** de 13 subconjuntos públicos con etiquetas humanas.

**Declaración explícita:** *"no destilamos de Jev"* — el objetivo es mostrar cómo curar datos y
entrenar. **Construido en un día.**

**Metodología:** el serving lee el prompt una vez y luego puntúa **un token de respuesta por
pregunta**; la curación de datos **cambia un hecho para que la respuesta correcta se invierta**;
el entrenamiento ajusta Qwen3.5-9B con LoRA **solo en los tokens de respuesta**.

### SemIf (ex-OpenJev) — la más rigurosa metodológicamente

| Fuente | Dato verificado |
|---|---|
| [github.com/TheoLeeCJ/SemIf-OpenJev](https://github.com/TheoLeeCJ/SemIf-OpenJev) | ★**4.251** · 286 forks · **MIT** · push 23-sep-2026 |
| [PyPI: fastjev](https://pypi.org/project/fastjev/) | v0.2.0 · MIT · fork independiente de SemIf, preserva historial y licencia |

**Lo que la distingue:** **temperatura por carga de trabajo con ECE fuera de muestra**, y un
**fixture propio de 37×21** con runners, salidas por fila y **fallos conocidos** commiteados.
Incluye un puente **Qwen3.8-27B EXL3 cuantizado a 5 bpw**.

**Honestidad:** *"reproduce el **patrón de interfaz**; no reproduce el modelo ni el entrenamiento
no divulgados de Jev."* Y sobre la calibración: *"La mejora clara es en WANLI; los intervalos se
solapan en las cargas authored y Every."*

---

## 4. Tier B — Adaptadores entrenados con medición honesta

| Fuente | Qué es | Dato clave | Verificado |
|---|---|---|---|
| [github.com/Gestalt-Lab/jeff](https://github.com/Gestalt-Lab/jeff) · [HF GestaltLabs/Jeff-1](https://huggingface.co/GestaltLabs/Jeff-1) | LoRA sobre Qwen3-4B-Instruct-2507 · Apache-2.0 | **La comparación más rigurosa contra Jev en vivo**: 9.730 filas humanas. Jeff **0.8183** vs Jev **0.8283**; ECE **0.0807** vs **0.0932** (Jev peor); Brier 0.2839 vs 0.2750. Documenta sus propios modos de fallo | ✅ 200 |
| [github.com/vagmi/jevlite](https://github.com/vagmi/jevlite) · [HF vagmi/jev-lite](https://huggingface.co/vagmi/jev-lite) | QLoRA NF4 sobre Gemma 4 E4B | **ECE 0.019**; entrenado **1 h 40 min en una RTX 4090**. Paradoja medida: servido en bf16 el ECE **se duplica** (0.036→0.069) y una temperatura de 1.4 lo restaura. Hallazgo: **`p_max` gana a la entropía normalizada** como estadístico de confianza | ✅ 200 (repo **sin licencia**) |
| [HF frontier-infra/jebadiah-9b-v1](https://huggingface.co/frontier-infra/jebadiah-9b-v1) · [jebadiah-9b-v0](https://huggingface.co/frontier-infra/jebadiah-9b-v0) | LoRA sobre Qwen3.5-9B, entrenado en AINode | 11.072 preguntas públicas, **1 época, 45 min en una H100**. **Hallazgo clave: la temperatura de `score` aprendida de targets del profesor empeora la calibración en rúbricas humanas** — y la v1 lo corrige | ✅ 200 |

El caso `jebadiah` es el más interesante conceptualmente: **el objetivo de entrenamiento optimiza
una cosa y la calibración en el mundo real es otra**, y el hecho de que haya que corregirlo es
el experimento.

---

## 5. Tier C — Lectura de logits sin entrenamiento

| Fuente | Qué es | Nota de honestidad | Verificado |
|---|---|---|---|
| [github.com/daseinlabs/open-jev](https://github.com/daseinlabs/open-jev) | ★110 · **MIT** · una pasada sobre Gemma 3 4B local, MLX/PyTorch | *"las probabilidades zero-shot son verosimilitudes softmax del siguiente token, **no juicios calibrados**"*. Trae **entrenamiento de cabeza por tarea sobre features congeladas**: cabeza de cross-attention, cross-entropy listwise, reporta top-1/top-3, ECE de 10 bins y un **control de contexto mezclado** | ✅ 200 |
| [PyPI: anyjev](https://pypi.org/project/anyjev/) | Convierte **cualquier** LLM en modelo tipo Jev, sin entrenar | **La mejor documentación del debiasing.** Tres niveles: `raw` / `L0` (marginalización por desplazamiento cíclico + prior sin etiquetas) / `L1` (temperatura con 100–500 etiquetas). Ejemplo medido: `noul` de spam da **0.62** con contenido y **0.70** con `N/A` → tras debiasear, **0.41**, el juicio se invierte | ✅ 200 |
| [PyPI: logit-classifier](https://pypi.org/project/logit-classifier/) | Acepta el formato de Jev; **soporta imágenes** (Qwen3-VL-4B) | Sesgo de etiqueta aprendido como media móvil sobre peticiones servidas, sin datos etiquetados. ~140 ms en una RTX 3090 Ti **independientemente del número de preguntas** hasta ~8 | ✅ 200 |
| [PyPI: tydex](https://pypi.org/project/tydex/) | Envuelve OpenAI/Anthropic/Ollama; escala a humano | MIT, sin dependencias de terceros. **Temperatura + recalibración isotónica (PAV)** y bucle de reajuste automático. Bench: ECE de `choice` **0.350 → 0.023** con T=2.7 | ✅ 200 |
| [PyPI: tinyjev](https://pypi.org/project/tinyjev/) | Qwen3-0.6B-Base + cabeza puntero, MLX/PyTorch | 596M, ~1,2 GB, corre en un M1. Hereda datos y diseño de **Kev**. Cuantizar 8 bits es gratis; 4 bits cuesta ~2 puntos | ✅ 200 |
| [github.com/JoshuaSP/open-jev](https://github.com/JoshuaSP/open-jev) | ★39 · MIT · **DiffusionGemma**, sin entrenamiento | **Replicó las 408 preguntas guardadas de las rutas de ejecución públicas de Jev.** Inferencia en 2 pasos con canvas JSON. Documenta **un bug de conteo de tokens en su propia corrida original** | ✅ 200 |
| [HF chaoliangUNSW/Jev-Style-Qwen3.5-2B](https://huggingface.co/chaoliangUNSW/Jev-Style-Qwen3.5-2B-Decision-MLX-bf16) | Qwen3.5-2B, MLX | ↓**2.801** · ECE **0.017**. Temperatura **plegada dentro del peso del RMSNorm final** — calibración a coste cero en inferencia | ✅ 200 |

---

## 6. Investigación y calibración (los arneses del índice `awesome-jev`)

Fuente del índice: [github.com/yibie/awesome-jev](https://github.com/yibie/awesome-jev) — ★**1.631**,
**367 entradas en 14 categorías**, con criterios de inclusión explícitos y una advertencia honesta
sobre envíos en bloque. Sus dos categorías relevantes se volcaron en `audit/jev-oss/` (copias eliminadas del repo el 13-oct-2026).

**Calibración y metrología:**

| Arnés | Qué mide |
|---|---|
| **ASSAY-001** | **Verificación independiente pre-registrada** de calibración y seguridad de tipos de Jev sobre Banking77 / CLINC150. **Veredicto dividido**, logs completos |
| **jev-ood-calibration** | Test independiente de calibración sobre 900 tickets de soporte generados por reglas que Jev no pudo haber visto |
| **jev-acento** | **Auditoría pareada pre-registrada de Jev en español sobre 3.200 ítems etiquetados por humanos** |
| **When a Judgment Layer's Self-Reported Fields Lie** | Contrasta los campos auto-reportados de la capa de acceso contra ground truth en vez de creerlos |
| **jev-verify** | Recomputa las identidades de confianza y de score esperado de Jev contra salidas publicadas en repos públicos |
| **jev-medhallu-benchmark** | Test **pre-registrado** de Jev como detector de alucinaciones sobre MedHallu de Stanford (1.000 ítems) |
| **Jev Does Not Play Dice** | Pide a Jev una `Choice` sobre las seis caras de un dado justo y oculto, 400 veces. **Jev elige la cara 1 en las 400** |
| **jev-orderby-bench** | Si un `ORDER BY` sobre una probabilidad de Jev es defendible: **inversión por pares**, ordinalidad del `Score` |
| **jevcal** | Ajusta un umbral de confianza por pregunta a una precisión objetivo sobre datos etiquetados propios y lo verifica |
| **AnyJev bench** | Reporta accuracy, Brier, ECE, **tasa de volteo por orden** y cobertura al 5% de riesgo |
| **DecisionBench** | Puntúa respuestas Noul/Choice/Score en tareas con documentos fijados, **contando probabilidades malformadas** |

**Evaluación comparativa:**

| Fuente | Qué es |
|---|---|
| [Jevals.com](https://jevals.com) | Leaderboard independiente, suite CC-BY-4.0, release 18-sep-2026 |
| `jev-eval` | Compara Jev contra GPT-4o-mini y Claude Sonnet 4.5 en condiciones idénticas |
| `Can Jev Be a Better Agent Evaluator?` | LangChain compara Jev contra jueces LLM en precisión, repetibilidad, latencia y costo |
| `Jev reranking is not a free win` | 33.047 entradas de catálogo, 164 consultas reales, 9.831 pares calificados |
| `jev-fanout-bench` | **Batching vs una pregunta por llamada** sobre 2.976 llamadas a `jev-1.13-20260917` vía OpenRouter |
| `An early-access test of TypeSafe's Jev` | Juicios calibrados en acceso temprano y **coste por decisión** resultante |
| `Jeff` (Gestalt) | La comparación en vivo más grande: 9.730 filas humanas |

**Metrología del propio ecosistema:**

| Fuente | Qué es |
|---|---|
| `Jev Pong`, `Jev Playground`, `Jev vs Mistral y Gemini`, `Jev vs GPT-4.1 en encuesta sintética`, `Convex Decision Evals`, `Curso Decision Evals`, `Jev IDS`, `WindTunnel`, `judgekit`, `SystemOneHarness`, `pytest-jev`, `jev-regress-bench`, `jev-test`, `Jev Web Analyzer`, `Jev judge call vs dimension scores` | 20+ arneses más, cubriendo dominios de juegos, agentes, seguridad de red, encuestas y testing |

---

## 7. Datos y benchmarks

| Fuente | Qué es | Verificado |
|---|---|---|
| [HF LocalLLaMA/typed-decisions](https://huggingface.co/datasets/LocalLLaMA/typed-decisions) | **El benchmark compartido**: 2.000 decisiones / 4 flujos de trabajo. ↓**9.620** · ♥31 · **Apache-2.0** | ✅ 200 |
| [HF jaredpalmer/kev-suites](https://huggingface.co/datasets/jaredpalmer/kev-suites) | Suites de evaluación congeladas de Kev | ✅ 200 |
| Nimble: 2.676 train + 324 retenidos | Publicados en el repo de Nimble | — |
| [HF alisawuffles/WANLI](https://huggingface.co/datasets/alisawuffles/WANLI) | Inferencia de lenguaje natural como verificación externa (la usa SemIf). ↓9.456 · CC-BY-4.0 | ✅ 200 |
| Banking77 / CLINC150 | Usados por ASSAY-001 para intención | — |
| MedHallu (Stanford MedHELM) | 1.000 ítems, detector de alucinaciones | — |

---

## 8. Runtime y despliegue

| Fuente | Qué es | Escala |
|---|---|---|
| [github.com/mizorewww/laya-mlx](https://github.com/mizorewww/laya-mlx) | Runtime MLX nativo para Laya. **7–14 ms** en M3 Max | ★**6.239** · Apache-2.0 |
| [github.com/mizorewww/laya-coreml](https://github.com/mizorewww/laya-coreml) | Core ML / Neural Engine. **~5 ms** | ★1.441 · Apache-2.0 |
| [github.com/OpenByteInc/QuantDinger](https://github.com/OpenByteInc/QuantDinger) | OS de trading con **integración de Jev System One** | ★**12.126** · Apache-2.0 |

---

## 9. Excéntricos (señal de amplitud del campo)

`jevlike-esp32` (firmware ESP32) · `CUA-S1-FORMS` (**706.048 parámetros, 2,8 MB**) ·
`minojev` (**547k parámetros**) · `NanoJev` (0,6B) · `jevbetter` (encoder de n-gramas con hashing) ·
`Luce` (un profesor LLM escribe los datos) · `von` (395M) · `Verdict` (118M bi-encoder) ·
`openJev-verdict-2.0` (151M) · `jev-paint` (pinta imágenes prediciendo el color de cada píxel) ·
`Parallel Constrained Decoding` (Qwen2.5-1B entrenado con RLCD).

---

## 10. Descartar o tratar con pinzas

| Fuente | Problema |
|---|---|
| [PyPI: openjevpro](https://pypi.org/project/openjevpro/) | Licencia **PolyForm Noncommercial** — **no es open source**. Se auto-reporta con 100% en su propio arnés frente a 80,56% de Jev. Valor de evidencia nulo |
| [github.com/vagmi/jevlite](https://github.com/vagmi/jevlite) | **Sin licencia** — limita reuso y redistribución |
| Envíos en bloque | El warning del propio índice aplica: repos con más prosa que código y un solo commit |

---

## 11. El hueco de este eje (para referencia)

Este eje **ES el elegido** (Ruta 1, metrología del campo `confidence`). El material de JEPA/`eje-1-jepa` se
descartó y se eliminó del repo el 13-oct-2026. Lo que sigue queda como registro de los huecos que se evaluaron:

- **El "cuánto" está ocupado:** hay auditorías **pre-registradas** de calibración, en **español**,
  de sesgo de posición, de inversiones de ranking, OOD y médico. No repitas eso.
- **El "por qué" sigue libre:** nadie ha caracterizado **de dónde viene** la descalibración.
  RLCD tiene un óptimo teórico (reportar honestamente) que **no emerge en la práctica** — verificado
  en Laya (0.466 → 0.081 solo con refit), Nimble (ajuste post-hoc), jebadiah (el ajuste del profesor
  no transfiere a rúbricas humanas) y Jev (ningún ECE publicado).
- **La metrología sigue rota:** hay **cuatro definiciones incompatibles del campo `confidence`** y
  cero estudios de transferencia de umbrales entre ellas.
- **No existe ground truth humano con kappa inter-anotador** en ningún lugar del ecosistema.

El análisis completo está en `08_estudio_ecosistema.md`.
