#!/usr/bin/env bash
# Espera a que termine la corrida del brazo pagado, reintenta los datasets que fallaron
# (el script es idempotente: salta los .jsonl ya escritos) y consolida la matriz combinada.
# Lanzado en background el 20-oct-2026 porque sst5 murió por un reset de conexión (Errno 104).
set -u
cd "$(dirname "$0")/../.." || exit 1
PID=${1:-}
if [ -n "$PID" ]; then
  while kill -0 "$PID" 2>/dev/null; do sleep 30; done
else
  while pgrep -f "correr_pagado\.sh" >/dev/null 2>&1; do sleep 30; done
fi
echo "=== $(date -Is) corrida principal terminada; reintento de los que falten ==="
bash src/matriz/correr_pagado.sh
echo "=== $(date -Is) matriz combinada ==="
bash src/matriz/correr_matriz_pagado.sh
echo "=== $(date -Is) FIN WATCHER ==="
ls -la results/pagado/*.jsonl results/matrix_pagado/ 2>/dev/null
