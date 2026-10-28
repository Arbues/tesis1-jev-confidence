# v1.0.0 — Instrumento de metrología del campo `confidence` (archivo de la Tesis 1)

> **Snapshot histórico.** Las cifras de esta nota (37 tests, 3.564 celdas) son las del momento del release y
> **no** describen el repo de hoy (**69 tests** hoy: ver `README.md`). Se conserva sin editar como registro del
> depósito; lo posterior va en `docs/release-v1.0.1.md` y en `docs/erratas_especificacion.md` (E5-bis).

Primer estado congelado del instrumento completo, tal como se mide y se publica. Este tag es el que
Zenodo archiva automáticamente (depósito GitHub→Zenodo habilitado el 12-oct-2026) y el que se envía a
Software Heritage.

## Qué contiene

- **Librería `jev-conf-metrics` 0.1.0** — `src/jev_conf_metrics/`: definiciones (`conf_pmax`, `conf_jev`,
  `conf_ent`, `conf_margin`, `conf_noul`), métricas (ECE, `ece_laya`, AUROC, Brier multiclase, NLL, RPS) y
  transferencia (umbrales, celdas, cross-fitting, bootstrap, BH-FDR). Stdlib puro, **37 tests**.
- **Especificación formal** — `paper/03_especificacion_confidence.md` (DEF-1…DEF-8, Proposiciones 1–3) y
  `docs/erratas_especificacion.md` (erratas E1–E5 documentadas).
- **Matriz de transferencia** — `results/matrix/matriz_transferencia.csv` (**3.564 celdas**, 23 grupos) con
  informe regenerable `results/matrix/RESUMEN_MATRIZ.md` y sus heatmaps.
- **Dataset de mediciones crudas** — `results/crudos/` (**65.185 decisiones**, 23 `.jsonl`, una fila por
  decisión con `row_hash`, `model`, definiciones calculadas sobre la misma distribución y `probs` completas).
- **Paso 0 (go/no-go)** — `results/paso0_informe.md` + `results/raw/`: las 5 métricas publicadas de Laya
  reproducidas con |Δ| ≤ 0.003 y `output_tokens = 0` verificado en los brazos de pesos abiertos.
- **Paper** — `paper/secciones/` (§1–§7, fuente en markdown) y `paper/ieee/` (versión IEEEtran, `main.pdf`,
  11 páginas, compila con `latexmk`).
- **Figuras** — `paper/figures/` (8, generadas por `src/figuras_paper.py` a partir de los artefactos).

## Cifras del titular

| Cifra | Valor |
|---|---|
| Decisiones medidas | 65.185 |
| Grupos (modelo × dataset) | 23 (5 configuraciones × 5 datasets) |
| Celdas de la matriz | 3.564 |
| Brecha entre la definición más alta y la más baja de la **misma** distribución | mediana **0.288** (p90 0.434, máx 0.848) |
| Error del porte directo del umbral vs el porte con mapa (nivel `raw`) | **0.2337 vs 0.0021 = 109×** |
| ECE de la misma corrida según definición (`typed-decisions`) | `pmax` 0.216 → `ent` 0.577 (**2.7×**) |

## Pre-registro

El método está congelado antes de la corrida confirmatoria: **DOI 10.5281/zenodo.23266795** (08-oct-2026).
Este release **no modifica** el nivel principal `raw`; la única desviación declarada es **D1** (el debiaser
`L0` no convergía), corregida y reportada en `RESUMEN_MATRIZ.md` §7 y §4 del paper.

## Cómo verificar

```bash
python -m pytest                                     # 37 tests
python src/matriz/informe_matriz.py && git diff --stat   # debe salir VACÍO
python src/figuras_paper.py                          # regenera las 8 figuras
cd paper/ieee && ./compilar.sh                       # main.pdf (11 páginas)
```

## Licencias

Código **Apache-2.0** (`LICENSE`); paper, figuras y docs **CC-BY-4.0** (`LICENSE-docs`). Cita: `CITATION.cff`.
