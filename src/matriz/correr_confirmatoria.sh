#!/usr/bin/env bash
# CORRIDA CONFIRMATORIA — el conjunto COMPLETO de ítems de cada dataset.
#
# Desbloqueada por el pre-registro publicado: DOI 10.5281/zenodo.23266795
# (el piloto usaba subconjuntos; esta es la medición que el pre-registro declara).
#
#   bash src/matriz/correr_confirmatoria.sh [laya|raw|kev|todo]
#
# Escribe en results/crudos_confirmatoria/ (NO pisa el piloto hasta verificarlo).
# Reglas: un modelo en VRAM a la vez; el guard aborta si la RAM baja de 1 GB.
set -u
cd "$(dirname "$0")/../.."
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

PY=.venv/bin/python
OUT=results/crudos_confirmatoria
LOG=$OUT/_log.txt
KEV_DIR="${KEV_DIR:-$HOME/kev-serve}"
SCRATCH="${HERMES_SCRATCH:-$HOME/.hermes/cache/scratch/paso0}"
QUE="${1:-todo}"
mkdir -p "$OUT" "$SCRATCH"
: > "$LOG"

# --limite 0 = "todos los ítems del split" (los adaptadores lo interpretan como len(ds))
LIMITE=0
DATASETS="typed-decisions sst5 wanli banking77 clinc150"

echo "===== CONFIRMATORIA: $(date +%H:%M:%S) · limite=$LIMITE (completo) =====" | tee -a "$LOG"

if [ "$QUE" = "todo" ] || [ "$QUE" = "laya" ]; then
  echo "===== BLOQUE 1: Laya (3 checkpoints) =====" | tee -a "$LOG"
  for sub in none typed-decisions multilingual; do
    for ds in $DATASETS; do
      echo "--- laya/$sub × $ds $(date +%H:%M:%S)" | tee -a "$LOG"
      $PY src/matriz/medir.py --model laya --subfolder "$sub" --dataset "$ds" \
          --limite $LIMITE --out "$OUT" 2>&1 \
        | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
      grep -q "ABORTADO" "$LOG" && { echo "!!! guard abortó: PARAR" | tee -a "$LOG"; exit 1; }
    done
  done
fi

if [ "$QUE" = "todo" ] || [ "$QUE" = "raw" ]; then
  echo "===== BLOQUE 2: control crudo (Qwen3.5-0.8B-Base) =====" | tee -a "$LOG"
  for ds in $DATASETS; do
    echo "--- raw × $ds $(date +%H:%M:%S)" | tee -a "$LOG"
    $PY src/matriz/medir.py --model raw --model-id Qwen/Qwen3.5-0.8B-Base --dataset "$ds" \
        --limite $LIMITE --out "$OUT" 2>&1 \
      | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
  done
fi

if [ "$QUE" = "todo" ] || [ "$QUE" = "kev" ]; then
  echo "===== BLOQUE 3: Kev (servidor solo para este bloque) =====" | tee -a "$LOG"
  if ! curl -s -o /dev/null --max-time 3 http://127.0.0.1:8008/docs; then
    ( cd "$KEV_DIR" && nohup uv run --extra serve python -m kev.serve \
        --run jaredpalmer/kev-0.8b --port 8008 > "$SCRATCH/kev_server.log" 2>&1 & )
    for i in $(seq 1 60); do
      curl -s -o /dev/null --max-time 3 http://127.0.0.1:8008/docs && break
      sleep 5
    done
  fi
  if ! curl -s -o /dev/null --max-time 5 http://127.0.0.1:8008/docs; then
    echo "!!! el servidor de Kev no respondió: se aborta el bloque" | tee -a "$LOG"
  else
    for ds in typed-decisions sst5 wanli banking77; do
      echo "--- kev × $ds $(date +%H:%M:%S)" | tee -a "$LOG"
      $PY src/matriz/medir.py --model kev --dataset "$ds" --limite $LIMITE --out "$OUT" 2>&1 \
        | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
    done
  fi
  pkill -f 'ke[v].serve' || true
  sleep 4
  nvidia-smi --query-gpu=memory.used --format=csv,noheader | tee -a "$LOG"
fi

echo "===== FIN CONFIRMATORIA $(date +%H:%M:%S) =====" | tee -a "$LOG"
echo "archivos:"; ls -la "$OUT"/*.jsonl 2>/dev/null | awk '{print "  "$5" "$9}'
