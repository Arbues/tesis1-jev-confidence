#!/usr/bin/env bash
# Corrida del BRAZO PAGADO (API de TypeSafe, jev-1.13.0) sobre los 5 datasets etiquetados.
# Extensión declarada posterior al pre-registro. No toca results/crudos ni results/matrix:
# escribe sus propios crudos en results/pagado/ para no alterar los artefactos sellados.
#
# Uso:  bash src/matriz/correr_pagado.sh
# Reanudable: si un .jsonl ya existe, se salta ese dataset.
set -u
cd "$(dirname "$0")/../.." || exit 1
PY=.venv/bin/python
OUT=results/pagado
LOG=$OUT/run.log
mkdir -p "$OUT"

correr () {           # $1=dataset  $2=limite  $3=presupuesto
  local ds=$1 lim=$2 pres=$3
  if ls "$OUT"/*__"$ds".jsonl >/dev/null 2>&1; then
    echo "[skip] $ds ya medido" | tee -a "$LOG"; return 0
  fi
  echo "=== $(date -Is) start $ds (limite=$lim, tope=USD $pres) ===" | tee -a "$LOG"
  $PY src/matriz/medir.py --model typesafe --dataset "$ds" --limite "$lim" \
      --presupuesto-usd "$pres" --out "$OUT" >>"$LOG" 2>&1
  echo "=== $(date -Is) end $ds rc=$? ===" | tee -a "$LOG"
}

correr sst5            1200 0.06
correr typed-decisions  500 0.08
# banking77 y clinc150: cardinalidad alta (77 y 150 opciones por prompt) -> el precio por ítem
# es 4x el de los datasets de 2-5 opciones (medido 20-oct-2026: USD 0.105 y 0.071 por 1.000).
correr banking77       4000 0.55
correr clinc150        4000 0.55
correr wanli           6000 0.15

echo "=== $(date -Is) FIN ===" | tee -a "$LOG"
ls -la "$OUT"/*.jsonl 2>/dev/null | tee -a "$LOG"
