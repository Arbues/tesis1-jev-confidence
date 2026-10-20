# Referencias — verificaciones pendientes (D4)

Estas comprobaciones estaban anotadas como comentarios `% verificar` **dentro** de las entradas de
`paper/02_referencias.bib`. BibTeX no admite comentarios dentro de una entrada: los interpreta como
texto sobrante y **aborta** («I was expecting a `,' or a `}'»), con lo que la compilación del paper
falla. Por eso se sacaron del `.bib` y se listan aquí.

Regla: ninguna cifra del paper depende de esto; es la **trazabilidad de las referencias** (regla D4),
que se confirma contra la fuente (DOI, páginas, venue, autores) antes de enviar el paper.

## Estado

**Las 9 verificaciones pendientes están resueltas y corregidas en el `.bib` (12-oct-2026): la tabla
queda vacía.** Cada corrección se hizo directamente en `paper/02_referencias.bib` y se copió a
`paper/ieee/referencias.bib` (los dos archivos quedan byte a byte idénticos).

Resumen de lo aplicado (detalle, valor final y URL de la fuente en el informe de verificación):

- `naeini2015` — páginas **2901--2907** confirmadas; el `.bib` ya las tenía.
- `good1952` — la nota era incorrecta: Good (1952) es el origen de la regla **logarítmica**, no de la
  esférica (la esférica se atribuye a Roby, 1964). Nota corregida.
- `jitkrittum2023` — lista completa de autores (seis) añadida; nota `confirmar lista de autores` borrada.
- `arXiv2609.38850` — autores reales (Gao, Zhimin y Wang, Pichao; las iniciales del `.bib` eran
  inventadas) y título canónico de arXiv.
- `arXiv2609.33843` — autor único: Nandakishore, Gowthamkumar.
- `arXiv2609.30216` — autores: Ling, Guoming; Xue, Muen; Ye, Zijian. Venue: arXiv (preprint).
- `arXiv2609.33209` — autores: Li, Keyi; He, Yihao; Li, Quanyi. Venue: arXiv (preprint). Título canónico.
- `arXiv2609.26758` — autores: Sun, Yu; Xu, Junhao; Shi, Jiajia; Yang, Zijin. Venue: arXiv (preprint).
  Título canónico.
- `arXiv2609.26550` — año **2026** confirmado (21-sep-2026), autores reales (antes `{CMU}`) y título completo.

## Resuelto por el autor (19-oct-2026)

| tema | decisión aplicada | estado |
|---|---|---|
| Atribución de la regla **esférica** | Se añadieron **dos** entradas verificadas contra Crossref: `roby1965` (Roby, T. B., «Belief states and the uses of evidence», *Behavioral Science* 10(3):255–270, 1965, DOI `10.1002/bs.3830100304`) y `jose2009` (Jose, V. R., «A Characterization for the Spherical Scoring Rule», *Theory and Decision* 66(3):263–281, 2009, DOI `10.1007/s11238-007-9067-x`). El texto pasa a citar `\cite{good1952,roby1965,epstein1969}` y añade la caracterización axiomática. La regla ya no queda huérfana. | ✅ cerrado |
| Títulos de arXiv | **Estándar global fijado** para todas las entradas arXiv (ver abajo). | ✅ cerrado |

**Nota de honestidad (D4).** La literatura repite «Roby (1964)»: ese año corresponde a la versión previa (no
publicada como artículo). El artículo indizado es de **1965** y es el que se cita. No se pudo leer el texto
completo (paywall), así que la atribución se sostiene en la fuente secundaria que la establece
(`jose2009`), no en una lectura directa. El PDF local se recompiló: 11 páginas, 36 ítems, 0 citas sin resolver.

## Estándar de citas (fijado el 19-oct-2026)

1. **arXiv** → tipo `misc`, con `eprint`, `archivePrefix={arXiv}`, `howpublished={\url{https://arxiv.org/abs/ID}}`
   y el **título canónico entre llaves dobles** para preservar mayúsculas. Nunca se inventa `primaryClass` ni `doi`.
2. **Artículo de revista** → `title`, `author`, `journal`, `volume`, `number`, `pages`, `year`, `doi`.
3. **Libro / actas** → `booktitle`/`publisher` + `pages` + `year` + `url` o `doi`.
4. **Repositorio o blog** → tipo `misc` con `author` (o la organización), `title`, `year` y `howpublished={\url{...}}`.
5. **Toda entrada** debe tener un localizador verificable (DOI o URL). Sin localizador no entra.
6. **Nunca** escribir una arroba (`@`) dentro de un comentario del `.bib`: BibTeX la lee como entrada y aborta.

### Excepciones declaradas

| clave | excepción | razón |
|---|---|---|
| `lakoreai2026` | no lleva `eprint`: se cita por el repositorio | se difundió como preprint + repo y no tiene un ID de arXiv resoluble |
| `sev` / `kev-suites` | citados como repositorio | no son publicaciones |
| `roby1965` · `jose2009` | — | ambas con DOI verificado en Crossref |

> Los dos `.bib` (`paper/02_referencias.bib` y `paper/ieee/referencias.bib`) se mantienen **byte a byte
> idénticos** (`md5 b28e7a8c…` antes de esta edición). Si se edita uno, se copia al otro en el mismo paso.

Cuando se detecten verificaciones nuevas, se corrigen **directamente en el `.bib`** (nunca como
comentario dentro de la entrada) y se añade una fila a la tabla de abajo.

| clave | qué falta confirmar |
|---|---|
| — | (ninguna) |
