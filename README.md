# README — Estado del proyecto de tesis (punto de entrada)

> **Si eres un agente que acaba de abrir esta carpeta: lee este archivo completo antes de actuar.**
> Contiene el contexto acumulado, las decisiones tomadas y sus razones. Última actualización: **25-oct-2026**.
>
> **Sesión nueva:** `.hermes.md` es el contexto de proyecto que Hermes auto-carga al arrancar, y `STATE.json`
> es el punto de reentrada. Los dos son de lectura obligatoria antes de proponer o cambiar nada.

---

> ## ✅ RUTA ELEGIDA (04-oct-2026): **RUTA 1 — Metrología y transferencia del campo `confidence`**
>
> **Tema:** el ecosistema open-source de modelos de decisión tipo **Jev** (RLCD), con **Laya** como
> implementación de referencia.
> **Documento principal vigente:** **`eje-2-jev-opensource/11_ruta1_metrologia_confidence.md`**.
>
> **Artefacto:** especificación formal + librería `jev-conf-metrics` + arnés de conformidad + **matriz de
> transferencia de umbrales** entre las definiciones incompatibles de `confidence`, medida sobre modelos de
> pesos abiertos, con dataset de mediciones crudas y script regenerador.
>
> **Por qué esta y no las otras dos:** un sondeo en vivo (04-oct-2026) mostró que la antigua ruta B (réplica
> de RLCD) quedó casi ocupada por `LakoreAI/sev` y la antigua ruta C (cartografía) por `arXiv:2609.30216`
> (*Jev in the Wild*). La metrología sigue libre como **tabla sistemática**.
> **Equipos:** Mac Mini + RTX 4050 (6 GB). El servidor `thinkpad-t440` no tiene GPU (solo orquesta).

---

## 1. Qué es esta carpeta

Carpeta de trabajo para elegir y desarrollar el tema de **Tesis 1** de Arbués Enrique Pérez V.,
estudiante de **Ciencia de la Computación (FC-UNI, Perú)**. Es el primero de tres trabajos encadenados,
cada uno publicable:

| Etapa | Curso | Aporte | Tipo |
|---|---|---|---|
| **Tesis 1** | curso de tesis 1 | El instrumento + la caracterización empírica | Medición |
| **Tesis 2** | curso de tesis 2 | El mecanismo (objetivo que induzca calibración) | Algorítmica |
| **Taller** | taller de tesis (último) | **Las bases matemáticas** (condiciones + demostración) | **Teórica** |

**Restricción de forma:** la norma admite **APA o IEEE** (R.R. 1439-2023-UNI); para este trabajo **se elige
IEEE** (fijado el 10-oct-2026). El Plan de Tesis tiene validez de 2 años.

---

## 2. ⚡ Estado en una línea

**Tema: modelos de decisión tipo Jev (RLCD) — eje 2, confirmado 01-oct-2026.** Tesis 1 = **Ruta 1**, elegida
bajo tres reglas: el resultado es un **artefacto** (no un hallazgo), el trabajo manual del autor es **mínimo**
y lo automatizable **máximo**, y las referencias/comparaciones son **trazables**. El Taller convertirá esa
evidencia en teoría del objetivo RLCD.

**Título definitivo (fijado el 10-oct-2026):**
> *Metrología y transferencia del campo `confidence` en modelos de decisión de pesos abiertos tipo Jev*
> *Metrology and Threshold Transfer of the `confidence` Field in Open-Weight Jev-Type Decision Models*

**Regla de estilo:** sin dos puntos, sin subtítulo, sin signos de interrogación. Frase nominal que declara
propiedad + objeto + alcance + tipo de método. **El título quedó fijado al cerrar la especificación.**

---

## 3. Índice de archivos

| Archivo | Qué contiene | Estado |
|---|---|---|
| `README.md` | **este archivo** — punto de entrada y estado consolidado | vigente |
| `STATE.json` | El mismo estado en formato máquina-legible para agentes | vigente |
| `.hermes.md` | Contexto de proyecto que Hermes auto-carga al arrancar | vigente |
| **`paper/`** | **EL PAPER**: `00_plan_del_paper.md` (plan, claim, riesgos y correcciones), `01_marco_teorico.md` (marco teórico base), `02_referencias.bib`, `03_especificacion_confidence.md` (especificación formal), `04_pre_registro.md`, `secciones/` (borradores §1–§7), **`ieee/`** (versión IEEE en LaTeX: `main.tex` + `secciones/`; se compila con `compilar.sh`), **`figures/`** (las 8 figuras del paper) | **vigente** |
| `docs/libreria.md` | **API de la librería** `jev-conf-metrics`: definiciones, métricas, transferencia y puntos de extensión | vigente |
| `docs/validacion-productos.md` | **Cómo validar los productos**, comando por comando (guía para el autor) | vigente |
| **`eje-2-jev-opensource/11_ruta1_metrologia_confidence.md`** | **DOCUMENTO PRINCIPAL VIGENTE**: la Ruta 1 (artefacto, diseño de medición, marco teórico, paso 0, plan) | **vigente** |
| `eje-2-jev-opensource/10_tres_rutas_tesis1.md` | Registro de las tres rutas entre las que se eligió | registro |
| `eje-2-jev-opensource/FUENTES.md` | Inventario de las 49 fuentes del eje, verificadas con API | lectura obligatoria |
| `eje-2-jev-opensource/08_estudio_ecosistema.md` | Estudio de campo: 20+ modelos con pesos, taxonomía por rigor, tabla de calibración, huecos | vigente |
| `audit/saturacion/` | Los 3 informes de saturación (ZO, modelo-vs-harness, agent skills) | ver §7 |
| **`results/`** | **ARTEFACTOS de medición**: `raw/` (paso 0), `crudos/` (65.185 mediciones confirmatorias, con `row_hash`), `matrix/` (la matriz sellada, CSV + figuras + `RESUMEN_MATRIZ.md`) y `paso0_informe.md` | **vigente** |
| `results/pagado/` | **Brazo pagado**: 5 `.jsonl` + metas de la API real (14.277 decisiones). Nunca se mezclan con `crudos/` | **vigente** |
| `results/matrix_pagado/` | Matriz **combinada** (5 modelos locales + Jev): 2.880 celdas + `RESUMEN_MATRIZ_PAGADO.md` | **vigente** |
| `results/matrix/EXTENSION_CONF_SCORE.md` | La **5.ª definición** (`conf_score`, MAD_unif) medida sobre `sst5` + su CSV | **vigente** |
| `src/matriz/extension_conf_score.py` · `correr_pagado.sh` · `correr_matriz_pagado.sh` · `correr_matriz_paralela.sh` · `fusionar_matriz_paralela.py` | Extensión declarada, corrida del brazo pagado y matriz combinada (serie y paralela) | **vigente** |
| `docs/plan-visibilidad.md` | Plan de visibilidad: diagnóstico de las 5 puertas + 4 decisiones del autor | **vigente** |
| `paper/02_referencias_pendientes.md` | Verificaciones D4 (cerradas) + **estándar único de citas** + nota de Roby | **vigente** |
| `contexto/` | Investigación previa (veredicto de Jev/TypeSafe y costos); su §3.1 lo corrige `notes/pago-jev-api-costos-2026-10-12.md` | contexto |
| `src/figuras_paper.py` | Genera las 8 figuras del paper desde los artefactos medidos | vigente |
| `pyproject.toml`, `.github/workflows/tests.yml` | Empaquetado de la librería (`pip install -e .`) y CI: 67 tests en cada `push` | vigente |
| `eje-1-jepa/`, `_descartado/` | **Eliminados del repo el 13-oct-2026** (eje descartado, fuera de alcance). Solo viven en el historial de git | eliminado |

### 3-bis. Estructura de trabajo y regla de orden

El repo tiene un **árbol de trabajo** para ir llenando poco a poco, sin ser rígido:

```
paper/      EL PAPER (00_plan, 01_marco_teorico, 02_referencias.bib, secciones/ §1-§7, ieee/ versión IEEE, figures/, tables/)
src/        CÓDIGO (librería jev-conf-metrics, pipeline) — se trabaja en el Acer Nitro
results/    ARTEFACTOS de medición (raw/ = mediciones crudas, matrix/ = matriz de transferencia)
data/       Datasets descargados (los pesados NO se versionan)
notes/      Apuntes, borradores y lluvia de ideas (aquí sí, suelto está bien)
docs/       Guías (libreria.md, validacion-productos.md, erratas, contrato de la API, guía de cierre, releases)
.github/    CI: los 67 tests en cada push/PR
```

**Regla de orden (para que nada quede suelto en la raíz):** la **raíz** es solo para los archivos de
entrada (`README.md`, `STATE.json`, `.hermes.md`, `AGENTS.md`, `.gitignore`, `LICENSE`, `LICENSE-docs`,
`CITATION.cff`) y las carpetas. Todo lo nuevo
va a su carpeta → código a `src/`, resultados a `results/`, texto a `paper/`, ideas a `notes/`, datos a
`data/`. Si dudas, crea una subcarpeta con nombre claro **dentro** de la que corresponda, no en la raíz.

> **Visibilidad:** repositorio **público** desde el 10-oct-2026. Licencias: **Apache-2.0** el código
> (`LICENSE`), **CC-BY-4.0** el paper y la documentación (`LICENSE-docs`); cita en `CITATION.cff`.

---

## 4. El tema: Jev, Laya y el ecosistema de modelos de decisión (eje 2)

**La referencia cerrada — Jev (TypeSafe System One, `jev-1.13.0`, 18-sep-2026).** Modelo de **decisión**,
no de lenguaje: termina la inferencia con un *readout* de los logits en la posición de cada etiqueta y
aplica softmax **solo sobre las etiquetas permitidas**, así que `output_tokens = 0` por construcción. Tres
primitivos: `choice` (≤255 opciones), `score` (2–10 niveles) y `noul` (booleano, **sin** campo `confidence`).
Estado compartido y preguntas aisladas → **no hay distribución conjunta** (una pregunta y su negación pueden
devolver 0.7 ambas). `confidence` **no es** la probabilidad ganadora: es concentración, `(n·p_max − 1)/(n − 1)`.
TypeSafe **no ha publicado un solo ECE, ni la pérdida, ni los pesos**.

**La implementación de referencia — Laya** (`NandhaKishorM/laya`, Apache-2.0, **421M** = ModernBERT-large
+ cabeza que puntúa un token `[MASK]` colocado en la opción). Es la única que publica el bucle **RLCD**
completo. **Encoder congelable → features cacheadas → todo el barrido cabe en la RTX 4050.** Su `confidence`
es `1 − entropía normalizada` (choice/score) — **no la fórmula de Jev**.

**RLCD** = ruido gaussiano de media cero en los logits (σ 1.0 → 0.3) + regla de puntuación
**estrictamente propia** (log con suelo −9.21 + 0.75·spherical; RPS para el `score` ordinal) + REINFORCE
con baseline de grupo + temperatura post-hoc. En teoría reportar honestamente es la única estrategia
óptima; en la práctica ningún proyecto lo logró.

**El dato central:** el ecosistema abierto **refutó empíricamente la premisa de Jev**. Donde hay
calibración, vino de un **ajuste de temperatura post-hoc sobre datos propios**, no del objetivo de
entrenamiento. Y hay **varias definiciones incompatibles** del campo `confidence` (Jev, Laya entropía, Laya
`noul`, `answer_confidence` = p_max, `act_probability`, prior aprendido) con **cero estudios de transferencia
de umbrales entre ellas** → **ese es el objeto de la Ruta 1.**

---

## 5. La Ruta 1 en una tabla

| | Detalle |
|---|---|
| **Problema** | El mismo campo `confidence` significa cosas distintas según el modelo, y un umbral calibrado sobre una definición no significa nada sobre otra, pero el ecosistema los porta como si fueran intercambiables |
| **Artefacto final** | Especificación formal + librería `jev-conf-metrics` (con tests de conformidad) + **matriz de transferencia de umbrales** (definición × definición × modelo × dataset) + dataset de mediciones crudas + script regenerador |
| **Por qué sobrevive** | Es el **instrumento**, no el hallazgo: quien afirme que los umbrales no transfieren tendrá que citar la matriz |
| **Agente (automático)** | descarga de pesos, inferencia, cálculo de todas las definiciones, ECE/Brier/AUROC, la matriz, bootstrap + FDR, figuras, BibTeX, pre-registro, la librería |
| **Autor (manual)** | definir el alcance (qué definiciones entran, qué cobertura) y **redactar**. **Cero etiquetado** |
| **Costo / riesgo** | **$0** · riesgo **bajo** |
| **Documento** | `eje-2-jev-opensource/11_ruta1_metrologia_confidence.md` |

---

## 6. La cadena de decisiones (qué se evaluó y por qué)

| Candidato | Veredicto | Razón |
|---|---|---|
| **Jev / TypeSafe "System One"** | ✅ **eje elegido** | La premisa vieja ("no es open source") murió: 20+ modelos con pesos en días |
| **Ruta 1 — Metrología de `confidence`** | ✅ **ELEGIDA (04-oct-2026)** | Artefacto puro, cero trabajo manual, riesgo bajo, densidad interna alta |
| **Ruta B — Réplica controlada de RLCD** | ❌ descartada | Casi ocupada por `LakoreAI/sev` (26-sep: ablación completa, 30 corridas, checkpoints) |
| **Ruta C — Cartografía del ecosistema** | ❌ descartada | Casi ocupada por `arXiv:2609.30216` (*Jev in the Wild*, 2.170 proyectos) |
| **Eje 1 (JEPA/LeWM)** | ❌ descartado | **Instrucción expresa del autor.** Fuera de alcance; el material se eliminó del repo el 13-oct-2026 |
| **T-B modelo vs harness** | ❌ descartado | Versión ingenua redundante (243 papers); es comparación, no núcleo de CC |
| **T-C seguridad de agent skills** | ❌ descartado | 8/10 saturado (el más saturado de los tres) |
| **T-A orden cero (ZO)** | 🔶 alternativa | 6/10; abierto solo en A1/A3/A4 |

> **Corrección de perspectiva del usuario (vigente):** valora el aporte **interno** (matemática, mecanismos,
> código). **Actualización 04-oct-2026:** ese aporte puede vivir en el **marco teórico** sin ser el núcleo del
> resultado — por eso Tesis 1 puede ser metrología/instrumento.

---

## 7. Auditorías de saturación (`audit/`)

Ejecutadas con subagentes el 19-sep-2026:

| Informe | Veredicto | Hallazgo clave |
|---|---|---|
| `audit/saturacion/auditoria_saturacion_zo.md` | **6/10** | Crecimiento 1.96× sobre 2025. Abierto: A1/A3/A4 |
| `audit/saturacion/auditoria_saturacion_modelo_vs_harness.md` | **6/10** | La pregunta ya está contestada y replicada (HV=18.48 vs MV=2.37 pp²) |
| `audit/saturacion/informe_saturacion_agent_skills.md` | **8/10** | Ningún escáner supera el baseline "marcar todo" |

Los dumps y scripts de esas auditorías (arXiv/OpenAlex, ~3 MB) se eliminaron del repo el 13-oct-2026: son recuperables y no sostienen ninguna cifra del paper.

---

## 8. Auditoría de huecos (por qué el resultado es un artefacto)

Verificado en vivo el 01-oct-2026 (ampliado el 04-oct-2026). **Las filas de eje 2 (Jev/Laya) son las que importan.**

| Hueco | Quién lo ocupó | Veredicto |
|---|---|---|
| Por qué RLCD no produce calibración | `arXiv:2609.38850` + reproducción con el lema de Stein | cerrado |
| Ablación controlada de RLCD (CE vs RL, σ, recompensa) | **`LakoreAI/sev`** (26-sep-2026): 30 corridas, código, checkpoints | cerrado |
| Coherencia / negación / axiomas | `arXiv:2609.33209` | cerrado |
| Sesgo de posición / etiqueta | `arXiv:2609.26758` + `arXiv:2609.26550` | cerrado |
| Cartografía del ecosistema | **`arXiv:2609.30216`** (*Jev in the Wild*) + awesomejev.com | cerrado |
| Metrología de `confidence` **dentro** de una definición | estudio pre-registrado UCLA (0.77–0.95 para 80 % de cobertura) | cerrado |
| Calibración de Laya | `arXiv:2609.33843` (checkpoint tal cual: sub-confianza 0.214; T=0.469 → 0.037) | cerrado |
| **Transferencia de umbrales ENTRE definiciones** | **nadie** | **ABIERTO → objeto de la Ruta 1** |
| Ground truth humano con kappa | **nadie** | abierto, pero **excluido por D2** (anotación manual) |

**Conclusión:** el "*cuánto*" y el "*por qué*" están ocupados. **Lo que queda libre es el instrumento de
metrología.** De ahí D1 y la Ruta 1.

---

## 9. Convenciones y preferencias del usuario (respetar siempre)

- **Idioma:** español. En el chat, **corto**; si no entiende, reformular en lenguaje llano. Los `.md` entregados, detallados.
- **Formato:** respuestas con **tablas y pasos**; aprende mejor con **diagramas de arquitectura**.
- **Formato de tesis:** **IEEE** (la norma R.R. 1439-2023-UNI admite APA o IEEE).
- **Aporte interno** (matemática, mecanismos, código) valorado; puede vivir en el marco teórico.
- **Git (este proyecto):** **todo directo a `main`, sin ramas ni PR** (instrucción del autor, 10-oct-2026).
  En los demás repos: rama separada → PR → squash merge.
- **Seguridad:** cero contraseñas o secrets en `.env` ni en repos; en docs, solo placeholders.
- **Docker en el servidor:** `restart: always`.
- **Si un enfoque falla 3 veces: parar y cambiar de perspectiva.**
- **Hardware:** **Mac Mini** (Apple Silicon) + **Acer Nitro, RTX 4050 Laptop 6 GB**. Servidor `thinkpad-t440` **sin GPU**.

---

## 10. Plan original (04-oct-2026) y su estado

Los nueve pasos del plan quedaron así: **pasos 0–7 ✅** (ruta elegida, paso 0 go/no-go, alcance congelado,
especificación formal, librería con tests, pipeline, matriz + dataset crudo, pre-registro con DOI) · **paso 8 ✅**
(título definitivo fijado el 10-oct) · **paso 9** (estudio del objetivo RLCD) queda como material de **Tesis 2 /
Taller**. El estado vigente y lo que falta están en §10-bis y en `STATE.json` → `pendientes`.

### 10-bis. Estado del cierre (13-oct-2026)

**La Tesis 1 está construida, medida y reservada.** No queda cómputo pendiente de la medición. Punto de
reentrada: `STATE.json` → `README.md` → `docs/guia-cierre-pendientes.md` (flujo completo por fases).

**Reserva con DOI** (verificada contra la API pública de Zenodo):

| Producto | DOI / identificador | Notas |
|---|---|---|
| Pre-registro del método | `10.5281/zenodo.23266795` (concepto `…23266794`) | Publicado el 09-oct-2026; el archivo depositado es la revisión previa (el método es idéntico) |
| **Instrumento (software)** | **`10.5281/zenodo.23330647`** v1.0.1 (concepto `…23328988`; histórica v1.0.0 `…23328989`) | Se publica automáticamente desde el Release de GitHub. La v1.0.1 corrige las referencias que el snapshot v1.0.0 archivaba mal |
| Preprint del paper | `10.5281/zenodo.23329431` (concepto `…23329430`) | PDF depositado de 11 páginas, CC-BY-4.0, en español; el PDF **vigente** del repo tiene 12 porque el 25-oct se le integró §5.8 (extensiones) |
| Archivo independiente | SWHID `swh:1:rev:39a685679905b7445b1a455d812b416f1acb9ef0` | Software Heritage |
| ORCID | 3 works | verificado en la API pública de ORCID |

**Hecho en la sesión del 12–13 oct-2026:** Release `v1.0.0` y `v1.0.1` → depósitos automáticos en Zenodo ·
archivo completo en Software Heritage · preprint depositado · 3 works en ORCID · `CITATION.cff` con 6
identificadores (validado contra el esquema oficial: 0 errores) · las **9 referencias pendientes resueltas** (se
corrigieron títulos y autores inventados en el `.bib`) · **erratas E4, E5 y E6** · **adaptador del brazo pagado**
(`src/matriz/backend_typesafe.py`, 15 tests sin red → 52 en total; medido USD 0.018 por 1.000 decisiones) ·
contrato de la API de TypeSafe verificado en vivo.

**Lo que falta** — detalle y sub-pasos en `docs/guia-cierre-pendientes.md` y en `STATE.json` → `pendientes`:

| ✋ Autor | 🤖 Agente |
|---|---|
| Leer §1–§7 y decidir si el PDF IEEE lo representa (es lo último que cierra la Tesis 1) — **en curso**; el PDF ya integra las extensiones, así que es la versión definitiva | **Nada de medición ni de redacción pendiente**: brazo pagado cerrado (14.277 decisiones, USD 0.79) y parte B hecha (§5.8). Queda la decisión del framework (ver §10-ter) y PyPI/CLI si la apruebas |
| arXiv: hace falta **endosso personal** (0 papers en arXiv) | — |
| (Opcional, cosmético) cerrar el grafo de relaciones en Zenodo | Visibilidad (N3) y paper en inglés (N5) — el inglés queda **bloqueado hasta que apruebes §1–§7** |

**Cerrado el 19–20-oct-2026:** las **dos** decisiones de referencias (se añadieron `roby1965` y `jose2009`, con DOI
verificado en Crossref, y se fijó un **estándar único de citas** para todo el `.bib`) · la definición
**`conf_score` (MAD_unif)** entró como **extensión declarada** (11 tests nuevos, `results/matrix/EXTENSION_CONF_SCORE.md`)
· los conteos de tests corregidos de 37 a **63** en la documentación viva · smoke test del brazo pagado verificado
contra la API real.

**Cerrado el 25-oct-2026 (parte B):** las dos extensiones entraron al paper como **subsección declarada §5.8**
(quinta definición `conf_score` y brazo pagado con la tabla por modelo y la causa medida de los empates de umbral),
§1 y §7 dicen ya **67 tests**, §7 gana las filas 10 y 11 de artefactos, y el PDF recompiló a **12 páginas**
(36 ítems, 0 citas sin resolver, 0 overfull). Además se corrigió un error de `STATE.json`: el brazo pagado no tiene
el |Δ| directo más bajo (0.1735, segundo) — el más bajo es `laya/multilingual` (0.1315); el |Δ| con mapa de Jev
(0.0130) sí es 4.6–9.3× el de los checkpoints abiertos, y la causa está medida (rejilla de 0.01 → 2.5 % de ítems
empatados en el umbral frente a 0.1 % en los abiertos).

Guías: `docs/guia-cierre-pendientes.md` (flujo por fases) · `notes/zenodo-publicar-guia-literal.md` (la interfaz
real de Zenodo, con etiquetas literales) · `docs/release-v1.0.1.md` (qué cambia y por qué).

### 10-ter. Dónde vive el framework — propuesta (19-oct-2026, pendiente de tu OK)

**Pregunta que planteó el autor:** ¿el framework de comparación va a un repo nuevo (`decision-calibration-bench`)
y aquí queda el paper, o al revés? ¿O no hace falta?

**Hecho que manda:** el DOI del instrumento (`10.5281/zenodo.23330647`, concepto `…23328988`) es un snapshot de
**este** repo. Zenodo publica solo desde Releases de GitHub: la versión nueva del framework sale **aquí**, como
`v1.1.0`, y hereda el **mismo DOI de concepto**. Mover el código a otro repo obliga a emitir un DOI nuevo y a que
el paper cite dos artefactos.

**Recomendación: no crear un repo nuevo.** Lo que falta no es separar, es **distribuir**:

| Bloqueador real | Solución en ESTE repo | Coste |
|---|---|---|
| No hay CLI | `cli.py` + `[project.scripts] jevconf` (`list-brazos · medir · matriz · informe · figuras`) | 1 sesión |
| `medir` exige GPU/red | backend simulado determinista por semilla (`--mock`) | incluido |
| El pipeline no está empaquetado | mover `medir/matriz/informe` dentro del paquete | incluido |
| `datasets` no declarado | extra opcional `[datasets]` + fixtures locales para los tests | incluido |
| Nadie lo encuentra | publicar en **PyPI** (`pip install jev-conf-metrics`) + README en inglés + topics | 30 min |
| Sin versión citable nueva | `v1.1.0` → DOI nuevo bajo el MISMO concepto, sin tocar el v1.0.1 | 5 min |

**Por qué no una librería conocida:** no existe un proyecto upstream equivalente (no hay «scikit-learn» de
metrología de `confidence` en modelos de decisión). El canal de distribución correcto es **PyPI + el DOI**, no
fusionarse en otro repo.

**Si algún día el repo estorba:** se separa `paper/` + `docs/` a `tesis1-paper` y el código se queda aquí. Al revés
es peor: rompe el DOI, los enlaces del preprint y las rutas de `README`/`STATE`.

### 10-quater. Brazo pagado — medido (20-oct-2026, t440 sin GPU)

El API real de TypeSafe (`jev-1.13.0`) sobre los 5 datasets: **14.277 decisiones**, ~**USD 0.79**.
Crudos en `results/pagado/` (nunca mezclados con `results/crudos/`), matriz combinada en `results/matrix_pagado/`.

| dataset | n | accuracy |
|---|---|---|
| clinc150 | 3.100 | 0.901 |
| banking77 | 3.076 | 0.796 |
| wanli | 5.000 | 0.754 |
| typed-decisions | 2.000 | 0.733 |
| sst5 | 1.101 | 0.541 |

**El titular nuevo** (nivel `raw`, 2.880 celdas, 6 modelos = 5 locales + Jev):

| modelo | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|
| **typesafe-ai/jev** | **0.1307** | 0.0130 | **10×** |
| laya | 0.2233 | 0.0028 | 79× |
| laya/multilingual | 0.1316 | 0.0018 | 75× |
| laya/typed-decisions | 0.2381 | 0.0014 | 165× |
| kev-0.8b | 0.2499 | 0.0022 | 114× |
| Qwen3.5 crudo (control) | 0.3635 | 0.0517 | 7× |

Jev tiene el error **directo** más bajo de todos pero el error **con mapa** 6–9× peor que los pesos
abiertos: la **rejilla de 0.01** multiplica los empates de umbral y degrada el mapa. La rejilla se declara
siempre; no se mezcla con los brazos de pesos abiertos.

**Verificación de E5 en vivo:** en filas `score` la confianza del API coincide con `conf_score` (máx 0.0050,
100 % de 800 filas); en `choice`, con `conf_jev` (600 filas). Cada primitiva usa una fórmula distinta, medido
contra el servicio.

**Rendimiento (medido, no estimado):** el costo de la matriz lo domina el prior del debiasing `L0`
(~44 min por grupo con 77 clases). Por eso la matriz combinada corre en `raw`+`L1`. La paralelización por
grupos existe (`correr_matriz_paralela.sh`) pero rinde **1.11×** en el t440 (2 núcleos físicos): se deja
documentada, no como camino por defecto.

---

## 11. Glosario mínimo

| Término | Significado |
|---|---|
| **Jev** | TypeSafe System One — modelo de decisión con *readout* de logits; **no genera texto**. **NADA que ver con JEPA** |
| **choice / score / noul** | los tres primitivos de Jev (elección / ordinal / booleano) |
| **RLCD** | Reinforcement Learning for Calibrated Decisions — ruido en logits + regla propia + REINFORCE con baseline + temperatura post-hoc |
| **regla estrictamente propia** | regla de puntuación cuyo óptimo es reportar la probabilidad verdadera (log, spherical, RPS) |
| **`confidence`** | campo con **definiciones incompatibles**: Jev `(n·p_max−1)/(n−1)`; Laya `1−entropía normalizada`; `p_max`; prior aprendido… |
| **transferencia de umbral** | aplicar a la definición B el umbral calibrado en A; cuánto se degradan cobertura y precisión |
| **ECE / Brier** | Expected Calibration Error / puntuación de Brier |
| **cobertura** | fracción de casos que el modelo decide responder; su compañera es *accuracy on answered* |
| **kappa** | acuerdo inter-anotador; **no existe** en este ecosistema (excluido por D2) |
| **CC** | Ciencia de la Computación (la carrera) |
| **typed-decisions** | `LocalLLaMA/typed-decisions`, el benchmark compartido (2.000 decisiones, Apache-2.0) |

---

## 12. Fuentes principales (eje 2)

**El objeto:** `docs.typesafe.ai/primitives/choice` · `typesafe.ai/blog/introducing-system-one-models-and-jev` ·
`archerhume.com/posts/jevs-architecture-unmasked` · `navinpai.github.io/decoding-jev/` · `note.com/wayne_chang`.

**Modelos y pesos:** `github.com/NandhaKishorM/laya` + `convaiinnovations/laya` (421M) · `jaredpalmer/kev` (+ kev-0.8b) ·
`bespokelabsai/nimble` · `TheoLeeCJ/SemIf-OpenJev` · `GestaltLabs/Jeff-1` · `vagmi/jev-lite` · `frontier-infra/jebadiah-9b-v0/v1` ·
AnyJev (Nokia) · `open-decision-ai`.

**Metrología (marco teórico):** Guo et al. 2017 (calibración) · Gneiting & Raftery 2007 (reglas propias) ·
Naeini et al. 2015 (ECE) · Chow 1970 / Geifman & El-Yaniv 2017 (predicción selectiva) · Angelopoulos & Bates 2021 (conformal) ·
`laya.studio/glossary/entropy-based-confidence` · rohitghumare.com (fórmula de Jev medida).

**Datasets:** `LocalLLaMA/typed-decisions` · `jaredpalmer/kev-suites` · `alisawuffles/WANLI` · Banking77 · CLINC150 · MedHallu.

**Cierres de septiembre (por qué el resultado es un artefacto):** arXiv:2609.38850 · `LakoreAI/sev` (RLCD) ·
arXiv:2609.33209 · arXiv:2609.26758 · arXiv:2609.26550 · arXiv:2609.33843 (Laya) · arXiv:2609.30216 (*Jev in the Wild*).

---

## 13. Paso 0 — resultado (08-oct-2026, Acer Nitro)

**GO.** Los tres criterios del paso 0 se cumplen y, de paso, el objeto de la Ruta 1 ya se ve en los datos.
Informe completo: **`results/paso0_informe.md`** (se regenera con `python src/paso0_informe.py`).

| criterio del paso 0 | resultado |
|---|---|
| Correr los tres primitivos en pesos abiertos | ✅ Laya (3 checkpoints) + Kev-0.8B sobre las **2.000 decisiones** de `typed-decisions` (split `test`, 400 casos) |
| Verificar `output_tokens = 0` | ✅ en Laya, todas las filas · **Kev reporta ese campo con otro significado** (recuento de tokens de la respuesta serializada: 869.310 en total) |
| Reproducir un número publicado | ✅ **las 5 métricas** del README de Laya, con **\|Δ\| ≤ 0.003** en `laya-typed-decisions` (ECE 0.213→**0.2157**, accuracy 0.766→**0.7685**, Brier 0.062→**0.0615**, soft acc 0.471→**0.4707**, score MAE 0.242→**0.2424**) |

**Lo que ya se ve, y es el objeto de la tesis:** la misma corrida, las mismas 2.000 decisiones, el mismo
modelo — el ECE cambia según la definición de `confidence`:

| checkpoint | `p_max` | Jev `(n·p−1)/(n−1)` | entropía `1−H/log k` | margen |
|---|---|---|---|---|
| `laya-typed-decisions` | **0.216** | 0.426 | **0.577** | 0.511 |
| `laya` (english) | 0.177 | 0.166 | 0.230 | 0.194 |
| `laya-multilingual` | 0.318 | 0.255 | 0.212 | 0.244 |
| `kev-0.8b` | **0.061** | 0.228 | 0.363 | 0.274 |

Factor **2,7×** entre la definición más benévola y la más severa sobre el mismo dato.

**Dos hallazgos de metrología que salen del código, no de un blog** (D4):

1. **La `choice_confidence` de Kev ES la fórmula de Jev.** `(p_max − 1/K)/(1 − 1/K) ≡ (K·p_max − 1)/(K − 1)`,
   verificado numéricamente. Estaban registradas como definiciones distintas → por la Proposición 1, **ese par
   transfiere el umbral de forma exacta**.
2. **El mismo campo `output_tokens` tiene tres significados**: Jev y Laya = 0 (no hay generación); Kev =
   *«billing-style figure: tokens of the serialised answers»* (`kev/api.py:163`).

**Entorno (D5):** `Arbues-AxeNitro` (WSL2) + RTX 4050 6 GB, costo $0. Detalle reproducible en
`src/README.md` — ojo: el `torch` de PyPI es **cu130** y el driver del Nitro es 556.19 (**CUDA 12.5**);
hay que instalar el build `cu126` o la GPU no arranca.

**Estado:** el **DOI del pre-registro** ya está publicado (`10.5281/zenodo.23266795`) y la **matriz de
transferencia** está medida (`results/matrix/`, ver §14).

---

## 14. La matriz de transferencia — medida (08-oct-2026, Acer Nitro)

**El entregable central ya existe, y es la corrida CONFIRMATORIA** (la que declara el pre-registro,
DOI `10.5281/zenodo.23266795`): el conjunto completo de cada dataset, **23 grupos** (5 configuraciones de
modelo × 5 datasets), **65.185 decisiones** y **3.564 celdas**. Informe regenerable:
`results/matrix/RESUMEN_MATRIZ.md`; figuras en `results/matrix/`.

> El **piloto** (subconjuntos, 17.600 decisiones) fue la puesta a punto. La confirmatoria lo sustituye.
> En `typed-decisions` (el único dataset donde el piloto ya cubría el split entero) los 5 modelos
> reprodujeron el **mismo número exacto**, así que el pipeline es determinista.

**El objeto de la tesis, en una cifra:** sobre 65.185 distribuciones medidas, la diferencia entre la
definición de `confidence` más alta y la más baja de la **misma** distribución tiene mediana **0.288**,
percentil 90 **0.434** y máximo **0.848**.

**El claim, cuantificado** (nivel principal `raw`, el que congela el pre-registro). 348 celdas tienen mapa
cerrado entre definiciones (misma clase y misma cardinalidad; 1.044 contando los tres niveles). Error
absoluto medio del porte de umbral:

| subconjunto | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| todas las celdas con mapa | 348 | 0.2528 | 0.0123 | 20× |
| **sin empates dominantes** | 312 | **0.2337** | **0.0021** | **109×** |
| solo modelos entrenados | 276 | 0.2289 | 0.0020 | 113× |
| solo `n = 2` (Prop. 3) | 180 | 0.3006 | 0.0218 | 14× |
| solo `n ≥ 3` (Prop. 1) | 168 | 0.2015 | 0.0021 | 96× |
| nivel `L0` (debiasing sin etiquetas) | 324 | 0.2190 | 0.0059 | 37× |
| nivel `L1` (temperatura con etiquetas) | 312 | 0.3022 | 0.0024 | 126× |

**El promedio no es el resumen:** la distribución de `Δ` es **bimodal** (hay pares que coinciden por
identidad matemática y pares que fallan en grande), así que el titular es la tabla **por par (A→B)** de
`RESUMEN_MATRIZ.md` §3b, no la media global. El peor par es `pmax → ent` (mediana 0.767: cambia la FORMA,
no solo la escala); el mejor, `margin → jev` (0.002, porque a `n = 2` son la misma función).

**Hallazgo que afina el claim en dos capas** (ver `docs/erratas_especificacion.md` E2):

1. **Capa de escala:** ni entre definiciones equivalentes en orden viaja el **número**. `jev` y `pmax`
   están en escalas afines distintas: portar `τ` tal cual pierde hasta el **80 %** de la cobertura
   (celdas con `Δ = 0.80` y cobertura 0). El **mapa** sí transfiere (Δ ≈ 0.004, un ítem de 400).
2. **Capa de forma:** entre clases distintas (`pmax ↔ ent`, `pmax ↔ margen`) no existe mapa estricto:
   no hay número **ni** mapa que transfiera. Ahí está el peligro real.

**Otras cosas medidas:** Kev-0.8B saca **0.813** de accuracy en `banking77` (n = 77) contra 0.377 de Laya
(el ecosistema sí entrena para cardinalidad alta); `clinc150` (n = 151) **no es ejecutable** en 1 de los 3
checkpoints de Laya (ventana de 512 tokens: solo caben 126 opciones) — el límite documentado de Jev (≤ 255)
no es alcanzable en esta implementación.

**Pre-registro publicado:** DOI **10.5281/zenodo.23266795** (Zenodo, 08-oct-2026).

**Hecho:** la **redacción §4–§7** quedó en `paper/secciones/` (09-oct-2026), en el t440, sin GPU. Falta solo
la revisión del autor y el formateo final APA/IEEE.

**Auditoría final de errores (08-oct-2026):** sin pérdida silenciosa de filas (0 saltadas en los 23
grupos), `matriz.py` **determinista**, folds balanceados, y **sin truncado silencioso** en cardinalidad
alta (Kev puntúa las 77 opciones, Laya las 151). Se encontró y corrigió un fallo real: el debiasing `L0` no
convergía (paso ~1000× demasiado pequeño), así que ese nivel era indistinguible de `raw`. Reportado como
**desviación D1** en `RESUMEN_MATRIZ.md` §7. El nivel principal `raw` no se tocó tras publicar el DOI.

---

> **Registro histórico (eje descartado):** el material del **eje 1 (JEPA/LeWM/DINO)** — incluida su corrección
> crítica del 25-sep-2026 — **se eliminó del repo el 13-oct-2026** (solo en el historial de git). Quedó **FUERA DE ALCANCE** por instrucción
> expresa del autor (confusión Jev/JEPA). **No trabajar sobre él ni proponer subrutas.**

---

*Fin del estado consolidado. Si actualizas algo en esta carpeta, actualiza también este README
y `STATE.json` — son el punto de reentrada para el siguiente agente.*
