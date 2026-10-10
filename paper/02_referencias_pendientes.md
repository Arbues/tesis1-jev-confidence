# Referencias — verificaciones pendientes (D4)

Estas comprobaciones estaban anotadas como comentarios `% verificar` **dentro** de las entradas de
`paper/02_referencias.bib`. BibTeX no admite comentarios dentro de una entrada: los interpreta como
texto sobrante y **aborta** («I was expecting a `,' or a `}'»), con lo que la compilación del paper
falla. Por eso se sacaron del `.bib` y se listan aquí.

Regla: ninguna cifra del paper depende de esto; es la **trazabilidad de las referencias** (regla D4),
que se confirma contra la fuente (DOI, páginas, venue, autores) antes de enviar el paper.

| clave | qué falta confirmar |
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

Cuando se confirmen, se corrigen **directamente en el `.bib`** (nunca como comentario dentro de la
entrada) y se borra la fila de esta tabla.
