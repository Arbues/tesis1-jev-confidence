# Plan del paper — Tesis 1 (Ruta 1)

*Documento de trabajo · 04-oct-2026 · eje 2 (Jev, Laya y los modelos de decisión) · arranque del paper*

---

## 0. Título provisional

- **ES:** *Metrología y transferencia del campo `confidence` en modelos de decisión de pesos abiertos tipo Jev*
- **EN:** *Metrology and Threshold Transfer of the `confidence` Field in Open-Weight Jev-Type Decision Models*

Regla de estilo: sin dos puntos, sin subtítulo, sin signos de interrogación; frase nominal que declara
propiedad + objeto + alcance + tipo de método. **El título se fija al cerrar la especificación.**

---

## 1. El problema en una frase

En el ecosistema de modelos de decisión tipo Jev, **el mismo campo `confidence` significa cosas distintas
según quién lo emite** (Jev usa `(n·p_max−1)/(n−1)`; Laya usa `1−H/log k`; `jev-lite` usa `p_max`; otros un
prior aprendido), y todos se usan para lo mismo: fijar un **umbral** de "actúo o escalo a un humano". Un
umbral calibrado sobre una definición **no significa nada** sobre otra, pero el ecosistema los porta entre
modelos como si fueran intercambiables. **Nadie ha medido sistemáticamente cuánto se degrada ese porte.**

---

## 2. El claim (falsable) — lo que la tesis afirma y mide

> **Claim.** De las definiciones de `confidence` en uso, unas son **equivalentes en orden** (transferencia
> exacta de umbral) y otras **no** (transferencia fallida). La matriz de transferencia cuantifica, para cada
> par (definición origen A → definición destino B), modelo y dataset, **cuánta cobertura y precisión se
> pierden** al aplicar el umbral `τ_A` con la definición B.

**Estructura teórica que lo respalda (núcleo interno):** la fórmula de Jev `(n·p_max−1)/(n−1)`, a `n` fijo,
es una transformación **estrictamente creciente y afín** de `p_max`; por tanto **su umbral transfiere de
forma exacta a `p_max`** aplicando el mapa `φ⁻¹` (misma cobertura). En cambio, la **entropía normalizada** es una función de *toda*
la distribución, no de `p_max` solo: dos distribuciones con el mismo `p_max` pueden tener entropías
distintas, así que **el umbral NO transfiere** en general entre una definición tipo entropía y una tipo
orden-estadístico. La matriz mide esas dos clases de caso. → **Esto convierte un "instrumento" en una tesis
con una proposición y evidencia**, que era el riesgo principal (ver §7).

---

## 3. Preguntas de investigación

1. **RQ1.** ¿Qué definiciones de `confidence` usa realmente el ecosistema tipo Jev y cómo se relacionan
   formalmente entre sí (funciones de la distribución y de `n`)?
2. **RQ2.** Entre dos definiciones, ¿el umbral que da una cobertura objetivo transfiere? ¿Cuánto se degrada
   cobertura y precisión? ¿Depende del modelo, del dataset o de la cardinalidad `n`?
3. **RQ3.** ¿Qué par de definiciones es "seguro" portar (transferencia exacta o casi) y cuál es "peligroso"?

---

## 4. Contribuciones

1. **Especificación formal** de cada definición de `confidence` como función de la distribución devuelta y
   de la cardinalidad `n` (dominio, rango, monotonía). Incluye una **proposición de equivalencia en orden**
   entre definiciones afines-de-`p_max` y la **no-equivalencia** con las de entropía.
2. **Librería `jev-conf-metrics`** (implementación de todas las definiciones + métricas) con **tests de
   conformidad** contra salidas publicadas (precedente en el ecosistema: el arnés `jev-verify`).
3. **Matriz de transferencia de umbrales** (definición × definición × modelo × dataset) + **dataset de
   mediciones crudas** (una fila por modelo × dataset × ítem) + **script regenerador** + figura *heatmap*.
4. **Catálogo trazable** de definiciones y licencias, con columna **medido aquí / auto-reportado**.

---

## 5. Artefactos entregables

| # | Artefacto | Dónde vive | Estado |
|---|---|---|---|
| 1 | `spec` de las definiciones | `paper/03_especificacion_confidence.md` | **hecho** (+ erratas en `docs/erratas_especificacion.md`) |
| 2 | Librería `jev-conf-metrics` + tests | `src/jev_conf_metrics/` | **hecho** (67 tests) |
| 3 | Matriz de transferencia | `results/matrix/matriz_transferencia.csv` | **medida** (3.564 celdas, corrida confirmatoria) |
| 4 | Dataset de mediciones crudas | `results/crudos/*.jsonl` | **medido** (65.185 filas, con `row_hash`) |
| 5 | Script regenerador | `src/matriz/{medir,matriz,figura,informe_matriz}.py` + `correr_*.sh` | **hecho** |
| 6 | Pre-registro con DOI | `paper/04_pre_registro.md` → Zenodo | ✅ **publicado: 10.5281/zenodo.23266795** |
| 7 | Paper (IEEE) | `paper/secciones/` | **§1–§7 borrador** (08–09-oct-2026) |

**Desviación de rutas respecto a la versión anterior de esta tabla:** los artefactos viven bajo
`results/matrix/` y `results/crudos/` (no en la raíz de `results/`), porque esas carpetas ya existían y así
lo describen `README.md` §5 y `.hermes.md` §5. Las figuras (`heatmap_*.png/pdf`) están en `results/matrix/`.

---

## 6. Estructura propuesta del paper (IEEE)

1. **Introducción** — modelos de decisión tipo Jev; el campo `confidence`; el problema del porte de umbrales.
2. **Trabajos relacionados** — calibración (Guo 2017), reglas propias (Gneiting & Raftery 2007), predicción
   selectiva (Chow 1970; Geifman & El-Yaniv 2017), y el ecosistema Jev-OSS de 2026.
3. **Marco teórico** — definiciones formales de `confidence`, calibrar, métricas, propiedad de transferencia
   (marco completo en `paper/01_marco_teorico.md`).
4. **Método** — modelos, datasets, procedimiento de medición, la matriz, bootstrap + FDR.
5. **Resultados** — la matriz, la degradación de cobertura/precisión, casos exactos vs fallidos.
6. **Discusión** — implicaciones para quien despliega un modelo tipo Jev; el error de portar umbrales.
7. **Conclusión + artefactos** — librería, matriz, dataset (enlace al repo).

---

## 7. Riesgos y correcciones de decisiones previas

> Revisión crítica pedida por el autor (04-oct-2026): *"identifica si algo concluí mal en mi toma de decisiones"*.

| # | Lo que se concluyó antes | ¿Era correcto? | Corrección aplicada |
|---|---|---|---|
| 1 | Que un **instrumento puro** bastaba como Tesis 1 | **Parcialmente mal**: un instrumento sin claim puede leerse como "solo una tabla" | **Fix:** el paper lleva un **claim falsable** (§2) + una **proposición** de equivalencia en orden. El instrumento *evidencia* el claim |
| 2 | Que la **Ruta C (cartografía)** era "la más segura" | **Mal**: quedó ocupada por `arXiv:2609.30216` (*Jev in the Wild*) | Descartada. La más segura era realmente la metrología |
| 3 | **Congelar la ventana 18→30-sep-2026** | **Mal para esta ruta**: la metrología no depende del corpus temporal; congelarla habría sido frágil | Reemplazado por **versionado + hash por modelo/dataset** |
| 4 | "Laya ships **over-confident**" (ECE 0.466→0.081) | **Incompleto**: eso es el model card; el checkpoint tal cual es **sub-confíado** (arXiv:2609.33843) | Reconciliado: miden artefactos distintos (se documenta con cuál coincide la reproducción) |
| 5 | El paso 0 con el **thinkpad-t440** como ejecutor implícito | **Imposible**: no tiene GPU | Fijado: el cómputo corre en **Nitro / Mac Mini**; el t440 hace el paper |
| 6 | Que el aporte interno debía ser el **núcleo** | No es error; el autor lo relajó | La matemática vive en el **marco teórico**; el resultado es metrología |

**Riesgo vivo:** que la matriz aparezca publicada por uno de los ~30 grupos del ecosistema.
**Mitigación:** pre-registro con DOI temprano; el valor del instrumento sobrevive igual.

---

## 8. Plan de trabajo (secuencia)

| # | Paso | Máquina | Responsable |
|---|---|---|---|
| 0 | Elegir ruta | — | ✅ hecho |
| 1 | Paso 0 go/no-go (Laya 421M + Kev-0.8B, `output_tokens=0`, reproducir un ECE) | **Nitro** | agente (dev) |
| 2 | Congelar definiciones + datasets + cobertura objetivo | t440 | autor |
| 3 | Especificación formal + proposición | t440 | autor/agente (paper) |
| 4 | Librería `jev-conf-metrics` + tests | Nitro | agente (dev) |
| 5 | Pipeline de medición | Nitro | agente (dev) |
| 6 | Matriz + dataset de mediciones crudas (hash por fila) | Nitro | agente (dev) |
| 7 | Pre-registro con DOI | — | agente |
| 8 | Medición principal + redacción | t440 + Nitro | ✅ hecho: matriz confirmatoria + §4–§7 |

---

## 9. Estado y pendiente inmediato

- **Hecho:** ruta elegida; documento principal (`eje-2-jev-opensource/11_ruta1_metrologia_confidence.md`);
  marco teórico base (`paper/01_marco_teorico.md`); **borradores §1–§7** (`paper/secciones/`);
  bibliografía (`paper/02_referencias.bib`); repo GitHub y `AGENTS.md`;
  **especificación formal** de las definiciones (`paper/03_especificacion_confidence.md`);
  **paso 0 ejecutado en el Acer Nitro (08-oct-2026) → GO** (`results/paso0_informe.md`): Laya (3 checkpoints)
  y Kev-0.8B sobre las 2.000 decisiones de `typed-decisions`, `output_tokens = 0` verificado y **las 5
  métricas publicadas de Laya reproducidas con |Δ| ≤ 0.003** (ECE 0.213→0.2157, accuracy 0.766→0.7685,
  Brier 0.062→0.0615, soft acc 0.471→0.4707, score MAE 0.242→0.2424).
- **Hecho además (08–09-oct-2026):** la **corrida confirmatoria** (23 grupos, 65.185 decisiones, 3.564
  celdas), la **librería** `src/jev_conf_metrics/` (67 tests) y **§1–§7 del paper** redactados en
  `paper/secciones/`. El **alcance está congelado** (§10) y el pre-registro, publicado.
- **Pendiente (solo del autor):** verificar el DOI del pre-registro en su cuenta, revisar el borrador §1–§7
  y hacer el formateo final **IEEE**. El repositorio ya es público (10-oct-2026). No queda cómputo pendiente.

---

## 10. Alcance congelado (04-oct-2026)

Decisiones tomadas por el agente conforme a D1–D5 (el autor delegó la resolución del alcance).

**10.1. Definiciones que ENTRAN en la matriz.** Las analíticas `C_max` (p_max), `C_Jev`, `C_ent` (Laya) y
`C_mar` (margen); `C_noul` en el bloque `n = 2`. Transformaciones evaluadas: `AnyJev L0` y `L1` aplicadas
sobre las anteriores.

**10.2. Solo catálogo (fuera de la matriz).** `act_probability` (DEF-6; opaca, AUROC 0.30 → sin señal) y
`open-decision-ai` (DEF-8; opaca).

**10.3. Modelos (≤ 6 GB en el Nitro).** Laya 421M (base), Laya-typed-decisions, Kev-0.8B, tinyjev 596M.
Extensión (Mac Mini / 4-bit): Kev-4B, jev-lite (Gemma 4 E4B), Jeff-1.

**10.4. Datasets (ya etiquetados — D2).** Primarios: `LocalLLaMA/typed-decisions` (benchmark),
`jaredpalmer/kev-suites`, `Banking77`, `CLINC150`, `SST-5` (ordinal), `alisawuffles/WANLI` (NLI).
Extensión: `MedHallu`, `AG News`, `DAIR Emotion`.

**10.5. Parámetros de la medición.** `q = 0.80` (principal), `0.50` y `0.95` (sensibilidad); reporte por
cardinalidad `n`; métricas accuracy / Brier / NLL / ECE (igual ancho e igual masa) / AUROC por definición +
`Δ` de transferencia; agregación con bootstrap (IC 95 %) y corrección FDR.

**10.6. Lo único que necesita al autor.** (i) crear el **DOI del pre-registro** (OSF/Zenodo, su cuenta);
(ii) correr el **paso 0** en el Nitro (o dar acceso). Nada de esto bloquea el clonado del repo.
