# Guía para cerrar la Tesis 1 — flujo correcto y pendientes (12-oct-2026)

Documento operativo: **qué hacer, en qué orden y por qué ese orden**, con quién hace cada cosa (✋ autor / 🤖 agente),
el criterio de cierre y el coste. Es el mapa de los pendientes `N1`–`N5` (`STATE.json` → `pendientes_2026_10_11`)
más los del autor, reordenados por **dependencia** y no por número.

Regla de mantenimiento: si algo de aquí cambia, se actualiza `README.md` y `STATE.json` en el mismo paso.

---

## 0. Punto de partida (lo que ya está cerrado el 12-oct-2026)

| Hecho | Evidencia |
|---|---|
| Tema, ruta, especificación, librería, matriz y paper redactados | `README.md` §7 · `paper/03_especificacion_confidence.md` · `src/jev_conf_metrics/` (37 tests) |
| Corrida confirmatoria medida | `results/crudos/` (65.185 decisiones) · `results/matrix/matriz_transferencia.csv` (3.564 celdas) |
| Pre-registro publicado | DOI **10.5281/zenodo.23266795** |
| Las 3 decisiones de alcance tomadas | `README.md` §10-ter (repo nuevo · pago vía TypeSafe · arXiv con endosso + preprint) |
| Contrato de la API de TypeSafe **verificado en vivo** | `docs/adaptador-typesafe-contrato.md` §11 (6 llamadas reales, sin GPU, < USD 0.0005) |
| Erratas E4 y E5 resueltas | `docs/erratas_especificacion.md` |
| `CITATION.cff` válido | Validado contra el esquema oficial: 0 errores |
| Zenodo ↔ GitHub conectado | Hecho por el autor |

**Lo que queda abierto, en corto:** reservar con DOI (Fase 1), cerrar el paper (Fase 2), el brazo pagado (Fase 3),
el repo del framework (Fase 4), visibilidad e inglés (Fase 5) y la extensión de Tesis 2 (Fase 6).

---

## 1. El orden correcto y por qué

```
  (0) Decisiones + contrato de la API verificados
        │
        ├─► FASE 1 · RESERVAR ......... gratis, hoy  ─┐  sin cómputo, sin GPU
        │      Release→DOI · preprint→DOI · SWHID · ORCID
        │
        ├─► FASE 2 · CERRAR EL PAPER .. tu revisión ──┘  (las 9 referencias + tu lectura)
        │      (opcional: añadir la medición del brazo pagado como extensión declarada)
        │
        ├─► FASE 3 · BRAZO PAGADO ..... N2, t440, ~USD 0.33
        │      adaptador → medir Jev → fila nueva en la matriz + costo/1.000 decisiones
        │
        ├─► FASE 4 · FRAMEWORK ........ N1, repo nuevo (bloquea N3 y N5)
        │
        ├─► FASE 5 · VISIBILIDAD (N3) + PAPER EN INGLÉS (N5) → arXiv
        │
        └─► FASE 6 · TESIS 2 .......... 4B–9B en el Mac Mini (opcional)
```

**Por qué este orden y no otro**

1. **Reservar antes que mejorar.** El instrumento ya existe y está medido; cada día sin DOI es un día en que otro
   puede publicar lo mismo. Reservar cuesta 0 y no exige cómputo.
2. **El smoke test de la API se hizo antes del Release** justamente para no fechar un texto con un dato sin verificar
   (pasó: `output_tokens` **no** era 0).
3. **El paper se cierra antes de medir el brazo pagado**, porque el resultado nuevo entra como *extensión declarada*:
   así el texto sellado por el pre-registro no se mueve y lo nuevo se añade encima, con su fecha.
4. **El framework va después**: no reserva nada y no bloquea al paper. Sí bloquea a N3 (visibilidad) y N5 (inglés),
   porque el README del framework y `paper/en/` son suyos.
5. **Tesis 2 al final**: exige el Mac Mini y un objetivo de entrenamiento, que es otra tesis.

---

## FASE 1 — Reservar la investigación (gratis, hoy)

Objetivo del autor: *que la investigación quede fechada y firmada antes de que alguien publíque lo mismo*.
Un DOI no prueba autoría, pero sí deja un registro público **con fecha** en Zenodo (CERN) al que cualquiera puede
llegar y que obliga a citar.

### 1.1 Release `v1.0.0` → DOI automático

| | |
|---|---|
| ✋ Autor | Dar el OK (una línea). Zenodo ya está conectado. |
| 🤖 Agente | `git tag v1.0.0` + `gh release create v1.0.0 --notes-file docs/release-v1.0.0.md` |
| ✋ Autor | Zenodo → *Upload → GitHub*: revisar el depósito (tipo **Software**, licencia Apache-2.0, autor con ORCID y FC-UNI) y **Publicar** |
| Resultado | **DOI de versión** + **DOI de concepto** |
| Cierre | Los dos DOI pegados en `CITATION.cff` (`identifiers`) y en `README.md` |

⚠️ **El error que invalida todo:** crear el Release **antes** de conectar Zenodo (ya está hecho, así que no aplica);
o dejar el depósito en borrador para siempre (sin Publicar no hay DOI).

⚠️ El depósito incluye `results/` (120 MB, 65.185 mediciones). Es correcto, pero si se prefiere el dataset crudo
como registro aparte, basta depositar el ZIP a mano (los metadatos están en `STATE.json` → `reserva_y_depositos`).

### 1.2 Preprint del paper → DOI propio (sin esperar a arXiv)

| | |
|---|---|
| ✋ Autor | ✅ **HECHO el 13-oct-2026**: el preprint está publicado con DOI `10.5281/zenodo.23329431` |
| Idioma | Español. **Zenodo no exige inglés** (arXiv sí). |
| Licencia | CC-BY-4.0 |
| Cierre | DOI del preprint enlazado desde `README.md` y desde el `CITATION.cff` (`is supplemented by` / relación al instrumento) |

Esto es lo que reserva **la narrativa**, no solo el código: fecha el texto completo hoy y deja arXiv para cuando
llegue el endosso, sin prisa y sin exponer la sustentación a depender de él.

### 1.3 Software Heritage (archivo independiente + SWHID)

| | |
|---|---|
| 🤖 Agente | *Save Code Now* sobre `https://github.com/Arbues/tesis1-jev-confidence` (se hace **después** del tag, para archivar el commit exacto del release) |
| Resultado | `SWHID` del commit/tag |
| Cierre | SWHID en `CITATION.cff` (`identifiers: type: swh`) |
| Nota honesta | SWH da preservación y un identificador intrínseco; **no** da prioridad ni crédito. Tarda horas en repos de GitHub ya conocidos. |

### 1.4 ORCID

| | |
|---|---|
| ✋ Autor | ORCID `0009-0004-7605-6569`: importar los DOI como *works* (hoy tiene **0 trabajos**) |
| 🤖 Agente | Dejar listo el BibTeX de los DOI para que el import sea copiar/pegar |

### 1.5 Opcional: sello de tiempo criptográfico (OpenTimestamps)

Ningún DOI prueba *cuándo* se escribió algo; solo cuándo se publicó. Si se quiere una prueba criptográfica de que
el commit existía antes de una fecha: `ots stamp <archivo con el hash del commit>` (herramienta **no instalada**
todavía; se instala con `uv tool install opentimestamps-client`). Es gratis y se refuerza con `ots upgrade` en unas
horas (ancla en Bitcoin). **Opcional**: el DOI ya da la fecha pública verificable.

---

## FASE 2 — Cerrar el paper (tu revisión; nada de cómputo)

### 2.1 Leer el borrador y dar observaciones ✋

`paper/secciones/01…07` (markdown, fuente de verdad) o `paper/ieee/main.pdf` (11 páginas). Puntos donde tu criterio
manda: énfasis del titular, longitud, qué queda en el marco teórico y qué en resultados.

### 2.2 Confirmar las 9 referencias ✋ (regla D4)

`paper/02_referencias_pendientes.md`:

| clave | falta |
|---|---|
| `naeini2015` | páginas del ECE |
| `good1952` | origen del *spherical score* |
| `jitkrittum2023` | lista de autores |
| `arXiv2609.38850` | autores |
| `arXiv2609.33843` | autores |
| `arXiv2609.30216` | autores / venue |
| `arXiv2609.33209` | autores / venue |
| `arXiv2609.26758` | autores / venue |
| `arXiv2609.26550` | año |

Se corrigen directamente en `paper/02_referencias.bib` (nunca como comentario dentro de la entrada: BibTeX aborta)
y se borra la fila de la tabla. Ninguna cifra del paper depende de esto: es trazabilidad.

### 2.3 Decidir si el PDF IEEE lo representa ✋

Si sí: se congela como `v1.0.0` del paper y el preprint se deposita desde ese PDF.
Si hay cambios: se editan `paper/secciones/*.md` **y** `paper/ieee/secciones/*.tex` (deben decir lo mismo), y se
recompila con `cd paper/ieee && ./compilar.sh`.

### 2.4 Extensión declarada (opcional, pero recomendable): la medición del brazo pagado

La primera llamada real ya dejó dos datos que el paper no tiene y que son material directo del argumento central:

| Dato medido | Dónde va |
|---|---|
| `output_tokens` **no** es 0 en la API pagada (71 / 58 / 31) | ya aplicado (errata E4) |
| La API devuelve `probabilities` y `confidence` **redondeadas a 0.01** → rejilla de 0.01, con empates de umbral mucho más probables que en los brazos de pesos abiertos | nueva subsección declarada como **posterior al pre-registro** |
| `score` usa **otra** fórmula (`MAD_unif`) que `choice` → quinta definición | errata E5; entra o no según §3.2 |

---

## FASE 3 — El brazo pagado (`N2`): medir Jev de verdad

Cuesta céntimos y no necesita GPU: el modelo corre en TypeSafe y el t440 solo manda HTTP.

### 3.1 Adaptador `typesafe-jev` 🤖

Según la receta de `docs/adaptador-typesafe-contrato.md` §12. Puntos que no se pueden improvisar:

- Clave: `TYPESAFE_API_KEY` desde `~/.env` (nunca al repo, nunca a una fila).
- `model = "jev-1.13.0"` explícito; `model_revision = response.model` por fila.
- `criteria` (mapa en `choice`, array ordenado en `score`), **1 request por ítem** (no hay lote).
- Copiar `usage` tal cual a la fila (`input_tokens`, `output_tokens`) y el coste.
- Reintentos con backoff en `429`/`529`; presupuesto máximo declarado por corrida.

### 3.2 Decisión pendiente del autor ✋

¿La definición que el API devuelve en `score` (`MAD_unif`) entra en la librería y en la matriz como **extensión
declarada** (definición nueva + test + celda), o se queda solo en el marco teórico? Toca artefactos sellados por el
pre-registro, por eso es decisión del autor.

### 3.3 Corrida y declaración 🤖

- Medir los datasets ya etiquetados (typed-decisions, SST-5, WANLI, Banking77, CLINC150 según cardinalidad).
- **Declarar la rejilla de 2 decimales** del brazo pagado: los empates de umbral (`n_empates_tau`) no son comparables
  con los brazos de pesos abiertos; no mezclar sin más.
- Añadir la columna **costo por 1.000 decisiones** (medido: ≈ USD 0.013–0.017 con 2–5 opciones).
- Cierre: un `.jsonl` crudo nuevo con su `.meta.json`, y su celda en `RESUMEN_MATRIZ.md`.

---

## FASE 4 — El repositorio del framework (`N1`)

Objetivo: que un tercero pueda **comparar modelos tipo Jev sin leer el paper**. La auditoría del 12-oct dice que esto
no es "limpiar": es construir. Núcleo a importar: `src/jev_conf_metrics/` (stdlib puro, autocontenido) + los 37 tests.

| Bloqueador (auditoría) | Qué exige |
|---|---|
| **B1** No existe la CLI | `cli.py` + `[project.scripts] jevconf = …` con `list-brazos · medir · matriz · informe · figuras`, `--out` y semillas |
| **B2** El pipeline no está empaquetado | Empaquetar `medir`/`matriz`/`informe`/`figuras` dentro del paquete (hoy viven en `src/` con hacks de `sys.path`) |
| **B3** `medir` exige GPU o red | Un backend **simulado** determinista (por semilla) + `--mock` real, para que los tests corran sin GPU |
| **B4** Adaptadores dependen de `datasets` + HF y `datasets` no está declarado | Extra opcional `datasets` + fixtures locales para los tests |
| B5–B9 | Tests portables, defaults fuera del layout del repo, `docs/adaptadores.md` y `docs/reproducibilidad.md`, `classifiers`/topics |

Cierre: un desconocido clona, instala, corre el ejemplo del README **sin leer el paper** y obtiene las mismas cifras.
El repositorio nuevo lleva su propio release y su propio DOI (que se pide cuando exista).

---

## FASE 5 — Visibilidad (`N3`) y paper en inglés (`N5`)

### 5.1 Visibilidad (gratis, sin cómputo)

1. README del framework **en inglés** con: qué resuelve, ejemplo mínimo, **cita del paper y los DOI**, enlace al
   dataset crudo y a las figuras.
2. `CITATION.cff` en el framework + sección "Cómo citar" en este repo.
3. Metadatos: `keywords`/`classifiers`/`description` con las cifras del titular y topics en GitHub.
4. Anuncio en los foros del ecosistema inventariados en `eje-2-jev-opensource/FUENTES.md`, **siempre enlazando al DOI**.
5. Versión corta divulgativa: 1 figura + la tabla por par ("el mismo campo, el mismo dato, el umbral que no viaja").

### 5.2 Paper en inglés (`N5`) — y arXiv

- `paper/en/secciones/` con la **misma numeración** que la versión en español; fuente única en markdown.
- Figuras: segunda salida en inglés desde el mismo `src/figuras_paper.py` → `paper/figures/en/`.
- Un solo `paper/02_referencias.bib` compartido (evita arreglar las 9 entradas dos veces).
- Terminología fija: *confidence* (nunca "trust"), *threshold transfer*, *coverage*, *answered accuracy*,
  *scoring rule*.
- ✋ **Endosso de arXiv** (no bloquea nada): hace falta un autor con publicaciones en el mismo dominio; se solicita al
  intentar el primer envío y arXiv da el código que esa persona introduce. **arXiv exige la versión completa en
  inglés** desde feb-2026.
- Declarar en el PDF la versión de idioma ("English version of the Spanish original", con fecha).

---

## FASE 6 — Tesis 2 (opcional, otro alcance)

Medir 4B–9B en el Mac Mini (Jeff-1, SemIf, jev-lite, Nimble-9B, tinyjev) con la skill `huggingface-local-models`.
En la RTX 4050 solo caben los pequeños con encoder congelado y features cacheadas. El objetivo de Tesis 2 es
**modificar el objetivo de entrenamiento RLCD para inducir calibración**, no volver a medir.

---

## 7. Resumen: quién hace qué

| Fase | ✋ Autor (tiempo) | 🤖 Agente | Coste | Criterio de cierre |
|---|---|---|---|---|
| 1.1 Release + DOI | OK + revisar y **Publicar** en Zenodo (~5 min) | tag + Release + pegar DOI en CITATION/README | $0 | DOI de versión y de concepto en el repo |
| 1.2 Preprint | pegar metadatos y Publicar (~5 min) | preparar draft y metadatos | $0 | DOI del preprint enlazado |
| 1.3 Software Heritage | — | Save Code Now + SWHID al CITATION | $0 | SWHID en `CITATION.cff` |
| 1.4 ORCID | importar works (~3 min) | dejar el BibTeX | $0 | DOIs en ORCID |
| 2. Paper | leer §1–§7 y decidir formato | corregir, recompilar, referencias | $0 | PDF definitivo + `.bib` sin pendientes |
| 3. Brazo pagado | decidir `conf_score` | adaptador + corrida + declaración | ~USD 0.33 | `.jsonl` crudo + celda + costo/1.000 |
| 4. Framework | OK para crear el repo | paquete + CLI + tests + docs + release | $0 | `pip install` + ejemplo del README |
| 5. Visibilidad + inglés | endosso de arXiv | `paper/en/`, anuncios, metadatos | $0 | arXiv enviado + anuncio hecho |
| 6. Tesis 2 | decidir alcance | medir 4B–9B (Mac Mini) | $0 (local) | modelos nuevos en la matriz |

---

## 8. Lo que NO hay que hacer (trampas de este proyecto)

- **No tocar `paper/04_pre_registro.md`**: es el texto depositado con DOI. Las correcciones van como errata.
- **No crear el Release antes de conectar Zenodo** (ya está conectado; no revertirlo).
- **No añadir definiciones al nivel `raw` sellado**: lo nuevo entra como extensión declarada, con su fecha.
- **No escribir la clave en el repo, en logs ni en una fila**: `TYPESAFE_API_KEY` solo en `~/.env`.
- **No decir "`output_tokens = 0`" del brazo pagado**: está medido que no lo es.
- **No mezclar el brazo pagado con los abiertos sin declarar la rejilla de 0.01.**
- **No usar `jev-latest` para medir**: se mueve; fijar `jev-1.13.0` y registrar `response.model`.
- **Jev ≠ JEPA.** El material de `eje-1-jepa/` y `_descartado/` está fuera de alcance y se eliminó del repo (solo en el historial de git).

---

## 9. Lo hecho el 12-oct-2026 (registro)

`docs/adaptador-typesafe-contrato.md` (contrato + verificación en vivo) · `docs/informe-blindaje-prioridad-2026.md`
(mecanismos de reserva verificados) · `notes/pago-jev-api-costos-2026-10-12.md` (economía del brazo pagado) ·
`docs/erratas_especificacion.md` E4–E6 · `docs/release-v1.0.0.md` y `release-v1.0.1.md` ·
`README.md` §10-ter y §10-quater · `STATE.json` → `decisiones_2026_10_12` y `contrato_api_typesafe_2026_10_12`.
