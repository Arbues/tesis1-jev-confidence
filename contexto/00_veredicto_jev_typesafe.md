# Tesis 1 — Definición de tema: "Modelos de decisión System One (Jev) vs LLMs de bajo costo"

Documento de trabajo · 18-sep-2026 · basado en verificación directa de fuentes (18-sep-2026)

---

## 1. Veredicto en una línea

**Sí hay base para investigar, y es un hueco real y bien delimitado.** Pero el hueco NO es
"explicar qué es Jev" (eso ya lo hicieron 20 blogs en 48 horas), sino **auditar con datos y
etiquetas humanas las dos afirmaciones que TypeSafe NO ha publicado: la calibración de las
probabilidades y la ventaja real de costo frente a los LLM baratos**. Nadie lo ha hecho con
ground truth. Es medible, es barato (< 20 USD en total), no requiere entrenar nada — apto
para un estudiante que empieza — y es publicable en las tres etapas (1 → 2 → taller).

Un riesgo crítico y **una decisión que debes tomar en la semana 1**: el acceso a Jev. Lo
resuelvo abajo con evidencia dura (existe una ruta sin lista de espera y de USD 5/mes).

---

## 2. Qué es Jev exactamente — verificado vs. afirmado

### 2.1 Dato crudo verificado por mí (no por blogs)

Consulté el catálogo público de Vercel AI Gateway (`GET https://ai-gateway.vercel.sh/v1/models`,
HTTP 200, 372 modelos). Entrada literal:

```
id: typesafe-ai/jev        name: Jev
type: evaluation           owned_by: typesafe-ai
released: 1789430400       (15-sep-2026)
pricing: input 0.000000042 USD/token  →  $0.042 por millón de tokens
         output 0                  →  salida gratis
zdr: all      no_training: all       (Zero Data Retention y No Training disponibles)
supported_specifications: ["v4"]
```

Esto confirma **tres cosas operativas**: (a) el modelo es real y llamable por API; (b) la
salida no se cobra; (c) se puede pedir Zero Data Retention — relevante para datos de terceros
y para el comité de ética.

### 2.2 Tabla: afirmación del vendor vs. evidencia disponible

| Afirmación de TypeSafe | Evidencia que la respalda | Estado |
|---|---|---|
| 70–500 ms por llamada | Medido por terceros: 777 juicios en <0.7 s (Every); 0.35 s/pasaje vs 8.83 s de Claude Fable 5.1 | **Confirmado** por terceros |
| 40–400× más barato | Cierto **solo contra modelos frontera** (Claude Sonnet 5, Opus 5). No contra LLMs económicos | **Depende del comparador** ← hueco |
| 0% de errores de tipo / "no puede alucinar" | Garantía **estructural** (el espacio de salida está enumerado antes de inferir), no empírica. No dice nada sobre corrección semántica | **Cierto pero malinterpretado** |
| "Inteligencia frontera" | Su propio dashboard: 67.8% de **acuerdo** con el promedio de GPT-6 Astra + Claude Fable 5.1 (que es el "ground truth" que usan); mejor comparador 74.1%. En facturación: 61.8% vs 79.1% | **Parcial / débil** |
| "Probabilidades calibradas" (RLCD) | **No hay una sola curva de confiabilidad, ni Brier, ni reliability diagram con etiquetas humanas.** El propio doc de TypeSafe dice "prueba con tus datos" | **NO DEMOSTRADO** ← hueco principal |
| Arquitectura nueva + RLCD | No hay paper, no hay pesos, no hay ablación. Acronymo sin receta reproducible | **No verificable** |

### 2.3 La evidencia independiente que ya existe (y por qué no te quita el tema)

| Artefacto | Qué hizo | Por qué NO cierra el hueco |
|---|---|---|
| Every / Mike Taylor (jul-sep 2026) | 1,709 juicios, latencia y costo reales | 12 pasajes en el punto decisivo; sin ground truth humano, sin curvas de calibración |
| Archer Hume, "Jev's Architecture Unmasked" (17-sep) | 10,000 llamadas API; ECE de 0.0313 en 1,200 ítems de MMLU | Blog auto-publicado, 1 cuenta, 1 región; **no es revisado por pares**; MMLU ≠ dominio de aplicación |
| OpenJev (GitHub, MIT) | Réplica del *interfaz* sobre Qwen3.5-4B con logits congelados: 0.813 acc. en decisiones propias, 0.637 en WANLI, 0.845 de acuerdo modal vs 0.883 publicado de Jev | No ejecutó Jev en vivo; explícitamente dice que "no reproduce la afirmación económica" |
| Laya (HF, `convaiinnovations/laya`) | Modelo de decisión **abierto** de 421M (ModernBERT-large) entrenado con RLCD = reglas de puntuación estrictamente propias (log + esférica + RPS) + temperaturas por cardinalidad. ECE 0.009 en enrutamiento | Es un *vendor competidor* autopromocionado; su tabla comparativa contra Jev mezcla cifras publicadas con medidas propias |
| 20+ blogs (Zenodo toolkit `daf-jev`, pearpages, kingy, orcarouter…) | Análisis documental | **Todos repiten el mismo vacío**: "la calibración está afirmada, no demostrada" |

Prueba de que el hueco está abierto: cinco analistas independientes distintos piden
explícitamente el mismo artefacto que tú vas a producir. pearpages lo enumera como el
"resultado #1 que importa": *una curva de calibración hecha por alguien distinto de TypeSafe,
sobre un dataset con etiquetas humanas, en un dominio lejos de los cuatro flujos de lanzamiento.*

---

## 3. Viabilidad técnica — evidencia dura

### 3.1 Acceso a Jev (el riesgo #1)

| Ruta | Requisito | ¿Sin lista de espera? |
|---|---|---|
| **Vercel AI Gateway** | Cuenta Vercel + método de pago + `AI_GATEWAY_API_KEY`; modelo `typesafe-ai/jev` | **Sí** |
| Directo TypeSafe | Lista de espera en typesafe.ai → consola → API key; límites reportados 250k tok/s y 1,200 req/min | No (días) |
| OpenJev / Laya (open weights) | RTX o CPU; sin API | Sí (plan B) |

Free tier de Vercel AI Gateway: **$5/mes de crédito incluido**, acceso a todos los modelos,
con método de pago registrado. A $0.042/M tokens eso equivale a **~595,000 decisiones de 200
tokens por mes**. Es decir: el estudio completo cabe en el crédito gratuito.

### 3.2 Presupuesto real (calculado, no estimado)

Escala del estudio: 3 tareas × 3 semillas ≈ **30,531 decisiones**.

| Brazo | USD total (prompt corto, 60 tok) | USD total (prompt realista, 500 tok) |
|---|---|---|
| **Jev** (salida gratis) | 0.077 | 0.64 |
| MiMo V2.5 ($0.14/$0.28) | 0.60 | 2.65 |
| GLM-5.3-Flash ($0.15/$0.50) | 0.89 | 3.21 |
| DeepSeek V4.1 Flash off-peak ($0.15/$0.60) | 1.01 | 3.39 |
| DeepSeek V4.1 Flash peak ($0.30/$1.20) | 2.02 | 6.78 |
| Qwen3.7-Plus ($0.40/$1.60) | 2.69 | 9.04 |
| Kimi K3 ($3.00/$15.00) | 23.81 | 73.27 |
| Claude Sonnet 5 (referencia caro) | 23.81 | 73.27 |

**Total del estudio completo con los 6 brazos baratos < USD 30.** El presupuesto no es riesgo.

### 3.3 Hallazgo temprano que ya justifica la tesis (y es cuantificable hoy)

Costo por 1,000 decisiones, mismo input:

```
Jev ............................. $0.0025
MiMo V2.5 ....................... $0.0196   ( 7.8× )
GLM-5.3-Flash ................... $0.0290   (11.6× )
DeepSeek V4.1 Flash (off-peak) .. $0.0330   (13.2× )
DeepSeek V4.1 Flash (peak) ...... $0.0660   (26.4× )
Qwen3.7-Plus .................... $0.0880   (35.2× )
Kimi K3 ......................... $0.7800   (312×  )
```

Es decir: **la ventaja de "40–400× más barato" colapsa a ~8–35× cuando el comparador es un
LLM chino de bajo costo, y solo se sostiene contra modelos frontera (Kimi K3, Claude).** Eso
es un resultado nuevo, publicable y verificable con aritmética de tarifas, antes de mover un
solo token. Nadie lo ha publicado así.

### 3.4 Datos (con etiquetas humanas, gratis, y en español)

| Dataset | Tamaño | Por qué encaja |
|---|---|---|
| **MASSIVE** (Amazon, CC BY 4.0) | 52 idiomas × 19,521 utt.; **60 intenciones**, 18 dominios; `es-ES` y `en-US` paralelos; test 2,974/idioma | 60 opciones cae **dentro del tope de 255 de Jev**; es paralelo → mide la brecha de idioma con el mismo ítem |
| **WANLI-es / XNLI** | NLI 3 vías | Tarea de decisión "difícil" con respuesta verificable; ya usada por OpenJev → comparabilidad directa |
| Tickets TI (Zenodo, 2,229; 7 clases; mayoría EN/DE/PT/ES) | 2,229 | Dominio aplicado real, multilingüe, con etiquetado por 3 profesionales |
| INDECOPI / `alexis07/consumidor_peru` (18.5k filas) | resoluciones en español peruano | **Valor local**: dominio jurídico de consumo, texto largo, español peruano |
| *Opcional*: MMLU (subconjunto) | — | Solo para replicar el ECE de Archer Hume y comprobar consistencia |

### 3.5 Modelos chinos ya habilitados (tu "acceso a modelos chinos")

Esta sesión tiene configurado el proveedor **OpenCode Go / Zen** con 38 modelos. Verificado en
caché local, IDs exactos: `deepseek-flash` (V4.1 Flash), `deepseek-v4-pro`, `deepseek-v4-flash`,
`qwen3.7-plus`, `qwen3.8-max`, `glm-5.3`, `glm-5.3-flash`, `mimo-v2.5`, `mimo-v2.5-pro`,
`minimax-m3`, `kimi-k3`, `longcat-2.0`, `hy3`, `omen-alpha`.

Dos advertencias metodológicas (importantes para que el paper no sea impugnable):

1. **OpenCode Go es una suscripción de USD 10/mes, no un vendor.** Para el *paper* los conteos
   de tokens y precios deben salir de las APIs oficiales (DeepSeek Platform, Alibaba DashScope,
   Zhipu, Moonshot) y citar su tarifa publicada. Usa Go/Zen para el **piloto** y la exploración;
   usa las APIs oficiales para **la tabla de resultados**.
2. Precios DeepSeek tienen **valle/pico** (0.15/0.30 in). Hay que registrar la hora de cada
   llamada y reportar ambas columnas — ese es exactamente el tipo de rigor que gana revisiones.

---

## 4. Estado del arte y posición (por qué esto es "nuevo" y no un ejercicio)

Marco donde se inserta tu tesis, con los papers ancla que ya existen:

| Línea | Trabajo ancla | Relación con tu tesis |
|---|---|---|
| Calibración de LLM y RLHF | **Tian et al., EMNLP 2023**, *Just Ask for Calibration* (ECE −50% verbalizando); Guo et al. 2017 (temperature scaling) | Tu **H1** es heredera directa: RLCD afirma corregir la sobreconfianza que RLHF introduce. Nadie lo midió con ground truth |
| Reglas de puntuación propias | Gneiting & Raftery, JASA 2007 | Base teórica de RLCD (log score, Brier, RPS) — la usarás para justificar tus métricas |
| Ruteo con calibración | **UCCI, arXiv:2605.18796** (isotonic + umbral costo-óptimo, −31% costo, ECE 0.12→0.03) | Tu **Tesis 2** compite/coopera con esto; es tu baseline obligado |
| Evaluación + ruteo en gateways | **SEAR, arXiv:2603.26728** | Mismo escenario arquitectónico (gateway multi-modelo) |
| Clasificador clásico vs prompt | **arXiv:2504.04277** (Thumbtack: embeddings vs prompt en accuracy, calibración, latencia, costo) | **Es tu plantilla metodológica exacta.** Tú la aplicas a un modelo System One en vez de embeddings |
| SLM como enrutador frontal | arXiv:2604.02367 (`confidence degeneracy` → no uses la confianza del modelo como disparador) | Justifica medir calibración en vez de confiar en ella |
| Lectura de logits vs probe interno | arXiv:2604.11943 (ProbeLogits), 2609.04582 (readouts miscalibrados), 2609.05125 (auditoría black-box) | Te da el brazo "baseline justo" que falta en la evaluación de TypeSafe |

**El hueco, formulado como oración publicable:**

> No existe ninguna evaluación independiente, con etiquetas humanas, de la calibración
> probabilística de un modelo de decisión "System One" ni de su ventaja de costo por decisión
> frente a LLM de bajo costo; la evidencia disponible o es del vendor, o es anecdótica, o se
> limita al acuerdo con otros modelos en lugar de la verdad de referencia.

---

## 5. Propuesta: tres tesis encadenadas, cada una publicable

Diseño deliberado: **medir → controlar → construir**. Cada etapa consume los artefactos de la
anterior, de modo que la Tesis 2 ya cita la Tesis 1 y el Taller cita a ambas.

### 5.1 Tesis 1 (la que estás definiendo ahora) — MEDIR

**Título propuesto:**
> *Evaluación empírica de la calibración y del costo por decisión de un modelo de decisión
> "System One" frente a LLM de bajo costo con salida estructurada, en tareas de enrutamiento
> de intenciones en español.*

**Pregunta de investigación (una sola, sin ambigüedad):**
¿Las probabilidades que emite un modelo de decisión System One están calibradas —es decir, una
confianza de 0.9 acierta ~90% de las veces— en datos reales con etiquetas humanas, en un
dominio y un idioma distintos a los de su lanzamiento, y conserva su ventaja de costo por
decisión frente a LLM de bajo costo cuando se iguala la calidad de la decisión?

**Objetivo general:** medir y comparar, con protocolo reproducible, accuracy, calibración,
costo y latencia de un modelo de decisión System One (Jev) frente a cuatro familias de
alternativas, en tres tareas de decisión con ground truth humano, en español e inglés.

**Objetivos específicos:**
1. Construir el arnés de evaluación (código abierto) que emita el mismo conjunto de decisiones
   tipadas a Jev y a los LLM con salida estructurada, registrando predicción, probabilidad,
   tokens y latencia por ítem.
2. Cuantificar calibración con ECE (10 bins + bins adaptativos), MCE, Brier multiclase, NLL y
   curvas de confiabilidad; por tarea, por idioma y por cardinalidad de opciones.
3. Medir el desempeño en régimen selectivo: riesgo en la fracción auto-aceptada, curvas
   riesgo-cobertura, AURC, aplicando el patrón de tres bandas (actuar/revisar/escalar).
4. Medir costo real por 1,000 decisiones y latencia p50/p95, con tarifas oficiales de cada
   vendor y separación valle/pico.
5. Verificar la afirmación de cero errores de tipo: tasa de conformidad de esquema y de
   respuestas fuera del conjunto enumerado (incluyendo inyección de opciones falsas).
6. Publicar dataset de resultados, prompts, salidas crudas y código (repositorio + Zenodo).

**Hipótesis:**
- **H1** Jev presenta menor ECE y mejor Brier que los LLM con salida estructurada y confianza
  verbalizada, en las mismas tareas.
- **H2** La ventaja de costo por decisión de Jev frente a LLM chinos de bajo costo es de
  **un orden de magnitud (~8–35×), no de dos órdenes (40–400×)**; la cifra de 400× solo
  aparece contra comparadores frontera.
- **H3** La calibración de los LLM con salida estructurada se degrada más que la de Jev al
  pasar de inglés a español y al aumentar el número de opciones (tareas de 60 clases).
- **H4** La confianza reportada por los LLM no sirve como señal de enrutamiento (se
  concentra cerca de 1.0 sin correlato en error), mientras que la de Jev sí ordena por error.

**Diseño experimental (6 brazos, mismo protocolo de decisión):**

| # | Brazo | Implementación | Rol |
|---|---|---|---|
| A | Jev | `POST /v1/systemone` (Choice/Noul/Score) vía Vercel Gateway y/o directo | Objeto de estudio |
| B | LLM bajo costo, salida estructurada + confianza verbalizada | DeepSeek V4.1 Flash, GLM-5.3-Flash, MiMo V2.5, Qwen3.7-Plus (API oficial) | Comparador principal ← H2, H3 |
| C | Baseline "logits de un solo token" | Qwen3.5-4B congelado, softmax restringido sobre tokens de opción + temperature scaling (estilo OpenJev) | **El baseline justo que TypeSafe omitió** |
| D | Clasificador clásico | TF-IDF + Regresión Logística; opc. mDeBERTa/XLM-R afinado | Referencia histórica y cota de calibración |
| E | Adaptador LLM→System One | El wrapper de TypeSafe para LLM (si aplica) | Control de interfaz vs modelo |
| F | Techo humano / de referencia | Etiquetas del dataset + revisión manual de una submuestra | Ground truth |

**Métricas y análisis estadístico:** intervalos de confianza por bootstrap (10,000 réplicas);
McNemar para diferencias pareadas de accuracy; bootstrap pareado para diferencias de ECE/Brier;
regresión logística de acierto ~ confianza + modelo + idioma + cardinalidad para H4; todo el
análisis pre-registrado en un documento de protocolo (OSF o Zenodo) **antes** de correr el test set.

**Contribuciones declarables:**
1. Primera auditoría de calibración de un modelo System One con ground truth humano, en
   dominio y idioma ajenos al lanzamiento.
2. Primera cuantificación de costo por decisión frente a LLM de bajo costo (acota la
   afirmación de 40–400×).
3. Arnés y benchmark abiertos y reproducibles (código, prompts, salidas crudas, tokens).
4. Evidencia operativa para umbrales de automatización en un dominio en español.

**Publicación objetivo:** workshop/conferencia (p. ej. workshop LatinX in AI o similar en NLP,
o congreso regional IEEE/CLEI). Plan B y complemento natural: **preprint en arXiv** (necesario
para que la Tesis 2 lo cite) + envío a revista de la universidad.

**Qué NO hace la Tesis 1 (por eso es alcanzable):** no entrena ningún modelo, no modifica
pesos, no diseña arquitectura. Solo orquesta APIs, mide y analiza.

### 5.2 Tesis 2 — CONTROLAR

**Título:** *Enrutamiento selectivo costo-óptimo con umbrales calibrados para capas de decisión
System One: diseño y evaluación end-to-end.*

Convierte tu medición en método. Aportes: (i) política actuar/revisar/escalar con calibración
post-hoc (isotónica/Platt) ajustada fuera de muestra; (ii) comparación contra UCCI (isotónica
sobre margen de tokens), predicción conformal selectiva (con garantía de riesgo finito-muestral),
umbral por entropía y FrugalGPT; (iii) evaluación end-to-end con escalado real al LLM chino
barato y un costo explícito de revisión humana; (iv) estudio de transferencia a un segundo
dominio en español (INDECOPI / tickets) para medir deriva de distribución.

Métrica estrella: **costo a riesgo fijo** (p. ej. ≤2% de error entre lo auto-aceptado) y tasa de
auto-aceptación. Publicable en conferencia principal o revista buena.

### 5.3 Taller de tesis (última) — CONSTRUIR

**Título:** *Un modelo de decisión System One abierto y calibrado para español: entrenamiento
con reglas de puntuación estrictamente propias y riesgo selectivo garantizado.*

Afinas un modelo abierto pequeño (familia ModernBERT-large / Qwen3.5-0.6–4B) con objetivo
estilo RLCD (reward = log score + esférica + RPS para Score ordinal, con temperaturas por
cardinalidad), liberas pesos, y evalúas con el benchmark y el protocolo de las etapas 1 y 2,
añadiendo garantía formal de riesgo selectivo y evaluación bajo cambio de distribución.
Es la versión "en español y con rigor de evaluación" de lo que hoy es Laya (y sin su conflicto
de interés). Publicable + liberación en HF.

---

## 6. Riesgos y mitigaciones

| # | Riesgo | Prob. | Impacto | Mitigación |
|---|---|---|---|---|
| R1 | No obtienes acceso a Jev (lista de espera, tarjeta, geobloqueo) | Media | Alto | **Prueba de acceso en semana 1**: Vercel AI Gateway ($5/mes, sin lista). Plan B: reencuadre el estudio como "modelos de decisión System One" y usas Laya + OpenJev como objetos de estudio — **sigue siendo publicable**, porque el hueco de calibración con ground truth es de la *clase de modelos*, no de un vendor |
| R2 | El benchmark se satura (accuracy ~99%, calibración trivial) | Media | Medio | Incluye WANLI-es y el subconjunto ambiguo del dominio; añade casos de información insuficiente (opción explícita `otro`/`insuficiente`) como hace OpenJev |
| R3 | Te "ganan" el tema (ya hay blogs y un toolkit en Zenodo) | Media-alta | Medio | Velocidad + diferenciación triple: ground truth humano, español, y costo vs LLM barato. Pre-registra el protocolo (fecha citable) |
| R4 | El asesor lo ve como "comparar APIs", no como ingeniería | Media | Medio | Enmarca como *evaluación de un componente de IA en una arquitectura de software*: capa de decisión, gate de confianza, umbrales en código, riesgo operativo. Añade un diagrama de arquitectura de referencia y su costo de error |
| R5 | Límites de tasa del free tier (429) en corridas de 30k llamadas | Media | Bajo | Reintentos con backoff; comprar USD 5–10 de crédito; fragmentar por tarea |
| R6 | Deriva de versión (`jev-latest` cambia de build) | Alta | Medio | Fijar `jev-1.13.0` y registrar el campo `model` de cada respuesta; reportar la versión en el paper |

---

## 7. Plan de 7 días (para cerrar la definición y no perder tiempo)

| Día | Acción | Entregable |
|---|---|---|
| 1 | Crear cuenta Vercel + método de pago + `AI_GATEWAY_API_KEY`; primera llamada a `typesafe-ai/jev` con `curl` | Captura de una respuesta real → **riesgo R1 cerrado** |
| 2 | Descargar MASSIVE 1.1 (`es-ES`, `en-US`) y WANLI; verificar licencias (CC BY 4.0) | Datos en disco + tabla de conteos |
| 3 | Escribir el arnés (Python): cliente Jev + cliente OpenAI-compatible; salida JSONL por ítem con predicción, probabilidad, tokens, latencia | Repo `decision-calibration-bench` con README |
| 4 | Corrida piloto n=200 por brazo; implementar ECE/Brier/curvas de confiabilidad y riesgo-cobertura | Notebook de métricas + primera figura |
| 5 | Pre-registro del protocolo (hipótesis, métricas, test estadísticos, criterios de exclusión) | Documento en OSF/Zenodo con DOI |
| 6 | Corrida completa de la Tesis 1 + tabla de resultados preliminar | Resultados crudos versionados |
| 7 | Borrador del perfil de tesis (problema, objetivos, hipótesis, metodología, cronograma) para el asesor | `01_perfil_tesis1.docx/pdf` |

---

## 8. Decisiones que necesito de ti (bloquean la redacción del perfil)

1. **Carrera/facultad y línea del asesor** — determina si el encuadre debe ser "ingeniería de
   software / sistemas de información" o "ciencia de datos / IA". Afecta el título y el formato.
2. **¿Tienes tarjeta para Vercel?** Si no, activamos el plan B (open weights) desde el día 1.
3. **Dominio de aplicación**: ¿prefieres (a) MASSIVE (asistente de voz, 60 intenciones,
   limpio y comparable), o (b) un dominio peruano real como INDECOPI/consumidor, que da más
   "aporte local" pero exige más trabajo de etiquetado?
4. **¿Hay GPU disponible?** Para el brazo C (logits congelados) basta una GPU modesta o Colab;
   sin GPU, el brazo C se corre en CPU con un modelo pequeño.

---

## 9. Fuentes primarias verificadas (para citar en el perfil)

**Vendor (primarias):**
- TypeSafe AI, *Introducing System One Models and Jev*, typesafe.ai/blog, 15-sep-2026.
- TypeSafe AI, documentación de API y primitivas (Noul/Choice/Score) y ML primer (RLCD).
- TypeSafe, dashboard de evaluaciones: evals.typesafe.ai (711 casos, 4 flujos; referencia =
  promedio de GPT-6 Astra + Fable 5.1; el propio vendor reconoce sesgo del arnés).
- BusinessWire, "TypeSafe AI Emerges From Stealth With $40M in Funding", 15-sep-2026 (DCVC).
- Vercel AI Gateway: `typesafe-ai/jev`, changelog 16-sep-2026, docs de modelos de evaluación,
  política de free tier ($5/mes) y ZDR.

**Independientes:**
- Every / Mike Taylor: 777 juicios en <0.7 s; 12 pasajes vs Claude Fable 5.1 (6/7 defectos).
- Archer Hume, *Jev's Architecture Unmasked*, 17-sep-2026 (10,000 llamadas; ECE 0.0313).
- OpenJev (TheoLeeCJ/openjev, MIT): baseline de logits congelados Qwen3.5-4B.
- Laya (`convaiinnovations/laya`): modelo System One abierto de 421M con RLCD.
- pearpages, kingy.ai, orcarouter, the-decoder, InfoWorld, The Register, SiliconANGLE,
  Forkast, TechStartups.

**Académicas:**
- Tian et al. (2023). *Just Ask for Calibration*. EMNLP. arXiv:2305.14975.
- Guo et al. (2017). *On Calibration of Modern Neural Networks*. ICML.
- Gneiting & Raftery (2007). *Strictly Proper Scoring Rules*. JASA 102(477).
- *UCCI: Calibrated Uncertainty for Cost-Optimal LLM Cascade Routing*. arXiv:2605.18796.
- *SEAR: schema-based evaluation and routing for LLM gateways*. arXiv:2603.26728.
- *Are traditional classification approaches irrelevant in this era of AI hype?* arXiv:2504.04277.
- *Small language models for front-door task classification / routing*. arXiv:2604.02367.
- *ProbeLogits*: arXiv:2604.11943. *Miscalibrated Readouts*: arXiv:2609.04582.
- *Single-Query Black-Box Calibration Auditing via Logit Bias*: arXiv:2609.05125.
- *Claim-Level Confidence Calibration*: arXiv:2608.22483.

**Datos:**
- MASSIVE 1.1 (Amazon Science, CC BY 4.0), ACL 2023: DOI 10.18653/v1/2023.acl-long.235.
- *Classification of IT Support Tickets*, Zenodo, 2022 (2,229 tickets, 7 clases).
- `alexis07/consumidor_peru` (18.5k resoluciones, español peruano) e INDECOPI Datos Abiertos.
