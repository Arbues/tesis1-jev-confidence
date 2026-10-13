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

## Pendiente de criterio del autor (12-oct-2026)

| tema | qué falta | nota |
|---|---|---|
| Atribución de la regla **esférica** | El texto la cubre con `\cite{good1952,epstein1969}`; Good (1952) es la **logarítmica** y Epstein (1969) el RPS, así que la esférica queda sin autoría propia | La atribución habitual es **Roby (1964)**, pero el agente **no la pudo verificar** en fuentes independientes (la búsqueda no devolvió nada). Alternativa: dejarla amparada en `gneiting2007`, que caracteriza la familia de reglas estrictamente propias y ya está citada en el mismo párrafo. **Decide el autor**: añadir `roby1964` (previa verificación) o dejarlo como está |
| Títulos canónicos de arXiv | Se sustituyeron 3 títulos descriptivos que no coincidían con la fuente (`38850`, `33209`, `26758`) y se completó `26550` | Si se prefieren los descriptivos, se revierten en un paso. Ninguna clave de cita cambió |

Cuando se detecten verificaciones nuevas, se corrigen **directamente en el `.bib`** (nunca como
comentario dentro de la entrada) y se añade una fila a la tabla de abajo.

| clave | qué falta confirmar |
|---|---|
