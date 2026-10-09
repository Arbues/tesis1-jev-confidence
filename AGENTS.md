# AGENTS.md — guía para agentes que trabajen en este repositorio

> **Léelo completo antes de tocar nada.** Este repo es la **Tesis 1** de Arbués Enrique Pérez V.
> (FC-UNI, Ciencia de la Computación). Punto de reentrada rápido: `STATE.json` → `README.md` → `.hermes.md`
> → `paper/00_plan_del_paper.md`.

---

## 0. Regla de oro (no negociable)

**Jev NO es JEPA.** Jev (TypeSafe System One) es un **modelo de decisión** que termina la inferencia con un
*readout* de logits y **no genera texto**. JEPA es una familia de *world models*. **No tienen ninguna
relación.** Todo el material de `eje-1-jepa/` y `_descartado/` está **FUERA DE ALCANCE**: no lo uses, no lo
evalúes, no propongas subrutas de ahí. Si algo te hace dudar del eje, **pregunta antes de asumir**.

---

## 1. Objetivo

**Tesis 1, Ruta 1 — Metrología y transferencia del campo `confidence`.** El artefacto: especificación +
librería `jev-conf-metrics` + arnés de conformidad + **matriz de transferencia de umbrales** entre las
definiciones incompatibles de `confidence`, medida sobre modelos de pesos abiertos, con dataset de mediciones
crudas y script regenerador. **Instrumento, no hallazgo.** Documento principal:
`eje-2-jev-opensource/11_ruta1_metrologia_confidence.md`.

---

## 2. Estructura del repo y REGLA DE ORDEN (evitar el desorden en la raíz)

> **La raíz es solo para archivos de entrada/configuración** (`README.md`, `STATE.json`, `.hermes.md`,
> `AGENTS.md`, `.gitignore`, y las carpetas). **Todo lo nuevo va a su carpeta.** No dejes artefactos sueltos
> en la raíz.

```
.
├─ README.md · STATE.json · .hermes.md · AGENTS.md · .gitignore   <- entrada (no meter más aquí)
├─ paper/               EL PAPER (texto y figuras)
│   ├─ 00_plan_del_paper.md · 01_marco_teorico.md · 02_referencias.bib
│   ├─ figures/         figuras del paper (generadas)
│   └─ tables/          tablas del paper (generadas)
├─ src/                 CÓDIGO (se trabaja en el Acer Nitro)
│   └─ jev_conf_metrics/  la librería
├─ results/             ARTEFACTOS de medición (con versión + hash por fila)
│   ├─ raw/             mediciones crudas (jsonl/csv)
│   └─ matrix/          la matriz de transferencia
├─ data/                datasets descargados (NO se versionan los pesados; usa .gitignore)
├─ notes/               apuntes, borradores, lluvia de ideas (aquí sí, suelto está bien)
├─ docs/                guías (p. ej. guia-agentes.md)
├─ eje-2-jev-opensource/  eje ACTIVO (docs del tema)
├─ audit/ · contexto/   material de apoyo
├─ downloads/           PDFs y descargas puntuales
└─ eje-1-jepa/ · _descartado/   FUERA DE ALCANCE (histórico; no tocar)
```

**Regla simple para decidir dónde va algo:**
- ¿Código? → `src/`
- ¿Un resultado/tabla/figura de medición? → `results/` (o `paper/figures`, `paper/tables` si es para el paper)
- ¿Texto del paper o del marco teórico? → `paper/`
- ¿Una idea suelta o un borrador? → `notes/`
- ¿Un dataset o pesos? → `data/` (o `models/`), **y no se versionan** (ver `.gitignore`)

No hace falta que sea rígido: si dudas, mete una subcarpeta nueva con nombre claro **dentro** de la carpeta
que corresponda, no en la raíz.

---

## 3. Reparto de trabajo entre máquinas (importante)

| Máquina | GPU | Qué se hace ahí |
|---|---|---|
| **thinkpad-t440** | **ninguna** (solo iGPU Intel) | **El PAPER**: redacción, marco teórico, referencias, especificación, revisión de fuentes. **No ejecutes inferencia aquí.** |
| **Acer Nitro** (Windows + WSL2) con **RTX 4050 Laptop 6 GB** | sí | **El DESARROLLO/computo**: descarga de pesos, inferencia, pipeline, librería (`src/`), matriz y figuras (`results/`). |
| **Mac Mini** (Apple Silicon) | memoria unificada | Modelos 4B–9B en 4-bit que no entran en 6 GB. |

**Contrato de handoff:** el cómputo (Nitro/Mac) **produce artefactos** (JSON/CSV de mediciones crudas,
matrices, figuras) con **versión de modelo + hash por fila**, y los commitea a este repo. El paper los
consume. Nunca dependas de datos generados en una sola máquina que no estén en el repo.

---

## 4. Reglas de diseño del autor (vinculantes — D1–D5)

- **D1 — Artefacto, no hallazgo.** El resultado es un **instrumento, dataset de mediciones crudas,
  especificación o tabla regenerable con un comando**. Debe seguir valiendo aunque otro publique el hallazgo.
- **D2 — Trabajo manual del autor al mínimo.** **Cero anotación, cero etiquetado humano, cero crowdsourcing,
  cero kappa.** Usa **datasets ya etiquetados** (typed-decisions, WANLI, Banking77, CLINC150, MedHallu, …).
- **D3 — Máxima automatización.** Descarga de pesos, corridas, métricas, tablas, figuras, BibTeX, librería y
  pre-registro los hace el agente.
- **D4 — Trazabilidad.** Cada cifra con su fuente; cada fila declara si fue **medida aquí** o **auto-reportada**.
- **D5 — Costo $0.** Mac Mini + RTX 4050. Nada de nube ni GPUs de 80 GB.

> Nota del autor (04-oct-2026): la matemática **no** tiene que ser el núcleo del resultado; basta con que
> esté en el **marco teórico** del paper. Tesis 1 puede ser metrología/instrumento.

---

## 5. Git

- **Nunca push directo a `main`.** Todo cambio va a una **rama separada → Pull Request → squash merge**.
- `gh` CLI está autenticado (SSH). Ejemplo: `git checkout -b feat/algo && git push -u origin HEAD && gh pr create`.
- Commits en español, mensajes claros.
- **Visibilidad:** el repo es **privado** por ahora; se pasa a **público** cuando existan resultados o al
  menos el MVP del framework.

---

## 6. Estado actual y cómo continuar

1. **Ruta elegida**: Ruta 1. Hecho.
2. **Paso 0 go/no-go**: ✅ **HECHO el 08-oct-2026 en el Acer Nitro → GO.** Laya (3 checkpoints) y Kev-0.8B
   sobre las 2.000 decisiones de `typed-decisions`; `output_tokens = 0` verificado; las 5 métricas publicadas
   de Laya reproducidas con |Δ| ≤ 0.003. Informe: `results/paso0_informe.md`; crudos en `results/raw/`.
   El pipeline real vive en `src/paso0_go_no_go.py` (`--model laya|kev|raw`).
3. **Congelado** (04-oct-2026): definiciones, datasets y cobertura objetivo → `paper/00_plan_del_paper.md` §10.
4. **Especificación formal**: ✅ `paper/03_especificacion_confidence.md` (DEF-1..DEF-8, Proposiciones 1–3).

### Pendiente, en orden

| # | Qué falta | Quién | Nota |
|---|---|---|---|
| 1 | **Librería `jev-conf-metrics` + tests de conformidad** — extraer lo ya validado en `src/paso0_go_no_go.py` | agente (Nitro) | lo siguiente |
| 2 | **Pipeline completo**: más modelos (Nimble, SemIf, Jeff-1, jev-lite, tinyjev; los 4B–9B en el Mac Mini) y más datasets (kev-suites, Banking77, CLINC150, SST-5, WANLI) | agente (Nitro/Mac) | |
| 3 | **Matriz de transferencia de umbrales** → `results/matrix/` + figura *heatmap* | agente (Nitro) | es el entregable central |
| 4 | **Pre-registro con DOI** | **autor** (OSF/Zenodo) | **va ANTES de la corrida principal (paso 3), no al final**; es lo único que no puede hacer el agente. No es urgente hoy |
| 5 | **Paper**: §4 Método, §5 Resultados, §6 Discusión, §7 Conclusión (§1–§3 son borrador) + pulir citas a APA/IEEE | autor + agente | depende de la matriz |

**Los resultados del paso 0 NO son el resultado de la tesis**: son el go/no-go y la línea base. El entregable
central (la matriz) todavía no existe.

### Entorno (trampa conocida)

El `torch` que instala PyPI es **cu130** y el driver del Nitro es 556.19 (**CUDA 12.5**) → hay que instalar
`torch==2.14.1+cu126` desde `https://download.pytorch.org/whl/cu126` o la GPU no arranca. Kev-0.8B no se carga
con `transformers`: se sirve desde su repo y el script le habla por HTTP.

---

## 7. Convenciones

- **Idioma:** español (paper y docs). Los `.md` deben ser **detallados y bien estructurados**; los mensajes de
  chat, **breves**.
- Formato de tesis: **APA o IEEE** (R.R. 1439-2023-UNI).
- Cero contraseñas o secrets en el repo. En docs, solo placeholders.
- Si un enfoque falla **3 veces**: parar y cambiar de perspectiva.
