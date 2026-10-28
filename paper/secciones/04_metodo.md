# §4. Método (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 4 · 08-oct-2026*
*Todo lo que sigue describe un procedimiento congelado antes de la corrida principal y declarado en el
pre-registro (`paper/04_pre_registro.md`, DOI 10.5281/zenodo.23266795). Ningún parámetro se ajustó después
de ver los resultados.*

> **Desviaciones declaradas.** El pre-registro exige reportarlas y están en `results/matrix/RESUMEN_MATRIZ.md`
> §7. La única con efecto sobre los datos es la D1: al auditar el pipeline se encontró que la
> implementación del debiasing `L0` no convergía (paso ~1000× demasiado pequeño), de modo que ese nivel era
> indistinguible de `raw`; se corrigió y las celdas `L0` se recalcularon. El nivel principal `raw` —
> sobre el que van todos los titulares— no se tocó tras publicar el pre-registro. D2 (un archivo
> contaminado del piloto, descartado) y D3 (`clinc150` no ejecutable en un checkpoint) no afectan a la
> confirmatoria.

---

## 4.1. Modelos bajo medición

Se midieron cinco configuraciones de pesos abiertos, todas con `output_tokens = 0` verificado (no generan
texto). La revisión exacta de cada una (sha del Hub) quedó registrada por grupo en `results/crudos/*.meta.json`
y en `results/raw/paso0_versions.json` (regla D4).

| configuración | familia | parámetros | papel |
|---|---|---|---|
| `convaiinnovations/laya` | encoder ModernBERT-large + cabeza de decisión | 421M | implementación de referencia |
| `convaiinnovations/laya`, subcarpeta `typed-decisions` | el mismo repositorio, ajustado al benchmark | 421M | variante afinada |
| `convaiinnovations/laya`, subcarpeta `multilingual` | el mismo repositorio, encoder multilingüe | n.d. | multilingüe |
| `jaredpalmer/kev-0.8b` | familia Kev (0.8B) | 0.8B | familia entrenable |
| `Qwen/Qwen3.5-0.8B-Base` | Qwen, sin ajuste a decisiones | 0.8B | **control crudo** (nivel `raw`) |

El control crudo es deliberado: permite ver la transferencia en un modelo que no fue entrenado para
emitir decisiones, y así separar lo que aporta el entrenamiento de lo que es propio del readout.

## 4.2. Datasets

Todos ya etiquetados. No hubo anotación, etiquetado humano ni kappa (regla D2).

| dataset | n (cardinalidad) | ítems | por qué |
|---|---|---|---|
| `LocalLLaMA/typed-decisions` | 2, 4, 5 | 2.000 | el benchmark compartido del ecosistema |
| `SetFit/sst5` | 5 | 1.101 | ordinal (primitivo `score`) |
| `alisawuffles/WANLI` | 3 | 5.000 | inferencia de lenguaje natural |
| `mteb/banking77` | 77 | 3.076 | cardinalidad alta |
| `clinc/clinc_oos` (`plus`) | 151 | 3.100 | extremo de cardinalidad (el límite documentado de Jev) |

Cinco configuraciones por cinco datasets dan 25 combinaciones posibles; se midieron 23 grupos. Las dos
ausencias no son fallos del pipeline y se declaran en §4.7.

Decisiones totales medidas: 65.185 (una fila por modelo, dataset e ítem), en `results/crudos/*.jsonl`.

## 4.3. Las definiciones bajo medición

Sobre la distribución `p` que cada modelo devuelve para cada ítem se calcularon, en paralelo y con el mismo
dato, las cuatro definiciones analíticas de la especificación (`paper/03_especificacion_confidence.md`):

`C_max = p_max` (DEF-4) · `C_Jev = (n·p_max − 1)/(n − 1)` (DEF-1) · `C_ent = 1 − H(p)/ln n` (DEF-2) ·
`C_mar = p_(1) − p_(2)` (DEF-5). La quinta, `C_noul = max(π, 1−π)` (DEF-3), entra en el bloque de `n = 2`.

Las dos definiciones opacas (`act_probability` de Laya y `open-decision-ai`) quedaron fuera de la matriz
por decisión de alcance: no son funciones de `p` y no tienen clase de equivalencia en orden. Las
transformaciones AnyJev (nivel `L0`, debiasing sin etiquetas; nivel `L1`, temperatura ajustada solo dentro de
la partición de calibración) se aplicaron sobre las cuatro analíticas, además del nivel `raw`.

## 4.4. Procedimiento

1. Cross-fitting `K = 5`, semilla `20261008`. El fold de cada ítem es determinista,
   `fold = sha256("20261008:id") mod 5`. El umbral se ajusta en cuatro folds y se evalúa en el que queda, de
   modo que cada ítem pasa por prueba exactamente una vez y ningún ítem participa en su propio umbral.
2. **Umbral objetivo.** Para un origen `A` y una cobertura objetivo `q`, se toma
   `τ_A = min { τ : cobertura(τ) ≤ q }` sobre los valores observados de `C_A` en calibración, con
   `cobertura(τ) = #{C_A ≥ τ}/N`.
3. **Dos portes por celda.** El porte directo aplica `τ_B := τ_A` tal cual, que es lo que practica el
   ecosistema, y su degradación es la métrica principal, `Δ(A→B) = q − cobertura_B(τ_A)`. El porte con
   mapa aplica `τ_B := ψ(τ_A)`, con `ψ` el mapa cerrado `A→B` (por ejemplo `ψ = φ⁻¹` para `jev→pmax`), y
   existe solo dentro de una clase de equivalencia y a cardinalidad fija. El par de columnas es necesario
   porque el número y el mapa son cosas distintas (ver erratas E1 y E2 en `docs/erratas_especificacion.md`).
4. Coberturas objetivo `q ∈ {0.80, 0.50, 0.95}`, con 0.80 como principal.
5. **Intervalos.** Bootstrap de ítems con `B = 2000` y semilla fija; el umbral `τ` no se reajusta dentro del
   bootstrap.
6. **Comparaciones múltiples.** Benjamini-Hochberg (FDR) con `α = 0.05` sobre todas las celdas.
7. Reporte por cardinalidad `n` y por nivel AnyJev.

Una celda de la matriz es, por tanto, la tupla
`(definición origen A, definición destino B, modelo, dataset, n, q, nivel)`. El resultado completo tiene
3.564 celdas, en `results/matrix/matriz_transferencia.csv`.

## 4.5. La figura central y los artefactos

La matriz se resume en un mapa de calor por dataset y cardinalidad (`results/matrix/heatmap_*.png` y `.pdf`),
con filas de definición origen y columnas de definición destino, y la caída de cobertura anotada por celda.
La figura `delta_vs_delta_mapa_raw_q80` contrasta, celda a celda, el porte directo contra el porte con mapa
(el enunciado de la Proposición 1 sobre los datos).

Todo el informe de resultados (`results/matrix/RESUMEN_MATRIZ.md`) se regenera con un comando, sin edición
manual:

```bash
python -m pytest tests/ -q
python src/matriz/matriz.py --crudos results/crudos --out results/matrix
python src/matriz/figura.py
python src/matriz/informe_matriz.py
```

`matriz.py` es CPU pura: lee los `.jsonl` de mediciones y no toca ningún peso. Si el CSV regenerado no es
idéntico al publicado, hay un bug o un cambio de versión.

## 4.6. Trazabilidad (regla D4)

Cada fila de `results/crudos/*.jsonl` contiene la distribución completa, la etiqueta, el acierto, las cuatro
definiciones calculadas, el modelo, la revisión del Hub y un `row_hash`. La columna medido aquí agrupa los
campos `conf_*` (calculados aquí sobre la distribución devuelta); la columna auto-reportado agrupa
`answer_confidence`, `confidence_reported` y `act_probability` (emitidos por el propio modelo). Las cifras de
ECE de las fichas del ecosistema son auto-reportadas y no se usan como medición propia.

## 4.7. Alcance no cubierto, declarado antes de los resultados

- `clinc150` (n = 151) no es ejecutable en el checkpoint base de Laya: su ventana de 512 tokens solo
  admite 126 de las 151 opciones. El límite documentado de Jev (hasta 255 opciones) no es alcanzable en esa
  implementación. Sí se midió con los otros checkpoints y con el control crudo.
- `jaredpalmer/kev-suites` no carga (fallo de generación en el Hub el 08-oct-2026); no es un fallo del
  pipeline.
- Los modelos de 4B a 9B (Jeff-1, SemIf, jev-lite, Nimble-9B) no caben en 6 GB de VRAM; quedan como extensión
  en el Mac Mini o a 4 bits.
