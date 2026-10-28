#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bloque A del plan de edición: quitar la negrita enfática de la prosa (28-oct-2026).

Regla (la del informe, verificable):

  · se CONSERVA la negrita dentro de `tabular` y de `quote` (26 + 8: resaltan el subconjunto principal y
    las Proposiciones, convención tipográfica);
  · se CONSERVA la negrita de *run-in head*: al inicio de un párrafo y con el contenido terminado en `.` o `:`
    (forma habitual en IEEE para abrir un bloque);
  · se QUITA todo el resto: énfasis dentro de la frase y en el arranque de los ítems de lista (es la
    `**negrita**` de Markdown que sobrevivió al `.tex`).

Uso:  .venv/bin/python limpiar_negritas.py [--dry-run]
"""
from __future__ import annotations

import glob
import re
import sys

ARCHIVOS = sorted(glob.glob("paper/ieee/secciones/*.tex")) + ["paper/ieee/main.tex"]
PROTEGIDAS = ("tabular", "quote")


def rangos_protegidos(t: str):
    out = []
    for env in PROTEGIDAS:
        for m in re.finditer(r"\\begin\{%s\}.*?\\end\{%s\}" % (env, env), t, re.S):
            out.append((m.start(), m.end()))
    return out


def es_run_in_head(t: str, i: int, contenido: str) -> bool:
    """¿La negrita abre párrafo y termina en `.` o `:`?"""
    prev = t[max(0, i - 200):i]
    if prev.strip() and not re.search(r"(\n[ \t]*\n|\A)[ \t]*$", prev):
        return False
    return contenido.rstrip().endswith((".", ":"))


def limpiar(t: str):
    """Quita las negritas de prosa. Parser con conteo de llaves: soporta \\textbf{\\texttt{x}}."""
    quitadas, conservadas = 0, 0
    while True:
        protegidos = rangos_protegidos(t)
        reemplazos = []
        i = 0
        while True:
            i = t.find("\\textbf{", i)
            if i < 0:
                break
            k = i + len("\\textbf{")
            prof = 1
            j = k
            while j < len(t) and prof:
                if t[j] == "{":
                    prof += 1
                elif t[j] == "}":
                    prof -= 1
                j += 1
            if prof:
                break                      # llaves desbalanceadas: no tocar
            contenido = t[k:j - 1]
            reemplazos.append((i, j, contenido))
            i = j
        if not reemplazos:
            return t, quitadas, conservadas
        cambios = 0
        for i, j, contenido in reversed(reemplazos):
            if any(a <= i < b for a, b in protegidos) or es_run_in_head(t, i, contenido):
                conservadas += 1
                continue
            t = t[:i] + contenido + t[j:]
            quitadas += 1
            cambios += 1
        if cambios == 0:
            return t, quitadas, conservadas


def main(argv):
    dry = "--dry-run" in argv
    total_q = total_c = 0
    for ruta in ARCHIVOS:
        t = open(ruta, encoding="utf-8").read()
        antes = t.count("\\textbf{")
        nuevo, q, c = limpiar(t)
        despues = nuevo.count("\\textbf{")
        total_q += q
        total_c += c
        print(f"{ruta.split('/')[-1]:28s} textbf {antes:3d} -> {despues:3d}   (quitadas {q}, conservadas {c})")
        if not dry:
            open(ruta, "w", encoding="utf-8").write(nuevo)
    print(f"\nTOTAL quitadas {total_q} · conservadas {total_c}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
