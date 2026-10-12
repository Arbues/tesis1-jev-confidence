# Notes/hallazgos.md — reentrada de sesión (11-oct-2026)

Registro de exploración mínima. Presupuesto gastado: bajo (~4k tokens). No se volcaron README.md ni
STATE.json: se parsearon por clave y por rango de líneas.

Encargo (11-oct-2026): exploración superficial del repo, reproduciendo el cuadro de resultados esperado;
verificación final en §5.

## 1. STATE.json (370 líneas, 26 claves de primer nivel)

- `proyecto`, `autor`, `ultima_actualizacion` = `2026-10-08`
- `pre_registro` → DOI `10.5281/zenodo.23266795` (Zenodo, 08-oct-2026), archivo `paper/04_pre_registro.md`
- `estado` (514 chars) → PASO 0 = GO; Laya (3 checkpoints) + Kev-0.8B medidos sobre 2.000 decisiones de `typed-decisions`
- Blobs grandes (no releídos, existen): `matriz_2026_10_08` (5.557), `objeto_de_estudio` (4.036),
  `paso0_2026_10_08` (3.922), `archivos` (3.792), `sondeo_2026_10_04` (2.424), `ecosistema_verificado` (2.057),
  `siguientes_pasos` (1.938), `hechos_verificados_del_eje` (1.722), `ruta_elegida_ruta_1` (1.686), `glosario` (1.495)
- Claves estructurales: `decision_2026_10_04`, `reglas_de_diseno_del_autor` (D1–D5), `deltas_2026_10_01_cierre_de_huecos`,
  `computo_y_costo`, `cadena_de_decisiones`, `riesgo_principal`, `tema`, `marco_teorico_minimo`,
  `plan_tres_etapas`, `preferencias_usuario`
- Nota: `ultima_actualizacion` está **desactualizado** (2026-10-08) frente al README, que ya documenta hechos del
  09–10-oct (redacción §4–§7, repo público). Si se toca el estado, sincronizar ambos.

## 2. README.md §3 — índice de archivos (líneas 61–108)

Productos vigentes y dónde viven:

| Producto | Ruta |
|---|---|
| Paper (plan, marco teórico, especificación, pre-registro, §1–§7) | `paper/` · `paper/secciones/` |
| Paper en LaTeX IEEE + figuras | `paper/ieee/` (compila con `compilar.sh`) · `paper/figures/` |
| Documento principal de la Ruta 1 | `eje-2-jev-opensource/11_ruta1_metrologia_confidence.md` |
| Fuentes del eje (49) | `eje-2-jev-opensource/FUENTES.md` |
| Artefactos de medición | `results/` → `raw/`, `crudos/`, `matrix/`, `paso0_informe.md` |
| Librería + API + validación | `src/jev_conf_metrics/`, `docs/libreria.md`, `docs/validacion-productos.md` |
| CI (37 tests) | `pyproject.toml`, `.github/workflows/tests.yml` |

Regla de orden §3-bis: la raíz solo lleva los archivos de entrada (`README.md`, `STATE.json`, `.hermes.md`,
`AGENTS.md`, `.gitignore`, `LICENSE`, `LICENSE-docs`, `CITATION.cff`); **todo lo nuevo va a su carpeta**
(`src/`, `results/`, `paper/`, `notes/`, `data/`), o a una subcarpeta con nombre claro dentro de la que
corresponda. Repo público; Apache-2.0 (código) + CC-BY-4.0 (paper/docs).

## 3. README §13 — Paso 0 (08-oct-2026, Acer Nitro): GO

- Los 3 criterios se cumplen; las **5 métricas publicadas de Laya** reproducidas con |Δ| ≤ 0.003.
- El mismo dato, el mismo modelo, y el ECE cambia **2,7×** según la definición de `confidence`:
  `p_max` 0.216 · Jev `(n·p−1)/(n−1)` 0.426 · entropía `1−H/log k` **0.577** · margen 0.511
  (checkpoint `laya-typed-decisions`).
- Dos hechos de metrología salidos del código: (i) la `choice_confidence` de Kev **ES** la fórmula de Jev
  (`(K·p−1)/(K−1)`), luego ese par transfiere el umbral de forma exacta (Prop. 1); (ii) `output_tokens`
  tiene **tres significados** (Jev/Laya = 0; Kev = cifra estilo facturación, `kev/api.py:163`).
- Trampa de entorno: `torch` de PyPI es cu130 y el driver del Nitro es CUDA 12.5 → instalar build `cu126`.

## 4. README §14 — Matriz de transferencia (corrida confirmatoria)

- **23 grupos** (5 configuraciones × 5 datasets), **65.185 decisiones**, **3.564 celdas**; informe regenerable
  `results/matrix/RESUMEN_MATRIZ.md`. El piloto (17.600) queda sustituido; el pipeline es determinista.
- Cifra del objeto de tesis: brecha entre la definición más alta y la más baja de la **misma** distribución →
  mediana **0.288**, p90 **0.434**, máx **0.848**.
- Claim cuantificado (nivel `raw`): porte directo del umbral vs porte **con mapa** →
  312 celdas sin empates dominantes: **0.2337 vs 0.0021 = 109×**; `L1` (temperatura) 126×; `n = 2` (Prop. 3) 14×.
- El promedio engaña: `Δ` es **bimodal** → el titular es la tabla **por par** (`RESUMEN_MATRIZ.md` §3b).
  Peor par `pmax → ent` (0.767, cambio de FORMA); mejor `margin → jev` (0.002).
- Dos capas del claim (errata E2): **escala** (ni entre equivalentes en orden viaja el número: `jev` vs `pmax`
  pierde hasta 80 % de cobertura; el mapa sí transfiere, Δ≈0.004) y **forma** (clases distintas: no hay número
  ni mapa).
- Datos colaterales: Kev-0.8B 0.813 acc en `banking77` (n=77) vs 0.377 de Laya; `clinc150` (n=151) no ejecutable
  en 1 de 3 checkpoints (ventana 512 → solo 126 opciones).
- Auditoría final: 0 filas saltadas, folds balanceados, sin truncado silencioso; desviación **D1** (el debiaser
  `L0` era un no-op) declarada en `RESUMEN_MATRIZ.md` §7.

## 5. Encargo y verificación (11-oct-2026)

Encargo recibido: **exploración superficial del repo** bajo presupuesto de contexto, reproduciendo el cuadro
de resultados esperado. Re-verificado hoy contra los archivos; todo cuadra salvo un matiz:

| Qué | Resultado | Fuente |
|---|---|---|
| STATE.json | 26 claves nivel 1; `ultima_actualizacion` = `2026-10-08`, **desfasado** (el archivo sí está editado: `herramientas` ya nombra skills del 11-oct) | `STATE.json:3`, `git diff STATE.json` |
| README §3 | Índice de archivos + regla de orden: raíz solo con archivos de entrada; todo lo nuevo a `src/`, `results/`, `paper/`, `notes/` | `README.md:61-108` |
| README §13 | Paso 0 = **GO**; mismas 2.000 decisiones de `typed-decisions`; ECE 0.216 → 0.577 según definición (**2,7×**) | `README.md:278-316` |
| README §14 | **23 grupos**, **65.185 decisiones**, **3.564 celdas**; porte directo 0.2337 vs con mapa 0.0021 = **109×** | `README.md:318-350` |
| `notes/` | **Matiz:** la carpeta **ya existía** con `.gitkeep` (commit 69a38fe, 08-oct); lo creado fue el archivo `notes/hallazgos.md` | `notes/.gitkeep` |

### Candidatos de trabajo (pendientes del autor; no hay cómputo pendiente)

Afiliación FC-UNI en Zenodo · importar el DOI al ORCID (`0009-0004-7605-6569`) · las 9 referencias por
confirmar (`paper/02_referencias_pendientes.md`) · revisión del borrador §1–§7 o del PDF IEEE · extensión a
4B–9B en el Mac Mini (Tesis 2).

**Pendientes nuevos que el autor ya anotó (11-oct-2026):** repo-framework limpio para comparaciones · soporte de
modelos de pago por API key · visibilidad del paper y del framework · blindaje de prioridad y crédito · paper en
inglés versionado → detalle en `notes/pendientes-framework-y-paper.md`, índice en `README.md` §10-bis.
