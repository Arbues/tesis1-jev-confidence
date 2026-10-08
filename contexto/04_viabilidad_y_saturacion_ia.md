# Tesis 1 — Ruta IA: mapa de viabilidad 2026, qué está deprecado y 5 temas candidatos

Documento de trabajo · 18-sep-2026 · basado en los "exploradores de estado del arte" de 2026

---

## 0. Aclaración sobre "sin GPU"

Cuando dije "sin GPU" en el portafolio anterior quise decir **"no la necesitas"**, no que no
tengas. Concretamente: en T1–T5 de ese documento la GPU **no es cuello de botella** — todo es
CPU + API, así que tu 4050 queda libre y deja de ser una restricción. En **este** documento hay
temas que sí la usan (ZO/local), y lo marco explícitamente en cada uno.

---

## 1. Los "exploradores" que pediste: quién mapeó la IA recientemente

Existen, y son varios. Estos son los que sirven para decidir, ordenados por utilidad para ti:

| Fuente | Qué es | Por qué te sirve |
|---|---|---|
| **arXiv:2608.06663 — "The Horizon Gap"** | Survey sistemático de **1,547 papers arXiv (2024–2026)** sobre agentes de largo horizonte; con tasa de ruido declarada (26.8% de hits descartados) | **Nombra explícitamente los problemas abiertos de medición** del campo. Es el más accionable: te da la lista de huecos ya priorizada |
| **"The State of AI Research 2026" (ArxivLens)** | Análisis de **422,059 papers** con descomposición de limitaciones auto-declaradas (883,724 enunciados) y temas de trabajo futuro | Te dice **qué se auto-reporta como débil**: "alcance estrecho/dominio específico" es la limitación #1 |
| **arXiv:2602.16763 — "When AI Benchmarks Plateau"** | Estudio de saturación sobre **60 benchmarks de LLM** con 14 propiedades e índice de saturación con incertidumbre | Te dice **qué benchmarks ya no sirven** (29/60 saturados, 14 con S≥0.9) |
| **Survey de evaluación de agentes (ACL Findings 2026)** | "El primer survey comprehensivo de evaluación de agentes LLM" | Lista las direcciones futuras explícitas: coste-eficiencia, seguridad, robustez, granularidad fina, **desacoplar LLM de harness** |
| **"The Edge of AI Research" (ICML/ICLR/NeurIPS 2023–2026)** | Survey guiado por el grafo de citas de las tres conferencias principales | Da la frase más útil de todas: **"el preentrenamiento ya no es la frontera"** |
| **State of AI / Stanford HAI AI Index 2026** | El reporte anual de referencia | Diagnóstico macro: benchmarks saturando, evaluación independiente que no confirma lo que los labs reportan, "evaluation gap" |
| **Position papers 2026** (NeurIPS/ICML) | Ej. arXiv:2605.15622 (ZO subexplorado), arXiv:2607.14123 (XAI debe priorizar fundamentos) | Un position paper *es* un mapa de viabilidad firmado: dice qué está subexplorado y propone agenda |
| **Schmidt Sciences — Trustworthy AI Research Agenda 2026** + **Singapore Consensus 2026** (arXiv:2608.14611) | Agendas de financiamiento con prioridades priorizadas | Si algo está ahí, hay dinero y hueco reconocido |

---

## 2. Qué está DEPRECADO (con evidencia, no intuición)

Esto es lo que debes evitar, y por qué:

| Deprecado | Evidencia |
|---|---|
| **Preentrenamiento / escalado como tema de investigación** | "Pretraining is no longer the research frontier. The frontier has moved to test-time compute, generative simulators, embodied grounding, and architectural primitives" (Edge of AI Research, 2023–2026) |
| **Benchmarks estáticos y saturados** | 29 de 60 benchmarks con saturación alta/muy alta (S≥0.7), 14 con S≥0.9. Y los estáticos "se vuelven obsoletos, saturados y abandonados"; la norma hoy son benchmarks **vivos**. ARC-AGI-1 ya está en 93% |
| **"Aplicar X a dominio Y" sin contribución metodológica** | "Alcance estrecho / específico de dominio" es la **limitación auto-reportada #1** en 422,059 papers. Un tema así es estructuralmente la contribución más débil posible |
| **3D Gaussian Splatting como objetivo de investigación** | "Saturated as a research target" (métrica PSNR de novel-view synthesis) |
| **Métodos ad-hoc de XAI** | Position paper 2026: pivotar de métodos ad-hoc a fundamentos; 44.1% de practicantes no sabe cómo verificar calidad de una explicación |
| **Fases ya cerradas de la IA** | La "fase de alineamiento" (RLHF) y la "fase de arquitectura" ya pasaron; estamos en la **fase de razonamiento** (RL sobre recompensas verificables). Publicar RLHF+DPO hoy es llegar tarde |
| **MMLU / GLUE / needle-in-a-haystack como instrumento** | Saturados o demasiado fáciles; RULER es el reemplazo creíble |

**Regla operativa que se desprende:** un tema viable en 2026 no es "entrenar un modelo" ni
"aplicar un modelo a mi dominio". Es **medir, desacoplar, verificar o evaluar mejor**.

---

## 3. Qué está SUBEXPLORADO (y por qué esto es una oportunidad real)

Los exploradores coinciden en algo contraintuitivo: **las áreas más importantes son las menos
atendidas**, porque el incentivo académico empuja hacia lo medible y rápido.

> "Los problemas más **subinvertidos en relación a su impacto** son **metodología de
> evaluación, capacidad multilingüe e interpretabilidad mecanicista**. Metodología de
> evaluación es el cuello de botella para medir progreso en todo lo demás."

> "Multilingüe y bajo recurso muestra el **crecimiento más lento** relativo a la expansión total
> del campo, indicando un **ensanchamiento absoluto de la brecha** de cobertura."

Y el survey de 1,547 papers nombra los dos problemas de medición abiertos más consecuentes:

1. **¿Cuánta capacidad de largo horizonte vive en el modelo y cuánta en el harness que lo envuelve?**
2. **Sesgo de medición correlacionado**: las señales de proceso usadas para *entrenar* agentes y las usadas para *evaluarlos* descansan en supuestos compartidos sobre qué cuenta como progreso.

El survey de evaluación de agentes (ACL 2026) lo confirma desde otro ángulo y añade
**"Decoupling LLM & Harness Evaluation"** como dirección futura, señalando que Harbor y Exgentic
apenas empiezan a abordarlo.

**Áreas subexploradas con evidencia, ordenadas:**

| Área | Evidencia de que está abierta | ¿Usa tu GPU? |
|---|---|---|
| **Optimización de orden cero (ZO)** | Position paper 2026: "subexplorada, no subpotenciada"; 5 calls to action; los límites percibidos vienen de "prácticas miópicas" | **Sí** (y ZO es memory-efficient por diseño → ideal para 6 GB) |
| **Desacoplar modelo de harness** | Nombrado problema abierto #1 por survey de 1,547 papers + dirección futura en ACL 2026 | No (API) |
| **Seguridad/verificación de agent skills** | 26.1% de skills de la comunidad con vulnerabilidades; "verificación de skills es un problema abierto que intersecta seguridad de IA y métodos formales"; 7 desafíos abiertos listados | No |
| **Metodología de evaluación** | Área #1 subinvertida; "sin mejor evaluación es imposible saber si las soluciones funcionan" | No |
| **Multilingüe / bajo recurso** | Crecimiento más lento del campo → brecha que se ensancha; y los benchmarks multilingües parecen robustos **solo porque son más nuevos** | Parcial |
| **Evaluación XAI anclada a tarea** | Solo 35.3% de practicantes usa métricas cuantitativas; 44.1% no sabe cómo verificar calidad; falta el pipeline de retroalimentación guiada por explicaciones | No |
| **Interpretabilidad mecanicista** | Área subinvertida #3 — pero "la escala es una barrera significativa" → **cuidado con 6 GB** | Sí, y no alcanza |
| **SSMs vs. transformers en recuperación precisa** | Pregunta arquitectónica abierta (RULER como banco de pruebas) | Sí, y probablemente no alcanza |

---

## 4. Cinco temas candidatos — Tesis 1 = comparación/exploración (tu hipótesis)

Tu intuición ("el primero quizás pueda comenzar con una comparación o exploración del modelo o
arquitecturas específicas") es **exactamente la forma correcta** para Tesis 1 en este campo: un
estudio de medición/comparación pre-registrado es un artefacto de primera clase y no requiere
inventar arquitectura. Los cinco de abajo están diseñados así.

### T-A. ZO: ¿subexplorada o subpotenciada? Auditoría comparativa de optimización sin gradiente

**Área CC:** algoritmos, optimización, aprendizaje automático (núcleo de CC).

**El hueco.** El position paper de 2026 sostiene que ZO está subexplorada por prácticas de
desarrollo miópicas (diseños elementales, centrados en el estimador, de espacio completo) y
propone 5 acciones: híbridos ZO-FO, estimadores de gradiente generativos, infraestructura
ZO-native, ZO en subespacio/espectral (reduce varianza de O(d) a O(r)), y —clave para ti—
**des-obfuscar la evaluación de ZO respecto de la complejidad de la tarea**. También propone el
baseline de **derivada direccional (DD)** como diagnóstico: si un método ZO falla, ¿es por mal
estimador o porque la tarea es intrínsecamente difícil?

**Tesis 1 (comparación/exploración):** comparación empírica de métodos ZO existentes (SPSA,
MeZO, LOZO, variantes de subespacio) sobre un banco de tareas **des-obfuscado**, midiendo
varianza del estimador, coste de consultas y **alineación tarea-preentrenamiento** como variable
de confusión — que es precisamente el defecto metodológico que el paper denuncia. Cierra con la
curva "¿cuándo ZO empata con FO?".
**Tesis 2:** reducción de varianza por subespacio/espectral en un régimen de recursos fijos.
**Taller:** infraestructura ZO-native (forward-only, comunicación-eficiente) para fine-tuning
con memoria acotada.

**Kit:** 4050 6 GB — **ZO es la excepción donde tu GPU es una ventaja, no una limitación**,
porque su tesis de venta es justamente eficiencia de memoria y forward-only. + APIs para el
régimen black-box.
**Riesgo:** es el más matemático de los cinco. Dijiste que las bases las tienes; aun así es el
que más exige.
**Venue:** workshop de ICML/NeurIPS → conferencia.

---

### T-B. ¿Modelo o harness? El problema de medición abierto #1

**Área CC:** sistemas de software, metodología de evaluación, ingeniería de software (núcleo CC).

**El hueco.** Dos surveys independientes de 2026 nombran lo mismo: el campo **no sabe cuánta
capacidad "de agente" vive en el modelo y cuánta en el harness que lo envuelve**. El survey de
1,547 papers lo pone entre sus dos problemas de medición más consecuentes; el survey ACL 2026 lo
lista como dirección futura y señala que Harbor y Exgentic "apenas empiezan". Y añade que los
benchmarks actuales **conflacionan** dos objetivos distintos: capacidad del LLM base y diseño del
scaffold — lo que impide atribuir sistemáticamente las ganancias.

**Tesis 1 (comparación/exploración):** protocolo de evaluación **controlado** que varía
independientemente (a) modelo y (b) harness, sobre una tarea agéntica acotada. Con tu acceso a
modelos chinos baratos esto es natural: **modelos chinos baratos × N harnesses**, midiendo la
fracción de varianza explicada por cada factor y por su interacción. Coste monetario bajo, cero
GPU.
**Tesis 2:** descomposición sistemática por componente (memoria, planificación, herramienta) con
métricas de coste-eficiencia — otro hueco que ACL 2026 señala explícitamente.
**Taller:** un harness con garantías de coste y trazas auditables.

**Kit:** solo API + CPU. El más barato de los cinco.
**Ventaja:** es literalmente "comparación de modelos", sin barrera matemática, y el hueco está
**firmado por dos surveys**.
**Venue:** workshop de ICLR/NeurIPS sobre agentes → ACL/EMNLP o ICSE.

---

### T-C. Seguridad y verificación de agent skills — el más nuevo

**Área CC:** seguridad informática, verificación, ingeniería de software (núcleo CC).

**El hueco.** El survey de 2026 que formaliza el paradigma de agent skills reporta que
**26.1% de las skills contribuidas por la comunidad contienen vulnerabilidades**, y lista siete
desafíos abiertos, de los cuales dos son tuyos: **verificación y testing de skills** ("confirmar
que una skill hace lo que dice y nada más es un problema técnico abierto que intersecta seguridad
de IA y métodos formales"; faltan frameworks de test estandarizados) y **modelos de permisos
basados en capacidades** (hoy: una skill cargada puede dirigir al agente a usar cualquier
herramienta). Propone tests negativos para procedimientos alucinados, fallos en cascada,
deadlocks entre skills en conflicto, **escalada silenciosa de permisos** y encadenamiento
adversarial.

**Tesis 1 (auditoría/comparación):** benchmark reproducible de un corpus real de skills con
taxonomía de fallos y vulnerabilidades, replicando y **verificando por tercera parte** el 26.1%
(que es una cifra auto-reportada y aún sin replicación independiente).
**Tesis 2:** modelo de permisos por capacidades con atenuación en subdelegación.
**Taller:** verificación automatizada de skills (contratos + tests negativos) integrada en CI.

**Kit:** cero GPU, CPU + APIs. Y tú ya usas skills a diario: **conoces el artefacto desde
dentro**, que es una ventaja real y no impostada.
**Ventaja:** es la capa más joven de todas — meses de antigüedad — y por eso la menos saturada.
**Riesgo:** la industria ya tiene escáneres de MCP servers; hay que verificar cuánto queda para
un académico (lo estoy auditando).
**Venue:** workshop de S&P/CCS → ICSE/ISSTA o USENIX Security.

---

### T-D. Metodología de evaluación multilingüe (español / quechua)

**Área CC:** PLN, metodología de evaluación, y —si tocas corpus— lingüística computacional.

**El hueco.** Dos hallazgos convergen: (1) multilingüe es una de las tres áreas **más
subinvertidas** en relación a su impacto, y su crecimiento es el más lento del campo, "un
ensanchamiento absoluto de la brecha"; (2) el estudio de saturación encuentra que los benchmarks
multilingües **parecen más robustos solo porque son más nuevos** — la edad es el predictor
dominante, y al controlar por edad el efecto desaparece. Es decir: **no sabemos si la evaluación
multilingüe funciona o si solo es joven.**

**Tesis 1 (auditoría/comparación):** aplicar el marco de índice de saturación con incertidumbre
a benchmarks **en español**, midiendo saturación, contaminación y **validez predictiva**; y
comparar el comportamiento de modelos chinos baratos vs. frontera en fallos específicos del
español.
**Tesis 2:** un benchmark **vivo** en español (los estáticos mueren) con criterio de
no-saturación por diseño.
**Taller:** evaluación con validez predictiva demostrada sobre tareas reales.

**Kit:** API + local. Barato.
**Ventaja personal:** eres hablante nativo y estás en una región subrepresentada — eso es
contexto legítimo, no una excusa. Y hay una versión con impacto social defendible ante jurado.
**Venue:** workshop de LatinX in NLP / LRec → ACL/EMNLP o LREC-COLING.

---

### T-E. Evaluación de explicabilidad anclada a tarea

**Área CC:** HCI, aprendizaje automático, estadística aplicada.

**El hueco.** Position paper 2026: la investigación en XAI debe pivotar de métodos ad-hoc a
fundamentos; hay **"una categoría fantasma de evaluación: métricas matemáticamente precisas pero
prácticamente sin sentido"**. Datos duros: solo **35.3% de los practicantes usa medidas
cuantitativas**; **44.1% reporta "no saber cómo verificar la calidad de una explicación"**;
**38.2% no pudo integrar explicaciones en sus flujos de trabajo**. Y un hallazgo incómodo: las
explicaciones basadas en SAE resultaron **inadecuadas para guiar el comportamiento del modelo y
peores que baselines simples**.

**Tesis 1 (comparación):** comparar métodos de explicación (atribución de características,
SAE, contrafactuales) no por métricas internas sino contra **una tarea downstream con usuarios
reales**, validando si las métricas automáticas son proxies válidos — el "task-grounded
evaluation" que el paper pide y que casi nadie hace.
**Tesis 2:** un pipeline de retroalimentación guiado por explicaciones (existe la ausencia).
**Taller:** protocolo de certificación de explicaciones por comunidad.

**Kit:** CPU + API. Requiere sujetos humanos (compañeros de curso) → logística, no cómputo.
**Riesgo:** el más dependiente de logística humana de los cinco.
**Venue:** workshop de NeurIPS (Human-centric ML) → CHI o FAccT.

---

## 5. Matriz comparativa

| # | Tema | Área CC | ¿Usa GPU? | Coste | Barrera matemática | Saturación (1-10) | Hueco firmado por |
|---|---|---|---|---|---|---|---|
| **T-B** | Modelo vs. harness | Sistemas / evaluación | No (API) | **~$20** | **Baja** | **6/10** — *versión ingenua ya redundante* | 2 surveys 2026 |
| **T-A** | ZO subexplorada | Algoritmos / optimización | **Sí (ventaja)** | ~$10 | **Alta** | **6/10** — *subespacio low-rank = matadero* | Position paper 2026 |
| **T-C** | Seguridad de skills | Seguridad / verificación | No | ~$550–1.500 | Baja-media | **8/10** — *el más saturado de los tres* | Survey 2026 (7 desafíos) |
| **T-D** | Evaluación multilingüe | PLN / metodología | Parcial | ~$40 | Baja | *sin auditar* | 2 fuentes convergentes |
| **T-E** | XAI anclada a tarea | HCI / ML | No | ~$0 | Baja-media | *sin auditar* | Position paper 2026 |

---

## 5.1 Auditoría de saturación — veredictos (3 subagentes, 19-sep-2026)

Los dos primeros veredictos coinciden en un patrón importante: **ambos temas están saturados en
su sub-línea dominante y abiertos en los bordes.** Eso no los descalifica — obliga a apuntar bien.

### T-A — ZO: veredicto **6/10**

**El position paper es retóricamente auto-indulgente y el área está MÁS saturada de lo que
admite.** Evidencia dura:

- **Crecimiento acelerado:** OpenAlex "zeroth-order optimization" 118 (2022) → 159 → 186 → 304
  (2025) → **427 en 8.5 meses de 2026** (≈595 anualizado, **1.96×** sobre 2025). El subconjunto
  acoplado a LLM crece aún más rápido: 1 → 8 → 30 → 65 → **117** (≈163 anualizado, **2.51×**).
- **El propio grupo del position paper ya había ejecutado su agenda:** ZO-Muon
  (arXiv:2602.17155, feb-2026), del mismo grupo, implementa A2 (subespacio + ortogonalización
  espectral) **antes** de que el position paper declare A2 "oportunidad subexplorada".
- **Enjambre de variantes casi intercambiables en 2026:** GRZO, ZO-Act (2607.01125), CurvZO,
  AR1-ZO, RoZO, MaZO, Hi-ZFO, MpSub, AGZO, SubZero+ (2608.15665), Dominant-Layer ZO — todas
  compitiendo por +1–3% en SST-2/RTE bajo el mismo cuello de botella.
- **Señales de madurez:** ya existe encuesta del campo y un baseline monolítico (MeZO).
- **A 4 meses de publicarse, el position paper tiene 1 sola cita.**

**Dónde SÍ está abierto (y esto es lo que importa):**

| Sub-línea | Estado real |
|---|---|
| **A1 — Evaluación des-obfuscada** | **El hueco más limpio y más barato.** ZO-Bench (arXiv:2402.11592, 2024) es el ÚNICO trabajo que incluye el baseline de gradiente directo (JVP). No existe ningún paper 2026 dedicado a protocolos con presupuesto de queries fijo, con/sin task alignment, y baseline DD obligatorio |
| **A3 — Estimadores generativos** | **Prácticamente VACÍA.** Búsqueda dirigida no encuentra NINGÚN trabajo que use difusión/denoisers condicionales como estimador de gradiente ZO. Solo adyacentes: ZO-Finetuner (2025) |
| **A4 — Infra ZO-native** | Abierto. Hay piezas (DistZO2, FedKSeed, sampling por capas), pero **no existe un stack ZO-native sobre un motor de inferencia (vLLM/PagedAttention)** |
| **A2 — Subespacio low-rank** | **CERRADO/saturado.** Aquí ir a competir "es ir a un matadero" |
| **A5 — ZO en alineación black-box vía API** | Casi virgen: ZO para alineación de LLMs accedidos SOLO por API, sin pesos |

### T-B — Modelo vs. harness: veredicto **6/10**

**Corrección importante a mi recomendación anterior: un estudio ingenuo del tipo "modelo vs
harness en SWE-bench" YA ES REDUNDANTE y sería rechazado.** El problema dejó de estar vacío:

- Conteos arXiv (19-sep-2026): `"agent harness"` = **243 resultados**, de los cuales 1 es de 2024
  y 3 de jul–dic 2025 — **el resto, 2026**. `"harness effect"` (frase exacta) = 10, **todos de
  2026**. `"trajectory-level evaluation"` = 10, 8 de ellos de 2026.
- **La pregunta "¿importa más el harness que el modelo?" ya está contestada y replicada** por vías
  independientes: arXiv:2605.23950 mide **HV=18.48 pp² vs MV=2.37 pp² (ratio 7.80×)** con 6
  reversiones de ranking; arXiv:2606.12344 mide **29.4 pp por modelo vs 27.4 pp por harness**;
  arXiv:2607.03691 y arXiv:2608.26218 lo confirman con el modelo congelado.
- **Cuatro sistemas ya ejecutan grillas factoriales reales:** Exgentic (5 arquitecturas × 5 LLMs
  × 6 benchmarks, ~$20K), Harbor Adapters (8 modelos × 54 benchmarks × 4 harnesses),
  Harness-Bench (5,194 trayectorias), Claw-SWE-Bench (OpenClaw × 9 modelos).
- Hallazgo incómodo de arXiv:2609.11987: **ningún contraste pareado resuelve una ventaja promedio
  para ningún harness (−1.25 pp)**, contra la suposición de que el harness nativo del vendor gana.

**Dónde SÍ está abierto:**

| Hueco | Estado |
|---|---|
| **Métricas de trayectoria propuestas pero NO estimadas** | **El hueco más limpio y verificable del área.** arXiv:2605.23950 propone Recovery Rate RR(k), Context Retention y Control Lag, y declara literalmente: *"We do not estimate these metrics on the 3×3 grid. Instead, we specify them as reporting requirements for future harness-aware evaluations"*. **Nadie las ha estimado todavía sobre una grilla modelo×harness** |
| **Modelos baratos / no-frontera como eje factorial** | **Abierto y es tu terreno.** Los estudios existentes usan casi exclusivamente modelos frontera; los modelos chinos baratos aparecen solo como "side cells" (deepseek-v3.2 en 2609.11987) o dentro de papers de evolución de harness (GLM-5, Qwen3.5, MiniMax M2.5). **No existe el estudio "¿el efecto-harness se mantiene, crece o colapsa al bajar de tier de modelo?"** |
| **Dominios no-código** | Sub-cubiertos: la evidencia factorial es abrumadoramente SWE/terminal. τ²-bench, deep research, data science apenas tienen una excepción aislada |
| **Bias de medición correlacionado** | Nombrado como problema abierto por el survey Horizon Gap y **prácticamente sin tratar**. HarnessDev (2609.01437) da evidencia indirecta: las ganancias de evolución "transfieren solo parcialmente a tareas held-out" |
| **Potencia estadística** | Nadie ha publicado **cuántas corridas hacen falta** para que una diferencia modelo-vs-harness sea separable del ruido de Bernoulli |
| **Atribución por componente del harness** | Propuesto como "layer-ablation designs" pero las ablaciones publicadas son ad-hoc sobre un solo harness |
| **Fuera de inglés / fuera de EE.UU.** | **Nada.** Un caso de uso peruano/latinoamericano sería novedad genuina **por ausencia** |

### T-C — seguridad de skills: veredicto **8/10** — el más saturado de los tres

**Corrección importante: subestimé esta área, y también me equivoqué al darte los siete desafíos
del survey como mapa de huecos.** El artefacto SKILL.md salió en octubre de 2025; en ~9 meses de
2026 el área produjo: **~56 papers de seguridad de skills** (2024: 0, 2025: 0), **~30** sobre la
capa MCP/tools (2025: 11), **~62** que tocan verificación/testing (2025: 2), y **29** sobre
modelos de permisos/capacidades (2024: 0, 2025: 0).

**Las tres etapas que yo había propuesto ya están pre-emptadas:**

| Etapa que propuse | Ya hecho por |
|---|---|
| Auditoría empírica a escala | arXiv:2601.10338 (**42.447** skills, 26,1% vulnerables), arXiv:2603.16572 (**238.180**), arXiv:2602.06547 (**98.380**), arXiv:2604.03070 (**170.226** artefactos), arXiv:2604.13064 (26.502) |
| Modelo de permisos por capacidades | SkillGuard (arXiv:2606.03024, **99,93% de cobertura** en 1.260 skills), arXiv:2603.21641, ToolPrivBench (arXiv:2606.20023), Contractual Skills/GovernSpec (arXiv:2605.22634) — y **ya existe un estándar con formato de permisos**: OWASP **AST10** "Universal Skill Format" con `permissions.files/network/shell`, `risk_tier`, `signature`, `content_hash` |
| Verificación automatizada | arXiv:2605.23951 (*Methods for Formal Verification of Agent Skills*: retícula de 4 niveles + **prueba de contención de capacidades** por interpretación abstracta y tipos de refinamiento), VASO (2606.05395), Sefz (2605.13044), SkillFuzz (2607.02345), SkillVetBench (2606.00925), MaliciousSkillBench (2608.19901) |

**Dos de los siete desafíos del survey fueron cerrados por trabajos de mayo–junio 2026 que el
survey de febrero no alcanzó a citar.** Su lista de desafíos **ya está obsoleta** y no debe usarse
como mapa de huecos. Eso corrige lo que yo mismo te dije antes.

**Y el escaneo ya es categoría comercial:** Snyk Agent Scan (ex-Invariant mcp-scan), Cisco
mcp-scanner / skill-scanner (Apache 2.0), Socket, Gen, NVIDIA SkillSpector, Akto, VirusTotal,
ClawScan. Escanear skills o proponer un formato de permisos **no son aportes académicos por sí
mismos**.

**Pero el hueco central sigue abierto, y es demoledor:**

- **El 26,1% nunca fue replicado limpiamente.** Mediciones independientes dan **9%, 13,4%, 0,16%,
  0,52% y 3,79–41,9%** según el escáner.
- **El acuerdo entre escáneres es de nivel azar:** kappa **0,045–0,082**, y solo **0,12%** de las
  skills son marcadas por los 5 escáneres.
- **Ningún escáner supera la línea base "marcar todo"** (F1 0,655 vs 0,551 el mejor real).
- **Trail of Bits evadió TODOS los escáneres probados** (ClawHub, Cisco, Gen, Socket, Snyk) con 3
  de 4 bypass en **menos de una hora**.
- **Vacío de metrología:** no existe ground truth humano público con acuerdo inter-anotador.
  arXiv:2603.16572 reporta que los datasets anotados prometidos por trabajos previos **"no fueron
  localizables"**; MalSkillBench tiene **13% de directorios vacíos** y **fuga de etiqueta** vía
  `_meta.json`.

**Lo que sigue abierto:** metrología y validez de la medición · portabilidad semántica de permisos
entre runtimes (SKILL.md → skill.json → manifest.json) · **fallos benignos de composición**
(deadlocks, no-terminación, contradicciones — la literatura de composición es casi toda de
*ataque*, no de *liveness*) · la **capa de instrucciones en lenguaje natural sigue sin garantías
formales** (2605.23951 solo cubre el lado script) · drift longitudinal.

**Tesis 1 revisada — auditoría de la MEDICIÓN, no otra medición de prevalencia:** congelar un
snapshot de un corpus real (GitSkills: 3,79M SKILL.md de 282.200 repos, en SQLite autocontenido) →
muestrear 300–500 skills estratificadamente → **construir ground truth humano con ≥2 anotadores
independientes y reportar kappa de Cohen (esto no existe hoy y es el aporte central)** → correr
6–8 escáneres existentes sobre la **misma** muestra (Snyk, Cisco, NVIDIA SkillSpector, regex
propio, LLM-as-judge con modelo chino barato, y el baseline trivial "marcar todo") → reportar
precisión/recall/FPR contra el ground truth, matriz de acuerdo inter-escáner y complementariedad →
auditar la validez de constructo de los benchmarks publicados (fuga de metadatos, artefactos
vacíos, sesgo del set benigno) con el esquema abierto de arXiv:2605.21404.

**Coste:** 50–200 USD (etiquetado LLM de apoyo) + tiempo humano de anotación. **Sin GPU.**
**Única restricción práctica:** almacenamiento — GitSkills completo ocupa 50–200 GB, así que hay
que trabajar con un subconjunto estratificado.

**Por qué es defendible pese al 8/10:** es el único hueco que **la industria no puede llenar**
—tiene conflicto de interés al auditar sus propios escáneres y no puede publicar ground truth
independiente— y la ventaja académica está en **validez, reproducibilidad y solidez**, no en el
número de prevalencia. Advertencia: cualquier medición de prevalencia **caduca en meses**.

---

## 6. Recomendación (revisada tras la auditoría)

La auditoría cambió el matiz, no la dirección. **Ambos temas puntúan 6/10 — saturados en su
sub-línea dominante, abiertos en los bordes.** La diferencia entre publicar y ser rechazado no
está en *qué tema* eliges, sino en **dónde apuntas dentro de él**.

### Primera opción: T-B, versión afinada — no la ingenua

**No hagas "modelo vs. harness en SWE-bench": eso ya es redundante.** Haz uno de estos dos, que
están explícitamente abiertos:

1. **Tier barato × harness (tu terreno).** Nadie ha publicado si el efecto-harness **se mantiene,
   crece o colapsa al bajar de tier de modelo**. La literatura usa casi exclusivamente modelos
   frontera; los chinos baratos aparecen solo como "side cells". Es literalmente una comparación
   de modelos —la forma que tú propusiste— con tus APIs como instrumento natural, ~$20, cero GPU,
   y con la ventaja de que **si el efecto colapsa con modelos baratos, ese resultado negativo es
   publicable y contraintuitivo**.
2. **Estimar las métricas que el campo propuso y nunca midió.** arXiv:2605.23950 declara
   Recovery Rate RR(k), Context Retention y Control Lag y dice textualmente que **no** las
   estima: *"we specify them as reporting requirements for future harness-aware evaluations"*.
   Nadie las ha estimado sobre una grilla real. Reutiliza los datos del punto 1, así que el coste
   marginal es casi cero.

**Por qué sigue siendo la primera opción:** coste ~$20, sin GPU, sin barrera matemática, y el
hueco está firmado por el propio paper que lo deja abierto. Además, la versión 2 te da un
artefacto (librería de análisis de trazas) que es citable y reutilizable — exactamente el tipo de
contribución que la literatura de 2026 premia.

### Segunda opción: T-A, apuntando a A1 o A3 — nunca a A2

**Si entras a competir en "variante de subespacio low-rank con +1.5% en SST-2", vas a un
matadero.** Los huecos reales:

- **A1 — Evaluación des-obfuscada: el más limpio y el más barato.** ZO-Bench (2024) es el único
  trabajo que incluye el baseline de gradiente directo; no existe ningún paper de 2026 dedicado a
  protocolos con presupuesto de queries fijo, con/sin task alignment. Factible en 6 GB
  (RoBERTa-large, OPT-1.3B en bf16, un modelo 4-bit).
- **A3 — Estimadores generativos: prácticamente VACÍA.** Nadie ha usado difusión/denoisers como
  estimador de gradiente ZO. Alto riesgo, máxima novedad.

Es el de mayor techo académico y el único donde tu 4050 es **ventaja estructural** — pero es el
más matemático.

### Tercera opción: T-C (seguridad de skills) — **8/10, el más saturado**

Es el **único de los tres que NO recomiendo como primera opción**, y la razón es que subestimé el
área: 56 papers de seguridad de skills en 9 meses, escaneo ya comercializado (Snyk, Cisco, Socket,
Gen, NVIDIA, Akto), estándar OWASP dedicado, y **mis tres etapas propuestas ya pre-emptadas**.
Además, dos de los siete desafíos del survey que te cité como huecos **fueron cerrados** por
trabajos de mayo–junio 2026.

**Si aun así te atrae**, entra por el único hueco que la industria no puede llenar: **la
metrología**. No existe ground truth humano público con acuerdo inter-anotador; los escáneres
acuerdan a nivel azar (kappa 0,045–0,082), ninguno supera el baseline "marcar todo", y los
datasets anotados prometidos por trabajos previos **no son localizables**. Construir ese ground
truth y auditar los escáneres contra él es un aporte real, barato (50–200 USD) y sin GPU.

### Hilo conductor que emerge de las tres auditorías

Fíjate en el patrón: **el hueco limpio es de medición en los tres casos** — evaluación
des-obfuscada (A1) en ZO, métricas de trayectoria no estimadas y potencia estadística en
modelo-vs-harness, y verificación de skills en T-C. Eso **coincide exactamente** con el hallazgo
de los exploradores: *metodología de evaluación es el área más subinvertida en relación a su
impacto*. No es coincidencia: el campo produce métodos más rápido de lo que produce instrumentos
para medirlos, y ahí es donde un pregrado con recursos limitados puede aportar algo real.

---

## Fuentes

**Exploradores / mapas de viabilidad:** arXiv:2608.06663 (The Horizon Gap, 1,547 papers) ·
ArxivLens "The State of AI Research 2026" (422,059 papers) · arXiv:2602.16763 (saturación de 60
benchmarks) · ACL Findings 2026 "A Survey on Evaluation of LLM-based Agents" · "The Edge of AI
Research: ICML/ICLR/NeurIPS 2023–2026" · Stanford HAI AI Index Report 2026 (arXiv:2606.15708) ·
arXiv:2608.14611 (Singapore Consensus 2026) · Schmidt Sciences Trustworthy AI Research Agenda
2026 · arXiv:2601.02749 (Path Ahead for Agentic AI) · arXiv:2601.12538 (Agentic Reasoning
roadmap) · arXiv:2603.22862 (multi-tool agents) · arXiv:2609.04894 (world-acting systems).

**Deprecación y saturación:** arXiv:2602.16763 · Edge of AI Research (pretraining, 3DGS) ·
arXiv:2603.13372 (ARC-AGI Living Survey: 93% en ARC-AGI-1, 68.8% en v2, 13% en v3) ·
arXiv:2607.14123 (XAI foundations) · arXiv:2602.24176 (siete supuestos falsos de XAI).

**Subexplorado:** arXiv:2605.15622 (ZO underexplored) · arXiv:2602.12430 (agent skills: 26.1%
vulnerables, 7 desafíos) · mbrenndoerfer, "Research Directions: Open Problems, Benchmarks,
Community Priorities" (áreas subinvertidas) · arXiv:2608.06663 (problemas de medición).

**Contexto UNI:** fc.uni.edu.pe (plan de estudios) · R.R. 1439-2023-UNI (formato APA o IEEE).
