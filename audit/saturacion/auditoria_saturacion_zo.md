# Auditoría de saturación: Optimización de Orden Cero (ZO) en Deep Learning
**Fecha de consulta:** 19-sep-2026 · **Fuentes:** OpenAlex REST API, arXiv API (abs:), Semantic Scholar Graph API, web search
**Paper auditado:** arXiv:2605.15622 — *Position: Zeroth-Order Optimization in Deep Learning Is Underexplored, Not Underpowered* (Sijia Liu et al., ICML 2026 Position Paper Track, **Spotlight**)

---

## 1. Conteo de papers por año

### OpenAlex (`title_and_abstract.search`)
| consulta | 2022 | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|---|
| `"zeroth-order optimization"` | 118 | 159 | 186 | 304 | **427** |
| `"zeroth-order"` (cualquier contexto) | 461 | 507 | 521 | 680 | **1217** |
| ZO ∩ (LLM ∨ deep learning ∨ fine-tuning) | 1 | 8 | 30 | 65 | **117** |

### arXiv (`abs:` + rango `submittedDate`)
| consulta | 2023 | 2024 | 2025 | 2026* |
|---|---|---|---|---|
| `abs:"zeroth-order"` | 118 | 148 | 201 | **235** |
| `abs:"zeroth-order optimization"` | 19 | 27 | 52 | 41 |
| `abs:"zeroth-order"` ∧ `abs:"fine-tuning"` | 5 | 21 | 42 | 39 |
| `abs:"zeroth-order"` ∧ `abs:"large language"` | 5 | 20 | 29 | 34 |

\* 2026 está **parcial** (hasta 19-sep = 71.8 % del año). Anualizado:
- OpenAlex `"zeroth-order optimization"`: **≈595** (ratio 1.96× vs 2025)
- OpenAlex ZO ∩ LLM/DL/FT: **≈163** (ratio 2.51× vs 2025)
- arXiv `abs:"zeroth-order"`: **≈327** (ratio 1.63× vs 2025)
- arXiv ZO ∧ fine-tuning: **≈54** (ratio 1.29× vs 2025)

**Lectura:** crecimiento sostenido y acelerado desde 2022; el subconjunto LLM es el que más crece.
La cifra ZO∩(LLM/DL/FT) de OpenAlex es un **piso conservador** (la búsqueda booleana de OpenAlex es difusa y subcuenta).

---

## 2. Papers clave (fundacionales vs 2026)

### Fundacionales
| año | título | id |
|---|---|---|
| 2022 | Black-Box Tuning for Language-Model-as-a-Service | arXiv:2201.03514 |
| 2023 | **MeZO** — Fine-Tuning Language Models with Just Forward Passes | arXiv:2305.17333 |
| 2023 | DeepZero: Scaling up Zeroth-Order Optimization for Deep Model Training | arXiv:2310.02025 |
| 2023 | FedKSeed — Federated Full-Parameter Tuning … under 18 Kilobytes | arXiv:2312.06353 |
| 2024 | **ZO-Bench** — Revisiting ZO Optimization for Memory-Efficient LLM FT | arXiv:2402.11592 |
| 2024 | HiZOO — Hessian Informed Zeroth-Order Optimizer | arXiv:2402.15173 |
| 2025 | TeZO — Low-Rankness on the Temporal Dimension | arXiv:2501.19057 |
| 2025 | Unraveling ZO through Low-Dimensional Structured Perturbations | arXiv:2501.19099 |
| 2025 | Harmony in Divergence (DiZO) | arXiv:2502.03304 |
| 2025 | Zeroth-Order Optimization Finds Flat Minima (NeurIPS'25) | arXiv:2506.05454 |
| 2025 | LOREN — Low-Rank Curvature for ZO in LLM FT (AAAI'26) | arXiv:2511.07971 |

### 2026
| título | id | call-to-action que cubre |
|---|---|---|
| **Position: ZO in DL Is Underexplored, Not Underpowered** | arXiv:2605.15622 | — (el paper auditado) |
| ZO-Muon — Powering Up ZO Training via Subspace Gradient Orthogonalization | arXiv:2602.17155 | **A2 (subespacio/espectral)** — del mismo grupo |
| Hierarchical Zero-Order Optimization for DNNs | arXiv:2602.10607 | — |
| AdaEvolve: Adaptive LLM-Driven ZO | arXiv:2602.20133 | A5 |
| Universally Empowering ZO via Adaptive Layer-wise Sampling | arXiv:2604.18264 | **A4 (infra: latencia de perturbación = 40 %)** |
| Learning Dynamics of ZO: A Kernel Perspective | arXiv:2605.03373 | teoría (P2) |
| ZeNO — Gradient-Free Noise Optimization for Reward Alignment | arXiv:2605.11347 | A5 |
| ZO-Act — One-Shot Activation-Informed Low-Rank Subspaces | arXiv:2607.01125 | A2 |
| SubZero+ — Efficient ZO LLM FT via Large Learning Rates | arXiv:2608.15665 | A2 (cita al position paper) |
| GRZO — Group-Relative ZO for LLM Fine-Tuning | S2:13afab16… | A2/varianza |
| Dominant-Layer ZO | S2:968e69e6… | A2 |
| CurvZO, AR1-ZO, RoZO, MaZO, Hi-ZFO, MpSub, AGZO, FZOO… | varios | A2/varianza |

---

## 3. ¿Crece o se estanca? ¿Siguen abiertos los claims?

**Crece fuerte** (~2× anualizado). No hay señal de estancamiento.

Estado de cada *call to action* (A1–A5):

| call | estado | evidencia |
|---|---|---|
| **A2 · subespacio/espectral (S-RGE)** | **CUBIERTO / SATURADO** | El propio position paper admite "several recent works have explored" (Chen'25, Yu'25, Nozawa'25, Gong&Li'25, Kozak'23, Lang'26a). Su propio follow-up ZO-Muon (2602.17155) lo implementa. Además: TeZO, SubZero+, ZO-Act, LOREN, ZO-Muon, GRZO, CurvZO, AR1-ZO… |
| **A4 · infra ZO-native** | **PARCIAL** | 2604.18264 diagnostica el cuello de botella de latencia (40 %) y lo ataca con sampling por capas; DistZO2 (2025) hace ZO distribuido. **No existe** un stack ZO-native real sobre vLLM con pipeline sin burbujas. Abierto pero requiere perfil de *systems*. |
| **A5 · ampliar frontera** | **PARCIAL** | ZeNO (2605.11347), AdaEvolve (2602.20133), ZO en cuántica, ZO en continual learning (2 papers), ZO + ASR (ZO-ASR). Bastante hueco en dominios no-LLM y en RLHF. |
| **A1 · evaluación des-obfuscada** | **ABIERTO** | ZO-Bench (2024) es, según el propio position paper, **el único** trabajo que incluye el baseline de gradiente directo (forward-gradient). No hay paper 2026 dedicado a protocolos des-obfuscados (presupuesto de queries fijo, con/sin task alignment, baseline DD). |
| **A3 · estimadores generativos** | **ABIERTO (casi vacío)** | Solo adyacentes: ZO-Finetuner (2025, política de sampling aprendida), "Learning Sampling Policy to Achieve Fewer Queries" (2024). **Ningún** trabajo usa modelos de difusión / denoisers como estimadores de gradiente ZO. |

---

## 4. Veredicto de saturación: **6 / 10**

**Saturado en la sub-línea dominante, abierto en los bordes.**
El position paper es parcialmente auto-indulgente: lo firma el grupo (Sijia Liu, Yihua Zhang, Yancheng Huang…) que posee varios de los métodos que cita, y su Tabla 1 muestra un campo densamente poblado —10 trabajos representativos de ICML'25/NeurIPS'25/ICLR'26— no un campo vacío. Llamar "underexplored" a un área que produce >400 papers en 8.5 meses es retórica de *agenda-setting*, no un diagnóstico descriptivo. Lo que realmente está poco explorado son 3 esquinas concretas (A1, A3, A4), no "ZO en deep learning".

---

## 5. Plan de 3 etapas para pregrado con RTX 4050 6 GB + APIs

**Etapa 1 — Tesis 1: auditoría empírica des-obfuscada de ZO (implementa A1).**
Replicar MeZO, HiZOO/DiZO, un método de subespacio (TeZO o SubZero-style low-rank), FZOO y el baseline de gradiente directo (JVP) + referencia FO-LoRA, sobre RoBERTa-large (355 M), OPT-1.3B y un modelo 4-bit (Gemma-2-2B / Qwen2.5-1.5B) en SST-2, RTE, WiC, COPA. Presupuesto de queries fijo y variable (q=1…512); con y sin task alignment. Cabe en 6 GB (MeZO no guarda estados de optimizador; 1.3B en bf16 ≈ 2.6 GB). Aporta: ranking de métodos sin el confounder de alignment + costo real por query. Nadie lo ha hecho desde ZO-Bench 2024.

**Etapa 2 — Paper 2: estimador aprendido/generativo (implementa A3, versión liviana).**
Entrenar una política de perturbación o un denoiser pequeño (MLP/difusión diminuta sobre features baratas: norma de activaciones, capa, paso) que transforme ruido ZO en direcciones de descenso mejores. Entrenar una vez por modelo, reusar entre tareas (línea ZO-Finetuner). Entrenable en 6 GB porque el modelo base está congelado y solo se aprende el estimador.

**Etapa 3 — Paper 3: ZO-native + frontera de aplicación.**
(a) *Sistemas:* amortizar la perturbación reutilizándola entre micro-batches y medir throughput/latencia vs el cuello de botella del 40 % (línea 2604.18264) — publicable como *systems/empirical* sin GPU grande. O (b) *Aplicación:* alineación black-box vía APIs de LLM (ZO sobre prompts/salidas con solo acceso de inferencia), o ZO + cuantización, o ZO para continual learning sin olvido.

**Riesgo a evitar:** no competir en "+1.5 % en SST-2 con una variante de subespacio más" — esa carrera está saturada.

---

## Archivos
- `/home/arbues/paper-tesis1/04_auditoria_saturacion_zo.md` (este archivo)
- `/home/arbues/paper-tesis1/arxiv_counts.json` (conteos crudos arXiv)
