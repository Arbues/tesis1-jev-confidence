# Pre-registro — Metrología y transferencia del campo `confidence`

*Tesis 1, Ruta 1. Borrador para publicar en Zenodo (autor: Arbués Enrique Pérez V., FC-UNI).*
*Estado: **PUBLICADO**. DOI: **10.5281/zenodo.23266795** (Zenodo, 08-oct-2026).*
*Una vez publicado, este archivo NO se modifica: los cambios van en una versión nueva.*

---

## 0. Declaración de transparencia (qué se hizo antes de este registro)

Un pre-registro vale por lo que congela **antes** de ver los resultados. Se declara aquí, sin
excepción, todo lo ya ejecutado en el momento de publicarlo:

1. **Paso 0 go/no-go (08-oct-2026):** se corrieron Laya (3 checkpoints) y Kev-0.8B sobre las 2.000
   decisiones de `LocalLLaMA/typed-decisions` y se reprodujeron las 5 métricas publicadas de Laya
   con `|Δ| ≤ 0.003`. Informe: `results/paso0_informe.md`.
2. **Piloto del pipeline (08-oct-2026):** se midió la matriz sobre **subconjuntos** (200 casos por
   config en `typed-decisions`; 400 ítems en los demás datasets). Esos resultados **existen** y están
   en `results/crudos/`. **No** son la corrida confirmatoria.
3. **Observaciones del piloto** (se declaran para que no parezcan hallazgos post-hoc): (a) en
   `banking77` (n=77) la accuracy de Laya fue ≈0.36; (b) `clinc150` (n=151) **no es ejecutable** en
   Laya: su ventana (`max_len=512`) solo admite 126 de las 151 opciones; (c) en `sst5` (n=5) el porte
   directo `pmax → jev` falló con `Δ ≈ 0.28` mientras el porte con mapa dio `≈ 0`.

**La corrida confirmatoria será una medición NUEVA, sobre el conjunto COMPLETO de ítems de cada
dataset** (no los subconjuntos del piloto), con el plan congelado abajo. Si algún resultado del
piloto cambia, se reportará el cambio.

---

## 1. Claim falsable

> De las definiciones de `confidence` en uso en el ecosistema tipo Jev, unas son **equivalentes en
> orden** y otras **no**. La matriz de transferencia cuantifica, para cada par (origen A → destino
> B), modelo y dataset, **cuánta cobertura y precisión se pierden** al aplicar el umbral `τ_A` con
> la definición B. El claim se refuta si la degradación es indistinguible de cero en todas las
> celdas, o si no hay relación con la clase de equivalencia ni con la cardinalidad `n`.

## 2. Definiciones que entran

`C_max` = `p_max` (DEF-4) · `C_Jev` = `(n·p_max−1)/(n−1)` (DEF-1) · `C_ent` = `1 − H(p)/ln n`
(DEF-2) · `C_mar` = `p_(1) − p_(2)` (DEF-5). `C_noul` (DEF-3) solo en el bloque `n = 2`.

Transformaciones AnyJev (DEF-7): niveles `raw` (principal), `L0` (debiasing sin etiquetas) y `L1`
(temperatura ajustada **dentro** del conjunto de calibración).

**Fuera de alcance (declarado):** `act_probability` (DEF-6) y `open-decision-ai` (DEF-8) → solo
catálogo, no entran en la matriz.

## 3. Modelos

Pesos abiertos, `output_tokens = 0`. La revisión exacta (sha del Hub) de cada uno queda registrada
en `results/crudos/*.meta.json` y en `results/raw/paso0_versions.json`.

| modelo | params | dónde corre | licencia |
|---|---|---|---|
| `convaiinnovations/laya` (`none` / `typed-decisions` / `multilingual`) | 421M | Nitro | Apache-2.0 |
| `jaredpalmer/kev-0.8b` (servido desde su repo) | 0.8B | Nitro | Apache-2.0 |
| `Qwen/Qwen3.5-0.8B-Base` (control crudo, sin entrenar) | 0.8B | Nitro | Apache-2.0 |

**Extensión declarada (no en esta corrida):** `GestaltLabs/Jeff-1` (4B), SemIf (Qwen3.5-4B),
`vagmi/jev-lite`, `Bespoke-Nimble-9B` (licencia no declarada), `tinyjev` → Mac Mini o 4-bit.
`chaoliangUNSW/Jev-Style-Qwen3.5-2B` no fue verificable (HTTP 401).

## 4. Datasets (ya etiquetados — cero anotación propia)

| dataset | n | split | nota |
|---|---|---|---|
| `LocalLLaMA/typed-decisions` | 2–6 / 2–10 / 2 | test | benchmark compartido, 4 flujos |
| `SetFit/sst5` | 5 | validation | ordinal |
| `alisawuffles/WANLI` | 3 | test | NLI |
| `mteb/banking77` | 77 | test | extremo de cardinalidad |
| `clinc/clinc_oos` (`plus`) | 151 | validation | **se declara no ejecutable en Laya** (ventana de 512 tokens) |
| `jaredpalmer/kev-suites` | — | — | **no carga** (fallo de generación en el Hub, 08-oct-2026) |

## 5. Procedimiento congelado

1. **Cross-fitting `K = 5`**, semilla `20261008`, fold por `sha256("seed:id") mod 5`. El umbral se
   ajusta en 4 folds y se evalúa en el que queda; cada ítem pasa por prueba una vez.
2. **Cobertura objetivo** `q ∈ {0.80, 0.50, 0.95}` (0.80 principal).
3. **Umbral:** `τ_A = min{ τ : cobertura(τ) ≤ q }` sobre los valores observados en calibración.
4. **Dos portes por celda** (ver `docs/erratas_especificacion.md`):
   - `Δ(A→B) = q − cobertura_B(τ_A)` — **porte directo**, métrica principal.
   - `Δ_mapa(A→B) = q − cobertura_B(ψ(τ_A))` — solo si existe mapa cerrado `ψ` (misma clase de
     equivalencia y misma cardinalidad).
5. **Bootstrap** de ítems `B = 2000`, semilla fija, IC 95 %.
6. **FDR** Benjamini–Hochberg (α = 0.05) sobre todas las celdas.
7. **Reporte por cardinalidad `n`** y por nivel AnyJev.

## 6. Qué se reportará pase lo que pase

- La matriz completa (todas las celdas, incluidas las no significativas).
- El error absoluto medio del porte directo y del porte con mapa.
- Los datasets/modelos que no pudieron medirse y **por qué**.
- Los resultados nulos o degenerados (p. ej. si a cardinalidad alta todas las definiciones coinciden).
- El dataset de mediciones crudas con `row_hash` por fila y la revisión de cada modelo.

## 7. Qué NO se hará

- Anotación humana de ningún tipo (cero etiquetado, cero kappa).
- Uso de la nube o de GPUs de pago (costo $0).
- Ajuste del método después de ver los resultados: cualquier desviación se reporta como tal.
- Presentar como "medido aquí" ninguna cifra que sea auto-reportada por el ecosistema (D4).

## 8. Artefactos

Repositorio: `github.com/Arbues/tesis1-jev-confidence`. Librería `src/jev_conf_metrics/` (con tests
de conformidad T1–T8), pipeline `src/matriz/`, mediciones crudas `results/crudos/`, matriz y figuras
en `results/matrix/`.
