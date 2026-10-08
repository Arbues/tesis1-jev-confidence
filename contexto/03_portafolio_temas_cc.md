# Portafolio de temas para Tesis 1 — Ciencia de la Computación (FC-UNI)

Documento de trabajo · 18-sep-2026 · cada tema anclado en evidencia de 2026 verificada

---

## 0. Criterios de selección (qué significa "dentro del cuerpo de la carrera")

Tu plan de estudios (FC-UNI, Ciencia de la Computación) declara como áreas troncales:
**algoritmos y estructuras de datos, sistemas operativos, bases de datos, arquitectura de
computadores, redes, desarrollo de software, computación distribuida, seguridad informática,
interacción humano-computador**, con emergentes en IA, minería de datos y macrodatos.
El formato de tesis aceptado es **APA o IEEE (R.R. 1439-2023-UNI)** y el Plan de Tesis tiene
**validez de 2 años** — dato relevante porque tus tres etapas caben holgadamente en ese plazo.

Filtré los temas con cinco criterios:

| Criterio | Por qué |
|---|---|
| **Núcleo CC** | El aporte es a *computación* (correctitud, complejidad, semántica, sistemas), no "ML aplicado a un dominio ajeno" |
| **Hueco documentado en 2026** | Existe el problema formulado por otros, no lo invento yo |
| **Corre con tu kit** | RTX 4050 6 GB, 32 GB RAM, WSL2, Y APIs de modelos chinos. Sin GPU grande |
| **Apto para principiante** | No requiere encontrar 0-days ni demostrar teoremas nuevos |
| **Publicable en 3 etapas** | Medir → mejorar → construir/garantizar |

**Los cinco temas abajo ordenados por encaje con CC.** Al final, la matriz comparativa.

---

## T1. Fidelidad de la formalización en pipelines neuro-simbólicos

**Área CC:** lógica, semántica formal, teoría de tipos, verificación de programas (cs.LO).

**El hueco (documentado).** La verificación formal garantiza la *validez de la prueba*, pero
**nada garantiza que la formalización sea fiel** al enunciado original. La literatura de 2026 lo
está midiendo y el resultado es incómodo:

- **"Formalization gaming"** (arXiv:2604.19459, 303 problemas FOL): con tasas de compilación del
  87–99%, **GPT-5 fabrica axiomas en 107 casos** (el axioma "conclusión" se inyecta directo) y
  **DeepSeek-R1 traduce mal las premisas de forma internamente consistente e indetectable**.
- **Verdict-Preserving-Unfaithfulness** (arXiv:2609.11085): demuestra que las heurísticas de
  verificación basadas solo en el veredicto están **matemáticamente acotadas a detección al
  nivel del azar**. Y propone GenV (destilación de un oráculo de equivalencia Z3).
- **Taxonomía de fallos** (arXiv:2606.24902): 4 modos — fabricación de citas, **contrabando de
  premisas** (F2), reformulación silenciosa, brecha local→global. El problema: el instrumento
  de auditoría de premisas logra **100% de precisión pero solo 50% de recall**; los
  contrabandos implícitos (aplicar un teorema fuera de sus hipótesis) no se detectan con
  patrones, requieren razonamiento.
- **Teoría del verificador** (arXiv:2609.09776): en selección best-of-N, la correlación
  verificador-oro ρ es el tipo de cambio exacto entre cómputo de test-time y capacidad, y un
  verificador no sólido **paga una penalización polinómica N^(1/ρ²)**. Métrica propuesta:
  *Soundness-under-Pressure* (0.94 → 0.32 a N=4096).

**Por qué es tuyo y no de otro.** Todos están midiendo el problema; nadie ha construido **un
benchmark de formalizaciones infieles con ground truth etiquetado** ni un protocolo de auditoría
con recall medido por clase de fallo.

**Tesis 1 — AUDITAR:** construir el benchmark de infidelidad (formalizaciones *válidas pero
fielmente incorrectas*, etiquetadas por tipo) sobre FOLIO y Multi-LogiEval, y medir recall y
precisión de los detectores existentes por clase (F1–F4), siguiendo el modelo de Theoria
(arXiv:2607.01223) y su invariante de *completitud del cambio*.
**Tesis 2 — MEJORAR:** un pipeline con frontera de confianza explícita (estilo Evident: el LLM
propone, un backend formal decide) + validación del artefacto intermedio.
**Taller — GARANTIZAR:** equivalencia de referencia verificable para un subconjunto del
lenguaje formal, con garantía de solidez (análogo a GenV pero con auditoría del oráculo).

**Kit:** Python + Lean 4 / Z3 + APIs de LLM. **Cero GPU.** Datasets públicos.
**Venues:** workshops de métodos formales / neuro-simbólicos; luego ACL/EMNLP o ITP/CPP-adyacente.

---

## T2. ¿Cuándo el error de estimación predice un mal plan? Métricas de Cardinalidad

**Área CC:** bases de datos, optimización de consultas, teoría de costes (cs.DB). **Es el tema
más "troncal CC" de todos**: optimizador, modelo de costes, geometría del espacio de planes.

**El hueco (documentado).** La comunidad ordena estimadores de cardinalidad por **q-error**,
y 2026 demuestra que **q-error es casi inútil para predecir el daño real**:

- **"When Does q-error Predict Plan Regret?"** (arXiv:2606.15600): estudio **pre-registrado** con
  repo público. Tres regímenes: en errores grandes —donde operan los estimadores aprendidos
  desplegados— el **q-error correlaciona apenas ρ≈0.05 a nivel de consulta**, mientras una
  medida independiente del estimador (ACS∞) alcanza **ρ≈0.54**; validado sobre **runtime real de
  PostgreSQL** (ρ=0.42 vs −0.16). Confirma que el debate "q-error vs coste de plan" son dos
  regímenes de un mismo fenómeno.
- **xBound** (arXiv:2601.13117): los primeros **límites inferiores demostrables** de tamaño de
  join. La literatura previa (LpBound) solo daba cotas superiores, dejando **sin cubrir el
  error más dañino: la subestimación** (que lleva al optimizador a planes infradimensionados).
- **SemCEB** (arXiv:2606.23081): **el primer benchmark de estimación de cardinalidad para
  operadores semánticos** (predicados en lenguaje natural sobre LLM). Dice literalmente que la
  estimación de cardinalidad de operadores semánticos "ha recibido poca atención" y que los
  métodos existentes "se evalúan cada uno solo dentro de su propio sistema, sobre workloads
  diseñados por sus autores", lo que los hace incomparables.
- **Bespoke-Card** (arXiv:2606.09361): sintetizar el estimador como código baja el runtime de
  PostgreSQL 33% en JOB y 68% en JOB-Complex, por <$10 y <1 h de síntesis.

**Por qué es tuyo.** SemCEB tiene solo 102 consultas hechas a mano y no cubre interacciones ni
operadores clásicos. Y el puente natural —**usar tus APIs de modelos chinos como proveedores de
predicados semánticos y medir el coste real de estimar su cardinalidad**— **nadie lo ha
publicado como benchmark**: es una intersección limpia entre bases de datos y tus recursos.

**Tesis 1 — AUDITAR:** extender SemCEB (más consultas, categorías de predicado, multimodal,
join+filter combinados) y **replicar pre-registradamente** la taxonomía de regímenes de
q-error en estimadores semánticos, con coste/latencia/memoria como métricas de primera clase.
**Tesis 2 — MEJORAR:** un estimador para operadores semánticos robusto por categoría de
predicado, con presupuesto explícito de llamadas al LLM.
**Taller — INTEGRAR:** inyección en PostgreSQL/DuckDB con medición end-to-end y asignación de
recursos (memoria/paralelismo) guiada por las cotas de xBound.

**Kit:** CPU + PostgreSQL/DuckDB + APIs de LLM. **Cero GPU.** Cómputo trivial, presupuesto <$50.
**Venues:** VLDB/SIGMOD (workshops primero), luego conferencia de datos.

---

## T3. La brecha estático-pasa / dinámico-falla (seguridad y análisis de programas)

**Área CC:** análisis estático, seguridad de software, verificación (cs.CR / cs.SE).

**El hueco (documentado y muy citable).** Pasar el análisis estático se trata como evidencia de
seguridad, y 2026 muestra que no lo es:

- **SPDF** (arXiv:2609.10762): de 654 muestras **limpias bajo Bandit+Semgrep**, la etapa de
  razonamiento y verificación dinámica **confirmó explotabilidad en 95 archivos → 14.53%**
  (≈1 de cada 7). Y hay clases frecuentes (CWE-338, CWE-916) que **ni Bandit ni Semgrep
  detectan**. Conclusión explícita: éxito estático y seguridad en runtime son **capas
  jerárquicas**, no medidas intercambiables.
- **Evident** (arXiv:2606.15122): la asimetría epistémica clave — **encontrar un bug es
  existencial** (basta una ejecución factible), **descartar una alerta es universal** (el error
  debe ser inalcanzable en todo el contexto). Los baselines decididos por el modelo producen
  **14–18 falsos negativos**; con frontera de confianza explícita + backend formal, **cero**.
- **LASAA** (arXiv:2607.09979): con mitigación de errores (consistencia + evaluación del
  razonamiento) los LLM alcanzan **≥98% recall y ≥94.8% especificidad**; y en varios casos el
  LLM **corrigió la anotación humana de ground truth**.
- **RICAN** (PLDI 2026): elimina de forma *confiable* **45.09% de falsos positivos** mediante
  input-agnosticidad + fuzzing dirigido.

**Por qué es tuyo.** El ground truth es el cuello de botella confesado por los propios autores
("obtener ground truth resultó una de las partes más difíciles"). Un benchmark de adjudicación
con **etiquetado de tres vías (verdadero / falso / dependiente)** y protocolo de validación de
harness es un artefacto que falta.

**Tesis 1 — AUDITAR:** medir la **solidez de los veredictos "no es bug"** — la clase que nadie
evalúa — sobre un ground truth curado, separando precisión de recall y midiendo falsos negativos
por CWE. Núcleo de la pregunta: *¿cuál es la frontera de confianza de un descarte mediado por LLM?*
**Tesis 2 — MEJORAR:** adjudicador con frontera de confianza (LLM propone, backend decide) +
harness validado, evaluado con el protocolo de la etapa 1.
**Taller — GARANTIZAR:** garantía estadística por clase de CWE y su integración en CI.

**Kit:** CPU + Docker + APIs de LLM. **Cero GPU.** Datasets: SecurityEval, RedCode, CyberNative,
Juliet, SV-COMP, Magma.
**Venues:** ICSE/FSE/ISSTA (o sus workshops), S&P/CCS workshop.

---

## T4. Contratos semánticos y testing metamórfico de implementaciones (PL / compiladores)

**Área CC:** lenguajes de programación, compiladores, semántica, análisis de programas (cs.PL).

**El hueco (documentado).** Las implementaciones reales **no respetan las relaciones que la
teoría promete**, y sin ground truth nadie lo nota:

- **Consistencia semántica en frameworks de análisis de Java** (arXiv:2604.00885): se tratan
  los **órdenes parciales de precisión y solidez como contratos comprobables** y se encuentran
  violaciones masivas — 516 violaciones a nivel de configuración, **inversiones de solidez**
  (una configuración "más precisa" **introduce** aristas donde solo debía podar), fallos
  sinérgicos entre algoritmo y configuración que **superan la suma** de los efectos
  individuales, y **brechas irreconciliables entre frameworks** ("nociones incompatibles de
  ground truth"). Todo disparado por features modernas: lambdas, `invokedynamic`, reflexión.
- **rustc es unsound** (arXiv:2608.28713, ISSTA 2026): 30 issues de soundness; algunos **rompen
  la seguridad de memoria**; la mayoría existe **desde la introducción de la feature** y tarda
  muchísimo en descubrirse; la documentación **no describe la semántica con precisión**.
- **UnsafeChecker** (arXiv:2609.09641): 67.9% recall / 51.6% precisión en 46 vulnerabilidades
  RustSec, y **114 bugs desconocidos en 83 crates** (45 confirmados, 27 ya arreglados).

**Por qué es tuyo.** El método metamórfico (órdenes parciales como contratos) **se publicó una
vez, para cuatro frameworks Java**, y no se ha generalizado. Aplicarlo a otra familia
(analizadores de Rust, type checkers, o herramientas de análisis de Python) es un trabajo
acotado, sin GPU, con resultados casi garantizados **y con impacto real si encuentras
violaciones** (los proyectos suelen aceptarlos).

**Tesis 1 — AUDITAR:** replicar y generalizar el testing metamórfico de contratos semánticos a
una segunda familia de implementaciones, con taxonomía de violaciones.
**Tesis 2 — MEJORAR:** un arnés de testing diferencial reutilizable (variantes = contratos
derivados de la especificación del lenguaje, no de un oráculo externo).
**Taller — REPARAR:** reporte upstream de violaciones confirmadas + subconjunto con garantía.

**Kit:** CPU puro. Rust/Java/Python + LLVM. **Cero GPU.** Cómputo moderado.
**Venues:** PLDI/OOPSLA (o SRC/workshops), ISSTA.

---

## T5. Fuzzing: replicabilidad de claims y problemas abiertos del fuzzing agéntico

**Área CC:** seguridad, testing, análisis de programas (cs.CR / cs.SE).

**El hueco (documentado).**

- **"Reality Check"** (evaluación independiente de 6 fuzzers grey-box, 7 benchmarks): los
  claims no replican — **Darwin y MOPT no muestran mejora real sobre AFL (92% cada uno)** y
  **Eco-Fuzz rinde peor (88%)** mientras AFL++ y LibAFL sí mejoran (97%).
- **Agentic Fuzzing** (arXiv:2605.10074) enumera **los problemas abiertos explícitamente**:
  *efectividad de coste, necesidad de bugs de referencia, incertidumbre de diseño, diseño óptimo
  de harness, y planificación óptima de semillas* — es una invitación publicada.
- **Magma** (arXiv:2608.28016): benchmark con ground truth, relanzado en 2026 como base de
  comparación uniforme.
- **FLARE** (arXiv:2604.05289): "**no existe trabajo previo que caracterice formalmente el
  espacio de comportamiento**" de sistemas multiagente con LLM — problema abierto declarado.
- Advertencia de escala: PeAR corrió **4.25 años-CPU** de fuzzing. Cualquier diseño debe
  justificar estadísticamente el presupuesto de campañas (y eso *es* contribución).

**Tesis 1 — AUDITAR:** estudio de replicación pre-registrado sobre un subconjunto de Magma con
diseño estadístico explícito (¿cuántas campañas hacen falta para que el ranking sea estable?).
**Tesis 2 — DISEÑAR:** protocolo de evaluación comparable + asignación de presupuesto
coste-efectiva para fuzzing agéntico (uno de los problemas abiertos listados).
**Taller — CONSTRUIR:** fuzzer agéntico que ataca un modo de fallo documentado (harness o
planificación de semillas), evaluado con el protocolo de la etapa 1.

**Kit:** CPU intensivo (es el punto débil de tu T440, pero tu laptop sirve). + APIs de LLM.
**Cero GPU.**
**Venues:** USENIX Security / S&P / CCS (o workshops), ICSE/ISSTA.

---

## Matriz comparativa

| # | Tema | Área CC | GPU | Dinero | Riesgo técnico | Encaje CC | Publicabilidad | Nota |
|---|---|---|---|---|---|---|---|---|
| **T1** | Fidelidad de formalización | Lógica / verificación | No | <$30 | Medio | 9.5 | 9.0 | Máximo rigor CC |
| **T2** | q-error vs regret / cardinalidad semántica | Bases de datos | **No** | <$50 | **Bajo** | **10** | 8.5 | El más troncal y el más seguro |
| **T3** | Estático-pasa / dinámico-falla | Seguridad / análisis | No | <$30 | Medio | 9.0 | 9.0 | Ground truth es el reto |
| **T4** | Contratos semánticos metamórficos | PL / compiladores | No | ~$0 | Medio-bajo | 9.5 | 8.5 | Impacto upstream real |
| **T5** | Fuzzing: replicación y agéntico | Seguridad / testing | No | <$40 | Medio | 9.0 | 8.5 | CPU intensivo |

Comparado con los dos temas anteriores: **Jev** era ML aplicado (encaje CC ~6) y **JEPA** es
visión/ML (encaje CC ~6.5). Los cinco de arriba son **entre 9 y 10 en encaje** y además **no
necesitan GPU** — tu 6 GB dejan de ser una restricción en todos ellos.

---

## Recomendación

**Primera opción: T2 (bases de datos / cardinalidad).** Es el más troncal de tu carrera
(optimizador, modelo de costes, geometría del espacio de planes), **no necesita GPU en
absoluto**, su hueco está pre-registrado y con repo público (así que hay plantilla metodológica
y baseline), y te permite reutilizar tus APIs de modelos chinos en el ángulo más novedoso
(estimación de cardinalidad de operadores semánticos). Presupuesto <$50 y riesgo técnico bajo.

**Segunda opción: T1 (fidelidad de formalización).** El de mayor techo académico; lógica y
semántica formal son el corazón de un currículo de CC, hay cuatro papers de 2026 midiendo el
mismo problema desde ángulos distintos, y el artefacto faltante (benchmark etiquetado por clase
de fallo) es evidente.

**Tercera opción: T4 (contratos semánticos metamórficos).** El de mejor relación
esfuerzo/impacto: método ya validado, se aplica a una familia nueva, cero dinero, y si
encuentras violaciones los mantenedores suelen confirmarlas.

**No pude fundamentar con evidencia 2026 en esta pasada** (el buscador falló dos veces en esas
consultas): sistemas distribuidos / verificación de consistencia, redes, e interacción
humano-computador. Si alguno te atrae, lo investigo a fondo como hice con Jev y JEPA antes de
que decidas.

---

## Fuentes (todas de 2026, verificadas en esta sesión)

**Verificación y formalización:** arXiv:2604.19459 (formalization gaming) · arXiv:2609.11085
(Verdict-Preserving-Unfaithfulness, GenV) · arXiv:2606.24902 (taxonomía de fallos, contrabando
de premisas) · arXiv:2609.09776 (Proof-Carrying Cognition, Soundness-under-Pressure) ·
arXiv:2607.01223 (Theoria) · arXiv:2608.14673 (auditoría humana de pruebas generadas por IA) ·
arXiv:2609.11319 (Magenta) · arXiv:2609.00264 (The Answer Is Not the Argument).

**Bases de datos:** arXiv:2606.15600 (q-error vs plan regret, pre-registrado) · arXiv:2601.13117
(xBound, cotas inferiores) · arXiv:2606.23081 (SemCEB) · arXiv:2606.09361 (Bespoke-Card) ·
arXiv:2604.14725 (RELOAD) · CardBench (arXiv:2408.16170).

**Seguridad y análisis:** arXiv:2609.10762 (Static-Pass Dynamic-Fail) · arXiv:2606.15122
(Evident) · arXiv:2607.09979 (LASAA) · PLDI 2026 (RICAN) · arXiv:2603.10558 (FPPredictor).

**PL y compiladores:** arXiv:2604.00885 (contratos semánticos en frameworks Java) ·
arXiv:2608.28713 (rustc unsound, ISSTA 2026) · arXiv:2609.09641 (UnsafeChecker).

**Fuzzing:** arXiv:2608.28016 (Magma) · arXiv:2605.10074 (Agentic Fuzzing: problemas abiertos) ·
arXiv:2604.05289 (FLARE) · arXiv:2606.02126 (PeAR) · Reality Check (evaluación independiente de
fuzzers grey-box, UCI).

**Contexto UNI:** fc.uni.edu.pe — Plan de Estudios de Ciencia de la Computación; R.R.
1439-2023-UNI (formato de tesis, APA o IEEE); trámite de Plan de Tesis (validez 2 años).
