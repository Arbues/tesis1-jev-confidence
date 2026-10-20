#!/usr/bin/env bash
# Matriz COMBINADA en paralelo: parte los grupos (modelo × dataset) entre N procesos.
#
# Por qué: la matriz es un bucle independiente por grupo y el bootstrap es lo que domina.
# El t440 tiene 4 CPU lógicas pero **2 núcleos físicos**: el techo práctico es ~1,8×, no 4×.
# Para 4 hilos usar --jobs 2; con 3+ se compite por los mismos núcleos y empeora.
#
# Uso:  bash src/matriz/correr_matriz_paralela.sh [jobs]
# Salida: results/matrix_pagado/matriz_transferencia.csv (idéntica a la versión serie, mismo orden)
set -eu
JOBS=${1:-2}
cd "$(dirname "$0")/../.." || exit 1
PY=.venv/bin/python
STAGE=results/_stage_pagado
OUT=results/matrix_pagado
PARTES=$OUT/partes
NIVELES=raw,L1          # L0 fuera: ~44 min por grupo (ver correr_matriz_pagado.sh)
mkdir -p "$STAGE" "$OUT"
rm -rf "$PARTES"; mkdir -p "$PARTES"

# 1) escenario con enlaces: crudos sellados + crudos del brazo pagado
rm -f "$STAGE"/*.jsonl
for f in results/crudos/*.jsonl results/pagado/*.jsonl; do
  [ -e "$f" ] || continue
  ln -sf "$(readlink -f "$f")" "$STAGE/$(basename "$f")"
  meta="${f%.jsonl}.meta.json"
  [ -e "$meta" ] && ln -sf "$(readlink -f "$meta")" "$STAGE/$(basename "$meta")"
done
echo "[stage] $(ls "$STAGE"/*.jsonl | wc -l) crudos"

# 2) lista de grupos (modelo|dataset) desde los .meta.json, ordenada para ser determinista
$PY - "$STAGE" <<'PY' > "$PARTES/grupos.txt"
import glob, json, sys
vistos = set()
for p in glob.glob(sys.argv[1] + "/*.meta.json"):
    m = json.load(open(p, encoding="utf-8"))
    vistos.add((m["modelo"], m["dataset"]))
for modelo, dataset in sorted(vistos):
    print(f"{modelo}|{dataset}")
PY
echo "[grupos] $(wc -l < "$PARTES/grupos.txt")"

# 3) un proceso por grupo, como máximo $JOBS a la vez (nombre de carpeta = grupo saneado)
correr_grupo () {
  local grupo=$1
  local nombre
  nombre=$(printf '%s' "$grupo" | tr '/|' '__')
  local dir="$PARTES/$nombre"
  mkdir -p "$dir"
  if $PY src/matriz/matriz.py --crudos "$STAGE" --out "$dir" --niveles "$NIVELES" \
      --solo "$grupo" >"$dir/log.txt" 2>&1; then
    echo "[ok] $grupo"
  else
    echo "[fallo] $grupo (ver $dir/log.txt)"
    return 1
  fi
}
export -f correr_grupo
export PY STAGE NIVELES PARTES
xargs -a "$PARTES/grupos.txt" -P "$JOBS" -I{} bash -c 'correr_grupo "{}"'

# 4) fusionar los CSV parciales en orden determinista y RECALCULAR el FDR global
$PY src/matriz/fusionar_matriz_paralela.py "$PARTES" "$OUT/matriz_transferencia.csv"

# 5) informe
$PY src/matriz/informe_matriz.py --crudos "$STAGE" \
    --matriz "$OUT/matriz_transferencia.csv" --out "$OUT/RESUMEN_MATRIZ_PAGADO.md"

echo "[ok] $OUT/matriz_transferencia.csv"
echo "[ok] $OUT/RESUMEN_MATRIZ_PAGADO.md"
