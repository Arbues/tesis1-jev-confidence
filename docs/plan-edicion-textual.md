# Plan de edición textual — qué cambiar y qué no (Tesis 1)

**Fecha:** 28-oct-2026 · base `b9068fd` · Insumos: `docs/auditoria-estilo-2026-10-28.md` y
`docs/auditoria-figuras-2026-10-28.md`.
> **ESTADO: APLICADO el 28-oct-2026** (commit de esa fecha). Bloques A y B (negritas 187→0 en prosa, 5 títulos
> descriptivos, 11 captions sin tesis, 9 cierres reformulados, léxico), bloque C (14 flotantes citados, donde
> antes había 0), bloque D (los 4 errores factuales) y bloque E (las 8 figuras regeneradas a la medida final,
> con `fig4` y `fig6` rediseñadas y `fig8` nueva). Lo que sigue queda como registro del criterio.

**Criterio de este plan:** no se aplica todo lo que se encontró. Se aplica lo que (a) un revisor humano
detecta como "esto no es un paper" y (b) se corrige sin tocar el contenido técnico. Todo va **en `.tex` y en
`.md`** en el mismo paso.

---

## 0. El diagnóstico en una frase

El paper **no** suena a IA por su vocabulario (0 «en otras palabras», 0 «no solo X sino Y», 0 «es importante
destacar»; medido). Suena a IA por **cuatro hábitos de formato**:

| Hábito | Medida | Por qué se lee como generado |
|---|---|---|
| **Negrita enfática en la prosa** | **187** `\textbf{}` fuera de tablas (1 cada 43 palabras; §1 una cada 29) | Es el `**negrita**` de Markdown que sobrevivió al `.tex`. En IEEEtran el cuerpo va en redonda: el valor esperado es **0** |
| **Título de sección = eslogan** | 4 de 8 subtítulos de §5 | Un paper titula por objeto ("Caída de cobertura por par de definiciones"), no por tesis ("El promedio engaña") |
| **El pie de figura argumenta** | 9 de 24 captions cierran con sentencia valorativa | En IEEE el caption dice qué se ve y qué ejes tiene; la tesis va en el cuerpo. Además el título se imprime **dos veces** (dentro del PNG y en el `\caption`) |
| **Cada párrafo remata en máxima** | 22 de 66 párrafos (33 %) cierran con oración ≤14 palabras **sin dato** | Es el ritmo de "conclusión de blog". Un paper cierra con el número o con la transición al siguiente párrafo |

Dos cosas que **se midieron y NO son problema** (no gastar tiempo ahí): la longitud de los párrafos es variada
(mediana 63 palabras, CV 0.57, 23 párrafos de <40 y 3 de >150: eso ya parece escrito por una persona) y las
oraciones no son staccato (mediana 21 palabras). Tampoco hay muletillas de LLM. **El problema es el registro,
no la sintaxis.**

---

## 1. Los 6 cambios que valen la pena (≈3 h en total)

| # | Cambio | Alcance | Esfuerzo | Efecto sobre el "indicio IA" | Riesgo |
|---|---|---|---|---|---|
| **1** | **Quitar la negrita de la prosa**: 187 → ≤30 (dejar las 26 de tablas + las Proposiciones) | todo §1–§7 | 40 min, mecánico | **El más alto de todos.** Cambia la textura visual del PDF de "post" a "paper" | nulo |
| **2** | **5 subtítulos descriptivos** (3 de §5, 1 de §5.6, 1 de §6) | §5, §6 | 10 min | Alto: un título-eslogan delata en el índice, antes de leer una línea | bajo |
| **3** | **Captions: 2 oraciones, sin tesis** (9 casos) + **borrar el `ax.set_title`** de las 8 figuras | §5 + `figuras_paper.py` | 60 min | Alto: elimina la duplicación "título dentro de la imagen + pie que repite" | bajo |
| **4** | **8 cierres-máxima** (de 22): dejar solo los que tienen dato detrás | §5, §6 | 30 min | Medio-alto: rompe el "cada párrafo concluye" | bajo |
| **5** | **Léxico periodístico**: «titular» ×5, «el ecosistema» como sujeto (2 generalizaciones sin cita), «el promedio engaña», «colapsa al suelo» | §4, §5, §6, abstract | 20 min | Medio: es lo que un lector nombra como "tono de divulgación" | bajo |
| **6** | **Repetición**: el claim central aparece **4 veces** con la misma frase (`03:103`, `05:97`, `06:8`, `07:7`); 8 captions repiten frases del cuerpo | §3, §5, §6, §7 | 20 min | Medio: la IA repite; un autor referencia ("véase §5.3") | bajo |

---

## 1b. Bloque E — Figuras: decisiones tomadas (28-oct-2026, criterio del autor)

**Criterio del autor:** un gráfico no se juzga por si su dato está también en una tabla — se juzga por si
**muestra una tendencia, una desviación o algo que llame la atención**. Bajo ese criterio **no se elimina ninguna
figura**: las dos débiles se rediseñan para mostrar la tendencia que hoy esconden. Sin límite de páginas; el
criterio es no abrumar repitiendo lo ya dicho.

### Reglas de dibujo (las tres, para las 8 figuras)

| # | Regla | Por qué |
|---|---|---|
| **R1** | **Dibujar a la medida final**: 3.45 in para una columna, 7.1 in para dos; escala 1:1, fuente 7 pt | Hoy se dibujan a 4.4–6.6 in y se insertan a 3.5 in → se imprimen a **5.0–5.8 pt**; el heatmap se dibuja a 21 in → **1.5–3.5 pt**. Con escala 1:1 el problema desaparece sin gastar una página |
| **R2** | **Sin título dentro de la imagen** (8/8 lo tienen y duplican el pie) | El mensaje se imprime dos veces y gasta ~8 % de la altura de cada figura |
| **R3** | **Citar cada figura** con `\ref{fig:…}` en el cuerpo | Hoy: 0 referencias a las 8 figuras y 0 a las 16 tablas. Un flotante huérfano es el primer defecto que marca un revisor |

### Acción por figura

| # PDF | Figura | Acción | Por qué |
|---|---|---|---|
| **Fig. 1** | accuracy banking77 | Las **5 configuraciones** (hoy 2), línea del azar 1/77 = 0.013, a 3.45 in | El pie cita un 0.378 que no está en el gráfico y dice «triplica» cuando es **2.16×**. Con las 5 barras el contraste 0.016 → 0.813 se ve solo |
| **Fig. 2** | histograma de la brecha | A 3.45 in, rótulos **horizontales** (hoy rotados sobre la propia línea y se leen mal) + anotar el pico en 0 | El pico de **2.167 decisiones saturadas** (3.3 %; 848 en `laya/banking77`) es el mismo fenómeno que el heatmap y hoy no se menciona |
| **Fig. 3** | directo vs mapa | Título interno corregido («~100×» → «hasta 109×»), eje en log o inset para las barras verdes, a 3.45 in | La primera categoría del propio gráfico da **20.5×**, y las barras de 0.002 son invisibles a escala lineal |
| **Fig. 4** | scatter Δ directo vs Δ mapa | **CDF emparejadas** de \|Δ\| (directo vs mapa) con vertical en 0.01 — o mínimo: eje y propio (0–0.12), sin la diagonal `y = x`, banda ±0.01 y `n = 116, q = 0.80` en el pie | La diagonal no informa (correlación 0.171; los puntos están en y ≈ 0) y el eje simétrico ±0.9 para datos que llegan a 0.104 deja el **88 % del área vacía**. La CDF muestra la desviación que el scatter esconde |
| **Fig. 5** | \|Δ\| por par A→B | A 3.45 in, **leyenda fuera de las barras**, n por par, declarar los cortes de color | La leyenda tapa **las dos barras del mensaje** (`pmax→margin` y `pmax→ent`). Es la figura del titular real del paper |
| **Fig. 6** | por cardinalidad | **Rediseño:** \|Δ\| mediana por n en **escala log** con IQR; fuera el porcentaje (ya está en la Tabla IV) | Hoy 3 de 6 barras valen 0 % sobre 30 celdas, que parece "no transfiere" y solo significa "no se observó". El dato tiene una tendencia real y no monótona: 0.214 → 0.178 → 0.409 → 0.200 → **0.006 → 0.013** (el colapso a n ≥ 77) |
| **Fig. 7** | heatmap banking77 | **`figure*`**, `figsize=(7.1, 3.6)`, fuentes 7 / 6.5, **una** barra de color compartida, sin `suptitle`, diagonal muda, y copiarla a `paper/figures/` con script | Hoy se imprime a **8.8 × 1.9 cm con texto de 1.5–3.5 pt**. Es la figura más informativa del paper (par direccional + dependencia del modelo + signo del error) y la única ilegible. `figure*` sola no alcanza: escala 0.34 → 3.1 pt |
| **Fig. 8** | ECE por definición | **Rediseño:** ECE de las 4 definiciones en los **23 grupos** (línea por grupo, 4 posiciones en x, mínimo de cada grupo marcado), `figure*` | Hoy son 2 números de 1 grupo. Con los 23 grupos el ECE tiene **spread mediano 0.124 y máximo 0.361**, y la definición mejor calibrada **cambia**: `pmax` en 7 grupos, `margin` en 6, `ent` en 6, `jev` en 4. Eso convierte "el ECE depende de la definición" (una corrida) en "ninguna definición es la mejor calibrada en todos los modelos" (23 grupos). Los 23 valores están en §6 |

### Qué se paga y qué se gana

- **Figuras:** siguen siendo 8. Dos a dos columnas (Fig. 7 y Fig. 8); las otras seis a una columna pero redibujadas
  a 3.45 in (R1), que no consume espacio: solo cambia el tamaño de la letra impresa.
- **Espacio:** se recupera quitando los títulos internos (R2) y acortando los captions que repiten el cuerpo (§2.2).
- **Costo real:** una sola corrida de `src/figuras_paper.py` y una de `src/matriz/figura.py` (matplotlib 3.11.2 en
  esta máquina). Reescribe los 7 PDF/PNG del set: hacerlo en un solo commit.
- **No hacer:** paleta accesible (solo si se regenera igual), IC de Wilson (el % de la Fig. 6 desaparece),
  renombrar archivos como tarea aparte (va dentro del mismo commit), y añadir figuras nuevas más allá de estos dos
  rediseños.

## 2. Ejemplos literales (antes → después)

### 2.1 Títulos

| Línea | Antes | Después |
|---|---|---|
| `05:61` | `El objeto de la tesis, en una cifra` | `Brecha entre definiciones sobre las 65\,185 distribuciones` |
| `05:97` | `El número no viaja; el mapa sí` | `Porte directo frente a porte con mapa cerrado` |
| `05:152` | `El promedio no es el resumen: la estructura está en el par` | `Caída de cobertura por par de definiciones` |
| `05:261` | `Dónde el umbral no viaja (nivel raw, q = 0.80, tras FDR)` | `Celdas sin transferencia tras FDR (nivel raw, q = 0.80)` |
| `06:26` | `Lo que esto dice de la calibración del ecosistema` | `Calibración de las implementaciones medidas` |

Se quedan como están (son correctos): `05:231 Efecto de la cardinalidad`, `05:304 Hallazgos de metrología del
paso 0 (contexto)`, `05:333 Extensiones declaradas`, todo §3, §4 y §7.

### 2.2 Pies de figura — regla: 1.ª oración = qué se ve; 2.ª = ejes/unidad/n. Cero tesis.

| Línea | Antes | Después |
|---|---|---|
| `05:91` (Fig. 2) | `La cifra central: sobre las 65 185 decisiones medidas, la definición más alta y la más baja de confidence difieren con mediana 0.288 y alcance máximo 0.848. Un umbral fijado con una definición no significa lo mismo con la otra.` | `Distribución de la brecha entre la definición más alta y la más baja de cada distribución (n = 65 185; mediana 0.288, p90 0.434, máximo 0.848). El pico en 0 son las filas saturadas, donde las cuatro definiciones valen 1.` |
| `05:132` (Fig. 3) | `El titular: el porte directo del umbral (sin transformar) se equivoca del orden de cien veces más que el porte con el mapa cerrado cuando este existe (0.2337 frente a 0.0021 sin empates dominantes).` | `\|Δ\| medio del porte directo y del porte con mapa, por subconjunto de celdas (nivel raw, q = 0.80; n = 348, 312, 276 y 168 celdas). El factor sobre cada par es la razón entre ambas barras.` |
| `05:147` (Fig. 4) | `La Proposición 1 sobre los datos: celda a celda, la caída de cobertura del porte directo (\|Δ\| directo) contra la del porte con mapa. Con el mapa el error colapsa al suelo que imponen los empates del umbral, no el mapa.` | `Δ del porte directo frente a Δ del porte con mapa, celda a celda (nivel raw, q = 0.80, 116 celdas). La línea y = x marca igual error; 98 de las 116 celdas quedan por debajo de \|Δ\| = 0.01 con el mapa.` |
| `05:193` (Fig. 5) | `El promedio engaña: la estructura está en el par. Hay pares de definiciones que coinciden por identidad matemática (medianas de 0.0023) y pares que fallan en grande (hasta 0.7667), y la media global borra esa bimodalidad.` | `\|Δ\| mediana y media por par A→B (nivel raw), ordenadas por la mediana. Los pares margin↔jev y pmax→ent ocupan los extremos (0.0023 y 0.7667).` |
| `05:298` (Fig. 7) | `Dónde el umbral no viaja: mapa de calor de la caída de cobertura en banking77 (n = 77, nivel raw), con filas de definición origen y columnas de definición destino. Cuando el modelo está saturado, celdas enteras pierden toda la cobertura al cambiar de definición.` | `Δ = q − cobertura_B al portar τ sin mapa, en banking77 (n = 77, nivel raw, q = 0.80). Filas: definición origen; columnas: destino; escala de color compartida; la diagonal no aplica.` |
| `05:326` (Fig. 8) | `El mismo dato, dos ECE: en laya-typed-decisions el ECE va de 0.216 con p_max a 0.577 con la entropía normalizada, un factor 2.7×. El ECE auto-reportado no es una propiedad del modelo sino de la definición elegida.` | `ECE sobre las mismas 2 000 decisiones de laya-typed-decisions, calculado con p_max y con entropía normalizada (binning exacto de Laya).` |

Y en el código: **borrar `ax.set_title(...)` de las 8 figuras** (`src/figuras_paper.py`, `src/matriz/figura.py`).
El mensaje va en el cuerpo y en el pie, una sola vez.

### 2.3 Cierres de párrafo (8 de 22)

| Línea | Antes | Después |
|---|---|---|
| `05:155` | `El titular es el par, no la media global.` | `Por eso la tabla se ordena por la mediana del par y no por la media global.` |
| `05:259` | `Es la distinción entre el número y el mapa.` | `La distinción formal está en §3.4.` |
| `05:382` | `Se declara el límite en lugar de inventar la escala.` | `El supuesto ordinal no se extiende a los datasets nominales.` |
| `06:8` | `Es la diferencia entre copiar la cifra y traducirla.` | `Las dos capas se miden por separado: la escala con el mapa cerrado, la forma con el par de definiciones.` |
| `06:18` | `el costo de confundir «mismo orden» con «mismo número».` | `…el costo de confundir «mismo orden» con «mismo número» (Tabla VI).` |
| `05:137` | `\textbf{Cómo leer la tabla.}` | `\textbf{El suelo de los empates.}` (un paper no enseña a leer su tabla; explica el artefacto) |

Se quedan: `05:85` `Cualquier umbral fijado sobre una de las dos no significa lo mismo sobre la otra.` (consecuencia
real del dato), y los cierres que llevan cifra.

### 2.4 Léxico

| Uso | Dónde | Cambio |
|---|---|---|
| «titular» (vocabulario de prensa) ×5 | `04:9`, `05:99`, `05:132`, `05:155`, `05:459` | «resultado principal» / «unidad de análisis» / «el dato central» (variar: no un reemplazo único) |
| «el ecosistema» como sujeto agente (20) | `05:48-50`, `05:56-57`, `06:26` | «las cinco configuraciones medidas», «los checkpoints publicados»; las **2 generalizaciones sin cita** (`05:49-50`, `05:56-57`) o llevan cita o pierden la generalización |
| «el promedio engaña» | `05:159`, `05:193` | «la media global oculta la bimodalidad» |
| «colapsa al suelo» | `05:147` | «se reduce hasta el límite que imponen los empates» |
| **se queda** «transferencia / no transfiere / portar el umbral» | todo | es el término técnico del campo (Chow, Geifman): borrarlo empobrece |

### 2.5 Abstract: una sola frase

`main.tex:62-63` — de `La contribución no es el hallazgo sino el instrumento: sobrevive a él y mide cualquier
implementación futura.` a `La contribución es el instrumento de medición: se aplica a cualquier implementación
futura del campo sin volver a medir el corpus.` El resto del abstract está denso en cifras y no se toca.

---

## 3. Lo que NO se toca (tocarlo empeora el paper y, además, se lee como "corrección de IA")

| Elemento | Por qué |
|---|---|
| Afirmaciones categóricas **con el dato detrás** (`05:126` «cien veces», `05:292` «0 % de los casos») | No son hipérbole: son el resultado. Suavizarlas con «podría» resta y agrega el tell opuesto (hedging) |
| Proposiciones 1–3 en `quote` con negrita (`03:78-100`) | Convención matemática, no énfasis retórico |
| Run-in heads de §2 (`02:8`…`02:46`) y negritas **dentro de tablas** (26) | Forma IEEE habitual; marcan el subconjunto principal |
| Frases de 20–25 palabras, rayas largas, dos puntos | Registro técnico correcto y dosis moderada (4 pares de raya, 0 muletillas) |
| Columnas de rol en tablas («quién la usa», «papel», «Estado») | Aportan información; solo «por qué» (`04:57`) pasa a «criterio de inclusión» |
| Trazabilidad D4, hashes, DOI, límites de hardware | Es **lo más humano** que tiene el paper: nadie inventa que su GPU tiene 6 GB y que Kev retiene 4.8 |
| Longitud de párrafos y oraciones | Ya es variada (CV 0.57). No hay nada que "humanizar" aquí |

**Y lo que no hay que hacer nunca** para "escapar de la IA": meter coloquialismos, contracciones, anécdotas en
primera persona, sinónimos a la fuerza, errores sembrados o pasar el texto por un "humanizer". Todo eso produce
un tell distinto y peor (registro inadecuado), y en un paper con DOI y artefactos verificables el riesgo es
inverso: perder credibilidad por parecer descuidado.

**Sobre los detectores:** no son el objetivo ni son fiables (sobre texto técnico en español dan falsos positivos
sistemáticos). El objetivo es que un revisor humano no piense "esto es un blog". Si alguien pregunta por la
autoría, la respuesta no es el estilo: son los artefactos (DOI, repo, `row_hash` por fila, 69 tests, matriz que
se regenera con un comando).

---

## 4. Errores factuales que hay que corregir igual (no es estilo)

| Dónde | Dice | Debe decir | Verificación |
|---|---|---|---|
| `05:56-57` (pie Fig. 1) | «duplica al mejor checkpoint de Laya (0.378) y **triplica** al checkpoint base (0.377)» | «duplica al mejor checkpoint de Laya (2.16× frente a 0.377)» — las dos comparaciones dan el **mismo** factor | 0.8134/0.3765 = 2.16 |
| `05:225-227` (pie Fig. 6) | «a n ≥ 77 la mitad o más lo logra» | «a n = 77 sube a 63 % y a n = 151 baja a 44 %» | 8/18 = 44.4 % |
| `05:132` y título de Fig. 3 | «~100×» | «hasta 109× (sin empates); 20.5× sobre todas las celdas» | la 1.ª categoría del propio gráfico es 20.5× |
| `05:203` (pie Tabla IV) | «El umbral solo viaja a cardinalidad alta» | «El umbral viaja en 63 % de las celdas a n = 77 y en 44 % a n = 151» | idem |

---

## 5. Orden de trabajo recomendado

1. **Bloque A (1 h, sin decidir nada):** borrar las 187 negritas de la prosa y los 8 `ax.set_title`. Recompilar y
   mirar el PDF. Es el cambio que más se nota y no requiere criterio editorial.
2. **Bloque B (1 h):** los 5 títulos, los 6 captions de §2.2 y los 6 cierres de §2.3.
3. **Bloque C (30 min):** léxico (§2.4), abstract y repetición del claim central (dejarlo una vez en §3 y
   referenciarlo en §5–§7).
4. **Bloque D (30 min):** los 4 errores factuales de §4 (dos de ellos son pies de figura).
5. **Bloque E (1 h + regeneración):** las 6 acciones de §1b. Orden interno: E3 y E4 primero (liberan el espacio),
   después E1 (regenerar el heatmap), al final E2, E5 y E6 (que ya requieren correr `src/figuras_paper.py`).

Al cerrar cada bloque: `cd paper/ieee && ./compilar.sh`, `grep -cE "^!|undefined" main.log` = 0,
`pdftotext main.pdf - | grep -c '??'` = 0, y `git diff --stat` para ver que no se movió ninguna cifra.
Actualizar el `.md` espejo en el mismo commit.

---

## 6. Anexo — ECE por definición en los 23 grupos (dato para la nueva Fig. 8)

ECE con el *binning* exacto de Laya, calculado sobre las filas crudas de `results/crudos/` (misma fórmula que
`jev_conf_metrics.metricas.ece_laya`). **Negrita** = definición con menor ECE en ese grupo.

| grupo (modelo / dataset) | n ítems | pmax | jev | ent | margin | spread |
|---|---:|---:|---:|---:|---:|---:|
| `Qwen3.5-0.8B-Base` / `banking77` | 3076 | 0.181 | 0.171 | 0.316 | **0.010** | 0.306 |
| `kev-0.8b` / `banking77` | 3076 | **0.201** | 0.206 | 0.219 | 0.290 | 0.089 |
| `laya` / `banking77` | 3076 | 0.506 | 0.506 | 0.529 | **0.457** | 0.072 |
| `multilingual` / `banking77` | 3076 | 0.445 | 0.442 | 0.488 | **0.362** | 0.126 |
| `typed-decisions` / `banking77` | 3076 | 0.162 | **0.160** | 0.174 | 0.163 | 0.014 |
| `Qwen3.5-0.8B-Base` / `clinc150` | 3100 | 0.119 | 0.113 | 0.332 | **0.014** | 0.318 |
| `multilingual` / `clinc150` | 3100 | 0.197 | 0.196 | 0.235 | **0.161** | 0.074 |
| `typed-decisions` / `clinc150` | 3100 | 0.077 | 0.083 | **0.075** | 0.125 | 0.051 |
| `Qwen3.5-0.8B-Base` / `sst5` | 1101 | **0.087** | 0.089 | 0.171 | 0.143 | 0.084 |
| `kev-0.8b` / `sst5` | 1101 | 0.088 | **0.059** | 0.117 | 0.209 | 0.151 |
| `laya` / `sst5` | 1101 | 0.264 | 0.176 | **0.088** | 0.150 | 0.176 |
| `multilingual` / `sst5` | 1101 | 0.588 | 0.547 | 0.488 | **0.464** | 0.124 |
| `typed-decisions` / `sst5` | 1101 | **0.061** | 0.156 | 0.225 | 0.292 | 0.231 |
| `Qwen3.5-0.8B-Base` / `typed-decisions` | 2000 | **0.096** | 0.254 | 0.349 | 0.320 | 0.254 |
| `kev-0.8b` / `typed-decisions` | 2000 | **0.061** | 0.228 | 0.363 | 0.274 | 0.302 |
| `laya` / `typed-decisions` | 2000 | 0.177 | **0.166** | 0.230 | 0.194 | 0.064 |
| `multilingual` / `typed-decisions` | 2000 | 0.318 | 0.255 | **0.212** | 0.244 | 0.106 |
| `typed-decisions` / `typed-decisions` | 2000 | **0.216** | 0.426 | 0.577 | 0.511 | 0.361 |
| `Qwen3.5-0.8B-Base` / `wanli` | 5000 | 0.297 | 0.129 | **0.062** | 0.145 | 0.235 |
| `kev-0.8b` / `wanli` | 5000 | **0.136** | 0.149 | 0.216 | 0.185 | 0.080 |
| `laya` / `wanli` | 5000 | 0.238 | 0.200 | **0.111** | 0.193 | 0.127 |
| `multilingual` / `wanli` | 5000 | 0.323 | 0.295 | **0.232** | 0.291 | 0.092 |
| `typed-decisions` / `wanli` | 5000 | 0.144 | **0.115** | 0.209 | 0.123 | 0.095 |

Resumen: spread **mediano 0.124**, mínimo 0.014 (`laya-typed-decisions/banking77`), máximo 0.361
(`laya-typed-decisions/typed-decisions`). La definición mejor calibrada cambia de grupo en grupo: `pmax` 7,
`margin` 6, `ent` 6, `jev` 4; `ent` es la peor en 13 de 23. Reproducible con `.venv/bin/python docs/auditoria-ece-por-grupo.py`.

