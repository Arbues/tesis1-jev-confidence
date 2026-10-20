#!/usr/bin/env bash
# Matriz COMBINADA: los 23 grupos sellados + los grupos del brazo pagado (Jev por API).
# Escribe en results/matrix_pagado/ y NO toca results/matrix/ (artefactos sellados intactos).
#
# Uso:  bash src/matriz/correr_matriz_pagado.sh
set -eu
cd "$(dirname "$0")/../.." || exit 1
PY=.venv/bin/python
STAGE=results/_stage_pagado
OUT=results/matrix_pagado
mkdir -p "$STAGE" "$OUT"

# 1) escenario con enlaces: crudos sellados + crudos del brazo pagado
rm -f "$STAGE"/*.jsonl
for f in results/crudos/*.jsonl results/pagado/*.jsonl; do
  [ -e "$f" ] || continue
  ln -sf "$(readlink -f "$f")" "$STAGE/$(basename "$f")"
  meta="${f%.jsonl}.meta.json"
  [ -e "$meta" ] && ln -sf "$(readlink -f "$meta")" "$STAGE/$(basename "$meta")"
done
echo "[stage] $(ls "$STAGE"/*.jsonl | wc -l) crudos"

# 2) matriz + informe
# Niveles: `raw` (el principal, el que congela el pre-registro) y `L1` (temperatura, barato).
# `L0` se omite a propósito: el ajuste del prior cuesta ~44 min POR GRUPO (medido 20-oct-2026)
# y `prior_vectorizado` no es bit-idéntico, así que no se usa para artefactos comparables.
$PY src/matriz/matriz.py --crudos "$STAGE" --out "$OUT" --niveles raw,L1
$PY src/matriz/informe_matriz.py --crudos "$STAGE" \
    --matriz "$OUT/matriz_transferencia.csv" --out "$OUT/RESUMEN_MATRIZ_PAGADO.md"

echo "[ok] $OUT/matriz_transferencia.csv"
echo "[ok] $OUT/RESUMEN_MATRIZ_PAGADO.md"
