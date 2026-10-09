# Plan — Cerrar la medición en el Acer Nitro y dejar el handoff al t440

*Fecha: 2026-10-08 · rama de trabajo propuesta: `feat/matriz-transferencia` (desde `feat/paso0-go-no-go`)*
*Ejecutor previsto: agente en el Acer Nitro (RTX 4050 6 GB, WSL2). Revisión humana: el autor.*

---

## 1. Goal

Convertir el paso 0 (ya hecho, GO) en el **entregable central de la Tesis 1**: la **matriz de transferencia de
umbrales** `confidence` × `confidence` × modelo × dataset, medida sobre pesos abiertos en el Nitro, con su
librería `jev-conf-metrics` + tests, sus mediciones crudas hasheadas, su figura *heatmap*, y **todo subido al
repo con el contexto suficiente para que el `thinkpad-t440` escriba el paper sin volver a la GPU**.

---

## 2. Contexto actual / supuestos (verificado el 2026-10-08, no supuesto)

| Hecho | Valor medido | Cómo se comprobó |
|---|---|---|
| Rama actual | `feat/paso0-go-no-go`, 3 commits, subida a origin | `git log --oneline -3`, `git ls-remote` |
| Estado del repo | limpio; `results/raw/` con 4 crudos + 4 resúmenes + `paso0_versions.json` | `git status --short`, `git ls-files results/` |
| `src/paso0_go_no_go.py` | 914 líneas; backends Laya/Kev/raw; `--selftest` **OK** | `--selftest` re-ejecutado |
| Librería `src/jev_conf_metrics/` | **solo `.gitkeep`** — no existe | `ls src/` |
| RAM de la VM | 15 GiB totales, ~11 GiB disponibles, swap 4 GiB casi sin usar | `free -h` |
| `/mnt/c/Users/harus/.wslconfig` | **no existe** (WSL2 sin límite explícito de memoria) | `cat` falla |
| VRAM | 6141 MiB totales, **4843 MiB usados, 1079 MiB libres** | `nvidia-smi` |
| Quién ocupa la VRAM | **el servidor de Kev** (PID 97074, `kev.serve --port 8008`, vivo desde 17:57) | `ps aux`, `curl :8008/docs` → 200 |
| Disco | 901 GB libres en `/`; caché HF 4.0 GB; `.venv` 8.6 GB | `df -h /`, `du -sh` |
| `bitsandbytes` | **NO instalado** (hace falta para 4-bit) | `import bitsandbytes` → ModuleNotFoundError |
| Repos HF verificados (HTTP 200) | `GestaltLabs/Jeff-1`, `vagmi/jev-lite`, `bespokelabs/Bespoke-Nimble-9B`, `jaredpalmer/kev-0.5b`, `Qwen/Qwen3-0.6B-Base`, `Qwen/Qwen3.5-4B` | `curl https://huggingface.co/api/models/<id>` |
| Repo NO verificable | `chaoliangUNSW/Jev-Style-Qwen3.5-2B` → **401** (nombre/visibilidad a confirmar) | mismo `curl` |
| Datasets HF verificados (200/307) | `jaredpalmer/kev-suites`, `PolyAI/banking77`, `clinc_oos`, `SetFit/sst5`, `alisawuffles/WANLI`, `LocalLLaMA/typed-decisions` | `curl .../api/datasets/<id>` |

**Pendiente de verificar por el ejecutor (tarea 0.3):** versiones exactas de `numpy`, `pytest`, `matplotlib`,
`scipy`, `pandas` en `.venv`, y los *schemas* de los datasets nuevos. No se asume nada.

**Dato que NO hay que volver a descubrir:** el paso 0 ya reprodujo las 5 métricas publicadas de Laya con
`|Δ| ≤ 0.003` y verificó `output_tokens = 0`. Ver `results/paso0_informe.md`.

---

## 3. Restricciones duras (las del autor + las de la máquina)

1. **No desbordar la RAM ni tumbar WSL2.** Reglas de oro, sin excepción:
   - **Un modelo en VRAM a la vez.** Cargar → medir → `liberar()` → siguiente.
   - **El servidor de Kev se levanta solo para su bloque y se mata al terminar.** Retiene 4.8 GB de 6 GB:
     con él vivo, Laya (≈1.2 GB) **no cabe** (quedan 1079 MiB).
   - Antes de cada carga, `exigir_recursos()` (tarea 1.4) aborta si `MemAvailable < 1 GB` o si la VRAM libre
     es menor que la estimada. **Regla del autor (2026-10-08): con 1 GB de RAM disponible se para TODO y se
     suspende.** Abortar es correcto; no se reintenta a lo bruto.
   - Nunca `device_map="auto"` con modelos que no quepan: hace *offload* a RAM y es la vía directa al cuelgue.
     Usar `device_map={"": 0}` (GPU 0) explícito.
   - `export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` en la sesión antes de correr nada.
   - **Nada de descargas ni inferencias en paralelo.** Secuencial siempre.
   - No tocar `/mnt/c/Users/harus/.wslconfig` (exigiría `wsl --shutdown` y mataría esta sesión). La disciplina
     se aplica desde el código, no desde la config.
2. **D2 — cero anotación humana.** Solo datasets ya etiquetados.
3. **D4 — versión + hash por fila** y distinción **medido aquí / auto-reportado**.
4. **D5 — $0.** Nada de nube.
5. **Git:** rama → PR → *squash merge*. **Nunca `push` a `main`.**
6. **Regla de 3 fallos:** si una misma tarea falla 3 veces, parar y cambiar de enfoque (regla del autor).
7. **`matriz.py` debe correr en CPU** (el t440 no tiene GPU): toda la matemática de la matriz se calcula a
   partir de los `.jsonl` crudos, nunca re-inferiendo.

---

## 4. Decisiones de diseño que este plan congela

*(El alcance de §10.1–§10.5 de `paper/00_plan_del_paper.md` ya está congelado; aquí se baja a detalle
ejecutable. Si el autor quiere cambiar algo, se cambia **antes** del pre-registro, no después.)*

### 4.1. Modelos del **núcleo** (corren en el Nitro, uno a la vez)

| id | params | backend | VRAM est. | Estado |
|---|---|---|---|---|
| `convaiinnovations/laya` `subfolder=none` | 421M | `LayaBackend` | ~1.2 GB | ya medido |
| `convaiinnovations/laya` `subfolder=typed-decisions` | 421M | `LayaBackend` | ~1.2 GB | ya medido |
| `convaiinnovations/laya` `subfolder=multilingual` | 421M | `LayaBackend` | ~1.2 GB | ya medido |
| `jaredpalmer/kev-0.8b` | 0.8B | `KevHTTPBackend` | ~4.9 GB | ya medido |
| `jaredpalmer/kev-0.5b` | 0.5B | `KevHTTPBackend` | ~3.5 GB | por añadir |
| `Qwen/Qwen3.5-0.8B-Base` (control crudo) | 0.8B | `HFLogitBackend` | ~1.8 GB | backend existe |
| `GestaltLabs/Jeff-1` (LoRA Qwen3-4B) | 4B | `HFLogitBackend` 4-bit | ~3.0 GB | por añadir |
| `TheoLeeCJ/SemIf-*` (Qwen3.5-4B) | 4B | `HFLogitBackend` 4-bit | ~3.0 GB | por confirmar id |
| `tinyjev` (pip) | 596M | backend nuevo | ~1.5 GB | por evaluar |

**Extensión (NO en este plan, van al Mac Mini):** `Bespoke-Nimble-9B` (9B, **sin licencia** → decidir si
entra al catálogo), `vagmi/jev-lite` (Gemma 4 E4B, ~5 GB en 4-bit: no cabe con margen), `kev-4B`, Jeff en
bf16. Se documenta qué modelo corrió dónde (§7 del plan de la ruta).

### 4.2. Datasets del **núcleo**

| dataset | `n` (opciones) | split usado | adaptador |
|---|---|---|---|
| `LocalLLaMA/typed-decisions` | 2–6 (`choice`), 2–10 (`score`), 2 (`noul`) | `test` | ya existe (`_load_cases`) |
| `SetFit/sst5` | **5** (ordinal) | `validation` | nuevo |
| `alisawuffles/WANLI` | **3** | `validation` | nuevo |
| `jaredpalmer/kev-suites` | según suite | el que traiga | nuevo |
| `PolyAI/banking77` | **77** | `test` | nuevo (extremo de cardinalidad) |
| `clinc_oos` (`plus`) | **150** | `validation` | nuevo (extremo de cardinalidad) |

El eje `n` es el corazón del trabajo (Proposiciones 1 y 3): 2 · 3 · 5 · 6 · 77 · 150.

### 4.3. Definiciones y niveles

- Definiciones: `pmax` (DEF-4), `jev` (DEF-1), `ent` (DEF-2), `margin` (DEF-5). `noul` (DEF-3) entra solo en
  el bloque `n = 2`.
- Niveles AnyJev (DEF-7): `raw` (**principal**), `L0` (debiasing sin etiquetas), `L1` (temperatura ajustada
  sobre 4/5 de los datos de calibración, nunca sobre prueba).
- **Fuera de la matriz:** `act_probability` (DEF-6) y `open-decision-ai` (DEF-8) → solo catálogo.

### 4.4. Diseño estadístico

- **Cross-fitting `K = 5`** con semilla fija `SEED = 20261008`: cada ítem se asigna a un fold por
  `int(sha256(id) , 16) % 5`. En cada fold: `τ` se ajusta en los otros 4 y se evalúa en el que queda. Así
  **todos** los ítems pasan por prueba exactamente una vez y no hay "suerte de split".
- `q ∈ {0.80, 0.50, 0.95}`.
- **Bootstrap** de ítems `B = 2000`, semilla fija, sobre las celdas → IC 95 %.
- **FDR** Benjamini–Hochberg sobre el conjunto de celdas (p bilateral de bootstrap: `2·min(P(Δ*≤0), P(Δ*≥0))`).
- Empates de `τ`: se toma el **menor** `τ` que alcanza la cobertura objetivo y se reporta `n_empates`.

### 4.5. **Errata detectada en la especificación** (aplicar antes del pre-registro)

`paper/03_especificacion_confidence.md` §5 paso 1 define

> `τ_A = min { τ : (1/|S_cal|)·Σ 𝕀[C_A(i) ≥ τ] ≤ 1 − q }`

pero el paso 3 y la celda de la matriz usan `cobertura = fracción por encima de τ` con objetivo `q`. Las dos
cosas no cuadran: con `q = 0.80`, `≤ 1 − q` seleccionaría un `τ` que deja **20 %** por encima, no 80 %.

**Corrección (la que implementa este plan):**

> `cobertura(τ) = #{i ∈ S_cal : C_A(i) ≥ τ} / |S_cal|`, decreciente en `τ`.
> `τ_A(q) = min { τ ∈ valores observados de C_A : cobertura(τ) ≤ q }`.

**Acción obligatoria:** editar esa línea de la especificación y anotar la errata en
`paper/00_plan_del_paper.md` §9. Si el ejecutor no está seguro, **preguntar al autor antes de medir**: el
pre-registro no puede citar una definición ambigua.

### 4.6. Rutas de artefactos (respetan la regla de orden del repo)

```
src/jev_conf_metrics/            librería (matemática pura, stdlib + numpy solo en transferencia.py)
tests/                           pytest: definiciones, métricas, transferencia, regresión del paso 0
src/matriz/                      pipeline: medir.py · matriz.py · figura.py · informe_matriz.py
results/crudos/                  <modelo>__<dataset>.jsonl   (una fila por ítem, con row_hash)
results/matrix/                  matriz_transferencia.csv · matriz_ic.csv · resumen.json · heatmaps · RESUMEN_MATRIZ.md
paper/04_pre_registro.md         borrador del pre-registro (lo publica el autor en Zenodo)
docs/handoff-t440.md             qué hay, cómo se regenera, qué falta, y mapa artefacto → sección del paper
```

**Desviación consciente de `paper/00_plan_del_paper.md` §5** (que nombra `results/matriz_transferencia.csv` en
la raíz): se usa `results/matrix/` porque ya existe con `.gitkeep` y porque README §5 y `.hermes.md` §5 ya
describen esa carpeta. Anotar la desviación en el README al cerrar.

---

## 5. Fase 0 — Higiene de recursos y terreno limpio

### Tarea 0.1 — Matar el servidor de Kev (libera 4.8 GB de VRAM)

```bash
pkill -f "kev.serve" ; sleep 3
nvidia-smi --query-gpu=memory.used,memory.free --format=csv
```
**Esperado:** `memory.used` baja de ~4843 MiB a <300 MiB y `memory.free` sube a >5800 MiB.
Si sigue ocupado: `ps aux | grep -i kev` y matar el PID restante.
**Nota:** no es Laya lo que está corriendo; es el servidor de Kev. Se vuelve a levantar solo en la tarea 2.4.

### Tarea 0.2 — Confirmar el venv y fijar el entorno de la sesión

```bash
cd /home/arbues-harus/Github/personales/tesis1-jev-confidence
source .venv/bin/activate
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```
**Esperado:** `2.14.1+cu126 True NVIDIA GeForce RTX 4050 Laptop GPU`.
Si `torch.cuda.is_available()` es `False`, **parar**: el build de torch se rompió (ver `src/README.md`,
trampa cu130 vs cu126).

### Tarea 0.3 — Inventario de dependencias y de schemas (sin asumir nada)

```bash
python - <<'PY'
for m in ["numpy","pytest","matplotlib","scipy","pandas","bitsandbytes","datasets","transformers","peft","laya"]:
    try:
        mod = __import__(m); print(f"  {m:14s} {getattr(mod,'__version__','?')}")
    except Exception: print(f"  {m:14s} NO")
PY
```
**Esperado:** `numpy`, `datasets`, `transformers`, `peft`, `laya` presentes; `pytest`/`matplotlib`/`bitsandbytes`
probablemente `NO`. Instalar solo lo que falte, en un solo comando:

```bash
uv pip install --python .venv/bin/python pytest matplotlib numpy
```
`bitsandbytes` **no** se instala aún: solo se necesita si se añaden los modelos 4-bit (tarea 2.6).

### Tarea 0.4 — Inspeccionar los schemas de los datasets nuevos

```bash
for d in SetFit/sst5 alisawuffles/WANLI jaredpalmer/kev-suites PolyAI/banking77 clinc_oos; do
  echo "=== $d"; curl -s --max-time 20 "https://datasets-server.huggingface.co/splits?dataset=$d" | head -c 300; echo
done
```
**Esperado:** JSON con `splits` y `config`. **Anotar en el chat (o en un scratch) los nombres exactos de
config/split y las columnas.** Es la entrada de la tarea 2.3; si un dataset no responde, se marca como
"extensión" y no bloquea.

### Tarea 0.5 — Rama de trabajo

```bash
git checkout -b feat/matriz-transferencia
git push -u origin feat/matriz-transferencia
```
**Esperado:** rama creada desde el tip de `feat/paso0-go-no-go` (así los tests de regresión tienen los
resúmenes del paso 0 commiteados).

---

## 6. Fase 1 — Librería `jev-conf-metrics` + tests

**Estrategia: extracción literal, no reescritura.** La matemática de `src/paso0_go_no_go.py` ya está validada
por `--selftest`; se **mueve tal cual** y se deja un `from jev_conf_metrics import *` para no romper nada.

### Tarea 1.1 — Crear el esqueleto y mover las definiciones (DEF-1…DEF-5, DEF-7)

Crear `src/jev_conf_metrics/definiciones.py` con la cabecera:

```python
# -*- coding: utf-8 -*-
"""Definiciones del campo `confidence` (DEF-1..DEF-5) y transformaciones AnyJev (DEF-7).

Especificación normativa: paper/03_especificacion_confidence.md
"""
from __future__ import annotations
import math

__all__ = ["conf_jev", "conf_ent", "conf_pmax", "conf_margin", "conf_noul",
           "CONFIDENCES", "all_confidences", "order_equiv_affine_jev_pmax",
           "phi_inv", "aplicar_l0", "aplicar_l1"]
```

y pegar **verbatim** desde `src/paso0_go_no_go.py`:

- líneas **49–105** (`conf_jev`, `conf_ent`, `conf_pmax`, `conf_margin`, `conf_noul`, `CONFIDENCES`,
  `all_confidences`, `order_equiv_affine_jev_pmax`).

Añadir al final (nuevas, con la lógica ya validada en el `selftest` líneas 789–803):

```python
def phi_inv(y, n):
    """Inversa de φ: φ⁻¹(y) = (y·(n−1) + 1)/n  (Proposición 1)."""
    return (y * (n - 1.0) + 1.0) / n


def aplicar_l0(p, b):
    """AnyJev L0 — debiasing sin etiquetas: p' = Proj_Δ(p − b), recortando y renormalizando."""
    q = [max(0.0, pi - bi) for pi, bi in zip(p, b)]
    s = sum(q)
    return [x / s for x in q] if s > 0 else list(p)


def aplicar_l1(p, T):
    """AnyJev L1 — temperatura con etiquetas: p' = softmax(log p / T)."""
    z = [math.log(max(pi, 1e-12)) / T for pi in p]
    m = max(z)
    e = [math.exp(v - m) for v in z]
    s = sum(e)
    return [v / s for v in e]
```

**Verificación:**

```bash
python -c "
from src.jev_conf_metrics.definiciones import *
p=[0.0118,0.4629,0.5253]
print(round(conf_jev(p),3), round(conf_ent(p),3), round(conf_pmax(p),3))
print(round(aplicar_l1(p,1.0)[2],4), round(aplicar_l0(p,[0.2,0.2,0.2])[2],4))"
```
**Esperado:** `0.288 0.32 0.525` y `0.5253 ...` (T=1 deja la distribución igual: `aplicar_l1(p,1.0) == p`).

### Tarea 1.2 — Mover las métricas

Crear `src/jev_conf_metrics/metricas.py` y pegar **verbatim** las líneas **107–192** de
`src/paso0_go_no_go.py` (`ece`, `ece_laya`, `auroc`, `brier_multi`, `nll`). Cabecera:

```python
# -*- coding: utf-8 -*-
"""Métricas de calibración y discriminación (stdlib puro)."""
from __future__ import annotations
import math
__all__ = ["ece", "ece_laya", "auroc", "brier_multi", "nll", "rps"]
```

Añadir `rps` (ranked probability score, para el primitivo `score` ordinal; lo usa el ecosistema y el paper
lo menciona):

```python
def rps(p, y):
    """Ranked Probability Score para distribuciones ordinales (menor = mejor)."""
    c = 0.0
    acc_p = acc_o = 0.0
    for i, pi in enumerate(p):
        acc_p += pi
        acc_o += 1.0 if i >= y else 0.0
        c += (acc_p - acc_o) ** 2
    return c / max(1, len(p) - 1)
```

### Tarea 1.3 — Escritura de `transferencia.py` (lo genuinamente nuevo)

`src/jev_conf_metrics/transferencia.py`:

```python
# -*- coding: utf-8 -*-
"""Transferencia de umbrales (definición operativa de la matriz).

paper/03_especificacion_confidence.md §5, con la errata corregida (§4.5 de este plan):
  cobertura(τ) = #{i : C(i) >= τ} / N          (decreciente en τ)
  τ_A(q)       = min{ τ : cobertura(τ) <= q }
"""
from __future__ import annotations
import random
import hashlib

__all__ = ["cobertura", "precision", "umbral_para_cobertura", "celda", "fold_de",
           "bootstrap_delta", "bh_fdr"]


def cobertura(confs, tau):
    return sum(1 for c in confs if c >= tau) / len(confs) if confs else 0.0


def precision(confs, correct, tau):
    sel = [c for c, a in zip(confs, correct) if c >= tau]
    return (sum(sel) / len(sel)) if sel else float("nan")


def umbral_para_cobertura(confs, q):
    """Menor τ observado cuya cobertura cae a <= q (y nº de empates en ese τ)."""
    vals = sorted(set(confs))
    for tau in vals:
        if cobertura(confs, tau) <= q:
            return tau, sum(1 for c in confs if c == tau)
    return vals[-1], sum(1 for c in confs if c == vals[-1])


def celda(conf_a_cal, conf_b_cal, conf_a_te, conf_b_te, correct_te, q):
    """Una celda (A -> B): τ_A de calibración, aplicado TAL CUAL a B en prueba."""
    tau, emp = umbral_para_cobertura(conf_a_cal, q)
    cov_b = cobertura(conf_b_te, tau)
    return {
        "tau": tau, "n_empates_tau": emp,
        "cobertura_B": cov_b, "delta": q - cov_b,
        "precision_B": precision(conf_b_te, correct_te, tau),
        "precision_A": precision(conf_a_te, correct_te, tau),
        "cobertura_A_te": cobertura(conf_a_te, tau),
    }


def fold_de(item_id, k=5, seed=20261008):
    """Asignación determinista de fold por hash del id (cross-fitting reproducible)."""
    h = hashlib.sha256(f"{seed}:{item_id}".encode()).hexdigest()
    return int(h, 16) % k


def bootstrap_delta(conf_b_te, correct_te, tau, q, B=2000, seed=20261008):
    """IC 95 % y p bilateral por bootstrap de ítems (τ fijo, no se re-ajusta)."""
    rng = random.Random(seed)
    n = len(conf_b_te)
    deltas = []
    for _ in range(B):
        idx = [rng.randrange(n) for _ in range(n)]
        cb = [conf_b_te[i] for i in idx]
        deltas.append(q - cobertura(cb, tau))
    deltas.sort()
    lo, hi = deltas[int(0.025 * B)], deltas[int(0.975 * B) - 1]
    p = 2 * min(sum(1 for d in deltas if d <= 0), sum(1 for d in deltas if d >= 0)) / B
    return {"delta_media": sum(deltas) / B, "ic95_lo": lo, "ic95_hi": hi, "p": min(1.0, p)}


def bh_fdr(pvals, alpha=0.05):
    """Benjamini-Hochberg: devuelve (rechaza, q_valor) en el orden de entrada."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank, i in enumerate(reversed(order), start=1):
        k = m - rank + 1
        val = min(prev, pvals[i] * m / k)
        q[i] = val
        prev = val
    return [qi <= alpha for qi in q], q
```

**Verificación inmediata (sin datos):**

```bash
python -c "
from src.jev_conf_metrics.transferencia import *
import random
rng=random.Random(1); a=[rng.random() for _ in range(1000)]; b=[rng.random() for _ in range(1000)]
c=[rng.randrange(2) for _ in range(1000)]
print(celda(a,b,a,b,c,0.8)); print(umbral_para_cobertura(a,0.8)); print(bootstrap_delta(b,c,0.5,0.8,B=200))"
```
**Esperado:** un dict con `delta` ≈ 0 (A y B son la misma variable aleatoria), un `(τ, empates)` con τ en
`[0,1]`, y un dict con `ic95_lo < ic95_hi`.

### Tarea 1.4 — `recursos.py` (el guard de RAM/VRAM)

`src/jev_conf_metrics/recursos.py`:

```python
# -*- coding: utf-8 -*-
"""Guard de recursos: aborta ANTES de cargar un modelo si no hay RAM/VRAM (WSL2 no perdona)."""
from __future__ import annotations
import gc
import subprocess
import sys

RAM_MINIMA_GB = 1.0
__all__ = ["ram_disponible_gb", "vram_libre_mb", "exigir_recursos", "liberar"]


def ram_disponible_gb():
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) / 1024 / 1024
    return float("inf")


def vram_libre_mb():
    try:
        out = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=15, check=True).stdout.strip().splitlines()
        return min(int(x) for x in out) if out else None
    except Exception:
        return None


def exigir_recursos(vram_necesaria_mb=0, ram_necesaria_gb=RAM_MINIMA_GB, etiqueta=""):
    ram, vram = ram_disponible_gb(), vram_libre_mb()
    if ram < ram_necesaria_gb:
        sys.exit(f"[recursos] ABORTADO{etiqueta}: RAM libre {ram:.1f} GB < {ram_necesaria_gb} GB")
    if vram is not None and vram < vram_necesaria_mb:
        sys.exit(f"[recursos] ABORTADO{etiqueta}: VRAM libre {vram} MB < {vram_necesaria_mb} MB "
                 f"(¿sigue vivo el servidor de Kev? prueba: pkill -f kev.serve)")
    print(f"[recursos] ok{etiqueta}: RAM {ram:.1f} GB · VRAM {vram} MB", flush=True)


def liberar(*objetos):
    """Suelta referencias y vacía la caché de CUDA. Llamar SIEMPRE entre modelos."""
    for o in objetos:
        del o
    gc.collect()
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
    except Exception:
        pass
    print("[recursos] liberado", flush=True)
```

**Verificación:**

```bash
python -c "
from src.jev_conf_metrics.recursos import *
exigir_recursos(vram_necesaria_mb=1000, etiqueta=' prueba')"
```
**Esperado:** `[recursos] ok prueba: RAM ~11.0 GB · VRAM ~5800 MB` (tras la tarea 0.1).
Si dice `ABORTADO`: el servidor de Kev sigue vivo → volver a 0.1.

### Tarea 1.5 — `__init__.py` y el puente desde el script del paso 0

`src/jev_conf_metrics/__init__.py`:

```python
# -*- coding: utf-8 -*-
"""jev-conf-metrics — metrología del campo `confidence` en modelos tipo Jev."""
from .definiciones import *          # noqa: F401,F403
from .metricas import *              # noqa: F401,F403
from .transferencia import *         # noqa: F401,F403
from .recursos import *              # noqa: F401,F403
__version__ = "0.1.0"
```

En `src/paso0_go_no_go.py`, **sustituir** el bloque de definiciones y métricas (líneas 45–192) por:

```python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from jev_conf_metrics.definiciones import *      # noqa: F401,F403
from jev_conf_metrics.metricas import *          # noqa: F401,F403
from jev_conf_metrics.recursos import liberar    # noqa: F401
```

**Verificación (regresión dura — no basta con que no explote):**

```bash
python src/paso0_go_no_go.py --selftest
```
**Esperado:** `SELFTEST OK — la matemática del marco teórico es consistente.` (idéntico al de antes del
refactor).

### Tarea 1.6 — Tests de conformidad (T1–T8) + regresión del paso 0

`tests/test_definiciones.py` — traduce 1:1 la tabla §6 de la especificación. Los tests **T4–T8 ya existen**
como aserciones dentro de `selftest()` (líneas 752–839 de `src/paso0_go_no_go.py`): se **copian** a pytest.

```python
# -*- coding: utf-8 -*-
import math, random, pytest
from src.jev_conf_metrics.definiciones import *

N = 3
PROBS = [[0.6, 0.2, 0.2], [0.6, 0.4, 0.0], [1/3, 1/3, 1/3], [1.0, 0.0, 0.0], [0.0118, 0.4629, 0.5253]]

def test_T1_rango():
    for p in PROBS:
        for v in all_confidences(p).values():
            assert 0.0 <= v <= 1.0 + 1e-9

def test_T2_extremos():
    u, oh = [1/3]*3, [1.0, 0.0, 0.0]
    assert abs(conf_jev(u)) < 1e-12 and abs(conf_ent(u)) < 1e-12
    assert abs(conf_jev(oh) - 1) < 1e-12 and abs(conf_ent(oh) - 1) < 1e-12

def test_T4_prop1_jev_es_phi_de_pmax():
    phi = order_equiv_affine_jev_pmax(N)
    for p in PROBS:
        assert abs(conf_jev(p) - phi(conf_pmax(p))) < 1e-12
        assert abs(phi_inv(conf_jev(p), N) - conf_pmax(p)) < 1e-12

def test_T5_prop2_entropia_no_determinada_por_pmax():
    a, b = [0.6, 0.2, 0.2], [0.6, 0.4, 0.0]
    assert abs(max(a) - max(b)) < 1e-12 and abs(conf_ent(a) - conf_ent(b)) > 1e-6

def test_T6_prop3_n2_todas_equivalentes_en_orden():
    pis = [0.5 + 0.5*i/499 for i in range(500)]
    p2 = [[x, 1-x] for x in pis]
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0]*len(v)
        for pos, i in enumerate(o): r[i] = pos
        return r
    base = rank([conf_pmax(p) for p in p2])
    for v in ([conf_jev(p) for p in p2], [conf_ent(p) for p in p2],
              [conf_margin(p) for p in p2], [conf_noul(x) for x in pis]):
        assert rank(v) == base

def test_T7_referencia_publicada():
    p = [0.0118, 0.4629, 0.5253]
    assert abs(conf_jev(p) - 0.288) < 0.001
    assert abs(conf_ent(p) - 0.3199) < 0.001
    assert abs(conf_pmax(p) - 0.5253) < 1e-12

def test_T8_noul_simetrico():
    for i in range(500):
        x = i / 499
        assert abs(conf_noul(x) - conf_noul(1-x)) < 1e-12 and conf_noul(x) >= 0.5 - 1e-12
```

`tests/test_transferencia.py`:

```python
# -*- coding: utf-8 -*-
import random
from src.jev_conf_metrics.definiciones import conf_jev, conf_pmax, conf_ent
from src.jev_conf_metrics.transferencia import *

def test_transferencia_exacta_jev_pmax():
    """Prop.1: dentro de la clase {pmax, jev} el Δ debe ser 0 (mismo conjunto por encima)."""
    rng = random.Random(7)
    probs = [[rng.random()**2 + 0.1 for _ in range(4)] for _ in range(2000)]
    probs = [[x/sum(p) for x in p] for p in probs]
    a = [conf_jev(p) for p in probs]; b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    r = celda(a, b, a, b, c, 0.80)
    assert abs(r["delta"]) < 1e-9, r

def test_transferencia_fallida_ent_pmax():
    """Prop.2: ent -> pmax NO transfiere (Δ distinto de 0)."""
    rng = random.Random(11)
    probs = [[rng.random()**2 + 0.1 for _ in range(4)] for _ in range(2000)]
    probs = [[x/sum(p) for x in p] for p in probs]
    a = [conf_ent(p) for p in probs]; b = [conf_pmax(p) for p in probs]
    c = [rng.randrange(2) for _ in probs]
    r = celda(a, b, a, b, c, 0.80)
    assert abs(r["delta"]) > 1e-3, r

def test_fold_determinista():
    assert fold_de("abc") == fold_de("abc")
    assert len({fold_de(f"item-{i}") for i in range(1000)}) == 5

def test_bh_fdr_monotono():
    rej, q = bh_fdr([0.001, 0.02, 0.5, 0.9])
    assert rej[0] is True and rej[3] is False and all(0 <= x <= 1 for x in q)
```

`tests/test_regresion_paso0.py` — **el test más importante**: recalcula los números del paso 0 desde los
crudos y los compara con los resúmenes commiteados.

```python
# -*- coding: utf-8 -*-
import json, glob, os
from src.jev_conf_metrics.metricas import ece, ece_laya, auroc, brier_multi

RAW = "results/raw"

def test_laya_typed_decisions_reproduce_el_resumen():
    summ = json.load(open(f"{RAW}/paso0_summary_laya_typed-decisions.json"))
    rows = [json.loads(l) for l in open(f"{RAW}/paso0_raw_laya_typed-decisions.jsonl")]
    confs = [r["conf_pmax"] for r in rows]
    correct = [r["correct"] for r in rows]
    assert abs(auroc(confs, correct) - summ["global"]["auroc_pmax"]) < 1e-9
    assert abs(ece(confs, correct, 15, "width") - summ["global"]["ece_pmax_width"]) < 1e-9
    assert abs(ece_laya(confs, correct, 15) - summ["global"]["ece_pmax_laya"]) < 1e-9

def test_row_hash_estable():
    import hashlib
    row = json.loads(open(f"{RAW}/paso0_raw_laya_typed-decisions.jsonl").readline())
    h = row.pop("row_hash")
    assert hashlib.sha256(json.dumps(row, sort_keys=True, default=str).encode()).hexdigest()[:16] == h
```

**Ciclo TDD de la fase (obligatorio):**

1. `uv pip install --python .venv/bin/python pytest`
2. `python -m pytest tests/ -q` → **debe fallar** con `ModuleNotFoundError: src.jev_conf_metrics`
   (aún no existe) → eso valida que los tests se ejecutan.
3. Implementar 1.1–1.5.
4. `python -m pytest tests/ -q` → **esperado:** `11 passed`.
5. `python src/paso0_go_no_go.py --selftest` → `SELFTEST OK`.
6. **Commit:** `git add src/jev_conf_metrics tests src/paso0_go_no_go.py && git commit -m "Libreria jev-conf-metrics + tests de conformidad (T1-T8) y regresion del paso 0"`

---

## 7. Fase 2 — Pipeline de medición multi-modelo / multi-dataset

### Tarea 2.1 — `src/matriz/medir.py` (runner genérico)

Responsabilidad: **un modelo × un dataset → `results/crudos/<modelo>__<dataset>.jsonl`**. Reutiliza
`_load_cases`/`_normalize_answer`/`_summarize` del paso 0 (importándolos, no copiándolos: mover esas tres
funciones a `src/matriz/comun.py` y que `paso0_go_no_go.py` las importe de ahí).

Esqueleto (los detalles de cada adaptador son la tarea 2.3):

```python
# -*- coding: utf-8 -*-
"""Mide un modelo sobre un dataset y escribe results/crudos/<modelo>__<dataset>.jsonl."""
import argparse, gc, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jev_conf_metrics.definiciones import all_confidences, conf_noul
from jev_conf_metrics.recursos import exigir_recursos, liberar
from matriz.adaptadores import ADAPTADORES

def medir(backend, dataset_key, out_dir, limite=None):
    casos = ADAPTADORES[dataset_key](limite)
    filas = []
    for i, c in enumerate(casos, 1):
        payload = backend.predict(c["state"], c["questions"])
        for qname, gold in c["gold"].items():
            ans = (payload.get("answers") or {}).get(qname) or {}
            # ... normalizar (igual que run_real) ...
            fila = {...}          # ver run_real, líneas 664-679 de src/paso0_go_no_go.py
            filas.append(fila)
        if i % 50 == 0: print(f"  [{i}/{len(casos)}]", flush=True)
    return filas

def escribir(filas, path, meta):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import hashlib
    with open(path, "w", encoding="utf-8") as f:
        for r in filas:
            r.update(meta)
            r["row_hash"] = hashlib.sha256(json.dumps(r, sort_keys=True, default=str).encode()).hexdigest()[:16]
            f.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
```

CLI: `python src/matriz/medir.py --model laya --subfolder typed-decisions --dataset typed-decisions`
(debe aceptar `--limite`, `--out results/crudos`, `--dataset`).

### Tarea 2.2 — Portar los backends al runner

Mover `LayaBackend`, `KevHTTPBackend`, `HFLogitBackend`, `BackendError`, `_softmax`, `BACKENDS` y
`build_backend` desde `src/paso0_go_no_go.py` a `src/matriz/backends.py` (verbatim), y que el script del paso 0
los importe. **No reescribir la lógica de Laya/Kev**: está verificada contra los números publicados.

**Verificación de no-regresión:**

```bash
python src/paso0_go_no_go.py --model laya --subfolder typed-decisions --split test --n 5 --out /tmp/prueba
```
**Esperado:** corre, imprime el resumen y dice `output_tokens == 0 en todas las filas: True`.
(Luego `rm -rf /tmp/prueba`.)

### Tarea 2.3 — Adaptadores de dataset (`src/matriz/adaptadores.py`)

Cada adaptador devuelve la misma estructura que `_load_cases`:
`{"id", "workflow", "config", "state", "questions", "gold"}`.

- `typed_decisions(limite)` → **ya existe**, se reutiliza `_load_cases`.
- `sst5(limite)` → `SetFit/sst5`, split `validation`; 5 niveles ordinales con su `legend`
  (`"1 = muy negativo" … "5 = muy positivo"`); `gold = {"sentiment": {"label": <str>, "score": <int>}}`.
- `wanli(limite)` → `alisawuffles/WANLI`, split `validation`; `n = 3` (`entailment`/`neutral`/`contradiction`).
- `kev_suites(limite)` → inspeccionar primero (tarea 0.4); puede traer ya el formato de Kev.
- `banking77(limite)` → `PolyAI/banking77` split `test`, `n = 77`; las opciones son los **nombres** de intent.
- `clinc_oos(limite)` → config `plus`, split `validation`, `n = 150`; **ojo:** hay una clase `oos`
  (fuera de dominio): decidir si entra como opción (documentarlo en el pre-registro).

**Regla de oro de los adaptadores:** si el dataset no se puede mapear sin inventar nada, **no se inventa**:
se registra como "extensión" y se sigue. Nada de anotación propia (D2).

**Verificación por adaptador (sin GPU):**

```bash
python -c "
from src.matriz.adaptadores import ADAPTADORES
for k in ADAPTADORES:
    c = ADAPTADORES[k](3)
    print(k, len(c), c[0]['state'][:60].replace(chr(10),' '), list(c[0]['questions'])[:2])"
```
**Esperado:** una línea por dataset con 3 casos y el estado truncado.

### Tarea 2.4 — Medir el núcleo, **modelo a modelo** (aquí está el riesgo de VRAM)

Orden de ejecución (de menor a mayor presión), un modelo a la vez, **matando el servidor entre bloques**:

```bash
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
# --- bloque 1: Laya (3 checkpoints) × todos los datasets
for sub in none typed-decisions multilingual; do
  for ds in typed-decisions sst5 wanli; do
    python src/matriz/medir.py --model laya --subfolder $sub --dataset $ds --out results/crudos
  done
done
# --- bloque 2: control crudo
python src/matriz/medir.py --model raw --dataset typed-decisions --out results/crudos
# --- bloque 3: Kev (se levanta el servidor SOLO aquí)
nohup uv run --extra serve python -m kev.serve --run jaredpalmer/kev-0.8b --port 8008 \
  > /home/arbues-harus/.hermes/cache/scratch/kev_server.log 2>&1 &
# esperar readiness (bucle acotado con health-check, no un sleep ciego):
for i in $(seq 1 60); do curl -s -o /dev/null --max-time 3 http://127.0.0.1:8008/docs && break; sleep 5; done
for ds in typed-decisions kev-suites; do
  python src/matriz/medir.py --model kev --dataset $ds --out results/crudos
done
pkill -f "kev.serve"   # <-- obligatorio: libera 4.8 GB antes del siguiente bloque
nvidia-smi --query-gpu=memory.used --format=csv     # esperado: <300 MiB
```

**Verificación por corrida:** cada comando imprime `[recursos] ok …` antes de cargar y `[recursos] liberado`
al terminar. Si aparece `ABORTADO`, **no se insiste**: se libera y se revisa qué quedó vivo.

### Tarea 2.5 — Modelos 4-bit (solo si 2.4 terminó limpio)

```bash
uv pip install --python .venv/bin/python bitsandbytes
python -c "import bitsandbytes, torch; print(bitsandbytes.__version__, torch.cuda.is_available())"
```
Luego `HFLogitBackend` gana un parámetro `load_4bit=True`:

```python
from transformers import BitsAndBytesConfig
bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                         bnb_4bit_compute_dtype=torch.bfloat16)
model = AutoModelForCausalLM.from_pretrained(mid, quantization_config=bnb,
                                             device_map={"": 0}, torch_dtype="auto").eval()
```
**Umbral de decisión:** si `exigir_recursos` no ve **≥ 3300 MB libres**, no se carga. Si `bitsandbytes` no
arranca en WSL2 tras **2 intentos**, se marca `Jeff-1`/`SemIf` como **extensión del Mac Mini** y se sigue —
no se bloquea el entregable.

**Para `GestaltLabs/Jeff-1`:** inspeccionar primero si el repo trae pesos fusionados o un adaptador LoRA:

```bash
curl -s https://huggingface.co/api/models/GestaltLabs/Jeff-1 | python -c "import json,sys; d=json.load(sys.stdin); print([s['rfilename'] for s in d.get('siblings',[])])"
```
Si hay `adapter_config.json` → cargar base + `PeftModel.from_pretrained(...)`; si hay `model.safetensors`
completos → cargar directo. **No adivinar.**

### Tarea 2.6 — Commit de la fase

```bash
git add src/matriz results/crudos
git commit -m "Pipeline de medicion multi-modelo/multi-dataset + mediciones crudas"
git push
```
**Antes de commitear:** `du -sh results/crudos` y confirmar que cada `.jsonl` tiene tantas líneas como ítems
(`wc -l results/crudos/*.jsonl`).

---

## 8. Fase 3 — La matriz, la estadística y la figura

### Tarea 3.1 — `src/matriz/matriz.py` (CPU puro, corre en el t440)

Entrada: `results/crudos/*.jsonl`. Salida: `results/matrix/matriz_transferencia.csv` y `matriz_ic.csv`.

Lógica, por cada (modelo, dataset):

1. Agrupar filas por `n_options` (la cardinalidad manda: Proposiciones 1 y 3).
2. Calcular, sobre la **misma** distribución, `conf_pmax`, `conf_jev`, `conf_ent`, `conf_margin`
   (ya vienen en la fila como `conf_*`) y los niveles `L0`/`L1` si están.
3. Asignar folds con `fold_de(id)`.
4. Para cada fold, cada par ordenado `(A, B)`, `A ≠ B`, y cada `q ∈ {0.80, 0.50, 0.95}`: llamar a `celda()`.
5. Promediar `delta`, `cobertura_B`, `precision_B` sobre los 5 folds; contar `n` de ítems.
6. `bootstrap_delta` sobre la unión de prueba + `bh_fdr` sobre todas las celdas.

Cabecera del CSV: `modelo,dataset,n,q,nivel,A,B,tau,cobertura_B,delta,precision_B,precision_A,n_items,ic95_lo,ic95_hi,p,q_fdr,rechaza`.

**Verificación (sin GPU, sobre los crudos ya escritos):**

```bash
python src/matriz/matriz.py --crudos results/crudos --out results/matrix
head -3 results/matrix/matriz_transferencia.csv
python -c "
import csv,collections
r=list(csv.DictReader(open('results/matrix/matriz_transferencia.csv')))
print('celdas:', len(r), '| modelos:', len({x['modelo'] for x in r}), '| datasets:', len({x['dataset'] for x in r}))
clase=[x for x in r if {x['A'],x['B']}=={'pmax','jev'} and x['n']=='3' and x['q']=='0.8']
print('celdas jev<->pmax n=3 (deben ser delta~0):', [round(float(x['delta']),4) for x in clase])"
```
**Esperado:** celdas = `(modelos × datasets × cardinalidades × niveles × 12 pares × 3 q)`; y **todas** las
celdas `jev↔pmax` con `|delta| < 1e-6` (Proposición 1). Si alguna no lo es, hay un bug — **parar y revisar**
antes de seguir.

### Tarea 3.2 — `src/matriz/figura.py` (matplotlib, `Agg`)

- `heatmap_<dataset>.png` y `.pdf`: filas = definición origen, columnas = destino, color = `delta`,
  una cara por modelo, anotación del valor en cada celda. Título con `q` y cardinalidad.
- `cobertura_vs_q.png`: cobertura real de B contra `q` objetivo, una curva por par.
- **Sin display:** `import matplotlib; matplotlib.use("Agg")`.

**Verificación:** `ls -la results/matrix/*.png` → al menos 2 ficheros de >20 KB; abrir uno con
`vision_analyze` y confirmar que se lee.

### Tarea 3.3 — `src/matriz/informe_matriz.py` → `results/matrix/RESUMEN_MATRIZ.md`

Genera (stdlib) el informe legible: la tabla de celdas por modelo/dataset, los pares **exactos** (Δ≈0) y los
**peligrosos** (mayor |Δ| con FDR), el efecto de `n`, y la comparación con lo auto-reportado por el ecosistema
(columna **medido aquí / auto-reportado**, D4). **Regla:** todos los números salen de `resumen.json`; nada
escrito a mano (misma disciplina que `src/paso0_informe.py`).

**Verificación:** `python src/matriz/informe_matriz.py && wc -l results/matrix/RESUMEN_MATRIZ.md` → >60 líneas.

### Tarea 3.4 — Aplicar la errata de §4.5 y commitear

```bash
# editar paper/03_especificacion_confidence.md §5 (línea de τ_A) y anotar en paper/00_plan_del_paper.md §9
git add src/matriz results/matrix paper/03_especificacion_confidence.md paper/00_plan_del_paper.md
git commit -m "Matriz de transferencia + bootstrap + FDR + figuras; errata de la definicion de tau_A"
git push
```

---

## 9. Fase 4 — Borrador del pre-registro (entrada del DOI del autor)

### Tarea 4.1 — `paper/04_pre_registro.md`

Contenido (1–2 páginas, congelado **antes** de la corrida principal):

1. Título y autores. 2. Claim falsable (plan §2). 3. Definiciones incluidas y excluidas (§4.3 de este plan).
4. Modelos y datasets con **sha del Hub** (`results/raw/paso0_versions.json` + el que se genere).
5. Procedimiento: cross-fitting K=5, `q ∈ {0.80, 0.50, 0.95}`, bootstrap B=2000, BH-FDR.
6. Qué se reportará pase lo que pase (incluidos resultados nulos).
7. Qué **no** se hará: `act_probability`, `open-decision-ai`, anotación humana, nube.
8. Declaración de que el paso 0 ya se ejecutó y que la corrida principal es posterior.

### Tarea 4.2 — Entregar al autor

Mensaje de una línea al autor: «sube `paper/04_pre_registro.md` (o su PDF) a Zenodo con
`Resource type = Preprint`, `CC-BY-4.0`, y pásame el DOI». **El DOI no lo puede crear el agente.**

---

## 10. Fase 5 — Handoff al t440 y cierre

### Tarea 5.1 — `docs/handoff-t440.md`

Debe responder, sin que el t440 tenga que abrir un `.jsonl`:

- **Qué hay**: lista de artefactos con ruta y qué contiene cada uno.
- **Mapa artefacto → sección del paper** (§4 Método ← pre-registro + este doc; §5 Resultados ←
  `matriz_transferencia.csv` + heatmaps; §6 Discusión ← `RESUMEN_MATRIZ.md`; §7 ← lista de artefactos).
- **Cómo se regenera todo sin GPU**: `python src/matriz/matriz.py`, `figura.py`, `informe_matriz.py`
  (solo numpy/matplotlib), y `python src/paso0_informe.py`.
- **Qué NO se puede regenerar en el t440**: la inferencia (pesos + GPU). Por eso los crudos están commiteados.
- **Qué queda abierto** (extensión al Mac Mini: Nimble-9B, jev-lite, kev-4B) y **qué modelos no entraron y
  por qué** (licencia/VRAM), para que el paper lo declare como limitación.
- **Trazabilidad D4**: sha de cada modelo/dataset y el `row_hash` por fila.

### Tarea 5.2 — Actualizar el estado del repo (en el mismo paso, regla de mantenimiento)

- `README.md` §13 (o nueva §14): resultado de la matriz en 5 líneas + desviación de rutas (§4.6).
- `STATE.json`: bloque `matriz_2026_10_XX` (celdas, pares exactos/peligrosos, sha, dónde corrió cada modelo).
- `.hermes.md` §7 y `AGENTS.md` §6: el pendiente pasa a ser «paper §4–§7 en el t440» + «DOI del autor».
- `paper/00_plan_del_paper.md` §5: marcar artefactos 3, 4 y 5 como **hechos**.

### Tarea 5.3 — PR

```bash
git push
```
Abrir el PR contra `main` (título: *Librería jev-conf-metrics + matriz de transferencia medida en el Nitro*).
**Recordatorio:** el PR del paso 0 sigue sin abrir; el autor lo abre desde
`https://github.com/Arbues/tesis1-jev-confidence/pull/new/feat/paso0-go-no-go`.

---

## 11. Validación global (criterios de aceptación)

| # | Criterio | Comando exacto | Esperado |
|---|---|---|---|
| V1 | La matemática no se rompió al extraer la librería | `python src/paso0_go_no_go.py --selftest` | `SELFTEST OK` |
| V2 | Conformidad T1–T8 | `python -m pytest tests/ -q` | `11 passed` (o más) |
| V3 | Regresión numérica contra el paso 0 | `python -m pytest tests/test_regresion_paso0.py -q` | `2 passed` |
| V4 | Proposición 1 en los datos reales | celdas `jev↔pmax` de `matriz_transferencia.csv` | `|delta| < 1e-6` en todas |
| V5 | Proposición 3 en los datos reales | celdas con `n == 2` | `|delta| < 1e-6` entre **todas** las definiciones |
| V6 | El efecto existe (no es ruido) | celda `ent→pmax` con FDR | `rechaza = True` y `|delta|` > 0.02 |
| V7 | Nada se quedó sin commitear | `git status --short` | vacío |
| V8 | Todo lo necesario está en el repo | `git ls-files results/matrix results/crudos` | CSV + PNG/PDF + `RESUMEN_MATRIZ.md` |
| V9 | El t440 puede regenerar la matriz | en el t440: `python src/matriz/matriz.py --crudos results/crudos --out /tmp/m` | CSV idéntico (comparar con `sha256sum`) |
| V10 | Recursos limpios al terminar | `nvidia-smi --query-gpu=memory.used --format=csv` | <300 MiB (sin servidores huérfanos) |

**V9 es el criterio que cierra el encargo del autor:** si la matriz se puede regenerar en el t440 a partir de
lo commiteado, no quedan huecos.

---

## 12. Riesgos, tradeoffs y preguntas abiertas

| Riesgo | Prob. | Impacto | Mitigación en este plan |
|---|---|---|---|
| WSL2 se cuelga por RAM (modelo grande + caché HF + dos procesos) | media | alto | un modelo a la vez, `exigir_recursos`, `liberar()`, sin paralelismo, sin `device_map="auto"` |
| `bitsandbytes` no arranca en WSL2 | media | bajo | Jeff-1/SemIf son **extensión**; el núcleo (Laya+Kev+raw) no depende de 4-bit |
| Un dataset nuevo no se mapea sin anotar | media | medio | regla "no se inventa": se marca extensión y se sigue (D2 intacto) |
| `kev-suites` trae un formato inesperado | media | bajo | se inspecciona antes (0.4); Kev ya está medido en typed-decisions |
| Los modelos grandes dan accuracy ≈ azar en `n = 77/150` | alta | medio | **es un resultado, no un fallo**: se reporta como límite de cardinalidad (y alimenta la Discusión) |
| La errata de `τ_A` cambia los números ya publicados | baja | alto | se corrige **antes** del pre-registro; el paso 0 no usa `τ` |
| El PR del paso 0 sigue sin abrir y `main` queda atrás | alta | bajo | la rama nueva sale del tip actual; rebase si el autor fusiona antes |

**Preguntas abiertas — RESUELTAS por el autor el 2026-10-08** («usa tu criterio, sin contradicciones ni
huecos de información»):

1. **Errata de `τ_A`: SE APLICA** (§4.5). El autor delega y solo pide coherencia interna.
2. **`banking77` / `clinc150`: NÚCLEO.** Son el extremo de cardinalidad (`n = 77`, `n = 150`) que hace
   visible la Proposición 1 al cruzar `n`. Si la accuracy sale ≈ azar, **se reporta como resultado**.
3. **`Bespoke-Nimble-9B`: SOLO CATÁLOGO**, con la licencia anotada como «no declarada» (D4 pide
   trazabilidad, no permiso).
4. **`tinyjev`: EXTENSIÓN.** El núcleo ya tiene 5 configuraciones de modelo distintas.

**Regla de recursos actualizada por el autor:** el umbral de parada es **1 GB de RAM disponible** (no 4 GB).
Al alcanzarlo: parar todo, suspender y avisar. `RAM_MINIMA_GB = 1.0` en `src/jev_conf_metrics/recursos.py`.

---

## 13. Orden de ejecución resumido

```
F0  higiene (matar Kev · venv · inventario · rama)              ~20 min
F1  librería + tests (TDD: rojo → verde → commit)               ~2 h
F2  pipeline + mediciones crudas (modelo a modelo)              ~4 h (la mayor parte, inferencia)
F3  matriz + bootstrap + FDR + figuras                          ~1.5 h
F4  borrador del pre-registro                                   ~30 min
F5  handoff + estado + PR                                       ~40 min
```

**Regla de parada:** cualquier tarea que falle 3 veces se aparca, se anota en el informe y se sigue con la
siguiente. El entregable (matriz + crudos + handoff) sobrevive a que falte un modelo o un dataset.
