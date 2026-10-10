# Handoff — qué hay, cómo se regenera y qué falta

*Para el redactor del paper en el `thinkpad-t440` (sin GPU). Actualizado: 08-oct-2026.*

> **Estado: la medición está CERRADA.** Es la corrida **confirmatoria** que declara el pre-registro
> (DOI **10.5281/zenodo.23266795**), sobre el conjunto completo de cada dataset: **23 grupos**
> (5 configuraciones de modelo × 5 datasets), **65.185 decisiones**, **3.564 celdas**.
> El piloto (subconjuntos) quedó sustituido y solo vive en el historial de git.
>
> **Cifras que van al paper** (todas en `results/matrix/RESUMEN_MATRIZ.md`, regenerable):
> - La diferencia entre la definición de `confidence` más alta y la más baja de la **misma** distribución:
>   mediana **0.288**, p90 **0.434**, máximo **0.848** (sobre 65.185 distribuciones).
> - Error absoluto medio del porte de umbral, **nivel principal `raw`**: **0.2337 directo contra 0.0021 con
>   mapa → factor 109×** (sin las celdas dominadas por empates de umbral); solo modelos entrenados, **113×**.
> - **El promedio no es el resumen**: la distribución de `Δ` es bimodal. Usar la tabla **por par (A→B)** de
>   §3b del informe: peor par `pmax → ent` (mediana 0.767), mejor `margin → jev` (0.002).
> - El porte directo llega a perder **toda** la cobertura (celdas con Δ = 0.80 y cobertura 0).

El t440 **no necesita GPU, ni pesos, ni acceso a HuggingFace**. Todo lo que el paper necesita está
commiteado. Lo que no se puede regenerar allí (la inferencia) ya está hecho y guardado fila a fila.

---

## 0. Nota para el agente del t440 (09-oct-2026)

Si ya escribiste §4–§7 con una versión anterior de la matriz, revisa estas cuatro cosas. Todas están ya
corregidas en `main` tras la **auditoría final de errores**:

| # | Qué cambió | Cifra vigente | Cifra vieja |
|---|---|---|---|
| 1 | El titular es sobre el **nivel principal `raw`**, no sobre los tres niveles mezclados | **109×** (0.2337 vs 0.0021, 312 celdas) | 104× (0.2577 vs 0.0025, 948 celdas) |
| 2 | El recuento de distribuciones tenía un tope de 2000 filas por archivo | **65.185** (mediana 0.288, p90 0.434, máx 0.848) | 41.505 (0.292 / 0.441 / 0.840) |
| 3 | El nivel **`L0` se recalculó** (desviación D1: su implementación no convergía y era indistinguible de `raw`) | `L0` 37× · `L1` 126× | `L0` indistinguible de `raw` |
| 4 | Las tablas **por par** de §5.4 ahora son sobre `raw` | celdas 15 / 99 | 45 / 297 |

**Cómo comprobar que todo cuadra** (sin GPU):

```bash
python src/matriz/matriz.py --crudos results/crudos --out results/matrix
python src/matriz/informe_matriz.py
```

Toda cifra del paper debe aparecer **literalmente** en `results/matrix/RESUMEN_MATRIZ.md`. Si alguna no
aparece, es que quedó de la versión anterior.

**Lo que NO hay que tocar:** el nivel `raw` —sobre el que van todos los titulares— **no se modificó** tras
publicar el pre-registro (DOI `10.5281/zenodo.23266795`). `L0` y `L1` son niveles de sensibilidad, y la
corrección del `L0` está declarada como desviación en `RESUMEN_MATRIZ.md` §7 y en §4 del paper.

---

## 1. Qué hay (y dónde)

| Ruta | Qué contiene | Estado |
|---|---|---|
| `results/paso0_informe.md` | el go/no-go del paso 0 + la reproducción de las 5 métricas publicadas de Laya | **hecho** |
| `results/raw/*.jsonl` | 2.000 decisiones × 4 configuraciones de modelo, con `row_hash` | **hecho** |
| `results/crudos/*.jsonl` | las mediciones **confirmatorias**: 65.185 filas, una por (modelo × dataset × ítem) | **hecho** |
| `results/crudos/*.meta.json` | por grupo: modelo, revisión del Hub, cardinalidades, accuracy, nº de filas | **hecho** |
| `results/matrix/matriz_transferencia.csv` | **la matriz**: celdas (A→B) × modelo × dataset × n × q × nivel | **hecho** |
| `results/matrix/resumen.json` | parámetros de la corrida (K, q, bootstrap, niveles) | **hecho** |
| `results/matrix/heatmap_*.png` / `.pdf` | la figura central, por dataset | **hecho** |
| `results/matrix/delta_vs_delta_mapa_*.png` | la Proposición 1 en los datos | **hecho** |
| `results/matrix/RESUMEN_MATRIZ.md` | informe legible con todas las tablas | **hecho** |
| `paper/04_pre_registro.md` | el pre-registro (lo publica el autor en Zenodo para el DOI) | **hecho** |
| `docs/erratas_especificacion.md` | las 3 contradicciones encontradas y cómo se resolvieron | **hecho** |
| §7 de `RESUMEN_MATRIZ.md` | las **desviaciones respecto al pre-registro** (el pre-registro exige reportarlas): D1 corrección del nivel `L0` | **hecho** |
| `src/jev_conf_metrics/` | la librería del entregable 2, con `tests/` | **hecho** |

## 2. Mapa artefacto → sección del paper

| Sección | Qué usar |
|---|---|
| §3 Marco teórico | `paper/03_especificacion_confidence.md` (DEF-1..8, Props. 1–3) + `docs/erratas_especificacion.md` (el porte tiene **dos** capas: escala y forma) |
| §4 Método | `paper/04_pre_registro.md` (procedimiento congelado: K=5, q, bootstrap, FDR) + §1 de este doc |
| §5 Resultados | `results/matrix/matriz_transferencia.csv` (las cifras) + `heatmap_*.png` (la figura central) + `RESUMEN_MATRIZ.md` §2–§5 (las tablas ya armadas) |
| §6 Discusión | `RESUMEN_MATRIZ.md` §3 (el mapa sí transfiere, el número no) y §5 (efecto de `n`) + §4 de este doc (limitaciones) |
| §7 Conclusión y artefactos | la tabla de §1 de este doc + el repo |

**Regla D4 (trazabilidad):** en `results/crudos/*.jsonl`, las columnas `conf_*` son **medidas aquí**
(calculadas sobre la distribución devuelta); `answer_confidence`, `confidence_reported` y
`act_probability` son **auto-reportadas** por el modelo. Ninguna cifra auto-reportada del ecosistema
(ECE de model cards, etc.) se usa como medición propia.

## 3. Cómo se regenera TODO sin GPU

```bash
# en el t440, con el repo clonado y un venv con numpy + matplotlib
uv venv --python 3.12 .venv && uv pip install --python .venv/bin/python numpy matplotlib pytest

python -m pytest tests/ -q                       # 36 tests: la matemática y la regresión del paso 0
python src/matriz/matriz.py --crudos results/crudos --out results/matrix
python src/matriz/figura.py
python src/matriz/informe_matriz.py
python src/paso0_informe.py                      # regenera results/paso0_informe.md
```

`matriz.py` es **CPU puro**: lee los `.jsonl` y no toca ningún peso. Si el CSV regenerado no es
idéntico al commiteado, hay un bug (o un cambio de versión): comparar con `sha256sum`.

## 4. Lo que NO se puede regenerar en el t440, y por qué

La **inferencia** (Laya, Kev, control crudo) necesita GPU y pesos. Por eso los crudos están
commiteados con `row_hash` por fila: cualquier fila del paper se puede rastrear hasta su medición
original sin volver a correr el modelo. Los `.meta.json` guardan la revisión del Hub de cada modelo.

## 5. Limitaciones a declarar en el paper (honestidad antes que cobertura)

| Qué | Por qué |
|---|---|
| `clinc150` (n=151) no medido | **Laya no puede**: su ventana de 512 tokens solo admite 126 de las 151 opciones (`only 126 of its 151 option markers fit in max_len=512`). El límite documentado de Jev (≤255 opciones) **no es alcanzable en esta implementación** |
| `jaredpalmer/kev-suites` no medido | el dataset **no carga** (fallo de generación en el Hub, 08-oct-2026), no es un fallo del pipeline |
| Modelos 4B–9B fuera de esta corrida | no caben en 6 GB de VRAM. Extensión prevista: Mac Mini o 4-bit (`GestaltLabs/Jeff-1`, SemIf, `vagmi/jev-lite`, `Bespoke-Nimble-9B` — este último **sin licencia declarada**) |
| `chaoliangUNSW/Jev-Style-Qwen3.5-2B` | no verificable (HTTP 401) |
| `act_probability` y `open-decision-ai` | fuera de la matriz por decisión congelada (opacas) |
| Cardinalidades altas | con distribuciones casi one-hot las definiciones **coinciden**: la incompatibilidad es un fenómeno de `n ≥ 3` con distribuciones dispersas (Proposición 2) |

## 6. Cómo citar el instrumento

- Librería: `src/jev_conf_metrics/` (implementa DEF-1..DEF-5 y DEF-7, las métricas y la
  transferencia, con tests de conformidad T1–T8).
- Pipeline: `src/matriz/medir.py` (mide), `matriz.py` (calcula la matriz), `figura.py`,
  `informe_matriz.py`.
- Reproducibilidad: `src/matriz/correr_nucleo.sh` y `correr_kev.sh` documentan el orden exacto de
  las corridas, incluido el manejo de la VRAM (un modelo a la vez).
