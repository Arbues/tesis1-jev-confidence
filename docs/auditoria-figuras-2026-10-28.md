# Auditoría de figuras del paper IEEE — Tesis 1

**Fecha:** 28-oct-2026 · **Alcance:** las 8 figuras de `paper/figures/` tal como salen en `paper/ieee/main.pdf`
(12 págs., `b9068fd`) · **Método:** cada cifra se recalculó hoy desde `results/crudos/` y
`results/matrix/matriz_transferencia.csv` (`docs/auditoria-figuras-verifica.py`), y cada figura se
inspeccionó renderizada y medida en el PDF final (`pdftotext -bbox`), no en el PNG de origen. El script de recálculo queda en el repo:
`docs/auditoria-figuras-verifica.py`.

**Informe hermano:** `docs/auditoria-estilo-2026-10-28.md` — redacción, títulos-gancho y marcas de
escritura asistida (las dos auditorías se hicieron el mismo día sobre el mismo commit, `b9068fd`).

---

## 0. Glosario mínimo (para leer las fichas)

| Término | Qué es |
|---|---|
| **Definición de `confidence`** | Regla que convierte la distribución `p` del modelo en un número: `pmax` (probabilidad máxima), `jev` ((n·pmax−1)/(n−1)), `ent` (1 − entropía normalizada), `margin` (margen entre las dos clases top) |
| **Brecha** | Diferencia entre la definición más alta y la más baja de la MISMA distribución. Objeto de la tesis |
| **Celda** | Cruce (modelo × dataset × par de definiciones A→B × nivel × q). La matriz sellada tiene 3.564 |
| **Nivel `raw`** | Nivel principal, el que congela el pre-registro (sin debias `L0` ni temperatura `L1`) |
| **Δ (delta)** | Caída de cobertura al portar un umbral: Δ = q − cobertura_B. `|Δ|` = error absoluto |
| **Porte directo** | Usar el umbral τ_A tal cual en la definición B |
| **Porte con mapa** | Aplicar antes la transformación monótona φ que lleva A a B (Proposición 1) |
| **q** | Cobertura objetivo del umbral (0.5 / 0.80 / 0.95) |
| **Empates del umbral** | Ítems que comparten exactamente el valor de τ; imponen un suelo al porte con mapa |

---

## 1. Resumen ejecutivo

| # PDF | Archivo | Qué muestra | Verificación | ¿Aporta? | Veredicto |
|---|---|---|---|---|---|
| **Fig. 1** | `fig7-accuracy-banking77` | Accuracy de 2 de las 5 configuraciones en banking77 | 0.3765 y 0.8134 ✓ | Poco: 2 barras, y 3 configuraciones faltan | **Rediseñar** (5 barras) |
| **Fig. 2** | `fig1-brecha` | Histograma de la brecha sobre 65.185 decisiones | mediana 0.2881 · p90 0.4344 · máx 0.8481 ✓ | Sí: es la única que muestra la FORMA | **Conservar** (arreglar rótulos) |
| **Fig. 3** | `fig2-directo-vs-mapa` | |Δ| medio directo vs con mapa, 4 subconjuntos | 20.5× / 109.2× / 112.8× / 95.8× ✓ | Sí, pero duplica Tabla III | **Conservar** (corregir título) |
| **Fig. 4** | `fig3-delta-vs-mapa` | Scatter celda a celda Δ directo vs Δ con mapa (116 celdas) | n=116 · corr=0.171 · 98/116 con |Δ|mapa|<0.01 ✓ | Poco: 116 puntos aplastados en y≈0 | **Rediseñar o eliminar** |
| **Fig. 5** | `fig4-por-par` | |Δ| mediana por par A→B (12 pares) + media | 12 medianas ✓ (0.0023 … 0.7667) | Sí: la estructura bimodal en el par | **Conservar** (leyenda tapa una barra) |
| **Fig. 6** | `fig5-por-cardinalidad` | % de celdas con |Δ|<0.01 por cardinalidad | 14/0/0/0/63/44 % ✓ | **No**: es la Tabla IV dibujada | **Eliminar** |
| **Fig. 7** | `fig8-heatmap-banking77` | 5 mapas de calor 4×4 (origen→destino) del Δ firmado | valores ✓ (md5 = heatmap de la matriz) | **Es la más informativa de todas** | **Rehacer a 2 columnas + regenerar** |
| **Fig. 8** | `fig6-ece-por-definicion` | 2 barras: ECE 0.216 vs 0.577 | 0.2157 vs 0.5766 → 2.67× ✓ | Poco: 2 números | **Rediseñar o pasar a texto** |

**Veredicto global:** los datos de las 8 figuras son **correctos y reproducibles** (los 31 números que muestran
se recalculan exactos desde los artefactos). Los problemas son **editoriales y de diseño**, y son cinco,
transversales a todas:

| # | Problema transversal | Evidencia medida | Impacto |
|---|---|---|---|
| **T1** | **Ninguna figura se cita en el texto**: 0 apariciones de `\ref{fig:...}` en los 7 `.tex`, y **tampoco de `\ref{tab:...}`** para las 16 tablas | `grep -rn "ref{fig" paper/ieee/secciones/` → vacío | Alto: es el defecto que un revisor IEEE marca primero ("floating figure never referenced") |
| **T2** | **Texto ilegible por sobre-escalado**: las figuras se dibujan a 4.4–6.6 in y se insertan a 3.5 in; el heatmap se dibuja a **21 in** y se inserta a 3.5 in | Tabla §2: la fuente de 9 pt sale impresa entre **1.5 y 7.7 pt**; medido en el PDF: 2.5–5.5 pt (cuerpo = 8.9 pt) | Alto: el heatmap es **ilegible**; 4 figuras más quedan por debajo del mínimo práctico (≈7 pt) |
| **T3** | **Título dentro de la figura duplicando el pie** (8/8): `ax.set_title(...)` reproduce casi palabra por palabra el `\caption` | p. ej. Fig. 2 dibuja "El objeto de la tesis: el mismo dato, 65.185 decisiones…" y el pie repite lo mismo | Medio: gasta ~8 % de la altura de cada figura y no es estilo IEEE |
| **T4** | **La numeración del archivo no coincide con la del PDF** | Fig. 4 del PDF = `fig3-…`; Fig. 7 = `fig8-…`; Fig. 1 = `fig7-…` | Medio: cualquier referencia cruzada autor↔agente se equivoca (en este informe se usan **siempre** los dos números) |
| **T5** | **Rojo/verde como única codificación** en Fig. 3, 5 y 6 (y azul/rojo en Fig. 7) | `COLORES` en `figuras_paper.py`, `RdBu_r` en `matriz/figura.py` | Bajo-medio: recomendación IEEE de accesibilidad; basta añadir trama/marcador |

---

## 2. Legibilidad real: cuánto se encoge cada figura al imprimirse

`\columnwidth` medido en el PDF = **253 pt (3.5 in)**; a dos columnas `\textwidth` ≈ **516 pt (7.17 in)**.
Escala = ancho insertado / ancho nativo. Con `font.size = 9` pt en `figuras_paper.py`:

| # PDF | Archivo | Ancho nativo | Escala a 1 col. | Fuente 9 pt sale a | ¿Legible? |
|---|---|---|---|---|---|
| Fig. 1 | `fig7-accuracy` | 294.2 pt (4.1 in) | 0.86 | **7.7 pt** | sí |
| Fig. 2 | `fig1-brecha` | 448.2 pt (6.2 in) | 0.56 | **5.1 pt** | no |
| Fig. 3 | `fig2-directo-vs-mapa` | 422.7 pt (5.9 in) | 0.60 | **5.4 pt** | no |
| Fig. 4 | `fig3-delta-vs-mapa` | 335.2 pt (4.7 in) | 0.75 | **6.8 pt** | límite |
| Fig. 5 | `fig4-por-par` | 453.8 pt (6.3 in) | 0.56 | **5.0 pt** | no |
| Fig. 6 | `fig5-por-cardinalidad` | 391.8 pt (5.4 in) | 0.65 | **5.8 pt** | no |
| Fig. 7 | `fig8-heatmap` | **1512 pt (21 in)** | **0.164** | **1.5 pt** | **ilegible** |
| Fig. 8 | `fig6-ece` | 305.4 pt (4.2 in) | 0.83 | **7.5 pt** | sí |

Comprobación independiente en el PDF final (`pdftotext -bbox`, altura de glifo; el cuerpo de 10 pt mide 8.9 pt):
Fig. 7 ocupa **248 × 54 pt = 8.8 × 1.9 cm** y sus rótulos de celda miden **2.5–3.5 pt**; en las páginas 8 y 4 hay
texto de figura de **4.0–5.5 pt**. Es decir: el diagnóstico no depende de la fórmula, está medido en el PDF.

**Regla para arreglarlo:** o se dibuja la figura a **su tamaño final** (`figsize=(3.4, …)` con fuentes 7–8 pt y
sin título interno), o se pasa a `figure*` (dos columnas, 516 pt) y se la dibuja a **7.1 in**. Nada de dibujar a
6.5 in para insertarlo a 3.5 in.

---

## 3. Fichas figura por figura

### Fig. 1 (PDF) — `fig7-accuracy-banking77.pdf` · §5.1, página 4

- **Qué afirma el pie:** "Kev-0.8B (0.813) duplica al mejor checkpoint de Laya (0.378) y **triplica** al
  checkpoint base (0.377)".
- **Qué muestra de verdad:** 2 barras — `laya` base 0.376 y `kev-0.8b` 0.813.
- **Verificación:** accuracy de `results/crudos/*.meta.json` → Qwen 0.0156 · laya 0.3765 · laya/multilingual 0.3560 ·
  laya/typed-decisions 0.3781 · kev 0.8134. ✓ los números de las barras.
- **Errores:**
  1. **Factual:** 0.8134 / 0.3765 = **2.16×**, no "triplica". Las dos comparaciones del pie dan el mismo factor
     (2.15 y 2.16), así que la frase "duplica … y triplica" es falsa y además se contradice consigo misma.
  2. La figura **no contiene** el 0.378 que el pie cita: el mejor checkpoint de Laya no está dibujado.
  3. De 5 configuraciones medidas se dibujan 2; el mensaje ("el ecosistema sí entrena para cardinalidad alta")
     se sostiene mejor con las 5 (Qwen 0.016 a la izquierda de todo, que es justamente el contraste que el texto
     del §5.1 destaca).
- **¿Aporta?** Poco tal como está: los mismos 5 números ya están en la Tabla I y en una frase del §5.1. Pero el
  contraste es real y útil como primera figura (0.016 / 0.36 / 0.38 / 0.81).
- **Recomendación:** 5 barras ordenadas (Qwen, laya/multilingual, laya base, laya/typed-decisions, kev), línea
  punteada en la accuracy de azar 1/77 = 0.013, y cerrar el pie con "2.2×, no un orden de magnitud". Ajustar el
  pie al dato: **"duplica"** y punto.

### Fig. 2 (PDF) — `fig1-brecha.pdf` · §5.2, página 5

- **Qué afirma el pie:** mediana 0.288, alcance máximo 0.848.
- **Verificación:** n = 65.185 · mediana **0.2881** · p90 **0.4344** · máx **0.8481** ✓.
- **Qué añade sobre la Tabla II:** la **forma**. El histograma tiene tres rasgos que la tabla no puede dar y que el
  texto no menciona:
  - **un pico de 2.167 decisiones (3.3 %) exactamente en 0**, que son las **distribuciones saturadas**: en todas
    ellas `pmax = jev = ent = margin = 1.0` (848 en `laya/banking77`, 607 en `laya-multilingual/banking77`,
    661 en `laya-multilingual/clinc150`). Es el mismo fenómeno de saturación que la Fig. 7 muestra como "celdas
    enteras que pierden toda la cobertura" — **las dos figuras hablan de lo mismo y el texto no las conecta**;
  - masa principal entre 0.2 y 0.45 (la mediana cae ahí);
  - cola hasta 0.85.
- **Problemas:**
  1. Los rótulos "mediana = 0.288" / "p90 = 0.434" van **rotados 90° encima de la propia línea**, con lo que se
     leen mal: un lector automático (y probablemente uno humano con prisa) los confunde con "p-valor" y "p50".
     Mejor: caja con flecha, horizontal, en el margen alto.
  2. El título interno repite el pie (T3) y usa el punto como separador de miles ("65.185") mientras el texto
     usa `65\,185`; en `.tex` conviene `siunitx` o al menos el mismo criterio.
  3. 60 bins sobre 65.185 filas: el pico en 0 se diluye en el primer bin. Con `bins` logarítmico en y o un inset
     se ve que es un pico puntual, no una cola.
- **¿Aporta?** **Sí, es la figura que mejor justifica la tesis** (el objeto es una discrepancia, y su distribución
  es el argumento). Vale la pena subirla a `figure*` y meterle la anotación del pico en 0.
- **Recomendación:** conservar; pasar a dos columnas (0.56 → 1.15 de escala, fuentes ~10 pt), rótulos
  horizontales, anotar el pico de saturación y enlazarlo en el texto con la Fig. 7.

### Fig. 3 (PDF) — `fig2-directo-vs-mapa.pdf` · §5.3, página 5

- **Qué afirma el pie:** 0.2337 frente a 0.0021 sin empates dominantes.
- **Verificación (todo ✓):** todas 348 celdas 0.2528/0.0123 = 20.5× · sin empates 312 celdas 0.2337/0.0021 = 109.2× ·
  sin control Qwen 276 celdas 0.2289/0.0020 = 112.8× · n≥3 168 celdas 0.2015/0.0021 = 95.8×.
- **Problemas:**
  1. **El título interno dice "~100×" pero la primera categoría del propio gráfico da 20.5×.** El "100×" solo vale
     para los tres subconjuntos filtrados; el lector ve 21× y 109× en la misma figura. Corregir a
     "hasta 109× (sin empates)" o titular por el subconjunto limpio.
  2. **Duplica la Tabla III**: son 4 de sus 7 filas. La figura no aporta ninguna cifra nueva; su valor es visual.
  3. Las barras verdes (0.002) son invisibles a escala lineal: la comparación entre subconjuntos del mapa no se
     puede leer. O escala log, o un inset, o quitar las barras del mapa y dejar el factor como anotación.
- **Recomendación:** conservar como "figura del titular", pero con el título corregido y el eje y en log (o
  barras agrupadas con corte). Si hay que recortar figuras, esta y la Tabla III no deberían coexistir: dejar la
  tabla completa y la figura reducida a 2 barras (todas / sin empates).

### Fig. 4 (PDF) — `fig3-delta-vs-mapa.pdf` · §5.3, página 5-6 · **(la que el autor preguntó)**

- **Qué afirma el pie:** "celda a celda, la caída de cobertura del porte directo contra la del porte con mapa.
  Con el mapa el error colapsa al suelo que imponen los empates".
- **Qué muestra de verdad (medido hoy):** 116 celdas (nivel `raw`, q = 0.80). Eje x = Δ directo, de **−0.200 a
  +0.800**; eje y = Δ con mapa, de **−0.002 a +0.104**. Correlación directo↔mapa = **0.171** (prácticamente
  nula). 98 de 116 celdas quedan con |Δ|mapa| < 0.01. **Ningún punto cae exactamente en (0,0).**
- **Respuesta directa a "¿se quiere mostrar una tendencia en la diagonal?"** → **No, y la diagonal no informa.**
  La diagonal `y = x` significa "el mapa no mejora nada". Los puntos **no la siguen**: están en una banda
  horizontal pegada a `y = 0` para todo el rango de x. Lo que la figura demuestra es
  **"y ≈ 0 con independencia de x"**, no "y < x". La referencia que sí informa es la recta `y = 0`
  (ya dibujada) y una banda de tolerancia `|y| = 0.01` (que no está dibujada y es la que hace interpretable el
  "colapsa"). Hoy la diagonal es tinta de más: solo un punto se le acerca.
- **Problemas de diseño (por eso "no se entiende"):**
  1. **Escala compartida ±0.9 en los dos ejes** cuando el eje y solo usa 0…0.104: el 88 % del área está vacía y el
     "colapso" se ve como una línea plana indistinguible.
  2. **Sobre-dibujo**: 116 puntos con α = 0.7 y s = 24 se solapan en la banda de y≈0; no se ve la densidad.
  3. La figura **no dice n ni q** (ni en el título ni en el pie): el lector no puede saber que son 116 de las 348
     celdas, ni que es un solo q de los tres.
  4. Título interno interpretativo + pie que repite (T3).
- **Recomendación (dos opciones):**
  - **A (preferida): sustituir el scatter por una comparación de distribuciones** — dos CDF empíricas (o un
    histograma apareado) de |Δ| directo vs |Δ| con mapa en las mismas 116 celdas, con la línea vertical 0.01.
    Eso dice lo mismo, se lee, no depende de la densidad de puntos y no necesita diagonal.
  - **B: conservar el scatter** con eje y propio (0 a 0.12), `y = x` fuera, banda ±0.01 rayada, `hexbin` o
    `alpha` bajo + jitter, y "n = 116, q = 0.80" en el pie.

### Fig. 5 (PDF) — `fig4-por-par.pdf` · §5.4, página 6

- **Qué afirma el pie:** pares que coinciden por identidad (0.0023) y pares que fallan (hasta 0.7667), y que la
  media global borra la bimodalidad.
- **Verificación:** las 12 medianas y las 12 medias se recalculan exactas (jev↔margin 0.0023/0.0293 y 0.0023/0.0250;
  ent→jev y ent→margin 0.1837 idénticas; pmax→ent 0.7667/0.6787 máximas). ✓
- **Qué aporta:** es la figura que sostiene el titular real del paper ("la estructura está en el par"). El punto
  negro de la media contra la barra de la mediana es la mejor idea gráfica del conjunto: se ve que en
  `pmax→margin` la media (0.515) queda **por debajo** de la mediana (0.526) mientras en `pmax→ent` pasa lo
  contrario.
- **Problemas:**
  1. **La leyenda (`loc="lower right"`) se monta sobre las dos barras más largas** (`pmax→margin`, `pmax→ent`), que
     son justo las del mensaje. En el PNG la media de `pmax→ent` queda tapada. Mover la leyenda arriba a la
     derecha o al eje y.
  2. **Colores por umbral arbitrario** (verde ≤ 0.05, naranja ≤ 0.30, rojo > 0.30) sin leyenda que explique los
     cortes: los cortes son una decisión de diseño, hay que declararlos en el pie.
  3. Los 12 pares incluyen **4 duplicados algebraicos** (ent→jev ≡ ent→margin; jev→margin ≡ por identidad a
     n = 2). Dibujar 12 barras para 8 valores distintos invita a leer "12 resultados" donde hay 8 clases.
  4. Sin n por par (99 celdas en los pares con pmax, 15 en el resto): comparar medianas de 15 contra 99 sin
     decirlo es un riesgo de lectura.
- **Recomendación:** conservar (es la figura del titular), mover leyenda, añadir el n por barra y declarar los
  cortes de color. Pasar a dos columnas resolvería la legibilidad (0.56 → 1.14).

### Fig. 6 (PDF) — `fig5-por-cardinalidad.pdf` · §5.4, página 6-7

- **Qué afirma el pie:** "con n ≤ 5 casi ninguna celda transfiere bien (14 % y menos), mientras que a n ≥ 77 la
  mitad o más lo logra".
- **Verificación:** 14.4 % (25/180) · 0 % (0/30) · 0 % (0/30) · 0 % (0/60) · 63.3 % (19/30) · **44.4 % (8/18)** ✓ los números.
- **Error factual del pie:** para n = 151 es **44 %**, no "la mitad o más". Corregir a "a n = 77 sube a 63 % y a
  n = 151 baja a 44 %" — que además es un matiz interesante (no es monótono en n).
- **¿Aporta?** **No.** Es exactamente la Tabla IV dibujada: la tabla ya tiene `n`, celdas, mediana y "% con
  |Δ|<0.01"; la figura grafica 2 de esas 4 columnas. Ningún dato nuevo, y encima el eje x equiespaciado
  (2, 3, 4, 5, 77, 151) sugiere una continuidad que no existe.
- **Problemas adicionales:** 0 % con 30 observaciones no es "no transfiere", es "no se observó"; sin intervalo de
  confianza (Wilson) la barra en 0 sobre 30 celdas es indistinguible de una en 0 sobre 3.000. Y las barras
  ausentes en 0 % son invisibles: un lector rápido ve 3 categorías, no 6.
- **Recomendación:** **eliminarla** y dejar la Tabla IV (que ya tiene el n y la mediana). Si se quiere una figura
  de cardinalidad, que sea con IC de Wilson y con la mediana de |Δ|, no el mismo porcentaje de la tabla.
  Libera ~1/3 de columna, que es exactamente lo que falta para el heatmap.

### Fig. 7 (PDF) — `fig8-heatmap-banking77.pdf` · §5.6, página 9 · **(la que el autor quiere a dos columnas)**

- **Qué es:** 5 paneles 4×4 (uno por configuración de banking77: Qwen, laya, multilingual, typed-decisions, kev),
  filas = definición **origen**, columnas = **destino**, color y número = Δ firmado (q − cobertura_B) con
  q = 0.80. Diagonal en gris (—).
- **Verificación:** el PDF es **byte a byte** el `results/matrix/heatmap_banking77_n77_raw_q80.pdf` (md5
  `ffc802a5…`), y los valores del panel Qwen coinciden con la Tabla VII (ent→margin +0.80, pmax→ent −0.20, etc.). ✓
- **Por qué es la mejor figura del paper:** es la única que muestra **las tres cosas a la vez**: (i) el par
  direccional (asimetría: `ent→pmax` = +0.80 pero `pmax→ent` = −0.20), (ii) que el daño depende del modelo
  (Qwen saturado vs laya casi plano) y (iii) que el signo del error cambia (infra vs sobre-cobertura). Ninguna
  tabla puede dar eso de un vistazo. **Es la figura que debería ser el "money shot" del paper, y hoy es la única
  ilegible.**
- **Problemas medidos:**
  1. **Ilegible por construcción:** dibujada a **21 × 4.6 in** (5 paneles × 4.2 in) e insertada a 3.5 in →
     escala **0.164**, o sea **8.8 × 1.9 cm** con texto de 1.5–3.5 pt. Medido en el PDF final: 248 × 54 pt.
  2. **Pasar a `figure*` NO alcanza.** A dos columnas la escala sería 516/1512 = **0.34 → 9 pt salen a 3.1 pt**.
     Sigue siendo ilegible. **Hay que regenerarla a la medida de destino** (ver receta).
  3. **5 barras de color para una sola escala compartida** (`fig.colorbar` dentro del bucle) — el propio
     subtítulo dice "escala COMPARTIDA". Ocupan ~20 % del ancho de la figura.
  4. `vmin = −vmax` simétrico con datos que solo llegan a **−0.20** (porque con q = 0.8 la cobertura no puede
     pasar de 1: Δ ≥ −0.2): **un cuarto del mapa de color no se usa nunca** y el azul se lee como "poco error"
     cuando es el extremo teórico.
  5. El título interno (2 líneas) + el pie dicen lo mismo (T3), y el `suptitle` repite "nivel raw, q=0.8" que
     debería estar en el pie.
  6. La diagonal (4 de 16 celdas = 25 % del área) está en gris: información cero.
- **Receta concreta para dejarla a dos columnas y legible** (un solo cambio en `src/matriz/figura.py`):
  ```
  figsize=(7.1, 3.6)              # 5 paneles de 1.42 in
  fontsize de ticks y títulos: 7  # a 1:1 → 7 pt impresos, legibles
  fontsize de los números: 6.5
  una sola colorbar compartida:  fig.colorbar(im, ax=axes, location="right", fraction=0.02)
  sin suptitle                    # el \caption ya lo dice
  diagonal: sin texto, celda blanca con "—" solo en la primera columna
  ```
  Con eso la figura queda en **7.1 × 3.6 in = 18 × 9.1 cm** a dos columnas (escala 1.0), con números a 6.5 pt.
  Costo: ~1/3 de página. Se paga con creces: es la figura que demuestra el hallazgo.
- **Si no hay espacio para dos columnas:** alternativa honesta = **un solo panel** (el de Qwen, o una fila de
  tasas de empate) a ancho de columna, y el resto a material suplementario. Lo que no se puede es imprimir
  5 paneles a 1.9 cm de alto.
- **Además:** nada genera este archivo dentro de `paper/figures/`. `src/figuras_paper.py` produce **7** figuras y
  no copia el heatmap; hoy es una copia manual de `results/matrix/` (md5 idéntico). Si se regenera la matriz,
  la Fig. 7 del paper queda **vieja sin avisar** — es una grieta en la regla D4. Añadir un `shutil.copy` al final
  de `figuras_paper.py` (o al `correr_matriz` script) y verificar con md5.

### Fig. 8 (PDF) — `fig6-ece-por-definicion.pdf` · §5.7, página 9

- **Qué afirma el pie:** ECE 0.216 con pmax → 0.577 con entropía, factor 2.7×.
- **Verificación:** ECE (binning de Laya) sobre las 2.000 filas de `laya/typed-decisions`: **0.2157** vs **0.5766**
  = **2.67×** ✓.
- **¿Aporta?** Poco: **dos números** en dos barras, y el mismo par ya está en una frase del texto. No está en
  ninguna tabla, así que algo aporta (visualiza la magnitud relativa), pero es la figura con peor relación
  información/espacio del paper.
- **Problemas:** sin n en el pie (el n = 2000 está solo en el título interno, que hay que borrar); sin
  incertidumbre (un ECE sin IC sobre 2.000 filas invita a sobreinterpretar 0.216 vs 0.577 cuando la propia
  definición de ECE cambia con el binning); y el eje x rotulado con dos líneas de texto que a 7.5 pt ya están al
  límite.
- **Recomendación:** o **se elimina** y el número va a la frase (que ya existe), o se **absorbe en la Tabla XIII**
  (que ya lista los 5 ECE globales de sst5: 0.204 / 0.184 / 0.199 / 0.237 / 0.241) ampliándola con la columna del
  ECE de `laya/typed-decisions` — así la comparación entre definiciones queda en una sola tabla, ordenada.

---

## 4. Qué figuras quedan si se aplican las recomendaciones

| Acción | Figuras |
|---|---|
| **Conservar y arreglar** | Fig. 2 (brecha), Fig. 3 (directo vs mapa), Fig. 5 (por par) |
| **Rehacer** | Fig. 1 (**5** configuraciones, pie con "2.2×"), Fig. 4 (CDF pareada en vez de scatter), Fig. 7 (regenerar a 7.1 in + `figure*`) |
| **Eliminar / absorber** | Fig. 6 (→ Tabla IV) y Fig. 8 (→ Tabla XIII o al texto) |

Resultado: **6 figuras** en vez de 8, tres de ellas a dos columnas (2, 5, 7), y ~1 página de flotantes liberada
para texto — que es lo que el paper necesita para respirar (24 flotantes en 12 páginas).

---

## 5. Prioridad de arreglos

| # | Arreglo | Impacto | Esfuerzo | Dónde |
|---|---|---|---|---|
| 1 | `\ref` a las 8 figuras y a las 16 tablas en el cuerpo | alto | bajo (30 min) | `paper/ieee/secciones/*.tex` |
| 2 | Regenerar el heatmap a 7.1 in + `figure*` + colorbar única | **muy alto** | medio (1 h) | `src/matriz/figura.py` |
| 3 | Borrar los `ax.set_title` de las 8 figuras y mover el mensaje al `\caption` | alto | bajo (15 min) | `src/figuras_paper.py`, `src/matriz/figura.py` |
| 4 | Corregir el pie de la Fig. 1 ("triplica" → "duplica", 2.16×) y de la Fig. 6 (44 % no es "la mitad") | alto (honestidad) | bajo | `05_resultados.tex` |
| 5 | Corregir el título interno de la Fig. 3 ("~100×" → "hasta 109×") | medio | bajo | `figuras_paper.py` |
| 6 | Eliminar Fig. 6 y Fig. 8 | medio | bajo | `05_resultados.tex` |
| 7 | Regenerar Fig. 1, 2, 3, 5 a ≤3.5 in (o a 7.1 in con `figure*`) con fuentes 7–8 pt | alto (legibilidad) | medio | `figuras_paper.py` |
| 8 | Rediseñar la Fig. 4 (CDF pareada) | medio | medio | `figuras_paper.py` |
| 9 | Paleta accesible (Okabe-Ito) + trama en las barras verdes/rojas | bajo | bajo | ambos scripts |
| 10 | Renombrar los archivos para que el número coincida con el del PDF (`fig1-…` = Fig. 1) | bajo (mantenimiento) | bajo | `paper/figures/` + `.tex` |

---

## 6. Cómo verificar todo lo anterior

```bash
cd ~/paper-tesis1
# 1. ningún flotante citado (debe devolver vacío hoy, y las líneas cuando se arregle)
grep -rn "ref{fig\|ref{tab" paper/ieee/secciones/
# 2. legibilidad: ancho nativo de cada figura vs 253 pt de columna
for f in paper/figures/*.pdf; do echo "$f $(pdfinfo $f | awk '/Page size/{print $3}')"; done
# 3. tamaño real impreso + altura de glifo en el PDF final
pdftotext -bbox paper/ieee/main.pdf /tmp/bb.xml   # y filtrar palabras con altura < 6 pt
# 4. los números de las figuras
.venv/bin/python docs/auditoria-figuras-verifica.py
# 5. el heatmap del paper es el de la matriz (hoy sí)
md5sum paper/figures/fig8-heatmap-banking77.pdf results/matrix/heatmap_banking77_n77_raw_q80.pdf
```
