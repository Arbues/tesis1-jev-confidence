# Pendientes anotados (11-oct-2026) — repo-framework, modelos de pago, visibilidad, prioridad y paper en inglés

Instrucción del autor (11-oct-2026), tras la exploración de reentrada (`notes/hallazgos.md`).
Espejo máquina-legible: `STATE.json` → `pendientes_2026_10_11` y `siguientes_pasos` n=11…15.
Índice: `README.md` §10-bis. Regla de orden vigente: la raíz solo lleva archivos de entrada (`README.md` §3-bis).

**Estado:** 5 pendientes, **0 con cómputo pendiente**; 3 exigen una decisión previa del autor (✋).

| # | Pendiente | Tamaño | Cierra cuando | ✋ |
|---|---|---|---|---|
| N1 | Repo-framework limpio y reutilizable | L | `pip install` + `--help` documentado + release con tag y CI verde | mismo repo vs repo nuevo |
| N2 | Modelos de pago por API key + costo por 1.000 decisiones | M | una corrida real contra `typesafe-ai/jev` con JSONL y tabla de costos | método de pago (API key) |
| N3 | Visibilidad del paper y del framework | S | README del framework con DOI + paper + dataset, y anuncio hecho | — |
| N4 | Blindaje de prioridad y crédito | S | cada entregable con fecha verificable (DOI/tag/archivo) | arXiv antes de sustentar: sí/no |
| N5 | Paper en inglés versionado | M | `paper/en/` y compilación IEEE en inglés con la misma numeración | — |

---

## N1. Repo-framework limpio (el actual está "sucio")

**Problema.** El repo mezcla tres cosas que no viajan juntas: (a) el **instrumento** (`src/jev_conf_metrics/`,
la matriz, las figuras), (b) la **exploración** (`audit/`, `contexto/`, `eje-2-jev-opensource/`, y las carpetas
fuera de alcance `eje-1-jepa/` y `_descartado/`) y (c) los **artefactos históricos** (`results/raw/`,
`results/crudos/` con 65.185 filas, `downloads/`, `data/`). Un tercero que quiera comparar modelos no debería
tener que atravesar eso.

**Objetivo.** Un repo donde comparar modelos tipo Jev sea una operación de tres comandos: instalar, declarar
los brazos (adaptadores), medir y obtener la tabla de transferencia + las mediciones crudas.

```
  datasets ──▶ ┌────────────────────────────────────────────────┐
               │ jev-conf-metrics · definiciones + métricas      │──▶ mediciones crudas (jsonl + row_hash)
               └────────────────────────────────────────────────┘    y matriz de transferencia (CSV)
                     ▲                    ▲                    ▲
        adaptador    │       adaptador    │       adaptador    │
        open-weights │       proveedor    │       control      │
     (Laya, Kev, …)  │  (Jev vía gateway, │   (p uniforme /    │
                     │   OpenAI-compat.)  │    azar reproducible)│
```

**Sub-pasos.**
1. Decidir la casa del framework (✋): (a) limpiar **este** repo y mover la exploración a `notes/` o a un tag
   histórico, o (b) **repo nuevo** (p. ej. `decision-calibration-bench`, nombre ya propuesto en
   `contexto/00_veredicto_jev_typesafe.md` §7) importando `src/jev_conf_metrics/` + tests.
2. Convertir el pipeline en paquete: interfaz única `medir(brazos, datasets, nivel, q)`; nada de rutas
   absolutas ni de rutas del Nitro; sin `data/` ni pesos versionados (se descargan por script).
3. CLI: `jevconf list-brazos | medir | matriz | informe | figuras`, con `--out` y semillas fijas.
4. Tests: los 37 actuales + tests de adaptadores con **proveedores simulados** (sin red) + un test de
   conformidad del contrato de salida (campos mínimos por ítem).
5. Docs: `README` (qué resuelve, cómo se instala, ejemplo mínimo de 10 líneas), `docs/libreria.md`,
   `docs/adaptadores.md` (cómo añadir un proveedor), `docs/reproducibilidad.md` (hashes y seeds).
6. Release: `v1.0.0` con tag, `CHANGELOG.md`, `CITATION.cff` y DOI de Zenodo para el código.
7. Mover a `notes/` (o borrar con historia en git) lo que no sea framework: `audit/`, `contexto/`,
   `eje-1-jepa/`, `_descartado/`, `downloads/`. Los `results/` grandes se publican como dataset con DOI, no
   como directorio del repo.

**Criterio de cierre:** un desconocido clona, instala, corre el ejemplo del README y obtiene un CSV con las
mismas cifras que la matriz publicada (o su propia medición) **sin leer el paper**.

---

## N2. Modelos de pago por API key (comparar no solo open-source)

**Por qué.** El objetivo no es comparar open-source entre sí, sino decidir **qué conviene en costo/beneficio**:
el propio Jev cuesta **$0.042 por millón de tokens de entrada y $0 de salida** (`FUENTES.md`, bloque de precio),
y el **crédito gratuito de la Vercel AI Gateway ($5/mes)** alcanza para el estudio completo; con los seis brazos
baratos el total queda **por debajo de USD 30** (`contexto/00_veredicto_jev_typesafe.md` §3.2). Comparar solo
pesos abiertos deja fuera justo al objeto de la tesis.

**Acceso (ya investigado, no hay que repetirlo).** `contexto/00_veredicto_jev_typesafe.md` §3.1: la ruta sin
lista de espera es la **Vercel AI Gateway** (cuenta + método de pago + `AI_GATEWAY_API_KEY`, modelo
`typesafe-ai/jev`); la vía directa de TypeSafe pasa por lista de espera. Plan B siempre disponible: pesos
abiertos.

**Sub-pasos.**
1. Definir el **contrato de adaptador** (una función por proveedor): recibe `estado` + `preguntas` etiquetadas
   y devuelve por ítem `{opción, probabilidades, confidence declarada, output_tokens, latencia, modelo,
   versión, usd}` — el mismo JSONL que ya producen los brazos abiertos.
2. Adaptador `openai_compatible` (cubre gateways y proveedores cerrados) + adaptador `jev_gateway`.
3. **Costo**: por ítem y agregado → tabla "costo por 1.000 decisiones" junto a ECE/Brier (la comparación
   honesta es calidad **por dólar**).
4. Robustez: reintentos con backoff ante 429, cache en disco por `(modelo, versión, ítem)` para no pagar dos
   veces, y presupuesto máximo declarado por corrida.
5. **Fijar versión y registrar el campo `model`** de cada respuesta: `jev-latest` cambia de build (riesgo R6
   de `contexto/00_veredicto_jev_typesafe.md` §6); el paper reporta la versión medida.
6. **Seguridad:** la API key vive en `~/.env` y se lee por variable de entorno; en docs y ejemplos va como
   placeholder `[VER ~/.env → AI_GATEWAY_API_KEY]`, nunca literal. `.gitignore` cubre `.env`.

**Criterio de cierre:** una corrida real (≥ 200 ítems) contra un modelo de pago, con su JSONL crudo, su
versión de modelo registrada y su fila de costo por 1.000 decisiones en la tabla comparativa.

---

## N3. Visibilidad del paper y del repo-framework

**Problema.** Hoy el paper vive en un repo de tesis y el framework no existe; nadie que busque "comparar
confianza en modelos tipo Jev" llega a ninguno de los dos.

**Qué se hace (sin costo).**
1. README del framework en inglés, con: qué resuelve, ejemplo mínimo, **cita del paper** (título, autor, DOI
   del pre-registro `10.5281/zenodo.23266795`), enlace al **dataset crudo** y a las **figuras**.
2. `CITATION.cff` en el framework + sección "Cómo citar" en la raíz del repo de tesis.
3. Metadatos para buscadores: `pyproject.toml` con `keywords`/`classifiers`, `description` con las cifras del
   titular (23 grupos, 65.185 decisiones, 3.564 celdas, 109×), topics del repo en GitHub.
4. Anuncio en los foros y comunidades del ecosistema inventariados en `eje-2-jev-opensource/FUENTES.md` y
   `eje-2-jev-opensource/08_estudio_ecosistema.md` (20+ arneses y proyectos), siempre enlazando al DOI y no a
   un archivo suelto.
5. Versión corta divulgativa (1 figura, la tabla por par) para el anuncio: el titular que sobrevive es
   "el mismo campo, la misma decisión, umbral que no viaja".

**Criterio de cierre:** el framework y el paper se citan mutuamente, y un tercero puede llegar al DOI desde el
README del framework en un clic.

---

## N4. Blindaje de prioridad y crédito (que nadie lo replique y se lleve el crédito)

**Problema.** El valor del instrumento "sobrevive igual" (`README.md` §10), pero **el crédito no**: si otro
publica la tabla de transferencia antes, la tesis igual sale, pero sale segunda.

**Mecanismos, de más barato a más expuesto.**

| Mecanismo | Qué reserva | Fecha verificable | Costo/riesgo |
|---|---|---|---|
| Pre-registro Zenodo (**ya hecho**) `10.5281/zenodo.23266795` | El **método**: definiciones, modelos, datasets, cross-fitting, q, FDR y los dos portes | 08-oct-2026 ✔ | hecho |
| **DOl por versión** en Zenodo (v1.0 código, v1.0 dataset crudo) | El **código** y las **mediciones crudas** completas (65.185 filas) | al publicar | gratis |
| **Tag + Release** en GitHub con notas y `CITATION.cff` | El estado exacto del software | fecha del release | gratis |
| **Software Heritage** (archivado del repo) | Preservación + sello temporal independiente de GitHub | inmediata | gratis |
| **CITATION.cff + licencias con atribución** (Apache-2.0 código, CC-BY-4.0 paper/docs) | La **obligación de citar** si alguien reutiliza | vigente | gratis |
| **arXiv** (preprint) | Sello temporal público y alcance inmediato | inmediata | ✋ revela el texto completo antes de la sustentación |

**Decisión del autor (✋).** arXiv maximiza prioridad y visibilidad, pero publica el borrador completo antes de
sustentar. Alternativa intermedia: subir **primero** al framework/DOI las piezas que ya están preregistradas
(código + dataset crudo + figuras: reservan la medición sin entregar la narrativa) y dejar el preprint para
después de la sustentación.

**Nota de honestidad (importante):** el repo **ya es público** desde el 10-oct-2026 y el borrador §1–§7 y el PDF
IEEE están versionados ahí. La prioridad del pre-registro está a salvo, pero "reservar al máximo" ya no puede
significar "ocultar": la vía realista es **citar y fechar** cada entregable (DOI por versión) y publicarlos
juntos, de modo que cualquier réplica quede, por fecha, detrás.

---

## N5. Paper en inglés, versionado

**Objetivo.** Mayor alcance sin duplicar el trabajo: una **fuente única en markdown** (español, `paper/secciones/`)
y su traducción versionada al inglés en `paper/en/secciones/`, con **la misma numeración** de secciones,
figuras y tablas (así dos lectores pueden hablar de "§4.2" sin ambigüedad).

**Sub-pasos.**
1. Esperar a que el borrador español se congele (revisión §1–§7 del autor) y traducir por secciones, no de una
   vez: mismo orden que la lectura.
2. `paper/en/ieee/` con `main.tex` en inglés (misma clase IEEEtran); el `compilar.sh` se parametriza por idioma.
3. **Figuras:** las 8 figuras se generan desde `src/figuras_paper.py`; hay que añadir el idioma de las etiquetas
   (una segunda salida, no un segundo script) → `paper/figures/en/`.
4. Terminología fija (glosario EN ↔ ES) para no traducir `confidence` de tres maneras distintas:
   `confidence` (nunca "trust"), *threshold transfer*, *coverage*, *answered accuracy*, *scoring rule*.
5. Referencias: un solo `02_referencias.bib` compartido (el mismo archivo, dos documentos) — evita que las
   9 entradas pendientes se arreglen por duplicado.
6. Declarar la versión de idioma en el propio PDF ("English version of the Spanish original", con la fecha).

**Criterio de cierre:** `main.pdf` en inglés compila con `latexmk`, con la misma numeración y las mismas
cifras que la versión en español, y ambas se citan desde el README.

---

## Falta información para actuar

1. **N1 — casa del framework:** ¿repo nuevo (`decision-calibration-bench`) o este repo limpiado? Define si el
   historial de exploración se conserva en el mismo lugar o queda como tag/archivo.
2. **N2 — método de pago:** ¿hay tarjeta para la Vercel AI Gateway (USD 5/mes de crédito incluido)? Si no, el
   brazo de pago espera y se sigue con pesos abiertos.
3. **N4 — arXiv:** ¿preprint antes o después de la sustentación? Cambia qué se publica primero.
4. N3 y N5 no bloquean nada: se pueden ejecutar en cuanto haya decisión sobre N1 (el framework es el soporte de
   ambos).
