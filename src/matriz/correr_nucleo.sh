#!/usr/bin/env bash
# Mide el núcleo de la matriz en el Nitro, UN MODELO EN VRAM A LA VEZ.
# Laya (3 checkpoints) + control crudo. El bloque de Kev va aparte (necesita su servidor).
#
#   bash src/matriz/correr_nucleo.sh
#
# Reglas: un modelo a la vez; si el guard de recursos aborta, se para (no se insiste).
set -u
cd "$(dirname "$0")/../.."
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

PY=.venv/bin/python
OUT=results/crudos
LOG=results/crudos/_log_nucleo.txt
mkdir -p "$OUT"
: > "$LOG"

# typed-decisions: 200 casos por config x 4 configs = 800 casos (superset de los 100 del paso 0)
# el resto de datasets: 400 casos
limite_de() { [ "$1" = "typed-decisions" ] && echo 200 || echo 400; }

bloque() {
  local modelo="$1"; shift
  for ds in "$@"; do
    local lim; lim=$(limite_de "$ds")
    echo "--- $modelo × $ds (limite=$lim) $(date +%H:%M:%S)" | tee -a "$LOG"
    $PY src/matriz/medir.py --model laya --subfolder "$modelo" --dataset "$ds" \
        --limite "$lim" --out "$OUT" 2>&1 \
      | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
    if grep -q "ABORTADO" "$LOG"; then
      echo "!!! guard de recursos abortó: PARAR TODO" | tee -a "$LOG"; exit 1
    fi
  done
}

echo "===== BLOQUE 1: Laya (3 checkpoints) =====" | tee -a "$LOG"
for sub in none typed-decisions multilingual; do
  bloque "$sub" typed-decisions sst5 wanli banking77 clinc150
done

echo "===== BLOQUE 2: control crudo (Qwen3.5-0.8B-Base) =====" | tee -a "$LOG"
for ds in typed-decisions sst5 wanli banking77 clinc150; do
  lim=$(limite_de "$ds")
  echo "--- raw × $ds (limite=$lim) $(date +%H:%M:%S)" | tee -a "$LOG"
  $PY src/matriz/medir.py --model raw --model-id Qwen/Qwen3.5-0.8B-Base --dataset "$ds" \
      --limite "$lim" --out "$OUT" 2>&1 \
    | grep -E "recursos\]|filas=|escrito|ABORTADO|Error|error" | tee -a "$LOG"
done

echo "===== FIN $(date +%H:%M:%S) =====" | tee -a "$LOG"
echo "crudos:"; ls -la "$OUT"/*.jsonl | awk '{print "  "$5" "$9}'
