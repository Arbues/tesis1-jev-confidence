# src/ — código (se trabaja en el Acer Nitro)

## `paso0_go_no_go.py` — verificación go/no-go de la Ruta 1

Tres modos, en orden de uso:

| Comando | Dónde | Qué hace |
|---|---|---|
| `python3 src/paso0_go_no_go.py --selftest` | **cualquier máquina** (cae en el t440) | Valida la matemática del marco teórico (solo stdlib): las definiciones de `confidence`, ECE/AUROC/Brier/NLL y las **dos proposiciones** (equivalencia en orden jev↔pmax = transferencia exacta; no-transferencia con la entropía) |
| `python3 src/paso0_go_no_go.py --inspect` | Nitro (con red) | Descubre la **API real** de Laya/Kev y el sha de cada modelo (para completar el adaptador) |
| `python3 src/paso0_go_no_go.py --model kev --n 200` | **Nitro / Mac Mini** | Corre el paso 0 real: pesos + primitivos + ECE sobre `typed-decisions`, y escribe artefactos en `results/raw/` |
| `python3 src/paso0_go_no_go.py --mock` | Nitro (probar el pipeline sin pesos) | Genera los artefactos con datos sintéticos (marcados como NO reales) |

## Puesta en marcha en el Nitro (RTX 4050)

```bash
git clone git@github.com:Arbues/tesis1-jev-confidence.git && cd tesis1-jev-confidence
python3 -m venv .venv && source .venv/bin/activate
pip install -r src/requirements.txt
python3 src/paso0_go_no_go.py --selftest      # debe imprimir: SELFTEST OK
python3 src/paso0_go_no_go.py --inspect       # descubre la API de Laya/Kev
# completar Backend.probs() con la llamada real (5 min) y correr:
python3 src/paso0_go_no_go.py --model kev --n 200
```

## Qué queda por enchufar (5 minutos, ya en el Nitro)

1. **`LayaBackend.probs()`** — la llamada real del paquete `laya` (PyPI v0.3.20) tras `--inspect`.
2. **Mapeo de campos de `typed-decisions`** en `run_real()` (pregunta / opciones / respuesta).

El resto —definiciones, métricas, hashes, artefactos— ya está implementado y probado en `--selftest`.

## Reglas

- Datos y pesos **no se versionan** (ver `.gitignore`).
- Cada fila de `results/raw/*.jsonl` lleva `model_revision` y `row_hash` (D4).
- Corre esto en el **Nitro** o el **Mac Mini**, nunca en el `thinkpad-t440` (sin GPU).
