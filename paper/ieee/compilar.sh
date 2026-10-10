#!/usr/bin/env bash
# ----------------------------------------------------------------------
#  Compila el paper en formato IEEE (clase IEEEtran).
#  Uso:  ./compilar.sh
#
#  Requiere TeX Live. Si `latexmk` no está, usa la secuencia pdflatex/bibtex.
#  En esta máquina TeX aún NO está instalado: ver README.md de esta carpeta.
# ----------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

if command -v latexmk >/dev/null 2>&1; then
    echo "[compilar] latexmk"
    # -gg = corrida completa, ignorando el estado cacheado: si un intento previo fallo,
    # latexmk guarda ese error y creeria que el PDF ya esta hecho y no recompilaria.
    latexmk -gg -pdf -interaction=nonstopmode -halt-on-error main.tex
    latexmk -c
else
    echo "[compilar] secuencia manual pdflatex + bibtex"
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    bibtex main
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
fi

echo "[compilar] listo: main.pdf"
