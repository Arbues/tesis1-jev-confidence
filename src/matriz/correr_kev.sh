#!/usr/bin/env bash
# Bloque de Kev: levanta su servidor SOLO para este bloque y lo mata al terminar.
# Kev retiene ~4.8 GB de los 6 GB de VRAM: con él vivo, Laya no cabe. Nunca en paralelo.
#
#   bash src/matriz/correr_kev.sh
set -u
cd "$(dirname "$0")/../.."
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

PY=.venv/bin/python
OUT=results/crudos
LOG=results/crudos/_log_kev.txt
KEV_DIR="${KEV_DIR:-$HOME/kev-serve}"
SCRATCH="${HERMES_SCRATCH:-$HOME/.hermes/cache/scratch/paso0}"
mkdir -p "$OUT" "$SCRATCH"
: > "$LOG"

echo "===== servidor de Kev =====" | tee -a "$LOG"
if ! curl -s -o /dev/null --max-time 3 http://127.0.0.1:8008/docs; then
  ( cd "$KEV_DIR" && nohup uv run --extra serve python -m kev.serve \
      --run jaredpalmer/kev-0.8b --port 8008 > "$SCRATCH/kev_server.log" 2>&1 & )
  # espera acotada con health-check (no un sleep ciego)
  for i in $(seq 1 60); do
    if curl -s -o /dev/null --max-time 3 http://127.0.0.1:8008/docs; then break; fi
    sleep 5
  done
fi
if ! curl -s -o /dev/null --max-time 5 http://127.0.0.1:8008/docs; then
  echo "!!! el servidor de Kev no respondió en 5 min: se aborta el bloque" | tee -a "$LOG"
  exit 1
fi
echo "servidor listo $(date +%H:%M:%S)" | tee -a "$LOG"
nvidia-smi --query-gpu=memory.used,memory.free --format=csv | tee -a "$LOG"

for ds in typed-decisions sst5 wanli banking77; do
  lim=400; [ "$ds" = "typed-decisions" ] && lim=200
  echo "--- kev × $ds (limite=$lim) $(date +%H:%M:%S)" | tee -a "$LOG"
  $PY src/matriz/medir.py --model kev --dataset "$ds" --limite "$lim" --out "$OUT" 2>&1 \
    | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
done

echo "===== matando el servidor de Kev (libera la VRAM) =====" | tee -a "$LOG"
pkill -f 'ke[v].serve' || true
sleep 4
nvidia-smi --query-gpu=memory.used,memory.free --format=csv | tee -a "$LOG"
echo "===== FIN Kev $(date +%H:%M:%S) =====" | tee -a "$LOG"
