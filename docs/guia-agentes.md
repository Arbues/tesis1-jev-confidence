# Guía de trabajo para agentes (handoff)

> **Nota:** ya existe el **`AGENTS.md` canónico** en la raíz (ese es el que auto-cargan los CLIs de agente).
> Este documento queda como **versión resumida** de handoff. Para un agente **Hermes**, el archivo
> auto-cargado del proyecto es **`.hermes.md`**.

---

## 0. Regla de oro (no negociable)

**Jev NO es JEPA.** Jev (TypeSafe System One) es un **modelo de decisión** que termina la inferencia con un
*readout* de logits y **no genera texto**; JEPA es una familia de *world models*. No tienen relación.
`eje-1-jepa/` y `_descartado/` están **FUERA DE ALCANCE**: no los uses ni propongas subrutas.

Punto de reentrada: `STATE.json` → `README.md` → `.hermes.md` → `paper/00_plan_del_paper.md`.

---

## 1. Objetivo

**Tesis 1, Ruta 1 — Metrología y transferencia del campo `confidence`.** El artefacto: especificación +
librería `jev-conf-metrics` + arnés de conformidad + **matriz de transferencia de umbrales** entre las
definiciones incompatibles de `confidence`, medida sobre modelos de pesos abiertos, con dataset de mediciones
crudas y script regenerador. **Instrumento, no hallazgo.** Documento principal:
`eje-2-jev-opensource/11_ruta1_metrologia_confidence.md`.

---

## 2. Reparto de trabajo entre máquinas

| Máquina | GPU | Qué se hace ahí |
|---|---|---|
| **thinkpad-t440** | **ninguna** | **El PAPER**: redacción, marco teórico, referencias, especificación. No ejecutes inferencia aquí. |
| **Acer Nitro** (WSL2) | **RTX 4050 6 GB** | **El DESARROLLO**: descarga de pesos, inferencia, pipeline, librería, matriz, figuras. |
| **Mac Mini** | memoria unificada | Modelos 4B–9B en 4-bit que no entran en 6 GB. |

**Handoff:** el cómputo produce **artefactos** (JSON/CSV + figuras) con **versión + hash por fila** y los
commitea; el paper los consume. _(Ver §6: el repo se clona en el Nitro.)_

---

## 3. Reglas D1–D5

- **D1** Artefacto, no hallazgo. **D2** Cero anotación/etiquetado humano (usa datasets ya etiquetados).
- **D3** Automatiza todo lo posible. **D4** Cada cifra con su fuente; cada fila *medido aquí* / *auto-reportado*.
- **D5** Costo $0 (Mac Mini + RTX 4050).
- La matemática puede vivir en el **marco teórico**; no tiene que ser el núcleo del resultado.

---

## 4. Git

**Nunca push directo a `main`.** Rama → PR → squash merge. `gh` autenticado (SSH).
`git checkout -b feat/algo && git push -u origin HEAD && gh pr create`.

---

## 5. Estructura

```
README.md · STATE.json · .hermes.md · docs/guia-agentes.md
paper/        00_plan_del_paper.md · 01_marco_teorico.md · 02_referencias.bib
eje-2-jev-opensource/   11_ruta1_metrologia_confidence.md (PRINCIPAL) · 10 · 08 · FUENTES.md
audit/ · contexto/      material de apoyo
eje-1-jepa/ · _descartado/   FUERA DE ALCANCE
src/ · results/         (por crear en el Nitro)
```

---

## 6. Cómo continuar (por dónde)

1. **En el Nitro:** `git clone <repo>` y correr el **paso 0 go/no-go** (Laya 421M + Kev-0.8B, verificar
   `output_tokens = 0`, reproducir un ECE sobre `typed-decisions`). Registrar versión + hash.
2. **Congelar** definiciones, datasets y cobertura objetivo.
3. **Librería + pipeline + matriz** (§4 del plan) → commitear artefactos con hash.
4. **En el t440:** redactar §1–§3 del paper con `paper/01_marco_teorico.md`. Pre-registro con DOI antes de la corrida principal.

---

## 7. Convenciones

Español; docs detallados, chat breve; formato **APA o IEEE** (R.R. 1439-2023-UNI); cero secrets en el repo;
si un enfoque falla **3 veces**, parar y cambiar de perspectiva.
