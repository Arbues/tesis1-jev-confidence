# Auditoría integral del repositorio — Tesis 1 (28-oct-2026)

**Alcance:** todo el repo `~/paper-tesis1` @ `342696f` (main == origin/main): paper (`.md` + `.tex` + PDF),
bibliografía, figuras, artefactos medidos (`results/`), código (`src/`, `tests/`) y documentación de estado
(`STATE.json`, `README.md`, `AGENTS.md`, `.hermes.md`, `docs/`, `notes/`).

**Método:** cinco auditorías independientes en paralelo (prosa, bibliografía, figuras, documentación, código)
más una verificación del orquestador. Ninguna cifra se tomó de `STATE.json`/`README`: **todas** se
recalcularon desde `results/crudos/*.jsonl` (65.185 filas), `results/matrix/*.csv`, `results/matrix_pagado/*.csv`
y `results/pagado/*.jsonl`, con `stdlib` puro; el PDF se recompiló desde las fuentes y se midió con
`pdftotext`/`pdfinfo`/`pdffonts`. Los metadatos de la bibliografía se contrastaron contra la fuente real
(Crossref, arXiv, HuggingFace, GitHub, API de Zenodo, API de ORCID).

**Nada del repo se modificó**, salvo este informe. El único cambio en el árbol es `paper/ieee/main.pdf`
recompilado (mismo tamaño y mismo texto; solo cambian `/CreationDate` y `/ID`).

Informes de detalle (fuera del repo): `~/.hermes/cache/scratch/audit/`
`00-hallazgos-orquestador.md` · `01-paridad-prosa.md` · `02-bibliografia.md` · `03-figuras.md` ·
`04-docs.md` · `05-codigo.md`.

---

## 0. Veredicto en una línea

**El núcleo está sano y es reproducible:** las cifras selladas (65.185 · 23 · 3.564 · 0.288/0.434/0.848 ·
0.2337 vs 0.0021 = 109.2× · ECE 0.216→0.577) se reproducen **al dígito publicado** por tres vías
independientes, la matriz se regenera byte a byte, los 67 tests pasan y el PDF compila con 0 errores,
0 desbordes y 36 referencias resueltas. **Lo que falla no son los datos: son siete afirmaciones del texto,
una tabla del PDF a la que le falta una columna, un rótulo de figura cortado, la mezcla de comas y puntos
decimales, la bibliografía y la documentación de estado.** Ninguno exige volver a medir nada.

**Recuento:** **62 hallazgos** — 8 de gravedad alta (A1–A8), 22 media (M1–M22) y 32 baja (B1–B32), sin
duplicados entre áreas (una misma afirmación falsa repetida en cuatro documentos cuenta una vez).

---

## 1. Lo que se verificó y está bien (no tocar)

| Comprobación | Resultado |
|---|---|
| `pytest` | **67 passed** en 5,3 s (8 archivos: backend 16 · conf_score 11 · definiciones 10 · medir_etiquetas 6 · medir_nombres 3 · prior_numpy 3 · regresión paso 0 10 · transferencia 8) |
| `informe_matriz.py` → `git diff` | **vacío**: `RESUMEN_MATRIZ.md` se regenera byte a byte |
| `extension_conf_score.py` | reproduce: 5.505 · 0.2724 → 0.2900 · ECE 0.204/0.184/0.199/0.237/**0.241** |
| Crudos sellados | 65.185 filas · 23 grupos · 65.185 `row_hash` **únicos** · los `conf_*` guardados coinciden con las fórmulas (0 discrepancias en 65.185×4 comparaciones) |
| Brecha entre definiciones | mediana **0.2881** · p90 **0.4344** · máx **0.8481** · **2.167** filas saturadas, y son exactamente las de brecha 0 |
| ECE por grupo (§5.7) | laya-typed-decisions **0.2157→0.5766** · brecha mediana **0.124** · máx **0.361** · mejor pmax 7 / margin 6 / ent 6 / jev 4 · `ent` peor en **13/23** |
| Matriz | 3.564 celdas (1.188 por nivel) · 348 con mapa por nivel · **1.044** con los tres niveles |
| Tabla §5.3 | 5 de 7 filas exactas (348 · 312 · 276 · 180 · 168) — las 2 restantes, ver **A4** |
| Tabla §5.4 por par | **12/12** pares exactos (celdas, mediana y media) |
| Tabla §5.4 cardinalidad | **6/6** filas exactas |
| Tabla §5.5 | **6/6** filas exactas (con el filtro raw + q=0.80 que el título no declara, **M6**) |
| Tabla §5.6 | **12/12** filas exactas |
| Figuras | **29 cifras** de los 8 pies y **22 recuentos** impresos se recalculan exactos; regeneración con el mismo texto extraído |
| §5.8.1 | 5.505 · 0.2724→0.2900 · p90 0.4113 · máx 0.5807 · Qwen mínimo **70,3 %** · multilingual máximo **92,6 %** |
| §5.8.2 | 14.277 · accuracies 0.796/0.901/0.541/0.733/0.754 · 7.092.972 tokens · 79.462 y 0.2727/0.4353 · 2.880 celdas · 420 con mapa · tabla por modelo **exacta** (0.1735/0.0130/13.4×/2,5 %/4 de 72; Qwen 0.3441/0.0517/5,0 %/36 de 72) |
| Ejemplo de portada | (0.0118, 0.4629, 0.5253) → 0.2879 / 0.3199 / 0.5253 / 0.0624 |
| LaTeX | 0 errores · 0 Overfull · **13 páginas** · 36 `\bibitem` · 0 `??` · 0 `[?]` · 24 flotantes, 24 con `\ref`, 0 huérfanos |
| Bibliografía | 0 claves citadas inexistentes · 0 duplicadas · los 3 DOI resuelven y coinciden al carácter · las 6 arXiv coinciden |
| Figuras ↔ disco | 8 `\includegraphics` → 8 archivos · 6 a `\columnwidth` (248,4 pt) y 2 a `\textwidth` (511,2 pt) · 0 repetidas · 0 huérfanas |
| Zenodo / ORCID / SWHID | los DOI resuelven y declaran la versión correcta · ORCID con **3 works** · SWHID 200 |

---

## 2. Hallazgos de gravedad ALTA

### A1 · `precision()` no calcula la precisión: devuelve la confianza media
`src/jev_conf_metrics/transferencia.py:35-38`

```python
sel = [c for c, a in zip(confs, correct) if c >= tau]   # guarda `c`, no `a`
return sum(sel) / len(sel)                              # media de confianzas
```

Repro: `precision([.9,.8,.7,.2],[1,0,1,0],.7)` → **0.80**; el acierto real entre los seleccionados es **0.667**.

Consecuencias medidas:
- Contamina `precision_A` y `precision_B` en **las 3.564 celdas** (7.128 valores) de
  `results/matrix/matriz_transferencia.csv` y la tabla §4 de `RESUMEN_MATRIZ.md`, que se titula
  «precisión A / B». En `Qwen/banking77` publica **0.204** cuando la accuracy del modelo es **0.0156**.
- El paper **no imprime** esas columnas en el PDF (sus tablas solo dan |Δ| y cobertura), pero
  `§3.5` promete «medir la cobertura efectiva y la precisión» y §1/§2 venden «cobertura y precisión»
  como la tabla del trabajo → la afirmación queda **sin respaldo** en el artefacto publicado.

**Arreglo:** `sel = [a for c, a in zip(confs, correct) if c >= tau]`, añadir un test (`precision` hoy no
tiene ninguno) y regenerar `matriz_transferencia.csv` + `RESUMEN_MATRIZ.md`. Solo cambian esas dos columnas;
`delta`, `delta_mapa`, `tau`, IC y FDR no dependen de `precision`, así que **ninguna cifra del paper se mueve**
y el chequeo «`informe_matriz.py` no cambia nada» seguirá siendo válido tras regenerar.

### A2 · `output_tokens` de Kev: el paper publica tres valores incompatibles del mismo campo
| Dónde | Qué dice |
|---|---|
| `04_metodo.md:20` (`.tex:20`) | «las cinco configuraciones …, **todas** con `output_tokens = 0` verificado» |
| `05_resultados.md` tabla §5.1 (`.tex` `tab:grupos`) | Kev-0.8B: tokens de salida **0** |
| `05_resultados.md:188-192` §5.7 | «Kev … recuento de tokens de la respuesta serializada (**869.310** en las mismas 2.000 decisiones)» |
| `05_resultados.md:253-255` §5.8.2 | «El contador no es cero en el servicio (7.092.972), **a diferencia de los brazos de pesos abiertos**» |
| `docs/erratas_especificacion.md` E4:95 | «`output_tokens = 0` en las 65.185 filas de `results/crudos/` **y en `results/raw/`**» |

Medido: en `results/crudos/` **todas** las 65.185 filas tienen `output_tokens = 0` (Kev incluido);
en `results/raw/paso0_summary_kev_kev-latest.json` hay `output_tokens_total = 869310`. Es decir, el 869.310
es del **paso 0**, no de la corrida confirmatoria, y el adaptador de la corrida sellada no propaga el campo
(`medir.py:94` lee `usage.output_tokens`; los backends HF no lo rellenan).

**Arreglo (sin re-medir):** en §5.7 decir «en el **paso 0**» y añadir «la corrida confirmatoria no propaga el
campo»; corregir E4 (quitar «y en `results/raw/`»); en §5.8.2 cambiar «a diferencia de los brazos de pesos
abiertos» por «a diferencia de la corrida confirmatoria». Decidir si el 0 de §5.1 se etiqueta como «campo no
propagado» en vez de «verificado».

### A3 · «0,1 % de empate en los abiertos … 0 de 72 celdas» es falso, y contradice la tabla de al lado
`05_resultados.md:282-283` y `.tex:479-481`; repetido en `STATE.json:132`, `README.md:285` y `.hermes.md:48`.

«Los abiertos» excluye en silencio al control: **Qwen3.5-0.8B-Base (pesos abiertos, control crudo) tiene
5,0 % de empate medio y 36 de 72 celdas por encima del 5 %**, más que los 2,5 % y 4 de 72 de Jev. Solo los
cuatro checkpoints Laya/Kev están en 0,1 % y 0 de 72.

**Arreglo:** «frente a 0,1 % en los **checkpoints entrenados** y 0 de 72 en ellos (el control crudo tiene
5,0 % y 36 de 72, consistente con su saturación)». La frase causal no cambia.

### A4 · La tabla §5.3 compara peras con manzanas: las filas `L0` y `L1` llevan un filtro no declarado
`05_resultados.md:78-79` / `.tex` `tab:error-transferencia` · origen: `informe_matriz.py:174-179`

Las filas `L0`/`L1` se construyen con `delta_mapa no vacío` **y** `n_empates_tau/n_items_te < 0,05`; las cinco
de arriba no llevan el filtro. Sin filtro (recomputado hoy):

| nivel | celdas | \|Δ\| directo | \|Δ\| con mapa | factor |
|---|---|---|---|---|
| raw | 348 | 0.2528 | 0.0123 | 20.5× |
| **L0** | **348** | **0.2312** | **0.0096** | **24.0×** |
| **L1** | **348** | **0.3145** | **0.0136** | **23.0×** |

La tabla publica 324/0.2190/0.0059/37.1× y 312/0.3022/0.0024/126.0× (las cifras **con** filtro). El lector
atribuye la diferencia al nivel cuando la produce el filtro, y el pie de tabla dice «(nivel `raw`)» cuando dos
filas no son `raw`.

**Arreglo:** etiquetar «nivel `L0`, **sin empates dominantes**» (y corregir el pie: «nivel `raw`; las filas
`L0`/`L1` con el mismo filtro de empates»), regenerando `RESUMEN_MATRIZ.md` y las dos copias del paper.

### A5 · Las cifras de §6.1 no salen de ningún artefacto
`06_discusion.md:15-16` / `.tex:9`: «|Δ| mediano de **0.20 a 0.31** en el par `pmax ↔ jev`, pero el mapa sí
transfiere (**0.0025**)».

Recomputado sobre las celdas con mapa, nivel `raw`: `jev→pmax` mediana **0.0759**, `pmax→jev` mediana
**0.2574**; |Δ_mapa| del par: media **0.0049**, mediana **0.0013**. Sobre los tres niveles: 0.076/0.257 (raw),
0.059/0.183 (L0), 0.199/0.417 (L1). **Ningún subconjunto declarado da 0.20–0.31 ni 0.0025.** El 0.0025 viene
de una agregación vieja de 948 celdas que quedó en `docs/handoff-t440.md:31` («104× (0.2577 vs 0.0025, 948
celdas)»).

**Arreglo:** escribir «0.076 y 0.257 (nivel `raw`); con mapa, 0.0013 de mediana (0.0049 de media)».

### A6 · El paper dice que `noul` entra en la matriz de `n = 2`; no entra
`04_metodo.md:58` / `.tex:82`: «La quinta, `C_noul = max(π, 1−π)` (DEF-3), **entra en el bloque de `n = 2`**».
La errata E3 repite «entra en la matriz solo en el bloque `n = 2`».

Medido: la matriz tiene **4** definiciones (`A,B ∈ {pmax, jev, ent, margin}`, 12 pares, 0 apariciones de
`noul`); los crudos solo tienen `conf_{pmax,jev,ent,margin}`; `matriz.py:45` fija `DEFS` con cuatro y no hay
ninguna referencia a `noul` en `src/matriz/`.

**Arreglo:** «está implementada como función propia sobre el escalar binario y **no entra en la matriz** de
esta corrida (a `n = 2` es idéntica a `p_max`, así que no añadiría información)»; corregir E3.

### A7 · §6.2 afirma algo matemáticamente falso: `C_mar` no es función de `p_max`
`06_discusion.md:31` / `.tex:9`: «Por eso `C_Jev`, `C_max` y **`C_mar`** (fijado `n`) seleccionan lo mismo con
el umbral traducido».

El margen `p_(1) − p_(2)` depende de la distribución entera. Contraejemplo medido (mismo `sst5`, `n = 5`):
`pmax 0.2621 / margin 0.0308` frente a `pmax 0.2483 / margin 0.0425` → el orden se invierte
(**101.377 inversiones** en 400×400 pares de filas). La propia §5.5 dice lo correcto: la equivalencia de
`jev ↔ margin` vale **solo a `n = 2`**.

**Arreglo:** quitar `C_mar` de la frase o añadir «…y `C_mar` **solo a `n = 2`**, donde es `2·p_max − 1`».

### A8 · La Fig. 2 se imprime con el rótulo del eje X cortado
El rótulo mide ~280 pt y la caja de la figura 248,4 pt: en el PDF se lee «separación entre la definición más
alta y la más baja de la MISMA **distr**». Medido con `pdftotext -bbox`: el último glifo cae en x = 250,66
(> 248,4) y en `main.pdf` la tinta se corta en el borde de la columna.

**Arreglo:** `.venv/bin/python src/figuras_paper.py` con el rótulo acortado («separación entre la definición
más alta y la más baja de la misma distribución» en dos líneas con `\n`) y volver a verificar con
`pdftotext -bbox` que ningún glifo salga de la caja.

---

## 3. Hallazgos de gravedad MEDIA

**M1 · La tabla `tab:porte-pagado` perdió una columna y el pie sigue describiéndola.**
`.tex:451` dice «La última columna es la fracción media de ítems de prueba que comparten el umbral», pero el
`tabular` tiene 5 columnas y la última es `factor`: **la columna `empate medio de τ` desapareció** al pasar a
LaTeX (el `.md` sí la tiene, línea 266). Con ella se pierde el respaldo tabular del argumento causal de
§5.8.2 (2,5 % vs 0,1 %, 25×, 4 de 72). **Arreglo:** devolver la columna o reescribir el pie.

**M2 · Comas y puntos decimales mezclados en el mismo párrafo.**
`babel(spanish)` convierte a coma los números en modo matemático: el PDF imprime
«(0,0118, 0,4629, 0,5253)» y, dos líneas después, «0.288 … 0.3199 … 0.5253». Recuento en `pdftotext`:
**31** números con coma frente a **462** con punto. Afecta a la prosa, a la tabla 3.1 y a 3 pies de figura
(Figs. 1, 4 y 7: «1/77 = 0,013», «q = 0,80», «+0,80»). **Arreglo:** `\spanishdecimal{.}` tras cargar `babel`
(o `\usepackage{siunitx}` con `output-decimal-marker={.}`), recompilar y verificar que el recuento de comas
decimales baja a 0.

**M3 · §5.5 no declara su filtro.** Las cifras (60 celdas, 0.3042, 52 con FDR…) son de **nivel `raw` y
`q = 0,80`** (`informe_matriz.py:250-257`); el título de la tabla no lo dice y §5.6 sí. Sobre los tres niveles
las cifras son otras (n=2: 540 celdas, 0.3138, 462). Además «celdas» significa tres cosas distintas en §5.3,
§5.4 y §5.5 (348 con las 3 q · 180 con las 3 q · 396 con una q y sin filtro de mapa).

**M4 · El mapa hacia `margin` a `n = 2` arrastra un artefacto de coma flotante.** `2t−1` y `p1−p2` difieren en
1 ulp (`0.15499999999999992` vs `0.15500000000000003`), y la comparación `c >= tau` pierde la masa empatada:
en **9 de 45** grupos `n = 2` (nivel×q) los 12 pares deberían dar el mismo `delta_mapa` y no lo hacen; los
pares culpables son siempre los que tocan `margin`. La celda más visible
(`Qwen/typed-decisions n=2 raw q=0,5`, `pmax→margin` y `jev→margin` = 0.2090 frente a 0.1288 del resto) es la
primera fila de la tabla «las 8 con mayor desviación» de `RESUMEN_MATRIZ.md` §3. Efecto en lo publicado:
«todas las celdas con mapa» 0.0123 → ~0.0115 (20,5× → 21,9×) y «solo n=2» 0.0218 → ~0.0203 (13,8× → 14,8×).
**El titular de 312 celdas / 109,2× no cambia** (ninguna de esas celdas está en el subconjunto limpio).
**Arreglo:** en `mapa_entre`, para `A/B = margin` a `n = 2`, usar la misma expresión que `conf_margin`
(`p1 − p2` con `p1 = (1+t)/2`), o comparar con tolerancia `>= tau - 1e-12`; regenerar y revisar las 9 celdas.

**M5 · «La incompatibilidad es un fenómeno de `n ≥ 3`» choca con los datos.** Abstract (`main.tex:61`),
§1 (`01_introduccion.md:51`) y Proposición 3 (`03_marco_teorico.md:74` / `.tex:99`). A `n = 2` la mediana de
|Δ| directo es **0.2141**, solo el **14 %** de las celdas transfiere y hay celdas con **Δ = 0,80 y cobertura 0**
(§5.6). La proposición es correcta si «incompatibilidad» = «no existe mapa»; es falsa si = «el umbral no
transfiere», que es como la lee el titular. **Arreglo:** «la incompatibilidad **de forma** aparece a partir de
`n = 3`; a `n = 2` el fallo es solo de **escala**».

**M6 · §5, §6 y §7 no tienen una sola cita.** Recuento de `\cite`: §1 = 13, §2 = 22, §3 = 7, **§4 = 0, §5 = 0,
§6 = 0, §7 = 0** — justo las secciones que nombran la literatura vecina (la reproducción de Laya, el término
de RL, la cartografía, la negación, los benchmarks). Es lo que más resta en la lectura de un revisor IEEE.

**M7 · Siete entradas del `.bib` nunca se citan** (`efron1993`, `layamultilingual`, `typeddecisions`,
`opendecisionai`, `awesomejev`, `waynechang`, `arXiv2609.26550`). Cuatro **deberían** citarse porque se usan en
el método o en los resultados: `efron1993` (bootstrap, §4.4), `layamultilingual` y `typeddecisions` (§4.1/§4.2:
son configuraciones y dataset medidos), `opendecisionai` (§4.3/§6). Faltan además dos referencias que el
método necesita: **Benjamini–Hochberg (1995)** para §4.4 y la del modelo **Qwen3.5-0.8B-Base**.

**M8 · Trece entradas no tienen DOI ni URL**, contra el estándar declarado en `paper/02_referencias_pendientes.md`
(«toda entrada con DOI o URL; única excepción `lakoreai2026`»). Son las nueve clásicas con DOI conocido
(`naeini2015`, `niculescu2005`, `brier1950`, `good1952`, `epstein1969`, `chow1970`, `zadrozny2002`, `vovk2005`,
`efron1993`) más `geifman2017`, `jitkrittum2023`, `platt1999` y `angelopoulos2021`. Y la supuesta excepción
`lakoreai2026` **sí** tiene URL, así que hoy no queda ninguna que justifique la excepción.

**M9 · `lakoreai2026` tiene el título inventado y el autor mal.** El informe real se titula «Dissecting RLCD:
What Reinforcement Learning Does (and Doesn't) Do for Calibrated Typed Decisions» y lo firma «Le Duc Minh»;
el `.bib` pone un título que es una frase del abstract y añade diacríticos que el PDF no usa. La nota mezcla
«30 corridas» (README) con la ablación real de **13 corridas**.

**M10 · `jev2026blog` tiene la fecha mal y el error se propaga al cuerpo.** La página está fechada
**15-sep-2026** (firma Diogo Almeida); el `.bib` dice 18-sep y §1 abre con «abrió la categoría el 18 de
septiembre de 2026». El 18-sep es la cobertura de prensa y el release de Laya.

**M11 · Las 20 `note` del `.bib` se imprimen en la lista de referencias.** No es estilo IEEE, envejecen dentro
del PDF y una es **falsa** (`jevLite`: «repo sin licencia» → la model card declara `license: gemma`). Otra
(`roby1965`) afirma una «versión previa de 1964» que ningún índice respalda.

**M12 · Dos entradas mal tipadas.** `platt1999` es un capítulo de libro (MIT Press, 2000) declarado como
`@article` con `journal = {Advances in Large Margin Classifiers}`; `angelopoulos2021` es `@article` con
`journal = arXiv preprint…` y sin `eprint`/`archivePrefix`/url, violando el estándar arXiv del propio archivo.

**M13 · El abstract no tiene fuente en `paper/secciones/`.** El texto del Resumen vive solo en
`main.tex:49-64`; no hay `.md` espejo, así que la regla «el `.md` es la fuente de verdad» no cubre la parte
más leída del paper (y la corrección M5 hay que hacerla sin paridad que la verifique).

**M14 · Cuatro documentos siguen publicando `0.1307` como «el |Δ| directo más bajo».** `README.md:332-344`
(la tabla §10-quater completa no reproduce: laya 0.2233 vs 0.2581, kev 0.2499 vs 0.2813, Qwen 0.3635 vs
0.3441…), `AGENTS.md:132`, `.hermes.md:48` y `docs/validacion-productos.md:140`. `STATE.json:132` ya lo
corrigió el 25-oct y **lo dice explícitamente**; la corrección no se propagó. `.hermes.md` es el archivo que
se auto-carga en cada sesión, así que el error se reinyecta.

**M15 · `docs/guia-cierre-pendientes.md` pide al autor tareas ya cerradas.** §2.2 «Confirmar las 9 referencias»
(cerradas el 12/19-oct) y §3.2 «Decisión pendiente: ¿la `MAD_unif` entra?» (decidido el 19-oct). Además
referencia `STATE.json → pendientes_2026_10_11`, **clave que no existe**, y da el gasto del brazo pagado como
«~USD 0.33» (real 0.79).

**M16 · `docs/validacion-productos.md` está roto como checklist.** «Esperado: **37 passed**» (hay 67), nombres
de figura viejos (`fig1-brecha`…`fig8-heatmap-banking77`), «tu ORCID tiene 0 trabajos» (tiene 3), «0.1307·10×»
y `.venv/bin/pip install` (el `.venv` es de `uv` y **no tiene pip**).

**M17 · El ejemplo de la librería es falso en dos documentos.** `docs/libreria.md:39` y
`validacion-productos.md:57` publican `jev 0.2428`, `margin 0.2148`; la salida real de
`all_confidences([0.19,0.22,0.43,0.16])` es `jev 0.24`, `margin 0.21` (`ent 0.0588`, `pmax 0.43`).

**M18 · `conf_score` y `score_mad_unif` no se pueden importar desde la raíz del paquete.**
`docs/libreria.md:51-54` los documenta en la API, pero `jev_conf_metrics/__init__.py` no los re-exporta:
`from jev_conf_metrics import conf_score` → `ImportError`.

**M19 · `bh_fdr` no filtra `NaN`.** `min(prev, nan)` devuelve `prev`, así que un p-valor `NaN` hereda el q del
vecino y puede salir **significativo**; además `sorted()` con `NaN` tiene orden indefinido y puede correr los
rangos de las demás celdas. Hoy lo tapan los dos llamadores (`matriz.py:321`, `fusionar_matriz_paralela.py:53`
sustituyen `NaN` por 1.0), pero la función es API pública (`__all__`).

**M20 · Las 8 figuras embeben fuentes Type 3.** `pdffonts` da `Type 3` en las ocho (matplotlib por defecto).
IEEE PDF eXpress y varias editoriales lo marcan como no conforme. **Arreglo:**
`plt.rcParams["pdf.fonttype"] = 42` en `src/figuras_paper.py` y en `src/matriz/figura.py`; regenerar.

**M21 · La leyenda de la Fig. 5 se imprime cortada.** En el PDF: `>0` en lugar de `> 0.30` y `0.05--0.30` con
doble guion. Además la entrada gris «|Δ| mediana (color según corte)» no corresponde a ninguna marca.
**Arreglo:** leyenda en dos filas (`ncol=2`), etiquetas cortas y raya tipográfica.

**M22 · La especificación normativa afirma «`n = 2` ⇒ Δ_mapa = 0» y su propia matriz la contradice, sin errata.**
`paper/03_especificacion_confidence.md:192, 226, 242` (tabla §4.5, §5 y test T6) prometen transferencia
**exacta** entre todas las definiciones a `n = 2`. En la matriz publicada, **36 de 180** celdas `n = 2` del nivel
`raw` superan |Δ_mapa| > 0,01 y el máximo es **0,2090**. La causa no es el mapa (es exacto): la regla
`τ = min{τ : cob ≤ q}` **subdispara** cuando hay masa empatada — con `q = 0,5` la cobertura lograda en
calibración es 0,366 — y ese déficit entra íntegro en `delta_mapa`. El paper lo explica en §5.3 («suelo por
empates»), pero el documento normativo no lo matiza y **no existe la errata E7** que la propia regla del repo
exige (`04_pre_registro.md` no se toca; los cambios van como errata). **Arreglo:** añadir E7 a
`docs/erratas_especificacion.md` («Δ_mapa = 0 vale para el mapa, no para el estadístico: el umbral se fija sobre
la grilla observada, así que la cobertura de calibración ya se desvía de `q` cuando hay empates») y remitir a
ella desde §4.5/§5.

---

## 4. Hallazgos de gravedad BAJA (cosméticos, notación y robustez)

| # | Dónde | Qué |
|---|---|---|
| B1 | `05_resultados.md:85` | «0.2337 frente a 0.0021, 109×»: la división de las cifras **redondeadas** da 111,3. El 109,2× sale de las medias sin redondear. Escribir «≈110×» o quitar el paréntesis |
| B2 | `03_marco_teorico.md:25` vs `04_metodo.md:57` | La misma entropía aparece como `log n` y como `ln n`. Con `log` decimal la tabla 3.1 daría −0,566 en vez de 0,320: la base es `e`. Unificar en `ln n` |
| B3 | `.tex` §5 | `C_{\text{jev}}` y `C_{\mathrm{Jev}}` en el mismo PDF; `C_{\max}`, `C_{\text{pmax}}` y `pmax` para el mismo objeto; `\mathrm` y `\text` mezclados |
| B4 | `03_marco_teorico.md:28` vs `04_metodo.md:58` | `C_noul(p) = max(p, 1−p)` (vector) frente a `C_noul = max(π, 1−π)` (`π` no definida en el paper) |
| B5 | `07_conclusion.md:32` | «DEF-1..DEF-8»: el paper solo nombra DEF-1..DEF-5 |
| B6 | `04_metodo.tex:69` | Único `§4.7` literal; el resto usa `Sección~\ref{}` |
| B7 | `01_introduccion.md:58` | El `.md` (fuente de verdad) contiene `\texttt{10.5281/…}` literal |
| B8 | `.ref` de la Fig. 4 | `docs/citar_flotantes.py` la insertó al final del párrafo que habla de `n_empates_tau`: la figura no muestra esa columna. Revisar a mano las 8 frases que añadió |
| B9 | Fig. 2 | El primer bin (0–0,0167) tiene **5.607** decisiones; el pie identifica la barra entera con las 2.167 saturadas. «El pico en cero (2.167 saturadas de 5.607 en el primer bin)» |
| B10 | Fig. 3 | Las barras del mapa miden 0,0021 sobre un eje de 0–0,31 (0,7 % de la altura): el «109×» se sostiene en el rótulo, no en la comparación visual. Anotar también el valor |
| B11 | Fig. 6 | «IQR» con índices truncados (`v[int(0.25n)]`) en vez de percentiles interpolados; desvío máximo 0,021 |
| B12 | Fig. 7 | La diagonal se pinta en gris claro, casi el mismo tono que Δ≈0 en `RdBu_r`; y `heatmap_paper` usa `set_title` por panel, lo que contradice la regla R2 tal como está escrita |
| B13 | `src/matriz/figura.py:126` | `n = int(n_objetivo) if … else ns[0]` elige la **cardinalidad más baja**: con `typed-decisions` dibujaría `n = 2` en silencio |
| B14 | `compilar.sh:17` | `latexmk -c` borra `main.log`, así que la verificación documentada (`grep -cE "^!|undefined" main.log`, `grep -c Overfull main.log`) es imposible justo después de compilar |
| B15 | `transferencia.py:41-47` | `umbral_para_cobertura` promete «menor τ con cobertura ≤ q» y el *fallback* devuelve `vals[-1]` con cobertura > q en silencio (y `IndexError` si la lista está vacía) |
| B16 | `definiciones.py:24-29` | `conf_jev` no recorta: con `p_max < 1/n` devuelve **negativo** (`conf_jev([0.01]*77) = −0.0030`), violando el rango `[0,1]` de DEF-1. No ocurre en el corpus sellado, pero es el régimen de la rejilla 0.01 con cardinalidad alta |
| B17 | `definiciones.py:32-38` | `conf_ent` no renormaliza `p`: 366 de 14.277 filas del brazo pagado suman 0,99 (sesgo máximo +0,0053). Y recorta a `[0,1]` mientras `conf_jev`/`conf_margin` no: tratamiento de bordes inconsistente |
| B18 | `matriz.py:247` + `informe_matriz.py:76` | `n_empates_tau` se cuenta en **calibración** y se divide por `n_items_te` (**prueba**): el corte «<5 %» es en realidad ≈6,25 % de la calibración. No mueve ninguna cifra (el subconjunto sigue siendo 312) |
| B19 | `matriz.py:42` | Import muerto de `bootstrap_delta`; hay **dos** bootstraps con el mismo contrato (numpy y stdlib) y el p «bilateral» es un p de Wald por percentiles, no un bootstrap recentrado bajo H₀ (3.165 de 3.564 celdas con `p = 0` exacto) |
| B20 | `medir.py:123-160` | No reanuda ni escribe incremental: un fallo en el ítem 14.000 de una corrida pagada pierde y **vuelve a cobrar** todo |
| B21 | `backend_typesafe.py:239-241` | `costo_por_mil_decisiones()` divide por *requests* y se documenta por 1.000 **ítems**: en `typed-decisions` (5 decisiones por request) sobreestima el costo **5×** |
| B22 | `STATE.json:220` | «26 de tablas + 8 de Proposiciones = 50»: 26+8 = **34**; medido son 34 en tablas/citas + 16 en prosa = 50. Y «14 flotantes citados» → son **24** (8 figuras + 16 tablas) |
| B23 | `STATE.json:63,141,143` | «52 tests en total (63 desde el 19-oct)» (hoy 67), «`02_referencias.bib` (36 ítems)» (son 43 entradas; 36 citadas), «`docs/` 9 guías» (son 13) |
| B24 | `.hermes.md:87` | `.venv/bin/python src/matriz/correr_matriz_pagado.sh` — es un script de shell: debe ser `bash` |
| B25 | `.hermes.md:48`, `AGENTS.md:141`, `README.md:483`, `informe-blindaje…` | Fecha del pre-registro «08-oct-2026»; la API de Zenodo y la errata E6 dicen **09-oct** |
| B26 | `AGENTS.md:135,146,143,145` | «las extensiones todavía no están dentro del paper» (están, §5.8 desde el 25-oct), pendiente #6 «integrar las extensiones» (hecho), «formato IEEE pendiente» (hecho), «PDF 11 págs» (13). `AGENTS.md` está protegido: hay que pedírselo al autor |
| B27 | `README.md:4,246` | «Última actualización: 25-oct» (se tocó el 28) y «el PDF vigente tiene 12» (13) |
| B28 | `docs/handoff-t440.md:130` | «`clinc150` no medido»: hay **9.300** filas de `clinc150`; la limitación es solo del checkpoint base de Laya |
| B29 | `STATE.json:104-105` vs README §10-ter | `STATE.json` sigue ordenando crear el repo nuevo `decision-calibration-bench`; README, la guía (fase 4) y `.hermes.md` recomiendan **no** crearlo |
| B30 | `paper/02_referencias.bib` | `waynechang` y `awesomejev` no se usan ni se necesitan: decidir entre citarlas o borrarlas |
| B31 | `CITATION.cff` | `date-released: 2026-10-10` no coincide con el tag (10-12) ni con Zenodo (10-13) |
| B32 | `matriz.py:319` | El comentario dice «FDR sobre el conjunto principal (nivel raw, q principal) y se propaga»; el código aplica BH **una sola vez sobre las 3.564 celdas** (3 niveles × 3 q mezclados). Defendible como corrección global conservadora, pero no es lo que dice el comentario ni lo que declara `RESUMEN_MATRIZ.md` §0 («BH-FDR α=0.05», sin familia) |

---

## 5. El plan de corrección, en orden de riesgo

Todo lo de abajo se hace **sin volver a medir** (salvo el bloque D, que es opcional) y **tocando siempre el par
`.md` → `.tex` → recompilar**.

### Bloque A — el PDF deja de tener defectos visibles (≈1 h)
1. **A8** Fig. 2: acortar el rótulo del eje X → `python src/figuras_paper.py` → `pdftotext -bbox` para confirmar.
2. **M2** `\spanishdecimal{.}` en `main.tex` → recompilar → `pdftotext main.pdf - | grep -cE "[0-9]+,[0-9]+"`
   debe dar 0.
3. **M1** devolver la columna `empate medio de τ` a `tab:porte-pagado` (o reescribir el pie).
4. **M20** `pdf.fonttype = 42` → regenerar figuras → `pdffonts` sin `Type 3`.
5. **M21** leyenda de la Fig. 5 en dos filas, etiquetas `≤0.05` / `0.05–0.30` / `>0.30`.
6. **B8** revisar a mano los 8 `\ref` que insertó `docs/citar_flotantes.py`.

### Bloque B — afirmaciones que hoy son falsas (≈2 h, cero medición nueva)
7. **A2** §5.7 «en el paso 0» + §5.8.2 «a diferencia de la corrida confirmatoria» + corregir E4.
8. **A3** «checkpoints entrenados» en §5.8.2 (paper, `STATE.json`, `README.md`, `.hermes.md`).
9. **A5** §6.1 con 0.076/0.257 y 0.0013 (mediana) / 0.0049 (media).
10. **A6** §4.3 y E3: `noul` no entra en la matriz.
11. **A7** §6.2: quitar `C_mar` o restringirlo a `n = 2`.
12. **M5** abstract/§1/Prop. 3: «incompatibilidad **de forma**».
13. **A4** etiquetar `L0`/`L1` con el filtro (o quitarlo y regenerar el informe).
14. **M3** título de la tabla §5.5: «nivel `raw`, `q = 0,80`».
15. **A1** arreglar `precision()` + test + regenerar CSV y RESUMEN (no mueve ninguna cifra del paper).
16. **B23/B22/B25/B24/B27** aritmética y fechas de `STATE.json`, `README.md`, `.hermes.md`.
17. **M14** propagar 0.1735/0.1315 y la tabla §10-quater correcta a README/AGENTS/`.hermes.md`/
    `validacion-productos`.
18. **M15/M16/M17** guía de cierre sin tareas cerradas; validación con 67 tests, figuras nuevas y ORCID 3;
    ejemplo de la librería con 0.24/0.21.
19. **M18** re-exportar `conf_score` y `score_mad_unif` en `jev_conf_metrics/__init__.py`.
20. **M22** añadir la **errata E7** (Δ_mapa = 0 vale para el mapa, no para el estadístico: el umbral se fija
    sobre la grilla observada y los empates ya desvían la cobertura de calibración) y remitir desde §4.5/§5 de
    la especificación.
21. **M6/M7/M8/M9/M10/M11/M12** bibliografía (ver §6 de este informe).

### Bloque C — calidad de envío (≈3 h, decisión del autor)
22. **M6** citar en §5–§7 (es la corrección con más efecto sobre la percepción del paper).
23. **M9/M10** corregir las dos entradas con metadatos falsos.
24. **M11** sacar las `note` de la bibliografía (a prosa del cuerpo o filtro en el `.bbl`).
25. **M8** añadir los 9 DOI que ya existen + URL de `geifman2017`/`jitkrittum2023`.
26. **M12** `platt1999` → `@incollection`; `angelopoulos2021` → `@misc` con `eprint`.
27. **M7** añadir Benjamini–Hochberg 1995 y la referencia de Qwen3.5-0.8B-Base; citar los 4 artefactos propios.
28. **M13** crear `paper/secciones/00_resumen.md` con el abstract.
29. **B2/B3/B4/B5** pasada de notación (`ln n`, `C_{\text{Jev}}`, `C_{\max}`, `\pi`).

### Bloque D — código (opcional ahora, obligatorio antes de un `v1.1.0` con PyPI)
30. **M4** el ulp del mapa `margin` (regenerar matriz y revisar las 9 celdas; el titular no cambia).
31. **M19** `NaN` en `bh_fdr`; **B15** fallback de `umbral_para_cobertura`; **B16/B17** bordes de
    `conf_jev`/`conf_ent`; **B14** `compilar.sh` sin `-c`; **B20** escritura incremental en `medir.py`;
    **B21** costo por decisión; **B19** un solo bootstrap.

---

## 6. Bibliografía: estado y correcciones concretas

| Clave | Problema | Corrección |
|---|---|---|
| `lakoreai2026` | Título inventado; autor con diacríticos que la firma no usa; «30 corridas» (el PDF dice 13) | Título real: *Dissecting RLCD: What Reinforcement Learning Does (and Doesn't) Do for Calibrated Typed Decisions*; `author = {Minh, Le Duc}`; nota a 13 corridas |
| `jev2026blog` | Nota «18-sep-2026» (la página dice **15-sep**); §1 repite el 18 | Quitar la fecha de la nota y corregir §1 a 15 de septiembre |
| `naeini2015`, `niculescu2005`, `brier1950`, `good1952`, `epstein1969`, `chow1970`, `zadrozny2002`, `vovk2005`, `efron1993` | Sin DOI (existe para todas) | `10.1609/aaai.v29i1.9602` · `10.1145/1102351.1102430` · `10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2` · `10.1111/j.2517-6161.1952.tb00104.x` · `10.1175/1520-0450(1969)008<0985:ASSPFP>2.0.CO;2` · `10.1109/TIT.1970.1054406` · `10.1145/775047.775151` · `10.1007/b106715` · `10.1201/9780429246593` (escapar `<`/`>` en `brier1950` y `epstein1969`) |
| `geifman2017` | Sin URL ni páginas (los índices discrepan) | `url = {https://proceedings.neurips.cc/paper/2017/hash/4a8423d5e91fda00bb7e46540e2b0cf1-Abstract.html}` |
| `jitkrittum2023` | Sin DOI (existe) | `10.52202/075280-0431` |
| `platt1999` | `@article` con `journal` = título del libro; es capítulo de MIT Press (2000) | `@incollection` con `booktitle`, `publisher = {MIT Press}`, `pages = {61--74}` |
| `angelopoulos2021` | `@article` con `journal = arXiv preprint…`, sin `eprint` | `@misc` con `eprint = {2107.07511}`, `archivePrefix = {arXiv}`, url a `/abs/` |
| `jevLite` | Nota «repo sin licencia» (la model card declara `license: gemma`) | Corregir o eliminar la nota |
| `roby1965` | Nota sobre una «versión previa de 1964» que ningún índice respalda | Quitar la nota (el año 1965 y el DOI son correctos) |
| `anyjev` | Autores: PyPI declara 4 personas; el `.bib` atribuye a la organización | Decidir (aceptable como está si se documenta) |
| Faltan | Benjamini–Hochberg (1995); Qwen3.5-0.8B-Base | Añadir ambas |
| Sin citar | `efron1993`, `layamultilingual`, `typeddecisions`, `opendecisionai` | Citar en §4.4, §4.1, §4.2 y §4.3/§6 |
| Sin citar | `awesomejev`, `waynechang`, `arXiv2609.26550` | Decidir: citar en §6 o borrar |

---

## 7. Lo que **no** es un error (para no reabrirlo)

- El PDF vigente tiene **13 páginas** y el preprint depositado en Zenodo **11**: son artefactos distintos y así
  está declarado.
- `docs/release-v1.0.0.md` (37 tests) y `release-v1.0.1.md` (52) son **snapshots históricos declarados**; su
  PDF coincide byte a byte con el depositado (md5 `c9d7d9bb…`).
- `paper/02_referencias.bib` y `paper/ieee/referencias.bib` son idénticos (md5 `20f169d3…`).
- Roby es **1965**, no 1964: Crossref, SafetyLit y OpenAlex dan 1965, y el DOI `10.1002/bs.3830100304` resuelve.
- 2.520 celdas sin mapa = 3.564 − 1.044 ✔ · «23 de 25 combinaciones» ✔ · 2,7× = 0.577/0.216 ✔ ·
  2,16 ≈ «factor de 2,2» ✔ · 79.462 = 65.185 + 14.277 ✔ · 7.092.972 = suma de los cinco datasets ✔.
- Las **cifras selladas no se mueven**: ningún arreglo del bloque A/B implica volver a medir ni regenerar la
  matriz, y el titular (312 celdas, 0.2337 vs 0.0021, 109,2×) queda intacto incluso aplicando el bloque D.
- El `main.pdf` del árbol aparece modificado solo por `/CreationDate` y `/ID` (recompilación de esta
  auditoría); `pdftotext` es idéntico.

---

## 8. Cómo volver a comprobar todo esto en un solo comando

```bash
cd ~/paper-tesis1
.venv/bin/python -m pytest -q                                     # 67 passed
.venv/bin/python src/matriz/informe_matriz.py && git diff --stat   # debe salir solo main.pdf (o vacío)
.venv/bin/python src/matriz/extension_conf_score.py               # 5.505 · 0.2724 → 0.2900
.venv/bin/python /home/arbues/.hermes/cache/scratch/audit/verify_master.py
cd paper/ieee && latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex
  grep -cE "^!" main.log          # 0
  grep -c Overfull main.log       # 0
  pdftotext main.pdf - | grep -c '??'                 # 0
  pdftotext main.pdf - | grep -cE "[0-9]+,[0-9]+"     # 0 tras M2
  pdffonts ../figures/*.pdf | grep -c "Type 3"        # 0 tras M20
```

*Informe generado el 28-oct-2026. Las cifras de este documento se recalcularon desde los artefactos del repo;
ninguna se copió de `STATE.json` ni de `README.md`.*

---

## 9. Cierre: qué se corrigió después de este informe (28-oct-2026)

Este informe describe el estado **antes** de las correcciones. Ese mismo día, y con la aprobación del autor,
se aplicaron el bloque A completo y las correcciones que arrastraba:

| # | Qué se hizo | Verificación |
|---|---|---|
| A1 | `precision()` corregida + 2 tests de regresión; `informe_matriz.py` recalcula la precisión desde los crudos para la tabla que publica; **errata E8**; §4.5 declara la excepción | re-ejecutada una celda completa: **todas** las columnas idénticas salvo `precision_A/B` (0.204 → 0.0176); 69 tests pasan |
| A2 | §4.1, nota de la tabla de §5.1, §5.7 y §5.8.2 distinguen **paso 0** / **corrida confirmatoria**; E4 corregida | 0 afirmaciones de «0 verificado»; el 869.310 queda atribuido al paso 0 |
| A3 | «checkpoints abiertos **entrenados**» + el control crudo explícito, en paper (`md`+`tex`), `STATE.json`, `README.md` y `.hermes.md` | 4 documentos con la misma redacción |
| A4 | filas `L0`/`L1` marcadas con `\dagger` + nota con las cifras sin filtro; etiquetas del generador corregidas | `RESUMEN_MATRIZ.md` regenerado; tabla del PDF con la nota |
| A5/A7 | §6.1 con 0.076/0.257 y 0.0013/0.0049; §6.2 restringe `C_mar` a `n = 2` | recalculado desde el CSV |
| A6 | §4.3 dice que `noul` **no entra** en la matriz; E3 corregida | `grep -c noul` en la matriz = 0 |
| A8 | rótulo de la Fig. 2 en dos líneas | `pdftotext -bbox`: máx 240,7 pt < 248,4 |
| M2 | `\spanishdecimal{.}`: se acabaron las comas decimales mezcladas con puntos | 0 comas decimales en el PDF (antes 31) |
| M20 | `pdf.fonttype = 42` en las dos librerías de figuras | `pdffonts`: **0** fuentes Type 3 (antes 8/8) |
| M21 | leyenda de la Fig. 5 en dos filas, etiquetas `≤ 0.05` / `0.05–0.30` / `> 0.30` | `pdftotext`: la leyenda ya no sale cortada |
| M14 | 0.1307 → **0.1735** (segundo) y la tabla por modelo correcta en `README.md`, `.hermes.md`, `docs/validacion-productos.md` | las 6 filas reproducen el CSV |
| — | Recuento de tests 67 → **69** en todo lo vivo (paper §1/§7, README, STATE, `.hermes.md`, `docs/`) | `pytest` = 69; `pdftotext` = 2 apariciones de «69 tests» |

**Queda pendiente** (sin aprobación todavía): M1 (columna `empate medio de τ` en `tab:porte-pagado`), M3 (filtro
de §5.5 en el título), M4 (ulp del mapa `margin` a `n = 2`), M5 («incompatibilidad de forma»), M6–M13
(bibliografía: citas en §5–§7, títulos y fechas, DOI/URL de 13 entradas, `note` impresas) y el bloque B de
cosméticos. Y `AGENTS.md` sigue con `0.1307` y «(67 tests)»: es un archivo protegido y la escritura fue
bloqueada; hay que aplicarlo a mano o autorizar el cambio.
