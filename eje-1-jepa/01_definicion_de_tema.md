# Tesis 1 (alternativa) — Definición de tema: JEPA / modelos de mundo latentes

Documento de trabajo · 18-sep-2026 · verificación directa de fuentes (18-sep-2026)

---

## 1. Veredicto en una línea

**Sí, pero por una razón opuesta a Jev.** JEPA está **100% abierto** (MIT, pesos, datasets) y
saturado de papers — así que no puedes ganar por "ser el primero en medir". Se gana por
**ser el que audita**: ya hay evidencia documentada de que la métrica principal de estos
modelos (éxito en lazo cerrado) **esconde fallos reales**, y ese es un hueco publicado,
reconocido y con veneno propio. Además existe una **pasarela de publicación creada para
exactamente este tipo de trabajo** (ICML Open Reproductions, FAGEN workshop).

Riesgo #1 distinto al de Jev: aquí no hay riesgo de acceso, hay **riesgo de cómputo**.

---

## 2. Qué es JEPA y en qué estado está (hechos verificados)

JEPA = *Joint Embedding Predictive Architecture*, propuesta por Yann LeCun en 2022
(*A Path Towards Autonomous Machine Intelligence*): predecir **representaciones** del futuro
en un espacio latente, en lugar de píxeles o tokens. La familia: I-JEPA (imágenes, 2023) →
V-JEPA (video) → V-JEPA 2 / 2.1 (mundo + robots) → LeJEPA (teoría) → LeWorldModel / LeVJEPA
(recetas estables y baratas) → y una docena de derivados en 2026 (audio-visual, molecular,
clínico, biomédico, tabular, lenguaje).

**Contexto empresarial:** LeCun dejó Meta en nov-2025 y fundó **AMI Labs** (París) con
**1,030 millones USD** de ronda semilla a una valoración pre-money de 3,500 M (mar-2026),
con NVIDIA y Samsung como inversores. AMI **libera su código** ("open-sourced its code,
aspires to build an ecosystem").

### 2.1 Lo que verifiqué directamente (no por blogs)

**GitHub API — repositorio oficial y ecosistema:**

| Repo | Estrellas | Licencia | Creado | Último push |
|---|---|---|---|---|
| `facebookresearch/vjepa2` (V-JEPA 2 / 2-AC / 2.1) | **4,650** | **MIT** | 2025-04-25 | 2026-03-23 |
| `lucas-maes/le-wm` (LeWorldModel) | **4,442** | **MIT** | 2026-03-13 | 2026-05-26 |
| `facebookresearch/ijepa` | 3,487 | (NOASSERTION) | 2023-06-12 | 2024-05-08 |
| `rbalestr-lab/lejepa` (teoría + SIGReg) | 1,356 | (NOASSERTION) | 2025-11-11 | 2026-01-25 |
| `facebookresearch/eb_jepa` (librería didáctica) | 783 | **Apache-2.0** | 2025-12-21 | 2026-07-17 |
| `facebookresearch/jepa-wms` (planificación) | 487 | **CC-BY-NC 4.0** ⚠ | 2025-12-02 | 2026-04-11 |
| `rbalestr-lab/llm-jepa` | 337 | Apache-2.0 | 2025-09-05 | 2026-04-15 |
| `facebookresearch/dinov2` (backbone de control) | 13,346 | Apache-2.0 | 2023-03-29 | 2026-06-03 |
| `TheoLeeCJ/openjev` (compare: el caso Jev) | 1,560 | MIT | 2026-09-16 | 2026-09-18 |

⚠ `jepa-wms` es **CC-BY-NC 4.0 = no comercial**, y su dataset (11.1 GB) está tras un
formulario de contacto.

**Hugging Face API — pesos y datasets (consulta real, búsqueda "jepa"):**
- Checkpoints oficiales: `facebook/vjepa2-vitl-fpc64-256`, `-vith-`, `-vitg-fpc64-256`,
  `-vitg-fpc64-384`, V-JEPA 2.1 (`vitb_384`, `vitl_384`, `vitg_384`, `vitGigantic_384`), y
  cabezas afinadas SSv2 (`facebook/vjepa2-vitg-fpc64-384-ssv2`).
- Dataset oficial: `facebook/jepa-wms` (5 checkpoints + 11.1 GB de datos de planificación).
- Integración nativa en `transformers`: `AutoModel.from_pretrained("facebook/vjepa2-vitl-fpc64-256")`.
- Ecosistema comunitario vivo: `braindecode/signal-jepa` (EEG), `NYUMedML/Neuro-JEPA`,
  `Flogrammer/Mol-JEPA`, `hamzashafiq/CardioState-Jepa`, `lerobot/VLA-JEPA-Pretrain`,
  y **cuantizaciones GGUF** (`jepacpp/vjepa2-*`, `jepacpp/levjepa-vitl16-GGUF`) → inferencia en CPU posible.

**Conclusión sobre apertura:** JEPA es lo contrario de Jev. Código, pesos, datasets,
benchmarks, leaderboard en HF y una librería permissiva (Apache-2.0) para empezar.
**No necesitas pedirle permiso a nadie para iniciar la investigación.**

### 2.2 El costo de la apertura: saturación

Paper tras paper en 2026 con el mismo patrón: receta estable + dropout de tokens + SIGReg,
y una suite propia de evaluación. Muestra representativa:

| Paper | Aporte | Fecha |
|---|---|---|
| LeJEPA (arXiv:2511.08544, Balestriero & LeCun) | Teoría: el óptimo es Gaussian isotrópico; SIGReg de 1 hiperparámetro | nov-2025 |
| LeWorldModel (arXiv:2603.19312) | JEPA end-to-end estable desde píxeles, sin EMA/stop-grad; 15M params, 1 GPU, planifica en <1 s | mar-2026 |
| V-JEPA 2.1 (arXiv:2603.14482) | Features densas temporalmente consistentes; +20 pp de agarre vs V-JEPA 2-AC | mar-2026 |
| LeVJEPA (arXiv:2608.27395) | 1 encoder, sin EMA ni masking, solo SIGReg; iguala V-JEPA 2 con **5.6–20.8× menos cómputo**; ViT-Tiny entrena **12 h en 1 GPU de consumidor** | ago-2026 |
| UniJEPA (2608.07409), JEPA-x (2608.24044), PSG-JEPA (2608.06799), Semigroup-JEPA (2609.10464), Flow-JEPA (2608.29029), Orthogonal JEPA (2608.20065), Mol-JEPA, MJEPA, JEPA-Anything (2609.20800), LLM-JEPA, Var-JEPA (2603.20111), LeVLJEPA | Variantes de dominio y de objetivo | 2026 |

Implicación para tu plan: **no propongas "aplicar JEPA a X"** — hay un competidor por semana
y probablemente ya existe (molecular, clínico, EEG, audio-visual, tabular, navegación).
Propón **metodología de evaluación**.

---

## 3. El hueco: la métrica miente

Aquí está la tesis. No es especulación mía: está diagnosticado en literatura revisada y en
un programa oficial de reproducción.

### 3.1 La prueba central — ARC-Bench (arXiv:2609.05461, 17-sep-2026)

Audita el supuesto silencioso de todos los planificadores JEPA: *"si el futuro latente
predicho queda más cerca del objetivo latente, la acción es mejor"*. El resultado:

- El supuesto **falla de forma severa y estructural**: en las auditorías de manipulación,
  **el candidato mejor puntuado es casi siempre subóptimo**; la misma inversión aparece en
  navegación.
- El defecto **persiste** al cambiar el backbone de DINOv2 a V-JEPA 1 y V-JEPA 2 en escala
  ViT-L/ViT-G.
- Se descartan explicaciones triviales (procedencia, subentrenamiento, controles de
  presupuesto igualado, circularidad de la métrica).
- **Y explica por qué nadie lo notó: el replanning en lazo cerrado lo enmascara.** Al bajar
  la frecuencia de replanificación, el éxito **colapsa**. Es decir: **las tasas de éxito en
  lazo cerrado sobreestiman sistemáticamente la calidad de las representaciones latentes.**

En una frase: *la comunidad reporta éxito de tarea, pero nunca audita si el objetivo latente
ordena acciones correctamente.*

### 3.2 Confirmación independiente del mismo patrón

| Evidencia | Hallazgo |
|---|---|
| **Reproducción independiente de Causal-JEPA** (HF, ICML 2026 Agent Reproduction) | Claims 1–3 **falsificados**: el *lift* de CF-VQA **se invierte** (+21 pp → −26 pp), Push-T 88.7% → **49.3%**, y el "8× más rápido" resulta **2.1× más lento**. Claim 5 (teorema) verificado. |
| **"Is the reconstruction loss culprit?"** (arXiv:2603.14131) | La comparación JEPA vs autoencoders está confundida por objetivos asimétricos; con baseline PCA sobre-parametrizado, parte del relato "JEPA es superior" se desmonta. Recomendación explícita: *"tratar las comparaciones de objetivos como hipótesis, no como veredictos; probar sensibilidad al protocolo de evaluación"*. |
| **JEPA-x** (arXiv:2608.24044) | **Decodabilidad ≠ predecibilidad**: la regresión directa al estado físico mejora la decodabilidad *sin* mejorar la predecibilidad ni el control. |
| **PSG-JEPA** (arXiv:2608.06799) | Diagnostica una *brecha de identificabilidad*: el objetivo de predicción hacia adelante no garantiza recuperar el estado relevante para el control. |
| **Teoría de generalización** (arXiv:2606.27014) | Primera cota finito-muestral: la predicción latente **no es universalmente mejor**; domina solo con ruido alto y horizontes largos. |
| **VJEPA / Var-JEPA** (ICML 2026) | Pregunta abierta textual: *"¿cómo debería comprobarse la calibración del estado latente cuando las coordenadas latentes son aprendidas y no observables directamente?"* |
| **UniJEPA** | Los números de V-JEPA 2 citados por distintos papers **no coinciden** (77.3 vs otros) → protocolos no armonizados. |

### 3.3 Formulación publicable del hueco

> La evaluación de modelos de mundo JEPA mide **decodabilidad** (sondas lineales) y **éxito
> de tarea en lazo cerrado**, pero no audita **ordenabilidad de acciones** (¿el ranking
> latente coincide con el coste real?) ni la **calibración del estado latente**. La evidencia
> disponible muestra que el éxito en lazo cerrado **enmascara** fallos de ranking, que las
> comparaciones entre objetivos no son simétricas, y que ningún protocolo con fugas-cero es
> estándar.

### 3.4 La pasarela de publicación existe (y es de 2026)

- **ICML 2026 Open Reproductions** (Hugging Face + alphaXiv): 1,221 participantes, **6,816
  logbooks**, 2,226 papers (34% del congreso), **35,908 claims juzgados**. Resultado: **51%**
  con al menos una claim verificada y **23% con al menos una claim falsificada o contestada**.
  Usaron Trackio logbooks + un juez automático (GLM-5.2) instruido para **desconfiar** de la
  autoevaluación. Premios: 2,000 / 1,000 / 500 / 500 USD en créditos GPU, incluido un premio
  específico a **"mejor falsificación / resultado negativo"**.
- **ICML 2026 Workshop FAGEN** (*Failure Modes in Agentic AI*): venue **no archivístico**
  (puedes publicar después en otro sitio), 8 páginas, explícitamente acepta **resultados
  negativos bien documentados**, y pide *"reproducciones mínimas"*, *"protocolos de
  evaluación comparables"* y *"diagnósticos a nivel de traza"*.

Traducción práctica: **una auditoría claim-por-claim de un paper JEPA es un trabajo
publicable en 2026 con infraestructura y premios ya montados.** Y no es un subproducto: es
el tipo de trabajo que la conferencia declaró explícitamente como valioso.

### 3.5 Por qué esto aporta aunque el resultado salga "como se espera"

El valor no está en el modelo ni en su accuracy: está en **el instrumento de medición**. En esta
línea, el resultado esperado **es** la contribución, siempre que el protocolo sea pre-registrado
y estanco (sin fugas), porque lo que se publica es la *cuantificación* de un defecto que hoy
solo está afirmado cualitativamente, más el protocolo que lo mide.

Precedente exacto: **Guo et al. (2017), *On Calibration of Modern Neural Networks*** no propuso
un modelo nuevo — midió la calibración de las redes de la época y se volvió la cita obligatoria
de toda afirmación sobre calibración desde entonces. Un paper de medición bien construido se
convierte en infraestructura.

**El diseño debe ser indiferente al signo del resultado.** Tres desenlaces posibles y qué aporta
cada uno:

| Desenlace | Hallazgo | Contribución | Qué habilita |
|---|---|---|---|
| **A. El defecto se replica** en V-JEPA 2.1 | El ranking latente sigue roto en la generación nueva | Validez externa + tabla de referencia por encoder/dominio/budget | Tesis 2: el fix. Cualquier trabajo futuro que use planificadores latentes debe citar tu tabla |
| **B. El defecto desaparece** en 2.1 | Algo del cambio de receta lo corrigió | Baseline **positivo**: caracterizas qué cambió y por qué. Es un resultado *mejor*, no peor | Tesis 2: adoptar y extendér a otros dominios; abres la pregunta "¿qué parte de la receta lo arregla?" |
| **C. Mixto** (depende del dominio, del budget de replanning, o de la escala) | El defecto aparece solo bajo ciertas condiciones | **Caracterización**: el paper de mayor valor, porque convierte un hallazgo binario en una frontera | Tesis 2: el criterio de cuándo confiar en el planificador |

Por eso el protocolo se pre-registra antes de correr el test (OSF/Zenodo con DOI): hace que
cualquiera de los tres desenlaces sea creíble y no "ajustado a lo que salió".

**Artefactos que son el baseline de trabajos futuros** (esto es lo que se cita y se reusa):
1. El protocolo no-leak como código ejecutable (definición operacional de *ordenabilidad*).
2. Tablas de ordenabilidad por encoder × dominio × frecuencia de replanning.
3. El **coeficiente de enmascaramiento**: cuánto del éxito en lazo cerrado depende del rescate
   por replanning — el número que hace interpretables los éxitos reportados por otros.
4. La **matriz de disociación** decodabilidad × predecibilidad × ordenabilidad.
5. Features cacheadas + números crudos: quien venga después no recalcula 60 h de encoder.

---

### 3.6 Qué NO puede dar una GPU de 6 GB (límites honestos del techo)

Para no vender humo: con una RTX 4050 **no** habrá afirmaciones sobre leyes de escala, ni
números SOTA, ni preentrenamiento desde cero a escala. Nada de eso hace falta para la
hipótesis, pero conviene decirlo.

| Afirmación | ¿Necesita GPU grande? |
|---|---|
| "El defecto existe a escala ViT-B/L en V-JEPA 2.1" | No — local |
| "El enmascaramiento por replanning sigue el patrón X" | No — local |
| "Decodabilidad ≠ ordenabilidad" (matriz de disociación) | No — local |
| "El defecto persiste hasta ViT-G (invariancia de escala)" | **Sí** — ~20-40 h rentadas (USD 40-60) |
| "Nuestra receta de entrenamiento corrige el defecto" (Taller) | No — ViT-Tiny/S local |

La escala **no es la variable científica** aquí: lo es la propiedad de ordenabilidad, y esa se
mide igual en 15M que en 1B parámetros. ViT-G es un brazo de robustez, no el núcleo.

---

## 4. Viabilidad técnica

### 4.1 Acceso a código, pesos y datos: resuelto

Nada de listas de espera. Todo está en GitHub (MIT/Apache-2.0) y Hugging Face.
Los entornos de evaluación están liberados: los datasets, planificadores y predicados de
éxito de Push-T, OGBench-Block, Two-Room y Reacher acompañan a LeWM; `jepa-wms` trae 5
checkpoints + 11.1 GB de datos (uso no comercial).

### 4.2 Cómputo — aquí está el riesgo real, y tiene solución

El truco: **los encoders están congelados → los embeddings se cachean.** El costo escala con
el número de clips **únicos**, no con la cantidad de candidatos ni de pasos de rollout.

Estimación (supuestos explícitos: ViT-L ≈ 0.10 s/clip en A100, ViT-G ≈ 0.25 s, 1,000 episodios
× 200 frames únicos × 3 seeds):

| Config | GPU-h | USD @ 1.50/h |
|---|---|---|
| V-JEPA 2.1 ViT-B/384 | 8.3 | 12.5 |
| V-JEPA 2 ViT-L/256 | 16.7 | 25.0 |
| V-JEPA 2 ViT-G/256 | 41.7 | 62.5 |
| DINOv2 ViT-L (control) | 13.3 | 20.0 |
| LeWorldModel 15M (control) | 1.7 | 2.5 |
| **Total** | **81.7** | **122.5** |

**Con pantalla reducida** (400 episodios, 3 configs, 3 seeds): **26.7 GPU-h ≈ USD 40** →
**cabe en la cuota gratuita de Kaggle (30 GPU-h/semana)** o en Colab.
El planificador (CEM 300×30×horizonte) corre sobre features cacheadas en NumPy: barato.

Referencia de que el escalón es real: LeVJEPA reporta ViT-Tiny preentrenado **12 h en una
GPU de consumidor**, y LeWorldModel entrena con 15M parámetros en 1 GPU. Para el Taller
(etapa 3) eso vuelve el entrenamiento propio viable.

### 4.3 Datos y dominios

| Recurso | Qué aporta |
|---|---|
| Push-T, OGBench-Block, Two-Room, Reacher (liberados con LeWM) | Auditoría de ranking en control con ground truth de éxito |
| `facebook/jepa-wms` (11.1 GB; **no comercial**) | Navegación + manipulación; 5 checkpoints para auditar |
| Metaworld 42 tareas + grabaciones Franka (en jepa-wms) | Escala multi-tarea |
| SSv2, Kinetics-400, EK-100, ImageNet | Evaluación de representación (decodabilidad) para la matriz de disociación |
| DROID (8.7 TB opcional) | Post-entrenamiento condicionado por acción — **solo si sobra cómputo** |
| **Alternativa local** (Perú) | Datos abiertos INEI/SUNAT/MINSA/SBS → variante **tabular-JEPA** (familia T-JEPA/Var-T-JEPA) con scikit-learn-tier y aporte local real |

### 4.4 Entorno: sin GPU desde el principio

Con GGUF (`jepacpp/vjepa2-vitl-fpc64-256-GGUF`, `jepacpp/lewm-pusht-GGUF`) hay inferencia en
CPU, y `dvd-jepa` entrena en ~10 s en CPU. Suficiente para el piloto de protocolo antes de
gastar GPU.

---

## 5. Propuesta: tres tesis encadenadas (medir → controlar → construir)

### 5.1 Tesis 1 — AUDITAR ⭐ recomendada

**Título propuesto:**
> *¿El éxito en lazo cerrado oculta un ranking latente roto? Auditoría no sesgada de la
> ordenabilidad de acciones en modelos de mundo JEPA congelados.*

**Pregunta de investigación:** ¿En qué medida las representaciones latentes de encoders JEPA
públicos ordenan correctamente las acciones candidatas según el coste real, y cómo depende
esa ordenabilidad de la frecuencia de replanificación, del backbone y del dominio?

**Objetivo general:** reproducir y extender la auditoría de ordenabilidad de acciones sobre
checkpoints JEPA liberados, y cuantificar el efecto de enmascaramiento del replanning en
lazo cerrado.

**Objetivos específicos:**
1. Reimplementar ARC-Bench sobre ≥4 encoders públicos (V-JEPA 2.1 ViT-B/L/g, V-JEPA 2 ViT-L,
   DINOv2 ViT-L como control) con protocolo de candidatos fijos sin fugas (*no-leak*).
2. Medir ordenabilidad con métricas de ranking: correlación de Spearman/Kendall entre
   distancia latente y coste real, NDCG@k, *regret* del top-1, y tasa de inversión top-1.
3. Cuantificar el **enmascaramiento**: éxito en lazo cerrado vs frecuencia de replanificación
   (barras: 1, 2, 5, 10, ∞ replans), midiendo cuánto del éxito depende del rescate.
4. Construir la **matriz de disociación** decodabilidad × predecibilidad × ordenabilidad ×
   éxito de control, para separar "representación buena para sondas" de "representación
   buena para planificar".
5. Reproducir claim-por-claim **un paper JEPA concreto** (candidato natural: las afirmaciones
   de planificación de V-JEPA 2.1 o de JEPA-x sobre decodabilidad vs predecibilidad),
   documentando verificado / falsificado / toy / inconcluso.
6. Publicar protocolo, código, features cacheadas y veredictos (GitHub + Zenodo + logbook HF).

**Hipótesis:**
- **H1** La ordenabilidad (Spearman latente vs coste real) es baja o negativa en una fracción
  sustancial de episodios, replicando ARC-Bench en checkpoints V-JEPA 2.1.
- **H2** El éxito en lazo cerrado correlaciona fuerte con la frecuencia de replanificación y
  débilmente con la ordenabilidad → el replanning enmascara el defecto.
- **H3** La decodabilidad (sonda lineal sobre estado físico) **no** predice la ordenabilidad
  ni el éxito de control (disociación replicada).
- **H4** La ordenabilidad degrada con la escala del backbone de forma no monótona (ViT-G no
  necesariamente mejor que ViT-L) → el defecto no es de capacidad.

**Diseño:** 4–6 configuraciones × 3 seeds × 2–3 dominios. Todo inferencia congelada, sin
entrenar el encoder. Cabezas de sonda ligeras (lineales) para la matriz de disociación.

**Contribuciones declarables:**
1. Primera auditoría independiente de ordenabilidad sobre la familia **V-JEPA 2.1** (ARC-Bench
   auditó JEPA-WM; falta la generación más reciente de checkpoints).
2. Cuantificación del **efecto de enmascaramiento** del replanning como curva, no como
   observación cualitativa.
3. Matriz de disociación decodabilidad/predecibilidad/ordenabilidad como diagnóstico estándar.
4. Protocolo, features cacheadas y veredictos claim-por-claim, reproducibles con cuota gratuita.

**Publicación objetivo:** track de reproducción / workshop de fallos (FAGEN-style, no
archivístico) → luego conferencia regional o revista con el preprint de arXiv.
**Qué NO hace:** no entrena encoders, no propone arquitecturas, no persigue SOTA.

**Esfuerzo:** ~27–82 GPU-h, USD 40–120, datos y pesos ya liberados. Cabe en Kaggle/Colab.

### 5.2 Tesis 2 — CONTROLAR (la corrección)

**Título:** *Planificación latente consciente del ranking: una cabeza de coste sin fugas y su
evaluación a presupuesto de replanificación fijo.*

Del diagnóstico a la mitigación. Aportes: (i) sustituir la puntuación por distancia latente
por una cabeza de ranking entrenada sobre trayectorias retenidas (pairwise/listwise, sin
fugas de la evaluación); (ii) comparar contra CEM, replanning frecuente, DINO-WM y
V-JEPA 2-AC **con presupuesto de replanning igualado** — que es la comparación que hoy no
existe; (iii) añadir **calibración del estado latente** con predicción conformal sobre
latentes (garantía de riesgo finito-muestral) y evaluar deriva de distribución entre dominios;
(iv) validar en dos dominios (control sintético + una segunda familia de tareas).
Métrica estrella: **tasa de éxito a presupuesto fijo de replanning y de cómputo**.

### 5.3 Taller de tesis — CONSTRUIR

**Título:** *Objetivo JEPA con ordenabilidad y calibración: preentrenamiento estable en una
GPU y liberación de pesos.*

Entrenar un JEPA pequeño desde cero (receta LeVJEPA: 1 encoder, SIN EMA, SIN masking, SIGReg;
ViT-Tiny/S, **12 h en 1 GPU de consumidor por corrida**) añadiendo un término de ordenabilidad
en el objetivo, y evaluarlo con el protocolo y el benchmark de las etapas 1 y 2. Liberar pesos
+ benchmark en HF. Variante con aporte local: **tabular-JEPA sobre datos abiertos peruanos**
(INEI/SBS/MINSA/SUNAT), que no requiere video ni GPU grande y produce contribución aplicada
verificable.

---

## 6. Riesgos y mitigaciones

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | **Cómputo insuficiente** (el verdadero cuello) | Media | Alto | Cachear embeddings (obligatorio); reducir a 3 configs y 400 episodios → 27 GPU-h; Kaggle 30 h/semana gratis; GGUF para piloto en CPU; pedir créditos a AMI Labs / HF Jobs / Google TRC |
| R2 | Te ganan el tema (ARC-Bench ya existe) | **Alta** | Medio | Diferenciar en tres ejes: (a) checkpoints **V-JEPA 2.1** (posteriores a ARC-Bench), (b) el **efecto de enmascaramiento** cuantificado como curva, (c) **matriz de disociación** con calibración latente |
| R3 | Licencia **CC-BY-NC** de `jepa-wms` (no comercial) y dataset tras formulario | Alta | Medio | Usa `jepa-wms` solo como referencia/auditoría académica y cita la restricción; los datasets de LeWM (MIT) son la base principal |
| R4 | El asesor lo ve como "reproducir un blog" | Media | Medio | Enmarca como **metrología de sistemas de IA**: definición operacional de métricas, protocolo sin fugas, intervalos de confianza, análisis de sensibilidad. Es ingeniería de evaluación, no crítica |
| R5 | Coste de entrenamiento en el Taller | Media | Medio | Acotar a ViT-Tiny/S con 12 h/GPU por corrida; 5 seeds ≈ 60 GPU-h ≈ USD 90 |
| R6 | Sesgo por falta de seeds / varianza | Alta | Bajo | 3–5 seeds obligatorias con IC bootstrap; reportar varianza de la propia métrica (ARC-Bench ya advierte que el top-1 puede ser estocástico) |

---

## 7. Comparación honesta: Jev vs JEPA para tu Tesis 1

| Criterio | Jev (System One) | JEPA |
|---|---|---|
| Open source | **No** (sin pesos, sin paper, API cerrada) | **Sí** (MIT/Apache-2.0, pesos en HF, datasets) |
| Riesgo de acceso | Medio (lista de espera / tarjeta) | **Nulo** |
| Riesgo de cómputo | **Nulo** (todo API, <USD 30) | **El riesgo principal** (27–82 GPU-h) |
| Novedad del tema | Alta (nadie auditó con ground truth) | Alta, pero en un carril ya definido (auditoría) |
| Saturación de literatura | Baja (20 blogs, 0 papers) | **Muy alta** (docenas de papers/mes) |
| Contribución típica | Medición empírica + benchmark | Auditoría metodológica + protocolo |
| Barrera para un principiante | Baja (llamar APIs y medir) | Media (entrenar/planificar y depurar código ajeno) |
| Techo de publicación | Workshop / conferencia regional | Track de reproducción / workshop → conferencia |

**Recomendación:** Jev es la Tesis 1 más segura para un estudiante que empieza (sin GPU,
sin código heredado). JEPA es más sólida académicamente y tiene mejor proyección, pero exige
depurar código de terceros y administrar cómputo — eso encaja mejor como **Tesis 2**, no
como primera tesis, salvo que ya tengas GPU propia.

---

## 8. Decisiones que necesito de ti

1. **¿Tienes GPU?** (propia, laboratorio, Colab Pro, o ninguna). Si no hay GPU, JEPA baja a
   segunda prioridad frente a Jev.
2. **¿Prefieres medir un modelo cerrado y nuevo (Jev) o auditar modelos abiertos y saturados
   (JEPA)?** Define todo el resto.
3. **Si eliges JEPA: ¿control/robótica o un dominio local peruano?** (tabular/EEG/series
   temporales tienen umbral de cómputo mucho menor que video + robótica).
4. **¿Te sirve un venue con plazo en 2027-I o necesitas publicar antes?** ICML/NeurIPS tienen
   calendarios duros; los workshops, no.

---

## 9. Fuentes primarias verificadas

**JEPA — fundamentos y releases oficiales:**
- LeCun (2022). *A Path Towards Autonomous Machine Intelligence*. OpenReview.
- Assran et al. (2023). *I-JEPA*. CVPR.
- Assran et al. (2025). *V-JEPA 2*. arXiv:2506.09985 (código MIT, checkpoints HF, 3 benchmarks).
- Mur-Labadia et al. (2026). *V-JEPA 2.1: Unlocking Dense Features*. arXiv:2603.14482.
- Balestriero & LeCun (2025). *LeJEPA: Provable and Scalable SSL Without Heuristics*. arXiv:2511.08544.
- Maes et al. (2026). *LeWorldModel*. arXiv:2603.19312.
- Kuhn, Maes, Serra, Le Lidec, LeCun, Balestriero, Buettner (2026). *LeVJEPA*. arXiv:2608.27395.
- Terver, Yang, Ponce, Bardes, LeCun (2025). *What Drives Success in Physical Planning with
  Joint-Embedding Predictive World Models?* arXiv:2512.24497 (`jepa-wms`, CC-BY-NC).
- EB-JEPA (2026). arXiv:2602.03604, `facebookresearch/eb_jepa` (Apache-2.0).
- Dupoux, LeCun & Malik (2026). *Why AI Systems Don't Learn…* arXiv:2603.15381.

**Auditoría y metodología (el hueco):**
- *ARC-Bench: Closed-Loop Replanning Masks Broken Action Ranking in Frozen JEPA World Models*.
  arXiv:2609.05461.
- *Is the reconstruction loss culprit? An attempt to outperform JEPA*. arXiv:2603.14131.
- *Generalization Theory for JEPA World Models*. arXiv:2606.27014.
- *PSG-JEPA: Physical State Grounding*. arXiv:2608.06799.
- *JEPA-x: Cross-Predictive Physics Grounding*. arXiv:2608.24044.
- *UniJEPA*. arXiv:2608.07409.
- *Semigroup-JEPA*. arXiv:2609.10464. *Flow-JEPA*. arXiv:2608.29029. *Orthogonal JEPA*. arXiv:2608.20065.
- *VJEPA: Variational JEPA* (ICML 2026, Y. Huang). *Var-JEPA*. arXiv:2603.20111.
- *Mol-JEPA*. arXiv:2608.22642. *MJEPA*. arXiv:2606.25225. *JEPA-Anything*. arXiv:2609.20800.
- Reproducción independiente de *Causal-JEPA* (ICML 2026 Agent Reproduction), HF blog:
  claims 1–3 falsificados, claim 5 verificado.

**Infraestructura de publicación y comunidad:**
- ICML 2026 Open Reproductions (Hugging Face + alphaXiv): 1,221 participantes, 6,816 logbooks,
  2,226 papers, 35,908 claims; 51% con claim verificada, 23% con claim falsificada/contestada.
- ICML 2026 Workshop FAGEN — *Failure Modes in Agentic AI* (no archivístico, acepta negativos).
- *A Survey of World Model Benchmarks* (Preprints.org).
- AMI Labs: WIRED (10-mar-2026), TechCrunch (09-mar-2026), Chosun (jul-2026).

**Comprobaciones directas realizadas (18-sep-2026):** GitHub REST API para 9 repositorios
(estrellas, licencia, fechas), Hugging Face API para modelos y datasets con "jepa",
`facebookresearch/vjepa2` README y colección HF de V-JEPA 2.
