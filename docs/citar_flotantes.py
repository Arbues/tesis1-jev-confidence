#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bloque C (R3): citar en el texto los flotantes que hoy nadie menciona (28-oct-2026).

Para cada flotante sin `\\ref`, inserta "(Tabla~\\ref{…})" o "(Fig.~\\ref{…})" al final del párrafo que lo
introduce (antes del punto final, o antes de los dos puntos si el párrafo es un anuncio).

Uso:  .venv/bin/python citar_flotantes.py [--dry-run]
"""
from __future__ import annotations

import glob
import re
import sys

PENDIENTES = [
    ("paper/ieee/secciones/01_introduccion.tex", "tab:definiciones", "Tabla"),
    ("paper/ieee/secciones/03_marco_teorico.tex", "tab:campo_confidence", "Tabla"),
    ("paper/ieee/secciones/03_marco_teorico.tex", "tab:cuatro_numeros", "Tabla"),
    ("paper/ieee/secciones/05_resultados.tex", "tab:grupos", "Tabla"),
    ("paper/ieee/secciones/05_resultados.tex", "fig:delta-vs-mapa", "Fig."),
    ("paper/ieee/secciones/05_resultados.tex", "fig:por-par", "Fig."),
    ("paper/ieee/secciones/05_resultados.tex", "tab:brazo-pagado", "Tabla"),
    ("paper/ieee/secciones/05_resultados.tex", "tab:porte-pagado", "Tabla"),
]


def insertar(texto: str, label: str, tipo: str):
    """Devuelve (nuevo_texto, parrafo_antes, parrafo_despues) o (None, motivo, ...)."""
    m = re.search(r"\\label\{%s\}" % re.escape(label), texto)
    if not m:
        return None, "sin label", None
    lab = m.start()
    # ¿dónde empieza el flotante?
    ini_flot = max(texto.rfind("\\begin{table}", 0, lab), texto.rfind("\\begin{figure}", 0, lab))
    if ini_flot < 0:
        return None, "sin \\begin antes del label", None
    # párrafo anterior al flotante: el bloque de texto entre los dos dobles saltos previos
    fin_par = texto.rfind("\n\n", 0, ini_flot)
    ini_par = texto.rfind("\n\n", 0, max(0, fin_par)) if fin_par > 0 else 0
    cand = texto[ini_par:fin_par if fin_par > 0 else ini_flot].rstrip()
    if len(cand.strip("\n")) < 40:
        return None, "párrafo demasiado corto", cand
    if cand.endswith(":"):
        pos = ini_par + len(cand) - 1
    else:
        fin = cand.rfind(".")
        if fin < 0:
            return None, "sin punto final", cand
        pos = ini_par + fin
    ins = f" ({tipo}~\\ref{{{label}}})"
    nuevo = texto[:pos] + ins + texto[pos:]
    despues = texto[ini_par:pos] + ins
    return nuevo, cand.splitlines()[-1][:90], despues.splitlines()[-1][-90:]


def main(argv):
    dry = "--dry-run" in argv
    for ruta, label, tipo in PENDIENTES:
        t = open(ruta, encoding="utf-8").read()
        if f"\\ref{{{label}}}" in t:
            print(f"[ya citado] {label}")
            continue
        nuevo, antes, despues = insertar(t, label, tipo)
        if nuevo is None:
            print(f"[FALLO] {ruta.split('/')[-1]} {label}: {antes}")
            continue
        print(f"[ok] {label}\n     ...{antes}\n     ...{despues}")
        if not dry:
            open(ruta, "w", encoding="utf-8").write(nuevo)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
