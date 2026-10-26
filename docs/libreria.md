# Librería `jev-conf-metrics` — API y guía de extensión

Instrumento del entregable 2 de la Tesis 1 (Ruta 1). Mide el campo `confidence` de los
modelos de decisión tipo Jev bajo **varias definiciones incompatibles** y cuantifica qué
pasa cuando un umbral se porta de una a otra.

La librería es **stdlib puro** (sin numpy ni scipy en el núcleo): se puede leer, auditar y
reusar en cualquier máquina. Solo el orquestador de la matriz (`src/matriz/`) y el generador
de figuras (`src/figuras_paper.py`) usan numpy y matplotlib, y lo declaran como extra.

## Instalación

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,figuras]"      # editable + tests + numpy/matplotlib
```

A partir de ahí, `import jev_conf_metrics` funciona desde cualquier directorio.

## Mapa de módulos

| módulo | qué contiene | depende de |
|---|---|---|
| `definiciones` | DEF-1..DEF-5 (Jev, entropía, p_max, margen, noul) y DEF-7 (AnyJev L0/L1) | stdlib |
| `metricas` | ECE (ancho y masa), binning exacto de Laya, AUROC, Brier, NLL, RPS | stdlib |
| `transferencia` | umbrales, celdas, cross-fitting, bootstrap, Benjamini–Hochberg | stdlib |
| `recursos` | guard de RAM/VRAM para WSL2 (aborta antes de cargar un modelo) | stdlib |

Todos los módulos tienen `__all__`, docstrings en cada función pública y `from __future__
import annotations`.

## Uso básico

```python
from jev_conf_metrics import all_confidences, celda, umbral_para_cobertura, phi_inv

p = [0.19, 0.22, 0.43, 0.16]           # distribución sobre 4 opciones
all_confidences(p)
# {'pmax': 0.43, 'jev': 0.2428, 'ent': 0.0588, 'margin': 0.2148}
```

### Definiciones

| función | fórmula | fuente |
|---|---|---|
| `conf_jev(p)` | `(n·p_max − 1)/(n − 1)` | Jev 1.13 (concentración, **no** la probabilidad ganadora) |
| `conf_pmax(p)` | `max(p)` | `answer_confidence` de Laya / jev-lite |
| `conf_ent(p)` | `1 − H(p)/log n` | Laya para `choice`/`score` |
| `conf_margin(p)` | `p_(1) − p_(2)` | margen top-2 |
| `conf_noul(px)` | `max(px, 1 − px)` | primitivo `noul` (binario) |
| `conf_score(p)` | `max(0, 1 − Σᵢ pᵢ·\|i − m\| / MAD_unif)` | primitivo `score` de TypeSafe — **extensión declarada** (posterior al pre-registro) |
| `all_confidences(p)` | las cuatro del pre-registro a la vez | — |
| `all_confidences(p, extensiones=True)` | las cinco | — |
| `score_mad_unif(n)` | `(1/n)·Σᵢ \|i − (n−1)/2\|` | constante de normalización de `conf_score` |

`CONFIDENCES` es el diccionario `nombre -> función` que usa la matriz **sellada** y contiene solo las
cuatro definiciones del pre-registro. `CONFIDENCES_EXT` contiene las posteriores (`score`). La separación
es deliberada: `matriz_transferencia.csv` y las filas crudas se regeneran byte a byte idénticos.

> `conf_score` exige **orden** en los niveles (`i` es la posición ordinal). Solo se define sobre datasets
> ordinales (`sst5`). Sobre etiquetas nominales habría que inventar la escala. Resultados:
> `results/matrix/EXTENSION_CONF_SCORE.md`.

### Relaciones formales

```python
order_equiv_affine_jev_pmax(n)   # φ(x) = (n·x − 1)/(n − 1);  C_jev = φ(C_pmax)   (Prop. 1)
phi_inv(y, n)                    # φ⁻¹(y) = (y·(n − 1) + 1)/n
```

A cardinalidad `n` fija, `C_jev` y `C_pmax` ordenan igual; el umbral **transfiere aplicando
`φ⁻¹`**, no copiando el número. Con `n = 2` todas las definiciones coinciden en orden
(Proposición 3), y a `n` alta `C_jev → C_pmax`.

### Transferencia de umbrales

```python
from jev_conf_metrics import cobertura, umbral_para_cobertura, celda

tau, n_emp = umbral_para_cobertura(conf_A_cal, q=0.80)   # umbral que da cobertura q en calibración
c = celda(conf_A_cal, conf_B_cal, conf_A_te, conf_B_te, correct_te, q=0.80,
          mapa=lambda t: phi_inv(t, 4))
c["delta"]        # q − cobertura_B con τ tal cual  (lo que hace el ecosistema)
c["delta_mapa"]   # q − cobertura con el mapa φ     (Proposición 1 → ≈ 0)
c["n_empates_tau"]# ítems que comparten el umbral (suelo del porte con mapa)
```

`fold_de(item_id, k=5)` da la asignación determinista de folds (cross-fitting reproducible);
`bootstrap_delta` y `bh_fdr` cierran el aparato estadístico (IC 95 % y control de
falsos descubrimientos).

### Métricas de calibración

`ece(confs, correct, n_bins=15, scheme="width"|"mass")`, `ece_laya(confs, correct)` (el
binning exacto del arnés de Laya, para comparar contra sus números publicados),
`auroc(scores, labels)`, `brier_multi(probs, y)`, `nll(probs, y)`, `rps(p, y)`.

### Recursos

`exigir_recursos(vram_necesaria_mb, ram_necesaria_gb)` aborta el proceso si no hay RAM/VRAM
antes de cargar un modelo; `liberar(*objetos)` suelta referencias y vacía la caché de CUDA.

## Extender (puntos de crecimiento)

La librería está segmentada para admitir cambios sin tocar el núcleo:

1. **Nueva definición de `confidence`.** Añadir la función `conf_x(p)` en
   `definiciones.py`, registrarla en `CONFIDENCES` y exportarla en `__init__.py`. La matriz
   la recogerá sola (`matriz.py` itera sobre `CONFIDENCES`) y las figuras también.
2. **Nuevo mapa cerrado entre definiciones.** Añadir la regla en `mapa_entre(A, B, n)` de
   `src/matriz/matriz.py`. Si el mapa existe, la celda gana la columna `delta_mapa`.
3. **Nuevo modelo o dataset.** Añadir su adaptador en `src/matriz/adaptadores.py`; los
   crudos se escriben con el mismo esquema (`conf_*`, `row_hash`, `correct`, …) y el resto
   del pipeline no cambia.
4. **Nueva métrica de calibración.** Añadirla en `metricas.py` (stdlib) y exportarla.

## Tests y regresión

```bash
.venv/bin/python -m pytest -q       # 67 tests
```

Los tests cubren: la matemática de las definiciones y las proposiciones, la regresión del
paso 0 (reproducción de las 5 métricas publicadas de Laya con |Δ| ≤ 0.003), la regresión del
bug `L0` (el debiaser debe mover las frecuencias de argmax) y la normalización de etiquetas
y nombres de los adaptadores. Se corren también en cada `push`/PR vía GitHub Actions
(`.github/workflows/tests.yml`).
