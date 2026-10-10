# Versión IEEE del paper (LaTeX)

Aquí vive la versión en **formato IEEE** de la Tesis 1, escrita en LaTeX con la clase
`IEEEtran`. Es la versión que se entrega y se formatea; las fuentes narrativas siguen en
`paper/secciones/*.md`, que es donde se redacta y se revisa.

## Estructura

```
paper/ieee/
├── main.tex                 documento principal (preámbulo, título, resumen, \input)
├── compilar.sh              script de compilación
├── referencias.bib          bibliografía (copia de paper/02_referencias.bib)
├── secciones/               §1–§7 convertidas a LaTeX
└── README.md                este archivo
```

Las figuras se leen de `paper/figures/` (ruta declarada con `\graphicspath`) y se generan,
desde los artefactos medidos, con:

```bash
.venv/bin/python src/figuras_paper.py
```

## Compilar

```bash
./compilar.sh          # produce main.pdf
```

## Instalar TeX (una sola vez)

En esta máquina (ThinkPad T440) **TeX no está instalado**. Dos rutas, ninguna exige
contraseña de administrador si se usa la segunda:

**Ruta A — TeX Live del sistema (necesita `sudo`, lo ejecuta el autor):**

```bash
sudo apt update
sudo apt install -y texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-publishers texlive-bibtex-extra biber latexmk
```

`texlive-publishers` trae la clase `IEEEtran`; `texlive-latex-extra` trae `booktabs` y
`latexmk`.

**Ruta B — TinyTeX, instalación local sin `sudo`:**

```bash
curl -fsSL https://yihui.org/tinytex/install-bin-unix.sh | sh
export PATH="$HOME/.TinyTeX/bin/$(ls "$HOME/.TinyTeX/bin" | head -1):$PATH"
tlmgr install ieeetran booktabs caption xcolor microtype url hyperref enumitem
```

La Ruta B deja TeX en `~/.TinyTeX` y basta con añadir su `bin/` al `PATH`.

## Notas

- La clase por defecto es `conference`. Para el formato de revista, cambiar la primera línea
  por `\documentclass[journal]{IEEEtran}`.
- El idioma de los epígrafes es español (`babel`, opción `spanish`): «Resumen» e «Índice de
  términos» en lugar de «Abstract» e «Index Terms».
