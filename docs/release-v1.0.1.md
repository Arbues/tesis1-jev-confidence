# v1.0.1 — Corrección de referencias y brazo pagado

Versión de corrección sobre `v1.0.0`. **El motivo del release es concreto:** el snapshot archivado en
`v1.0.0` llevaba el paper y el `.bib` con **referencias incorrectas**, y cualquiera que descargue el ZIP
obtendría esos datos. Se publica una versión nueva en lugar de reescribir la anterior (los tags publicados
no se reescriben; `v1.0.0` queda como histórico).

## Qué cambia respecto a v1.0.0

| Área | Cambio |
|---|---|
| **Referencias (lo que motivó el release)** | Las 9 verificaciones de trazabilidad (D4) resueltas: 3 títulos descriptivos sustituidos por los **canónicos de arXiv**, autores **inventados** corregidos (`arXiv2609.38850` decía «Gao, X. and Wang, Y.»; `2609.26550` decía «{CMU}»), la nota falsa de `good1952` corregida (Good 1952 es la regla **logarítmica**, no la esférica). `paper/02_referencias.bib` y `paper/ieee/referencias.bib` quedan idénticos. |
| **Paper** | `paper/ieee/main.pdf` recompilado con las referencias corregidas; **errata E4** aplicada (el mecanismo no genera texto ≠ el contador `output_tokens` del proveedor: medido ≠ 0 en la API de pago). |
| **Brazo pagado (nuevo)** | `src/matriz/backend_typesafe.py`: adaptador de la API directa de TypeSafe (System One / Jev) registrado en el pipeline. Clave desde `TYPESAFE_API_KEY`/`~/.env`, `model` fijo `jev-1.13.0` con fallo explícito si el servidor responde otro build, reintentos con backoff, contabilidad de tokens y **costo por 1.000 decisiones**, tope con `--presupuesto-usd`. |
| **Tests** | 37 → **52** (15 nuevos sin red, con transporte inyectado). |
| **Cita y trazabilidad** | `CITATION.cff` con el DOI de Zenodo y el **SWHID** de Software Heritage de esta revisión; `docs/` con el contrato de la API verificado en vivo, el informe de blindaje de prioridad y la guía de cierre; `notes/` con la guía literal de la publicación y los costos del brazo pagado. |
| **Metrología nueva documentada** | La API pagada devuelve `probabilities` y `confidence` **redondeadas a 0.01** (rejilla de 0.01) → los empates de umbral no son comparables con los brazos de pesos abiertos; declarado en `docs/erratas_especificacion.md` (E5) y en el contrato. |

## Qué NO cambia

- El nivel principal **`raw`** de la matriz y el dataset de mediciones crudas (65.185 decisiones, 3.564 celdas):
  el pre-registro sigue congelado y no se re-midió nada.
- Las licencias: **Apache-2.0** el código, **CC-BY-4.0** el paper y los docs.
- Los tres depósitos de Zenodo: pre-registro `10.5281/zenodo.23266795`, software (este),
  preprint `10.5281/zenodo.23329431`.

## Verificar

```bash
python -m pytest                                        # 52 tests
python src/matriz/informe_matriz.py && git diff --stat   # debe salir VACÍO
cd paper/ieee && ./compilar.sh                          # main.pdf (11 páginas)
```

El paper en PDF de **esta** revisión coincide byte a byte con el PDF depositado como preprint
(`md5 c9d7d9bb2a65e4addabb5da0663dc5a7`).
