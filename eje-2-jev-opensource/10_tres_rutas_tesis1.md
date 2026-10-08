# Tesis 1 — eje 2 (Jev, Laya y el ecosistema de modelos de decisión): las tres rutas

Documento principal vigente · 01-oct-2026 · sustituye a `09_ruta1_cartografia_ejecutable.md` (descartado)

---

## 0. Reglas de diseño que toda ruta debe cumplir

Fijadas por el autor el 01-oct-2026. Una ruta que no las cumpla queda fuera, por buena que sea la idea.

| # | Regla | Consecuencia práctica |
|---|---|---|
| **D1** | **El resultado es un ARTEFACTO, no un hallazgo** | Los huecos de tecnologías nuevas se cierran en días. Entre el 12 y el 30-sep-2026 cayeron 5 de los 6 huecos de §5 de `FUENTES.md`. El entregable debe seguir valiendo si otro publica el descubrimiento: instrumento, dataset de mediciones crudas, especificación, tabla que se regenera con un comando |
| **D2** | **Trabajo manual del autor al mínimo** | Cero anotación, cero etiquetado humano, cero crowdsourcing, cero kappa. Solo: definir el alcance, decidir, redactar. **Queda prohibida toda ruta cuyo núcleo sea el único hueco abierto del eje 2** (ground truth humano con kappa, §5.4) |
| **D3** | **Todo lo automatizable lo hace el agente** | Descarga de pesos, corridas de inferencia, métricas, tablas, figuras, BibTeX, pre-registro |
| **D4** | **Referencias trazadas y comparaciones verificables** | Un estado del arte es tesis válida si cada cifra tiene fuente y cada fila dice si fue **medida aquí** o es **auto-reportada** |
| **D5** | **Costo $0 y RTX 4050 (6 GB)** | Nada que exija nube, créditos o GPUs de 80 GB |

**Dato que ordena todo:** en este eje, el *"cuánto"* (calibración medida) está ocupado por auditorías
pre-registradas, y el *"por qué"* (por qué RLCD no produce calibración) fue ocupado en septiembre por
arXiv:2609.38850 y la reproducción que lo deriva con el lema de Stein. **Lo que queda libre es el
instrumento**: nadie ha construido la metrología del campo, ni el banco de ablación, ni la cartografía
ejecutable del ecosistema.

---

## RUTA A — Metrología del campo `confidence`

### Resultado final
Una **especificación + implementación + arnés de conformidad** del campo `confidence` del ecosistema
tipo Jev, más la **matriz de transferencia de umbrales** medida sobre modelos de pesos abiertos.

El problema es real y está documentado: hay **cuatro definiciones incompatibles del mismo campo** y
cero estudios de transferencia entre ellas.

| Implementación | Definición de `confidence` |
|---|---|
| Jev 1.13 | `(n·p_max − 1)/(n − 1)` — concentración, **no** es la probabilidad ganadora |
| Laya | `1 − entropía normalizada` |
| `jev-lite` (medido) | `p_max` — gana a la entropía normalizada (AUROC 0.816) |
| `logit-classifier` | prior de etiqueta aprendido como media móvil |
| AnyJev | tres niveles `raw` / `L0` / `L1` |

### Entregables
1. **Especificación formal** de cada definición como función de la distribución devuelta (y de la
   cardinalidad de opciones).
2. **Librería** `jev-conf-metrics` que las implementa, con **tests de conformidad** contra salidas
   publicadas (el ecosistema ya tiene un precedente: el arnés `jev-verify` recomputa las identidades
   de confianza de Jev contra salidas de repos públicos).
3. **Matriz de transferencia de umbrales**: para cada par (definición A → definición B) y cada modelo,
   el umbral que da 80% de cobertura en A y **qué cobertura y precisión reales produce al aplicarlo
   con B**. Es la tabla que convierte "los umbrales no son comparables" en una cifra.
4. **Script que regenera la matriz** desde cero.

### Por qué sobrevive al hueco
No afirma un hallazgo: **es el instrumento con el que otros lo miden**. Quien publique "los umbrales no
transfieren" tendrá que citar la matriz, no reemplazarla. Es el patrón Guo et al. (2017) del eje de
calibración.

### Reparto de trabajo
- **Agente (automático):** descarga de los 6–8 modelos de pesos abiertos que caben en 6 GB, inferencia
  sobre datasets **ya etiquetados** (typed-decisions, kev-suites, WANLI, Banking77, MedHallu),
  cómputo de ECE/Brier/AUROC por definición, construcción de la matriz, figuras, BibTeX.
- **Autor (manual):** decidir el alcance de la especificación y redactar. **Cero etiquetado.**

### Estado del hueco (01-oct-2026)
Un estudio pre-registrado (UCLA) ya midió umbrales **dentro** de la definición de Jev (0.77–0.95 para
80% de cobertura entre datasets). Lo que **nadie** ha hecho es la **transferencia entre definiciones**.

### Costo y riesgo
Costo: **$0** · Riesgo: **bajo** · Cuello: ninguno técnico; el riesgo es de alcance (acotarlo bien).

---

## RUTA B — Réplica controlada del objetivo RLCD sobre Laya

### Resultado final
Un **harness reproducible del bucle RLCD completo** (política → ruido gaussiano de media cero en los
logits → regla de puntuación estrictamente propia → REINFORCE con baseline de grupo → ajuste de
temperatura post-hoc) sobre **Laya (ModernBERT-large 421M, Apache-2.0)**, con un **grafo de ablación
factorial** y **3 semillas**, más el **dataset de corridas crudas** (curvas de ECE, Brier y accuracy
por componente y por semilla).

Laya es la única implementación que publica el bucle completo, y su encoder es **congelable**: las
features se cachean y todo el barrido cabe en la 4050 de 6 GB.

Ejes de la ablación: σ y su annealing (1.0 → 0.3) · regla de puntuación (log con suelo −9.21 /
spherical 0.75 / RPS ordinal) · baseline de grupo vs individual · ruido en logits vs en probabilidades ·
temperatura post-hoc (una global vs una por tipo de pregunta y cardinalidad).

### Por qué sobrevive al hueco
El **"por qué" teórico ya está reclamado** (arXiv:2609.38850 + la derivación por lema de Stein:
el término RL es el gradiente de la entropía cruzada suavizada con ruido, y el suavizado vuelve la
inferencia sobre-confiada). Lo que **no existe** es el **banco de ablación con semillas y datos
crudos**: un dataset de 5 componentes × 3 semillas no lo publica nadie, y sigue siendo útil después
de cualquier paper.

### Reparto de trabajo
- **Agente:** cacheo de features, corridas de ablación, curvas, dataset, figuras.
- **Autor:** definir el grafo de ablación y redactar. **Cero etiquetado** (los datasets tienen etiquetas).

### Costo y riesgo
Costo: **$0** en dinero, **alto en horas de GPU** (muchas corridas sobre 421M con encoder congelado).
Riesgo: **alto** — es el terreno con más grupos compitiendo en el ecosistema. Se elige solo si el
objetivo de entrenamiento es lo que se quiere tocar de verdad.

---

## RUTA C — Cartografía ejecutable del ecosistema Jev-OSS

### Resultado final
Un **estado del arte** del ecosistema tipo Jev cuya tabla de comparación **se re-mide aquí**, con
pipeline propio, sobre los mismos datos públicos — y donde cada fila declara su trazabilidad.

El material es enorme y desordenado: **152 repos** en 6 días, **367 entradas** curadas, **20+ modelos
con pesos**, **2 datasets de entrenamiento abiertos**, **~30 arneses independientes**, y una advertencia
del propio índice de la comunidad: *"el volumen no es evidencia de calidad"*. Casi todos los números
publicados son **auto-reportados**.

### Entregables
1. **Corpus congelado y taxonomía** (ventana 18 → 30-sep-2026): familia, base, tamaño, licencia,
   si publica pesos, si publica receta, si publica números y con qué arnés.
2. **Tabla de comparación re-medida**: cada modelo de pesos abiertos que quepa en 6 GB, corrido sobre
   **los mismos** datasets públicos, con accuracy + Brier + ECE y **las cuatro definiciones de
   `confidence`** calculadas en paralelo.
3. **Columna de trazabilidad por fila**: `medido aquí` / `auto-reportado` / `no verificable`.
4. **Catálogo de licencias y reproducibilidad** — hoy nadie lo tiene: `nimble` y `jevlite` sin licencia,
   `openjevpro` con licencia PolyForm Noncommercial (no es open source), `kev-suites` congeladas, etc.
5. **Script de refresco** (el ecosistema crece a diario; la ventana congelada se refrezca a un comando).

### Por qué sobrevive al hueco
Nadie "se adelanta" en tu cartografía: es la referencia canónica del ecosistema, y ordenar un campo
de 6 días de edad **con código y no con prosa** es el aporte. Es exactamente la respuesta a la pregunta
del autor: un estado del arte sí es Tesis 1 cuando trae referencias trazadas y comparaciones verificables.

### Reparto de trabajo
- **Agente:** recolección y parsing del corpus, descarga de pesos, corridas, métricas, tablas, figuras, BibTeX.
- **Autor:** la taxonomía y la redacción. **Cero etiquetado.**

### Costo y riesgo
Costo: **$0** · Riesgo: **bajo** · Cuello: el ecosistema es ruidoso; se mitiga con la ventana congelada
y la columna de trazabilidad.

---

## Comparación de las tres rutas

| | **A — Metrología de `confidence`** | **B — Réplica controlada de RLCD** | **C — Cartografía del ecosistema** |
|---|---|---|---|
| Artefacto entregable | Librería + especificación + matriz de transferencia | Harness + grafo de ablación + dataset de corridas | Corpus + tabla re-medida + catálogo de licencias |
| Sobrevive al hueco | Alto (es el instrumento) | Alto en el artefacto, medio en el hallazgo | Alto (la referencia es tuya) |
| Densidad técnica / interna | **Alta** (identidades, metrología, conformidad) | **Alta** (scoring rules, REINFORCE, ablación) | Media (medición + trazabilidad) |
| Horas de GPU | Bajas | Altas | Medias |
| Trabajo manual del autor | Redacción | Redacción | Redacción |
| Riesgo de que te adelanten | **Bajo** | **Alto** | **Bajo** |
| Encaje con el Taller | Directo (teoría de la metrología) | Directo (teoría del objetivo) | Indirecto |

### Lectura recomendada

- **A** es la que mejor cumple las tres reglas a la vez: artefacto puro, cero trabajo manual, riesgo bajo,
  y densidad interna alta — que es lo que el autor valora de Ciencia de la Computación.
- **C** es la más segura y la que responde directamente a "¿un estado del arte puede ser Tesis 1?": sí,
  así. Se combina de forma natural con A (la matriz de transferencia es una columna de la tabla).
- **B** solo si el autor quiere tocar **el objetivo de entrenamiento RLCD** con sus manos; es la más
  ambiciosa y la más expuesta.

---

## Paso 0 — go/no-go común a las tres rutas (medio día)

1. Descargar **Laya** (`convaiinnovations/laya`, 421M, Apache-2.0) y **Kev-0.8B** (Apache-2.0).
2. Correr una inferencia de los tres primitivos (`choice`, `score`, `noul`) y verificar
   `output_tokens = 0`.
3. Reproducir **un** número publicado: el ECE de Laya sobre `typed-decisions` (`LocalLLaMA/typed-decisions`,
   2.000 decisiones, Apache-2.0).
4. Registrar versiones y hashes en `STATE.json`.

- Si [3] sale → la ruta elegida arranca; se puede empezar por el paso 1 del README §10.
- Si [3] falla tras 3 intentos → parar y cambiar de perspectiva (regla del autor: no ser terco).

---

## Fuentes de las tres rutas

**Referencia cerrada:** `typesafe.ai/blog/introducing-system-one-models-and-jev` · `docs.typesafe.ai/primitives/choice` ·
`langchain.com/blog/building-a-harness-with-jev` · `jev-1.13-20260917`.

**Mecánica derivada desde fuera:** `archerhume.com/posts/jevs-architecture-unmasked` (7 principios, 10.000 llamadas) ·
`navinpai.github.io/decoding-jev/` (derivación de RLCD) · `systemonemodels.org/guides/jev-architecture/` ·
`dev.to/programmerraja` (*The Logit Trick*) · `dev.to/stalwartcoder` (única medición externa de calibración de Jev).

**Modelos y pesos:** Laya `NandhaKishorM/laya` + `convaiinnovations/laya` (421M) y `laya-multilingual` (322M, 100+ idiomas) ·
Kev `jaredpalmer/kev` (0.5B→27B, 7 checkpoints, Apache-2.0) · Nimble `bespokelabsai/nimble` (9B, **sin licencia**) ·
SemIf `TheoLeeCJ/SemIf-OpenJev` (MIT) + `fastjev` · Jeff-1 (LoRA Qwen3-4B, Apache-2.0) ·
`vagmi/jev-lite` (QLoRA Gemma 4 E4B, **sin licencia**) · `frontier-infra/jebadiah-9b-v0/v1` ·
`tinyjev` (596M, corre en un M1) · `chaoliangUNSW/Jev-Style-Qwen3.5-2B` (ECE 0.017, temperatura **plegada en el
peso del RMSNorm final**) · `daseinlabs/open-jev` (MIT) · `mizorewww/laya-mlx` y `laya-coreml`.

**Datasets:** `LocalLLaMA/typed-decisions` (2.000 decisiones / 4 flujos, Apache-2.0) · `jaredpalmer/kev-suites` ·
Nimble (2.676 train + 324 retenidos) · `alisawuffles/WANLI` (CC-BY-4.0) · Banking77 · CLINC150 · MedHallu (1.000 ítems).

**Arneses:** `ASSAY-001` (pre-registrado, veredicto dividido) · `jev-ood-calibration` (900 tickets) ·
`jev-acento` (español, 3.200 ítems humanos) · `jev-verify` (recomputa las identidades de confianza) ·
`jev-orderby-bench` (inversión por pares) · `jevcal` · `DecisionBench` · `Jev Does Not Play Dice` (cara 1 en 400/400) ·
`AnyJev bench` · `jev-fanout-bench` (2.976 llamadas) · `jevals.com` (leaderboard, CC-BY-4.0) · Jeff (9.730 filas humanas).

**Cierres de septiembre (por qué el hallazgo no es la apuesta):** arXiv:2609.38850 (por qué RLCD no calibra;
identidad de varianza; receta "calibrar y luego reforzar") · reproducción independiente del término RL con el
**lema de Stein** · arXiv:2609.33209 (480 pares de negación; `s + n = 1` falla en 6.4%; las tres mono-etiqueta
suman 1.14) · arXiv:2609.26758 (sesgo nombre↔definición: flip 70.4 pp, AUC 93.8% → 23.2%) · arXiv:2609.26550
(JEV-as-a-Judge, CMU) · arXiv:2609.33843 (Laya **sub-confiada** −0.214; T=0.469 arregla ECE 0.204 → 0.037; la
regla de selección por NLL falla fuera de muestra) · estudio pre-registrado UCLA de metrología de `confidence`.
