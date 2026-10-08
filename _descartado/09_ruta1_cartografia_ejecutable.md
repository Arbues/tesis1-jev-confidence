# RUTA 1 — Cartografía ejecutable: estado del arte reproducible del carril JEPA world models

Tesis 1 · decisión del 01-oct-2026 · **sustituye al planteamiento de `06_dossier_tesis1.md` §3–§5**
(documento principal vigente del proyecto)

---

## 0. La ruta en una frase

El propósito de Tesis 1 es un **estado del arte reproducible**: una revisión del carril *JEPA world
models* (2025–2026) cuyo anexo es una **tabla de comparación donde cada número re-medible está medido
aquí**, ejecutando los checkpoints liberados en la RTX 4050, y donde todo lo que no se puede re-medir
queda **marcado explícitamente como third-party**.

Es decir: el resultado final no es un hallazgo, es un **artefacto** (documento + tabla + dataset de
mediciones + código que regenera la tabla).

---

## 1. Por qué esta ruta y no un hueco

**1.1 Los huecos se cierran en días.** Entre el 12 y el 30 de septiembre de 2026 cayeron, uno tras otro,
los seis huecos del eje 2 y varios del eje 1 (detalle en `README.md` §7-bis). Varios de los que los
cerraron son estudios **pre-registrados** con DOI: no hay margen de carrera para un estudiante a medio
tiempo.

**1.2 Lección de diseño (permanente):** *el hueco es perecedero, el artefacto no.* Un hallazgo pierde
todo su valor si otro lo publica una semana antes; un harness, un dataset de mediciones crudas, una
bibliografía trazada y una tabla que se regenera con un comando conservan su valor aunque el hallazgo
se publique en otro sitio.

**1.3 Y es defendible académicamente.** Un survey reproducible no es "poca contribución": es
infraestructura citable. El precedente es Guo et al. (2017) — no propuso modelo, midió la calibración
de las redes de la época y se volvió la referencia obligada. Aquí la diferencia es que la tabla no se
copia: **se ejecuta**.

---

## 2. Entregables

| # | Entregable | Por qué vale |
|---|---|---|
| 1 | Documento de survey (taxonomía + evaluación crítica + limitaciones), formato **IEEE o APA** (R.R. 1439-2023-UNI) | El documento en sí |
| 2 | **Tabla de comparación reproducible** + script que la regenera desde cero | Es lo que otros citan y reusan |
| 3 | **Dataset de mediciones propias** (JSON/CSV) con hash de checkpoint, versión de harness y seed por fila | Dato crudo; quien venga después no recalcula |
| 4 | **Figuras generadas por código** (no dibujadas a mano) | Reproducibilidad verificable |
| 5 | **BibTeX + tabla de trazabilidad claim → fuente** (verificado / third-party / no verificado) | Rigor de referencias |
| 6 | **2–3 réplicas independientes** de claims centrales del carril, pre-registradas con DOI | Convierte el survey en contribución técnica |
| 7 | Repositorio público (rama → PR → squash merge) + pre-registro en OSF/Zenodo | El artefacto reutilizable |

---

## 3. Alcance — qué se re-mide y qué NO

### 3.1 Sí se descargan y ejecutan localmente (pesos abiertos, régimen de 6 GB)

| Grupo | Modelos | Origen | Tamaño | Qué se mide |
|---|---|---|---|---|
| Objeto central | **LeWM 15M**, 4 checkpoints (`quentinll/lewm-pusht` · `-cube` · `-tworooms` · `-reacher`) | HF | decenas de MB cada uno | planificación CEM, error de predicción, probes lineales, rango efectivo |
| Baselines de LeWM | **PLDM · LeJEPA · IVL · IQL · GCBC · DINO-WM · DINO-WM-noprop** | Google Drive (según repo de LeWM) | DINO-WM es el pesado (backbone DINOv2); el resto ligero | mismas métricas, solo **inferencia congelada** |
| Generation más reciente | **V-JEPA 2.1 ViT-B/L destilados (80M/300M)** + V-JEPA 2 ViT-L/256 | HF `facebook/vjepa2-*` | ~0.3–1.2 GB | encoder **congelado** + features cacheadas → probes, ordenabilidad |
| Comunitarios | GGUF (`jepacpp/vjepa2-*`, `jepacpp/lewm-pusht-GGUF`) | HF | MB | piloto de protocolo en **CPU**, sin gastar GPU |

Cuota de descarga estimada: **< 5 GB** sin DINO-WM; DINO-WM puede sumar varios GB. Todo cae en disco
local, sin nube y sin costo monetario.

### 3.2 NO se descargan (quedan como third-party published)

V-JEPA 2 ViT-G / ViT-Gigantic (1B–2B) · DINOv3 7B · cualquier modelo cerrado · cualquier checkpoint
que exija formulario de acceso o licencia no comercial sin respuesta.

Cada fila así **entra igual en la tabla**, con su cita, su cifra publicada y una columna de estado
(`third-party`). Esa honestidad de etiquetado es parte del aporte.

---

## 4. Protocolo de medición — las reglas que hacen la tabla citable

| # | Regla | Motivo |
|---|---|---|
| R1 | Todo número propio va con **checkpoint + hash, versión del harness, seed y protocolo de evaluación** | Sin esto, no es reproducible |
| R2 | **Reparar el BatchNorm del proyector** antes de medir cualquier cosa que dependa de la escala | El BN tiene varianza de running ~1e-4: en modo eval la pérdida se infla hasta ~300× y el rango efectivo de 192 salta de 11.9 a 18.6 **sin tocar un peso** (arXiv:2608.10145 + issue #67) |
| R3 | Medir en **bucle abierto con candidatos fijos** (protocolo *no-leak* de ARC-Bench, arXiv:2609.05461) | Medir dentro del bucle de planificación **enmascara** el defecto medido |
| R4 | Una fila entra como *re-medido* solo con **3 seeds**; con menos, se marca *preliminar* | Varianza de la propia métrica |
| R5 | Criterios de inclusión/exclusión del corpus **declarados antes** de buscar | Evita sesgo de selección post-hoc |
| R6 | Toda cifra third-party lleva su advertencia de alcance (prompts, muestras y pipeline no idénticos) | El ecosistema está lleno de comparaciones no controladas |

---

## 5. Reparto de trabajo (regla de esfuerzo vinculante)

**Autor (manual, mínimo absoluto):**
- definir la **taxonomía** y la pregunta de cada eje de la tabla;
- redactar el documento;
- validar visualmente las figuras y las tablas;
- decidir inclusiones/exclusiones del corpus.

**Nada de:** anotación, etiquetado humano, kappa, crowdsourcing, nube, compra de créditos, solicitudes
de acceso que dependan de terceros.

**Agente (automático):**
- búsqueda y parsing del corpus arXiv del carril (ventana fija);
- clonado e instalación de harnesses; descarga de checkpoints;
- corridas de evaluación por entorno y seed (sobre la 4050 local);
- reparación del BatchNorm y chequeo de integridad de medición;
- cómputo de métricas, generación de tablas, figuras y BibTeX;
- redacción del pre-registro.

---

## 6. Riesgos y mitigación

| Riesgo | Prob. | Mitigación |
|---|---|---|
| El harness (`stable-worldmodel`) no instala o rompe | Media | **Paso 0** de medio día como go/no-go. Si falla 3 veces → ruta 3, que no depende de harness de terceros |
| Los baselines de DINO-WM (Google Drive) son inaccesibles | Media | Esa fila queda `third-party`; el núcleo (LeWM + V-JEPA 2.1 ViT-B/L) no depende de eso |
| El asesor lo lee como "poca contribución técnica" | Media | La tabla se regenera con un comando + 2–3 réplicas independientes pre-registradas |
| El corpus del carril crece sin control (docs/mes) | Alta | Ventana cerrada (2025 → 30-sep-2026) y criterios fijados de antemano; el exceso va a un anexo de seguimiento |
| Gastar GPU en reentrenar | — | **Prohibido en ruta 1.** Solo inferencia congelada y features cacheadas |

---

## 7. Lista de exclusión — lo que NO se propone, con motivo

| No hacer | Motivo |
|---|---|
| Construir/caracterizar el diagnóstico *decision-metric alignment* | Ya publicado: arXiv:2608.18746 |
| Auditoría *no-leak* de candidatos fijos como aporte propio | Ya publicado: arXiv:2609.05461 (ARC-Bench) |
| **Barrido de λ como hallazgo central** | Hueco perecedero y "nadie barrió λ" es falso: hay barridos en otros dominios (eb_jepa/CIFAR-10; ChronoJEPA/PEMS08, donde *placement* domina sobre λ) |
| Two-Room por dimensionalidad intrínseca baja | Ya diagnosticado y arreglado: arXiv:2605.09241 (Sub-JEPA) |
| Geometría de ranking vía cabezas auxiliares | Saturado: DA-LeWM, D-JEPA (2609.24749), TD-JEPA (2607.25337) |
| Comparativas con modelos cerrados o de > 1B | Fuera del régimen de 6 GB y sin valor añadido |

---

## 8. Paso 0 — criterio de go/no-go (medio día)

1. Clonar e instalar `le-wm` + `stable-worldmodel` (+ `stable-pretraining`).
2. Cargar el checkpoint `quentinll/lewm-tworooms`.
3. Correr la planificación de ejemplo de extremo a extremo.
4. Registrar versiones, hashes y tiempo por etapa en `STATE.json`.

- **Si [3] pasa** → ruta 1 confirmada; se congela el protocolo del corpus (paso 1 del README §10).
- **Si [3] falla tras 3 intentos** → parar (regla del usuario: no ser terco) y evaluar la ruta 3.

---

## 9. Qué deja Tesis 1 al Taller

- La **tabla de frontera**: qué propiedades del latente predicen la planificación y cuáles no, con
  evidencia propia y no de terceros.
- La **cota de transferencia de umbrales** y la descomposición por componente quedan en las rutas 2 y 3
  (ver `06_dossier_tesis1.md` §4.3–4.5, conservado como especificación de esas rutas).
- Los dos hallazgos de integridad de medición registrados en `README.md` §7-bis (BN sesgado; SIGReg
  ciego al colapso anisotrópico) son material natural del Taller si se quiere un resultado interno.

---

## Fuentes de la ruta 1

**Núcleo re-medible:** arXiv:2603.19312 (LeWM) · `github.com/lucas-maes/le-wm` ·
`github.com/galilai-group/stable-worldmodel` · `quentinll/lewm-{pusht,cube,tworooms,reacher}` ·
arXiv:2603.14482 (V-JEPA 2.1) · arXiv:2506.09985 (V-JEPA 2).

**Protocolos y metrología:** arXiv:2608.18746 (Plan-Real / CEM-stage Spearman) · arXiv:2609.05461
(ARC-Bench, no-leak) · arXiv:2608.10145 (reproducción independiente de LeWM en TwoRoom) · issue #67
de `lucas-maes/le-wm` · arXiv:2605.26379 (identificabilidad LeJEPA, Lean 4) · arXiv:2607.13612 (SIGReg
como energía libre variacional) · Maes et al. (benchmark de robustez `stable-worldmodel`).

**Delta del carril (sep-2026):** arXiv:2609.24749 (D-JEPA) · arXiv:2607.25337 (TD-JEPA) ·
arXiv:2605.09241 (Sub-JEPA) · arXiv:2605.31111 (SD-JEPA) · arXiv:2605.08732 (GC-IDM) ·
arXiv:2606.09311 (FF-JEPA) · arXiv:2606.32026 (AdaJEPA) · arXiv:2604.03208 (HWM).
