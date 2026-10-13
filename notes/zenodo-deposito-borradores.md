> **USADO Y CERRADO (13-oct-2026).** Los metadatos de §A y §B se aplicaron: el depósito automático del software
> y el preprint están publicados (DOIs `10.5281/zenodo.23330647` y `10.5281/zenodo.23329431`). Se conserva como
> plantilla para depósitos futuros; la interfaz real de Zenodo está en `notes/zenodo-publicar-guia-literal.md`.
# Borradores de depósito en Zenodo (12-oct-2026)

Dos depósitos independientes. El **A** es automático (GitHub→Zenodo, ya habilitado por el autor); el **B**
se sube a mano. Todo lo de aquí se copia/pega en el formulario de Zenodo; nada de esto lleva secretos.

---

## A. Depósito automático del release (código + artefactos + paper)

Se dispara solo al publicar el Release `v1.0.0` en `Arbues/tesis1-jev-confidence`. No hay que crear nada en
Zenodo: el depósito aparece en *Upload → GitHub*.

| Campo del formulario | Valor |
|---|---|
| Upload type | `Software` |
| Title | Metrología y transferencia del campo `confidence` en modelos de decisión de pesos abiertos tipo Jev — instrumento v1.0.0 |
| Creators | Pérez Villegas, Arbués Enrique — ORCID `0009-0004-7605-6569` — FC-UNI, Lima, Perú |
| Description | Instrumento de medición (librería + especificación formal + arnés de conformidad) y matriz de transferencia de umbrales entre las definiciones incompatibles del campo `confidence`, medida sobre 65.185 decisiones de modelos de pesos abiertos (Laya, Kev y control crudo). Incluye el dataset de mediciones crudas con `row_hash` por fila, las 8 figuras y la versión IEEE del paper. |
| Version | `1.0.0` |
| Language | Spanish |
| License | Apache-2.0 (código); los textos y figuras del paper son CC-BY-4.0 |
| Keywords | `confidence calibration`, `decision models`, `Jev`, `TypeSafe`, `threshold transfer`, `open weights`, `metrology` |
| Related identifiers | `is supplemented by` → `10.5281/zenodo.23266795` (pre-registro del método) · `is described by` → arXiv del paper cuando exista |
| Contributors | (opcional) asesor de tesis, si el autor quiere |

**Al terminar:** copiar el **DOI de versión** y el **DOI de concepto** que devuelve Zenodo y pegarlos en
`CITATION.cff` (`identifiers`) y en `README.md`.

---

## B. Depósito manual del preprint (paper, `publication` + `preprint`)

Se hace a mano porque no cuelga de un release. Es la vía de reservar el texto **sin esperar al endosso de
arXiv** (decisión del autor, 12-oct-2026).

| Campo del formulario | Valor |
|---|---|
| Upload type | `Publication` → `Preprint` |
| Title | Metrología y transferencia del campo `confidence` en modelos de decisión de pesos abiertos tipo Jev |
| Creators | Pérez Villegas, Arbués Enrique — ORCID `0009-0004-7605-6569` — FC-UNI, Lima, Perú |
| Description | (el resumen del paper, §Resumen; en Zenodo se pega como texto, sin caracteres raros: **evitar tildes problemáticas** si el formulario las rechaza) |
| Version | `1.0` |
| Language | Spanish |
| License | CC-BY-4.0 |
| Keywords | igual que el depósito A |
| Related identifiers | `is supplemented by` → DOI del depósito A (el instrumento) · `is previous version of` → arXiv (cuando exista) · `is supplemented by` → `10.5281/zenodo.23266795` |
| File | `paper/ieee/main.pdf` (11 páginas) — Zenodo **no exige inglés** |

**Notas de honestidad que van en la descripción** (y que no deben omitirse):
1. El instrumento y las mediciones están publicados por separado (depósito A) y el dataset crudo es verificable.
2. El contador `output_tokens` de la **API de pago** de TypeSafe no está medido todavía (ver `docs/erratas_especificacion.md` E4).
3. Existe una **quinta definición** de `confidence` (la que TypeSafe devuelve en `score`) declarada en E5.

**Después:** versión en inglés → `paper/en/` (N5) → arXiv, una vez concedido el endosso.

---

## C. Software Heritage (después del tag)

`Save Code Now` → `https://github.com/Arbues/tesis1-jev-confidence` → guardar el **SWHID** del tag en
`CITATION.cff` (`identifiers: type: swh`). Sobre un repositorio de GitHub ya conocido, la visita suele
completarse en horas; la fecha del SWHID es la del **commit**, no la de la visita.
