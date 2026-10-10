# Cómo validar los productos — guía para el autor

Esta guía responde a una sola pregunta: **¿está bien o no lo que hicimos?** Está pensada
para que la corras tú en el `t440` (o en cualquier máquina con Python 3.10+). Separa dos
cosas que conviene no mezclar:

- **Lo que valida un comando** (objetivo): que los tests pasan, que los números se regeneran
  idénticos, que el PDF compila. Si el comando da lo esperado, el producto está sano.
- **Lo que solo validas tú** (criterio): si el texto dice lo que quieres decir, si el título
  y el alcance son los tuyos. Eso no lo puede comprobar ninguna máquina.

---

## 0. Validación de una sola pasada

En un clon limpio:

```bash
git clone git@github.com:Arbues/tesis1-jev-confidence.git
cd tesis1-jev-confidence
python3 -m venv .venv
.venv/bin/pip install -e ".[dev,figuras]"

.venv/bin/python -m pytest -q                       # 1) los tests
.venv/bin/python src/matriz/informe_matriz.py       # 2) regenera el informe
git diff --stat                                     # 3) debe salir VACÍO
.venv/bin/python src/figuras_paper.py               # 4) las 8 figuras
cd paper/ieee && ./compilar.sh                      # 5) el PDF IEEE
```

Si los cinco pasos dan lo esperado, los productos **están sanos**. El detalle, producto por
producto, va abajo.

---

## 1. Tests de la librería

```bash
.venv/bin/python -m pytest -q
```

**Esperado:** `37 passed`. Cubren la matemática de las definiciones y las proposiciones, la
regresión del paso 0 y la del bug `L0`.

**Si falla:** algo cambió en la librería y rompió la reproducción. No sigas: primero hay que
ver qué test cayó (`-x -vv`).

---

## 2. La librería (funcional y documentada)

```bash
.venv/bin/python -c "from jev_conf_metrics import all_confidences; print(all_confidences([0.19,0.22,0.43,0.16]))"
```

**Esperado:** un diccionario con las cuatro definiciones sobre la misma distribución; los
valores son `pmax 0.43`, `jev 0.2428`, `ent 0.0588`, `margin 0.2148`. Verás que **el mismo dato
da cuatro números distintos**: ese es el objeto de la tesis.

La API completa, con ejemplos y los puntos de extensión, está en `docs/libreria.md`.

**Lo que valida el comando:** que importa, que la matemática es la publicada y que está
segmentada (cuatro módulos + CI en cada `push`).
**Lo que validas tú:** si el diseño te parece el adecuado, si quieres más o menos azúcar.

---

## 3. El dataset de mediciones crudas

```bash
.venv/bin/python - <<'PY'
import glob
n = 0
for p in glob.glob("results/crudos/*.jsonl"):
    if p.split("/")[-1].startswith("_"):
        continue
    n += sum(1 for _ in open(p, encoding="utf-8"))
print(n)
PY
```

**Esperado:** `65185`. Cada fila lleva sus cuatro definiciones, la etiqueta, el acierto y un
`row_hash` (trazabilidad D4).

**Si no coincide:** algún archivo `.jsonl` cambió; el informe lo delatará (paso 4).

---

## 4. La matriz y el informe regenerable (la prueba fuerte)

```bash
.venv/bin/python src/matriz/informe_matriz.py
git diff --stat
```

**Esperado:** `[informe] results/matrix/RESUMEN_MATRIZ.md` y luego **`git diff` vacío**, es
decir, el informe se regenera **byte a byte** igual. Esto demuestra que las cifras del paper
no se escribieron a mano: salen de los artefactos.

Puedes comprobar los dos números centrales:

| cifra | dónde | valor |
|---|---|---|
| brecha entre definiciones (mediana) | §2 del informe | 0.288 |
| el porte directo se equivoca | §3 del informe | 109.2× |

**Si el `diff` no está vacío:** cambió el dataset, la matriz o el código. Es exactamente el
mecanismo que avisa de una inconsistencia antes de que llegue al paper.

---

## 5. Las figuras

```bash
.venv/bin/python src/figuras_paper.py
ls paper/figures/*.pdf
```

**Esperado:** 8 figuras (`fig1-brecha` … `fig8-heatmap-banking77`), en PDF vectorial (para
LaTeX) y PNG (para leer). Los números que imprime al final deben coincidir con el informe:
mediana 0.288, factores 20.5 / 109.2 / 112.8 / 95.8, ECE 0.216 → 0.577.

---

## 6. El paper en formato IEEE (LaTeX)

```bash
cd paper/ieee && ./compilar.sh
```

**Esperado:** `main.pdf`. **Ojo:** en el `t440` TeX todavía **no está instalado**; hay dos
rutas en `paper/ieee/README.md` (una con `sudo`, otra con TinyTeX local sin `sudo`). La
compilación es el paso que queda pendiente de tu aprobación.

**Si `\cite` sale como `[?]`:** falta correr `bibtex` (el script ya lo hace) o el `.bib` no
está junto a `main.tex`.

---

## 7. El pre-registro (DOI) y su relación con el repositorio

- Abre `https://zenodo.org/records/23266795`. **Esperado:** el registro en tu cuenta, con tu
  **ORCID** `0009-0004-7605-6569`, licencia **CC-BY-4.0** y el archivo `04_pre_registro.md`.

Lo que **falta ahí** (decisión tuya, ver §9): añadir tu **afiliación** (FC-UNI) al registro,
y **vincular el DOI a tu perfil ORCID** (ahora tu ORCID tiene 0 trabajos; añadir el trabajo
desde el DOI lo publica en tu historial).

---

## 8. Licencias, cita y visibilidad

- `LICENSE` (Apache-2.0, código) y `LICENSE-docs` (CC-BY-4.0, paper y docs) existen.
- En GitHub debe aparecer **«Cite this repository»** (lo habilita `CITATION.cff`, que ya lleva
  tu nombre completo, ORCID, afiliación y el DOI).
- El repositorio es **público** desde el 10-oct-2026.

---

## 9. Lo que solo puedes validar tú (criterio, no comando)

| # | Qué revisar | Por qué es tuyo |
|---|---|---|
| 1 | **El texto §1–§7** | la voz y las afirmaciones son tuyas; ningún test las cubre |
| 2 | **El título y el alcance** | ya fijados (título definitivo, formato IEEE), pero puedes cambiarlos |
| 3 | **Afiliación y ORCID en Zenodo** | son tus datos personales |
| 4 | **Licencias** | ya elegidas (Apache-2.0 / CC-BY-4.0); cambiarlas es tu decisión |
| 5 | **Vincular el DOI con tu ORCID** | tu perfil |
| 6 | **Formato IEEE final** | revisar que el PDF compilado te represente |

---

## 10. Resumen: qué significa «está bien»

| producto | comando / dónde | esperado |
|---|---|---|
| Tests | `pytest -q` | 37 passed |
| Librería | `import jev_conf_metrics` | cuatro definiciones sobre el mismo dato |
| Dataset | conteo de filas | 65185 |
| Matriz/informe | `informe_matriz.py` + `git diff` | diff vacío; 0.288 y 109.2× |
| Figuras | `figuras_paper.py` | 8 PDF con los números del informe |
| Paper IEEE | `compilar.sh` | `main.pdf` |
| Pre-registro | Zenodo | tu ORCID y afiliación |
| Licencias | repo | Apache-2.0 + CC-BY-4.0 |
| Cita | GitHub | botón «Cite this repository» |
