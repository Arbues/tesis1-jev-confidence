# Auditoría de estilo del paper IEEE — Tesis 1 (Jev `confidence`)

**Fecha:** 28-oct-2026 · **Repo:** `/home/arbues/paper-tesis1` · **Alcance:** `paper/ieee/secciones/*.tex` (7), `paper/secciones/*.md` (7), `paper/ieee/main.tex` (resumen y preámbulo).
**No se modificó ningún archivo del repo.** Conteos verificados de forma independiente el 28-oct-2026 (ver §8).

**Informe hermano:** `docs/auditoria-figuras-2026-10-28.md` — las 8 figuras del PDF: contenido,
legibilidad medida, redundancia con las tablas y errores de pie de figura (mismo commit, `b9068fd`).

---

## 0. Método y corpus medido

| Corpus | Archivos | Palabras | Uso |
|---|---|---|---|
| `.tex` (artefacto compilado) | 7 | **10.076** | fuente canónica de los conteos |
| `.md` (fuente de verdad declarada) | 7 | 8.349 | contraste; es casi paralelo al `.tex` |
| `main.tex` | 1 | 411 | resumen (abstract) |

Los conteos se obtuvieron con cinco scripts reproducibles (`audit_counts*.py` en este mismo directorio, salidas en `audit_counts*.txt`). **Todas las cifras de este informe son conteos de `grep`/regex sobre el texto, no impresiones.** Los `.md` y los `.tex` son versiones paralelas: un mismo vicio aparece dos veces en el repo, por lo que **cada arreglo debe aplicarse en ambos** para no reintroducirlo en la próxima recompilación.

Denominadores para leer las densidades: 10.076 palabras (§1–§7), 41 títulos (7 secciones + 32 subsecciones + 2 subsubsecciones), 24 `\caption`, 95 párrafos con prosa (66 de ellos con ≥2 oraciones), 16 tablas y 8 figuras.

---

## 1. Tabla resumen por categoría

| # | Categoría | Conteo verificado | Dónde (muestra) | Veredicto |
|---|---|---|---|---|
| **1** | Sintaxis `[Concepto]: [explicación]` y dos puntos explicativos | **106** `": "` (89 si se excluyen líneas con `\path`/`\url`); **36** negritas iniciales (17 de párrafo + 19 de ítem), de las que solo **3** contienen `:` | `05_resultados.tex:84`, `03:120-121`, `01:45` | **Mixto.** El patrón con dos puntos es marginal (3 de 36). El real es `[Concepto]. [explicación]` (**16** run-in heads de párrafo + **17** ítems de lista sin `:`). Forma legítima en IEEE; **la densidad no** (10,5 ‰, 1 dos puntos cada 95 palabras). |
| **2** | Tablas con columna clave-valor (`por qué`, `quién la usa`) | **4** cabeceras + **1** tabla sin cabeceras usada como lista de definiciones | `03:26`, `04:29`, `04:57`, `07:21`, `05:357-378` | **Mixto.** `rol`/`estado`/`quién la usa` son legítimas (tablas de método). `por qué` es coloquial y la tabla sin cabeceras **no es aceptable** en IEEE. |
| **3** | Titulares dramáticos / frases-gancho | **8 de 41** títulos (19,5 %); de ellos **4** son los citados por Gemini. Además **7** captions abren con gancho y **9** cierran con sentencia valorativa, de 24 | `05:61`, `05:97`, `05:152`, `01:81`, `05:91/132/147/159/193/203/265/298/326` | **Verdadero positivo (el más fuerte).** No es el volumen: es que el titular de §5 es un eslogan, no una descripción. |
| **4** | Aseveraciones categóricas de cierre de párrafo | **22 de 66** párrafos (33 %) cierran con oración ≤14 palabras; **49 de 66** cierran sin ninguna cifra | `05:85`, `05:155`, `05:259`, `05:382-383`, `06:18`, `06:24` | **Verdadero positivo**, concentrado en §5 y §6. |
| **5** | Ritmo «párrafo breve + lista numerada con negritas» | **4** `enumerate` + **4** `itemize` en 12 páginas; **19/19** ítems con negrita inicial | `01:56-71`, `04:92-112`, `06:32-38`, `07:44-48` | **Falso positivo como «ritmo»** (8 listas es *poco* para IEEE). **Verdadero positivo como negrita sistemática.** |
| **6a** | Negritas enfáticas en prosa | **213** `\textbf{}`: 26 en tablas + **187 en prosa** = 1 negrita cada 43 palabras (23 ‰) | `05:63-64`, `05:126`, `07:6` | **Verdadero positivo, el más objetivo de todos.** En cuerpo IEEEtran el valor esperado es ~0. |
| **6b** | Antítesis «X, no Y» | **12** (1,2 ‰) | `05:155` «el par, no la media global»; `05:465`; `06:20` | **Verdadero positivo moderado.** Es el quiasmo de cierre favorito del texto. |
| **6c** | «no solo X sino Y» / «en otras palabras» / «es importante destacar» | «no solo»: **4**, pero **0** con la estructura completa «sino»; los otros dos: **0 / 0** | `06:10`, `06:16`, `06:22`, `07:46` | **Casi falso positivo.** La muletilla completa no existe; sí hay **1 escalada retórica** (`06:22` «no solo cambia una métrica de calibración, cambia la \textbf{política de abstención}») que conviene revisar. |
| **6d** | «en otras palabras» / «es importante destacar» | **0** y **0** («es decir»: 2; «por tanto»: 2) | `03:137`, `05:84` | **Falso positivo.** Conectores normales, en dosis bajas. |
| **6e** | Rayas largas `---` como inciso | **8** ocurrencias = **4 pares** (0,8 ‰) | `01:9`, `04:8-9`, `05:387`, `05:427`, `05:458-459` | **Falso positivo.** Uso correcto de raya en español y dosis moderada. |
| **6f** | Metáforas («viaja», «colapsa», «manda», «engaña») | **24** ocurrencias; «no viaja» **10**; «titular» (vocabulario de prensa) **5** | `01:78`, `02:47`, `05:160`, `05:193`, `05:291` | **Mixto.** «Transferencia de umbral» es término técnico; **el eslogan** («El número no viaja; el mapa sí», «el promedio engaña») no. |
| **6g** | «La lectura es…» / resumen de una frase | **3** | `05:291` «La lectura es directa:»; `05:456` «La lectura es en dos partes»; `06:6` «La primera lectura de la matriz es una sola frase:» | **Verdadero positivo.** Fórmula de blog, tres veces. |
| **6h** | Enumeración romana `(i)…(ii)` en prosa | **6** en **3** bloques | `05:184-186`, `05:418-421`, `05:456-460` | **Verdadero positivo leve** (descomposición retórica binaria). |
| **6i** | Captions que repiten el cuerpo (≥8 palabras literales) | **8** de 24 | `05:68`, `05:91`, `05:106`, `05:298`, `05:326`, `05:359` | **Verdadero positivo no señalado por Gemini.** Viola el criterio IEEE de caption autocontenido y no redundante. |
| **6j** | Tríadas de adjetivos/sustantivos | **2** | `01:11` «clasificar, enrutar, verificar, abstenerse»; `01:60` «dominio, rango, monotonía» | **Falso positivo / débil.** Dos en 10.000 palabras no es firma de nada. |
| **6k** | Frases cortas tipo staccato | mediana de oración **18–25 palabras**, media **21** | — | **No se cumple.** El texto no es staccato; el ritmo roto está al **final** de los párrafos, no en las oraciones. |

---

## 2. Detalle con evidencia literal

### C1 · Dos puntos y `[Concepto]: [explicación]`

Lo que Gemini describe como «sintaxis `[Concepto]: [explicación]` en listas» **casi no existe en esa forma**. El conteo real:

| Forma | Nº | Ejemplo literal |
|---|---|---|
| Negrita de párrafo que cierra en `.` (una de ellas con `:` interno) | **16** | `01_introduccion.tex:56` `\textbf{Contribuciones.}` · `02:8` `\textbf{Calibración de clasificadores.}` · `03:102` `\textbf{Consecuencia: el fallo tiene dos capas.}` · `06:8` `\textbf{Capa 1, la escala.}` |
| Negrita de párrafo sin puntuación final | **1** | `04_metodo.tex:71` `\textbf{Decisiones totales medidas: 65\,185}` |
| Ítem de lista con negrita terminada en `:` | **2** | `03:120` `\item \textbf{porte directo:} $\tau_B := \tau_A$` · `03:121` `\textbf{porte con mapa:}` |
| Ítem de lista con negrita sin `:` | **17** | `04:97` `\textbf{Umbral objetivo.}` · `06:33-37` (5 ítems de Limitaciones) · `07:45-47` |
| **Total negritas iniciales** | **36** | 17 de párrafo + 19 de ítem |

Dos puntos totales: **106** en 10.076 palabras = **10,5 ‰** (uno cada 95 palabras). Reparto: §1 15,6 ‰ · §2 7,2 ‰ · §3 11,5 ‰ · §4 7,2 ‰ · **§5 10,6 ‰ (43 de 106)** · §6 11,4 ‰ · §7 9,6 ‰.

Marcos retóricos explícitos (cada uno 1 vez, patrón de plantilla): `01:23` «Y aquí está el problema:» · `01:45` «El efecto es inmediato:» · `05:84` «Es decir:» · `05:291` «La lectura es directa:» · `05:456` «La lectura es en dos partes» · `06:6` «es una sola frase:» · `06:22` «la conclusión práctica es que».

> **Veredicto:** el run-in head en negrita **es práctica IEEE legítima** (así se escriben las subsecciones de un survey). El problema no es la forma sino la **densidad** (36 arranques en negrita en 12 páginas, cuando el estándar sería `\subsubsection` o párrafo sin marca) y la **negrita dentro de la frase**, que es otra categoría (6a).

### C2 · Tablas clave-valor

| Archivo:línea | Cabecera literal | Veredicto |
|---|---|---|
| `03_marco_teorico.tex:26` | `definición & fórmula & dominio & quién la usa` | Legítimo (rol de cada implementación) |
| `04_metodo.tex:29` | `configuración & familia & parámetros & papel` | Legítimo |
| `04_metodo.tex:57` | `dataset & $n$ (cardinalidad) & ítems & por qué` | **Coloquial.** «por qué» como cabecera es registro de diapositiva; en IEEE sería «criterio de inclusión» o «rol en el diseño». |
| `07_conclusion.tex:21` | `\# & Artefacto (y dónde vive) & Estado` | Legítimo (tabla de artefactos es estándar) |
| `05_resultados.tex:357-378` | tabla **sin cabeceras** (`Brecha, mediana con 4 definiciones & 0.272`) | **No aceptable.** Es una lista de definiciones disfrazada de tabla; en el `.md` es una tabla de dos columnas con encabezado vacío (`05_resultados.md:225` `\| | |`). IEEE espera cabecera o prosa. |

> **Veredicto:** 3 de 5 usos son correctos. El problema real es la **tabla sin cabeceras** de §5.8.1, no la existencia de columnas de rol.

### C3 · Titulares y pies de figura (el núcleo del problema)

Los cuatro ejemplos que citó Gemini existen y están verificados literalmente:

| Archivo:línea | Texto literal | Diagnóstico |
|---|---|---|
| `05_resultados.tex:61` | `\subsection{El objeto de la tesis, en una cifra}` | Gancho de blog: el título no dice **qué** mide la subsección (la brecha entre definiciones). |
| `05_resultados.tex:97` | `\subsection{El número no viaja; el mapa sí}` | Eslogan con punto y coma; duplica el claim de §3.102 y de §6.6 → el lector lo lee tres veces. |
| `05_resultados.tex:152` | `\subsection{El promedio no es el resumen: la estructura está en el par}` | Dos tesis en un título; «la estructura está en el par» es interpretación, no contenido. |
| `01_introduccion.tex:81-82` | `La aportación sobrevive al hueco: cualquiera que afirme que los umbrales no transfieren tendrá que \textbf{citar la matriz}, no reemplazarla.` | Cierre de desafío («tendrá que») + metáfora mezclada («sobrevive al hueco»). |

Otros cuatro títulos con marca: `05:261` «Dónde el umbral no viaja (…)», `05:341` «Quinta definición del campo: `conf_score` (…)» (dos puntos descriptivos: aceptable), `05:390` «Brazo pagado: el modelo detrás del campo» (gancho), `06:20` «El umbral es una política, no un número suelto» (antítesis).

**Captions con gancho (7):** `05:91` «La cifra central: (…)» · `05:132` «El titular: el porte directo (…)» · `05:147` «La Proposición 1 sobre los datos: (…)» · `05:159` «(…) La mediana del par manda sobre la media global: el promedio engaña.» · `05:193` «El promedio engaña: la estructura está en el par.» · `05:265` y `05:298` «Dónde el umbral no viaja: …».

**Captions con cierre valorativo (9):** `04:21`, `04:49`, `05:55`, `05:91`, `05:147`, `05:203`, `05:265`, `05:298`, `05:326`. Ejemplo: `05:203` «(…) **El umbral solo viaja a cardinalidad alta.**»

> **Veredicto: verdadero positivo.** En IEEE el caption describe qué se ve y qué eje tiene; la tesis va en el cuerpo. Aquí el caption **argumenta**. Los 4 títulos citados por Gemini son correctos como diagnóstico.

### C4 · Cierres categóricos

Métrica: de 66 párrafos con ≥2 oraciones, **22 (33 %)** terminan con una oración de ≤14 palabras, y **49 (74 %)** terminan con una oración sin ninguna cifra. Ejemplos:

| Archivo:línea | Cierre literal | Palabras |
|---|---|---|
| `05:155` | `El titular es el par, no la media global.` | 9 |
| `05:259` | `Es la distinción entre el número y el mapa.` | 9 |
| `05:382-383` | `Se declara el límite en lugar de inventar la escala.` | 10 |
| `05:424` | `La especificación describe el servicio real, no una reconstrucción.` | 9 |
| `06:18` | `el costo de confundir «mismo orden» con «mismo número».` | 9 |
| `06:8` | `Es la diferencia entre copiar la cifra y traducirla.` | 9 |
| `06:24` | `no descubre que hay sobre-confianza (…) sino que \textbf{cuantifica el error de trasladar el umbral entre ellas}` | — |

> **Veredicto: verdadero positivo.** No es que el texto sea categórico (los datos lo son); es que **cada párrafo remata con una máxima**. Un paper IEEE cierra párrafos con el dato o con la transición, no con la moraleja.

### C5 · Párrafo breve + lista con negritas

8 listas en 12 páginas (4 `enumerate`: `01:58`, `03:114`, `04:92`, `05:309`; 4 `itemize`: `03:119`, `04:150`, `06:32`, `07:44`). **19 de 19** ítems llevan negrita inicial. Los párrafos-introductorios son de 2 a 26 palabras (`01:56` «**Contribuciones.**» solo; `07:42` «El arco completo tiene tres etapas, y esta tesis cubre la primera.»).

> **Veredicto: falso positivo como «ritmo»** (la densidad de listas es baja para un paper de 12 páginas y las listas son apropiadas: contribuciones, procedimiento, limitaciones, trabajo futuro). **Verdadero positivo solo en el rasgo «todo ítem empieza en negrita»**, que es la firma visual del texto generado.

### C6 · Marcadores adicionales

**6a — Negritas (el tell más objetivo).** 213 `\textbf{}` en total; 26 dentro de tablas (legítimas, resaltan el subconjunto principal: `05:116` `\textbf{0.2337}`), **187 en prosa** sobre 8.114 palabras de prosa = **23 ‰**. Por sección: §1 **34,5 ‰** (una negrita cada 29 palabras), §2 25,2 ‰, §7 23,3 ‰, §3 23,0 ‰, §6 21,8 ‰, §4 18,7 ‰, §5 17,2 ‰. En IEEEtran el cuerpo va en redonda: **el valor esperado es 0**. Esto es un artefacto de `**negrita**` de Markdown importado al `.tex`, y es lo que un revisor detecta primero como «no es un paper».

Ejemplos: `05:63-64` `\textbf{65\,185} distribuciones` · `05:126` `\textbf{del orden de cien veces más}` · `07:6` `\textbf{23 grupos, 65\,185 decisiones y 3\,564 celdas} \textbf{no viaja entre implementaciones}` · `06:8` `\textbf{igual}`.

**6b — Antítesis «X, no Y»: 12.** `05:148` «no el mapa» · `05:155` «no la media global» · `05:316` «no un fallo de Kev» · `05:424` «no una reconstrucción» · `05:465` «no la equivalencia» · `06:20` «no un número suelto» · `07:50` «no para un conjunto fijo de modelos».

**6f — Metáforas: 24 ocurrencias.** Núcleo: «no viaja» (10: `02:47`, `03:103`, `03:131`, `05:97`, `05:261`, `05:265`, `05:298`, `06:6`, `06:8`, `07:6`), «el promedio engaña» (2), «manda sobre» (1), «colapsa» (1), «el hueco» (2), «floreció» (1), «abrió la categoría» (1), «puertas adentro» (1), «desastres» (1), «suelo» (2), «titular» (5: `04:9`, `05:99`, `05:132`, `05:155`, `05:459`).

Frase hecha que hay que mirar con lupa: `05:147` «Con el mapa el error **colapsa al suelo** que imponen los empates del umbral, no el mapa.»

> **Veredicto: mixto.** «Transferencia de umbral» / «no transfiere» es la terminología estándar del campo (Chow, Geifman) y **debe quedarse**. Lo que sobra es la **esloganización** («El número no viaja; el mapa sí») y el léxico periodístico («titular» cinco veces).

---

## 3. Hallazgos propios (no señalados por Gemini)

| # | Hallazgo | Evidencia | Por qué importa |
|---|---|---|---|
| H1 | **187 negritas en prosa** (1 cada 43 palabras; §1 una cada 29) | conteo de `\textbf{}` fuera de `tabular` | Es el tell mecánico más fuerte y el más fácil de arreglar. |
| H2 | **8 captions repiten frases del cuerpo (≥8 palabras literales)** | `05:68`, `05:91`, `05:106`, `05:298`, `05:326`, `05:359`, `05:399` vs. cuerpo | Caption no autocontenido/no redundante: criterio IEEE. Ej.: `05:91` repite `05:84-86` casi palabra por palabra. |
| H3 | **Tabla de §5.8.1 sin cabeceras** usada como lista de definiciones | `05:357-378` / `05:364` `\begin{tabular}{@{}lr@{}}` | Rechazo seguro en revisión. |
| H4 | **Metáfora con sujeto agente**: «**El ecosistema** sí entrena (…)», «el ecosistema los porta» | 20 ocurrencias de «el ecosistema» como sujeto | Antropomorfiza un conjunto de repositorios; además dos de esas frases son generalizaciones sin cita (`05:49-50`, `05:56-57`). |
| H5 | **Resumen termina en eslogan** | `main.tex:62-63` «La contribución no es el hallazgo sino el instrumento: sobrevive a él y mide cualquier implementación futura.» | El abstract es lo primero que se lee; el registro debe ser medido. |
| H6 | **Claim de creencia atribuida sin cita**: «Dos pares que **se creían** distintos» | `07:8` | Afirma un estado de la literatura sin referencia; un revisor lo pide. |
| H7 | **Tesis repetida 4 veces con la misma frase** («el número no viaja… el mapa sí») | `03:103`, `05:97`, `06:8`, `07:7-8` | Además de estilo, es redundancia estructural: se puede decir una vez y referenciar. |
| H8 | **Framing binario «Dos X»** como apertura | `05:184` «Dos de las coincidencias», `05:418` «Dos observaciones», `05:456` «en dos partes», `07:8` «Dos pares», `04:69` «Las dos ausencias» | Patrón de «toda idea viene en pares»; 5 aperturas. |
| H9 | **Densidad de dos puntos 10,5 ‰** (43 en §5) | §5 | El dos puntos explicativo sustituye a la subordinación; en un paper cansa. |

---

## 4. Contraste con los señalamientos de Gemini

| Señalamiento | ¿Se verifica? | Matiz |
|---|---|---|
| 1) `:` para definir en listas / `[Concepto]: [explicación]` | **Parcialmente** | Solo **3** casos con `:` (`03:102`, `03:120`, `03:121`). El patrón dominante es `[Concepto]. [explicación]` (16 párrafos + 17 ítems). |
| 2) Tablas clave-valor «por qué» / «quién la usa» | **Sí, 4 casos** | 3 de 4 legítimos; el problema serio es la tabla **sin cabeceras** (`05:357`). |
| 3) Titulares y pies dramáticos | **Sí** | Los 4 textos citados existen literales en `05:61`, `05:97`, `05:152`, `01:81-82`. Es el diagnóstico más certero. |
| 4) Aseveraciones categóricas de cierre | **Sí** | 22/66 párrafos (33 %) con cierre ≤14 palabras. |
| 5) Ritmo «párrafo breve + lista numerada con negritas» | **Parcialmente** | Las listas son pocas (8); lo sistemático es la **negrita en cada ítem** (19/19). |
| 6) «no solo X sino Y» | **Casi no** | 4 apariciones de «no solo», **ninguna** con el «sino» del cliché; 1 de ellas (`06:22`) es una escalada retórica del mismo tipo. |
| 6) «en otras palabras» / «es importante destacar» | **No** | **0** y **0**. |
| 6) Rayas largas | **Sí, pero irrelevante** | 4 pares: uso correcto y moderado en español. |
| 6) Metáforas «viaja / colapsa» | **Sí** | 24 ocurrencias; pero «transferencia» es término técnico: hay que distinguir término de eslogan. |
| 6) Tríadas | **No** | 2 en 10.000 palabras. |

---

## 5. Los 10 arreglos de mayor impacto (antes → después)

Ordenados por relación impacto/esfuerzo. Todos son de edición local, no reescritura.

**1. Tres títulos de §5 (el eslogan como título).**
- `05_resultados.tex:61` · antes: `\subsection{El objeto de la tesis, en una cifra}` → después: `\subsection{Brecha entre definiciones sobre las 65\,185 distribuciones}`
- `05:97` · antes: `\subsection{El número no viaja; el mapa sí}` → después: `\subsection{Porte directo frente a porte con mapa cerrado}`
- `05:152` · antes: `\subsection{El promedio no es el resumen: la estructura está en el par}` → después: `\subsection{Caída de cobertura por par de definiciones}`

**2. Cierre de la introducción (desafío al lector).**
- `01:81-82` · antes: `La aportación sobrevive al hueco: cualquiera que afirme que los umbrales no transfieren tendrá que \textbf{citar la matriz}, no reemplazarla.`
- después: `Toda afirmación posterior sobre la transferencia de umbrales puede contrastarse contra esta matriz, que se regenera con un comando.`

**3. Captions que argumentan (9 casos).** Regla: primera oración = qué se ve; segunda = eje/unidad; cero tesis.
- `05:193` · antes: `El promedio engaña: la estructura está en el par. Hay pares (…) y la media global borra esa bimodalidad.`
- después: `Caída de cobertura por par de definiciones (nivel \texttt{raw}), ordenada por mediana. Los pares \texttt{margin}$\leftrightarrow$\texttt{jev} y \texttt{pmax}$\to$\texttt{ent} ocupan los extremos (0.0023 y 0.7667).`
- `05:132` · antes: `El titular: el porte directo del umbral (sin transformar) se equivoca (…)` → después: `$\lvert\Delta\rvert$ del porte directo frente al porte con mapa, celda a celda (nivel \texttt{raw}, subconjunto sin empates dominantes).`

**4. Las 187 negritas en prosa.** Dejar negrita solo en tablas (26) y, si se quiere, en los run-in heads de §2.
- `05:63-64` · antes: `Sobre las \textbf{65\,185} distribuciones medidas (…)` → después: `Sobre las 65\,185 distribuciones medidas (…)`
- `05:126` · antes: `El porte directo se equivoca \textbf{del orden de cien veces más}` → después: `El porte directo se equivoca del orden de cien veces más`
- `07:6` · antes: `\textbf{23 grupos, 65\,185 decisiones y 3\,564 celdas} … \textbf{no viaja entre implementaciones}` → después: sin negritas.

**5. Cierres-máxima (22 casos).** Criterio: si la última oración no aporta dato ni transición, se funde con la anterior.
- `05:155` · antes: `(…) pares que fallan en grande. El titular es el par, no la media global.` → después: `(…) pares que fallan en grande; por eso la tabla se ordena por la mediana del par y no por la media global.`
- `05:259` · antes: `(…) aunque el orden sea el mismo. Es la distinción entre el número y el mapa.` → después: `(…) aunque el orden sea el mismo (Sección 3.4).`
- `05:382-383` · antes: `Se declara el límite en lugar de inventar la escala.` → después: `El supuesto ordinal no se extiende a los datasets nominales.`

**6. Fórmulas de lectura («La lectura es…» / «Es decir:»).**
- `05:291` · antes: `La lectura es directa: hay celdas en las que portar el umbral \textbf{pierde toda la cobertura}.` → después: `Hay celdas en las que portar el umbral pierde toda la cobertura.`
- `06:6` · antes: `La primera lectura de la matriz es una sola frase: un umbral de \texttt{confidence} no viaja entre implementaciones.` → después: `El resultado principal es que un umbral de \texttt{confidence} no transfiere entre implementaciones.`
- `05:84` · antes: `Es decir: en el caso típico, (…)` → después: `En el caso típico, (…)`

**7. Tabla sin cabeceras de §5.8.1.**
- `05:357-378` · antes: `\begin{tabular}{@{}lr@{}}` con filas `Brecha, mediana con 4 definiciones & 0.272`
- después: dos columnas con cabecera — `estadístico & valor` — o, mejor, prosa: `La brecha mediana pasa de 0.272 (cuatro definiciones) a 0.290 (cinco); el ECE global de $C_{\text{score}}$ es 0.241 frente a 0.184--0.237 de las otras cuatro.`
- `04:57` · antes: `dataset & $n$ (cardinalidad) & ítems & por qué` → después: `dataset & $n$ & ítems & criterio de inclusión`

**8. Metáforas esloganizadas → término técnico.**
- `05:160` · antes: `La mediana del par manda sobre la media global: el promedio engaña.` → después: `La mediana por par describe la distribución; la media global la oculta.`
- `05:147` · antes: `Con el mapa el error colapsa al suelo que imponen los empates del umbral, no el mapa.` → después: `Con el mapa el error se reduce hasta el límite que imponen los empates del umbral, no el mapa.`

**9. «Titular» (5 usos, vocabulario de prensa).**
- `05:99` · antes: `El titular es sobre el \textbf{nivel principal \texttt{raw}}, que es el que congela el pre-registro.` → después: `El resultado principal corresponde al nivel \texttt{raw}, que es el que congela el pre-registro.`
- `05:459` · antes: `(…) por eso el titular de este trabajo es el par de definiciones, no el modelo.` → después: `(…) por eso la unidad de análisis de este trabajo es el par de definiciones, no el modelo.`

**10. Resumen y §7: quitar el eslogan y la creencia atribuida.**
- `main.tex:62-63` · antes: `La contribución no es el hallazgo sino el instrumento: sobrevive a él y mide cualquier implementación futura.` → después: `La contribución es el instrumento de medición, que se aplica a cualquier implementación futura del campo.`
- `07:8` · antes: `Dos pares que se creían distintos resultan ser la \textbf{misma} fórmula` → después: `Dos pares que la documentación registra como definiciones distintas coinciden algebraicamente` (con la cita de la documentación).

---

## 6. Qué NO hay que tocar (registro académico correcto)

| Elemento | Dónde | Por qué se queda |
|---|---|---|
| Subtítulos descriptivos de §3 y §4 | `03:4` Notación · `03:54` Calibración frente a discriminación · `03:110` Transferencia de umbrales (definición formal) · `04:13` Modelos bajo medición · `04:139` Trazabilidad (regla D4) · `04:148` Alcance no cubierto, declarado antes de los resultados | Son títulos IEEE modélicos: dicen el objeto y el alcance, sin veredicto. |
| Tres `quote` con **Proposición 1/2/3** en negrita | `03:78-100` | Convención matemática estándar; la negrita ahí es estructural, no énfasis. |
| Run-in heads de §2 | `02:8`, `02:17`, `02:24`, `02:30`, `02:35`, `02:46` | Es la forma habitual de organizar un estado del arte en IEEE. Si se quiere más canónico, convertir a `\subsubsection` — pero **no borrar**. |
| Negritas **dentro de tablas** (26) | `05:116`, `05:367`, `05:373`, `05:444` | Resaltar la fila del subconjunto principal es convención de tabla, no énfasis retórico. |
| Tabla de artefactos con columna «Estado» | `07:14-36` | Estándar en papers con artefacto/software. |
| Rayas largas (4 pares) | `01:9`, `04:8-9`, `05:387`, `05:427`, `05:458-459` | Uso correcto de la raya en español; cantidad moderada. |
| Frases largas (mediana 18–25 palabras) | todo el texto | Registro técnico correcto. **No acortar por «legibilidad»**: el problema está en los cierres, no en la longitud. |
| Conectores «es decir» (2), «por tanto» (2), «de modo que» (4), «sin embargo» (1) | — | Dosis normales; el texto **no** abusa de muletillas. |
| Listas de contribuciones, procedimiento, limitaciones, trabajo futuro | `01:58`, `04:92`, `06:32`, `07:44` | Estructura IEEE esperada. Solo hay que quitar la negrita de cada ítem si se quiere el registro más sobrio. |
| Cifras con separador fino `65\,185` y `\times` | todo §5 | Correcto tipográficamente. |
| Afirmaciones categóricas **con el dato detrás** | `05:126` «se equivoca del orden de cien veces más» (0.2337 vs 0.0021) · `05:292` «puede terminar actuando en el 0 %» | No son hipérbole: son el resultado. **No suavizar.** |

---

## 7. Diagnóstico de conjunto

1. **El problema no es el vocabulario ni la sintaxis: es el registro.** El texto casi no tiene muletillas de LLM («no solo X sino Y» completo: **0**; «en otras palabras» y «es importante destacar»: **0**; sí 4 «no solo» sueltos, uno de ellos escalada retórica en `06:22`). Lo que tiene es **tono de divulgación**: títulos con gancho, captions que argumentan, párrafos que rematan en máxima y 187 negritas en prosa.
2. **La negrita es el tell más delator y el más barato de corregir.** Es un artefacto de Markdown: el `.md` está escrito para leerse en pantalla y el `.tex` heredó el énfasis. Quitarla de la prosa cambia la percepción del PDF más que cualquier reescritura de frases.
3. **La repetición es el segundo problema.** El claim «el número no viaja, el mapa sí» aparece 4 veces (`03:103`, `05:97`, `06:8`, `07:7`), y 8 captions repiten frases del cuerpo. En 12 páginas eso se lee como relleno.
4. **El aparato técnico está limpio.** Preposiciones, notación, trazabilidad D4, cifras con fuente, limitaciones declaradas: nada de eso necesita cambios y es lo que sostiene el paper frente a un revisor.
5. **Riesgo de proceso:** `.md` y `.tex` son paralelos. Cualquier arreglo aplicado solo en el `.tex` se pierde en la próxima regeneración, y viceversa. Aplicar cada arreglo en los dos archivos en el mismo paso.

---

## 8. Anexo: reproducir los conteos

```bash
cd ~/paper-tesis1/paper/ieee
# negritas totales, dentro de tabular y en prosa (213 / 26 / 187)
grep -o '\\textbf{' secciones/*.tex | wc -l
/home/arbues/paper-tesis1/.venv/bin/python - <<'EOF'
import re, glob
tot = tab = 0
for p in sorted(glob.glob('secciones/*.tex')):
    t = open(p, encoding='utf-8').read()
    tot += t.count('\\textbf{')
    for m in re.finditer(r'\\begin\{tabular\}.*?\\end\{tabular\}', t, re.S):
        tab += m.group(0).count('\\textbf{')
print(tot, tab, tot - tab)          # 213 26 187
EOF
grep -c '\\subsection{' secciones/*.tex        # 32 subsecciones
grep -h '\\caption' secciones/*.tex | wc -l    # 24 captions
grep -rn "titular" secciones/*.tex             # 5 usos periodísticos
grep -ro -- "---" secciones/*.tex main.tex | wc -l   # 8 = 4 pares de raya
grep -rn -i "no solo" secciones/ main.tex      # 4, ninguna con «sino»
for p in "en otras palabras" "es importante destacar" "cabe destacar"; do
  printf "%-26s %s\n" "$p" "$(grep -roi "$p" secciones/ main.tex | wc -l)"; done   # 0 0 0
```

Verificaciones puntuales usadas en el informe:

```bash
grep -c '\\subsection{' paper/ieee/secciones/*.tex          # 32 subsecciones
grep -h '\\caption' paper/ieee/secciones/*.tex | wc -l      # 24 captions
grep -rn "titular" paper/ieee/secciones/*.tex               # 5 usos periodísticos
grep -oE '\\textbf\{[^{}]*\}' paper/ieee/secciones/*.tex | wc -l   # 213
```
