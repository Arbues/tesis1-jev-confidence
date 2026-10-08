# Ruta de aprendizaje: de cero a entender el paper de decision-metric alignment

Para Arbués · 19-sep-2026 · ordenada por dependencias reales, no por temario de curso

---

## Cómo usar esto

Cada nivel tiene: **qué aprender**, **por qué importa para el paper** y **cómo saber que lo dominas**.
No saltes niveles: la matemática del nivel 1 y 2 es la que hace que el nivel 7 (la teoría del Taller) sea
entendible en vez de mágica.

Los **diagramas de arquitectura** están en el archivo visual aparte — ábrelo en el navegador.

---

## Nivel 0 — Herramientas (1–2 semanas)

**Qué aprender:** Python (clases, decoradores, typing), NumPy (broadcasting, `einsum`), PyTorch
(tensores, `autograd`, `nn.Module`, `DataLoader`), Git.

**Por qué:** todo el paper es PyTorch. `stable-worldmodel` y `le-wm` son repos de PyTorch con Hydra.

**Cómo saber que lo dominas:** puedes escribir desde cero un MLP con `nn.Module`, entrenarlo, y
explicar qué hace `.backward()`.

**Recursos:** Karpathy, *Neural Networks: Zero to Hero* (video 1–2). Documentación oficial de PyTorch.

---

## Nivel 1 — La matemática que el paper realmente usa (3–4 semanas)

Este es el nivel que decide si el Taller te resulta posible.

### 1a. Álgebra lineal

| Concepto | Por qué está en el paper |
|---|---|
| SVD, autovalores/autovectores | El latente vive en R^192; la "estructura métrica" es la geometría de ese espacio |
| **Norma espectral y rango bajo** | Cui et al. demuestran que el objetivo JEPA ≡ **factorización de bajo rango** de una matriz de co-ocurrencia |
| Proyecciones ortogonales | El proyector del encoder es un MLP que mapea a un espacio nuevo; SIGReg usa **1024 proyecciones aleatorias** |
| Norma L1 vs L2 | El coste de planificación es una distancia L1/L2 al latente objetivo — **la elección de norma ES el problema** |

**Cómo saber que lo dominas:** puedes explicar por qué cambiar la norma del coste cambia qué plan gana.

**Recursos:** 3Blue1Brown, *Essence of Linear Algebra* (visual, empieza aquí). MIT 18.06 (Strang).
Trefethen & Bau, *Numerical Linear Algebra* (para el espectro).

### 1b. Probabilidad y estadística

| Concepto | Por qué está en el paper |
|---|---|
| **Gaussiana multivariada**, covarianza | SIGReg fuerza latentes gaussianos; el teorema de LeJEPA exige gaussiana y es un "si y solo si" |
| Estacionariedad, ruido aditivo | Segunda condición del teorema de identificabilidad |
| **Correlación de rangos: Spearman ρ, Kendall τ** | Son las métricas del coeficiente de alineación de Tesis 1 |
| Bootstrap, intervalos de confianza | Para reportar la alineación con incertidumbre |
| Test de hipótesis | Pre-registro y reglas de decisión |

**Cómo saber que lo dominas:** puedes derivar la densidad de una gaussiana multivariada y explicar
qué significa "isotrópica" en el contexto de SIGReg.

**Recursos:** Blitzstein, *Stat 110* (Harvard, en YouTube). Bishop, *PRML*, cap. 2.

### 1c. Optimización

Gradiente descendente, Adam, no-convexidad, búsqueda por bisección (LeWM lo usa: λ se optimiza con
bisección porque es el único hiperparámetro efectivo).

**Recursos:** Boyd, *Convex Optimization* (cap. 1–5), Goodfellow cap. 8.

---

## Nivel 2 — Redes neuronales (2–3 semanas)

Backpropagation, funciones de activación, capas, inicialización, normalización (**BatchNorm**,
**LayerNorm** — crítico: el LayerNorm final del ViT impide optimizar el anti-colapso, y por eso LeWM
añade un proyector con BatchNorm), dropout, overfitting.

**Cómo saber que lo dominas:** puedes explicar por qué un LayerNorm al final del encoder rompería
el objetivo de SIGReg.

**Recursos:** Karpathy, *Zero to Hero* completo. Goodfellow, *Deep Learning*, cap. 6–8.

---

## Nivel 3 — Transformers y ViT (3 semanas)

| Concepto | Dónde aparece |
|---|---|
| Atención: Q, K, V, softmax, multi-head | El predictor de LeWM: 6 capas, 16 cabezas |
| **Enmascaramiento causal** | El predictor es autoregresivo con máscara causal temporal: no puede ver el futuro |
| Patch embedding, [CLS] token | El encoder ViT-tiny: patch 14, y `z_t` es el **[CLS] de la última capa** |
| Positional embeddings | Necesarios para la estructura espacial |
| **AdaLN** (Adaptive LayerNorm) | La acción entra al predictor por AdaLN, con parámetros **inicializados en cero** para que el condicionamiento por acción crezca progresivamente |

**Cómo saber que lo dominas:** puedes dibujar de memoria el flujo de un bloque transformer y
explicar cómo AdaLN inyecta una acción externa.

**Recursos:** *Attention Is All You Need*. *An Image is Worth 16×16 Words* (ViT). Karpathy,
*Let's build GPT*. *DiT* (Peebles & Xie) para AdaLN.

---

## Nivel 4 — Self-supervised learning y el problema del colapso (3–4 semanas)

**Este es el nivel más importante para el paper.** Todo JEPA es una respuesta al problema del colapso.

| Concepto | Por qué |
|---|---|
| Predecir vs contrastar | Las dos familias de SSL |
| **InfoNCE / SimCLR** | Contrastivo: usa negativos. JEPA **no** los usa |
| **BYOL / SimSiam** | Sin negativos → riesgo de colapso; soluciones: predictor asimétrico, **stop-gradient**, **EMA del target encoder** |
| **Colapso dimensional** | El latente colapsa a un subespacio de dimensión baja: pierde estructura métrica → **es el candidato #1 a explicar la desalineación** |
| **MAE / masking** | El enmascaramiento como tarea pretexto; V-JEPA 2.1 lo lleva a "Dense Predictive Loss" |
| **SIGReg y la hipótesis gaussiana** | LeWM reemplaza stop-gradient y EMA por un regularizador gaussiano. **Esta es la contribución interna clave** |

**Cómo saber que lo dominas:** puedes explicar por qué sin stop-gradient BYOL colapsa, y por qué
LeWM puede prescindir de él.

**Recursos:** LeJEPA (para SIGReg). BYOL, SimSiam, MAE. Surveys de SSL (p.ej. Balestriero et al.).

---

## Nivel 5 — Modelos basados en energía y JEPA (2–3 semanas)

| Concepto | Por qué |
|---|---|
| **Energy-Based Models** | JEPA se formula como EBM: dos entradas se codifican y el **desajuste entre representación predicha y real define una energía** que el entrenamiento baja |
| La position paper de LeCun (2022) | El manifiesto: percepción, world model, cost module, actor |
| **I-JEPA** (2023) | JEPA en imágenes: el primer modelo concreto |
| **V-JEPA / V-JEPA 2 / 2.1** | El salto a video y a robot planning |
| **JEPA vs generativo** | LeCun: *"JEPA no es IA generativa"* — predecir en espacio abstracto, no reconstruir píxeles |

**Cómo saber que lo dominas:** puedes explicar por qué predecir en espacio latente evita gastar
capacidad modelando detalle impredecible.

**Recursos:** LeCun 2022. I-JEPA (Assran et al. 2023). V-JEPA. V-JEPA 2 / 2.1.

---

## Nivel 6 — World models, planificación y control (2–3 semanas)

| Concepto | Por qué |
|---|---|
| MDP, dinámica `p(s_{t+1} | s_t, a_t)`, dinámica latente | La formulación de LeWM |
| **MPC** (Model Predictive Control) | Planifica, ejecuta los primeros k pasos, observa, **replanifica** |
| **CEM** (Cross-Entropy Method) | El optimizador sin gradiente que usa LeWM: muestrea N secuencias, refina la distribución, elige la mejor |
| **Error acumulado (compounding error)** | Por qué la alineación debería decaer con el horizonte |
| Tareas: Push-T, OGBench-Cube, Two-Room, Reacher | Los cuatro entornos de LeWM |

**Cómo saber que lo dominas:** puedes escribir el pseudocódigo de MPC con CEM y explicar dónde entra
el coste latente.

**Recursos:** Rubinstein, *The Cross-Entropy Method*. Dreamer/PlaNet (Hafner et al.). LeWM. HWM
(MPC jerárquico latente). OGBench.

---

## Nivel 7 — La teoría que el Taller necesita (4–6 semanas, el más duro)

| Concepto | Por qué |
|---|---|
| **Identificabilidad lineal** | El teorema de LeJEPA: recuperar las variables latentes verdaderas hasta una transformación lineal |
| **Condiciones "si y solo si"** | La gaussiana es **necesaria de forma única**. Entender por qué es el corazón del Taller |
| **ICA lineal y no lineal** | La identificabilidad viene de ahí; es el marco matemático heredado |
| **Teoría espectral de grafos** | La ruta de Cui et al.: JEPA ≡ factorización de bajo rango de una matriz de co-ocurrencia condicionada por acción |
| **Lema de Johnson–Lindenstrauss** | Aparece en el análisis de proyecciones aleatorias (SIGReg usa 1024) |
| **Teoría de la aproximación / complejidad de muestra** | El trade-off entre error de aproximación y error de muestra en función de la dimensión latente |
| **Lean 4 + Mathlib** | El teorema de identificabilidad se **verificó mecánicamente en Lean 4**. Ese es el estándar del Taller |

**Cómo saber que lo dominas:** puedes enunciar el teorema de identificabilidad con sus tres
condiciones y explicar qué falla si quitas una.

**Recursos:** el paper de Klindt/LeCun/Balestriero. Cui et al. Hyvärinen & Oja (ICA). Chung, *Spectral
Graph Theory*. *Theorem Proving in Lean 4* + *Mathematics in Lean*.

---

## Orden de lectura de los papers (este es el orden, no otro)

1. **LeCun 2022** — *A Path Towards Autonomous Machine Intelligence*. La filosofía.
2. **I-JEPA** (2023) — la primera implementación concreta.
3. **LeWM** (arXiv:2603.19312) — **el objeto de tu tesis**. Léelo con el nivel 3–4 ya cubierto.
4. **Decision-Metric Alignment** (arXiv:2608.18746) — **el paper central**. Léelo después de LeWM.
5. **When Does LeJEPA Learn a World Model?** (mayo 2026) — la teoría.
6. **Cui et al.** (junio 2026) — la ruta espectral.
7. **stable-worldmodel benchmark** (mayo 2026) — el benchmark de robustez.
8. **V-JEPA 2.1** (arXiv:2603.14482) — el estado del arte, para contexto.

---

## Estimación realista

| Nivel | Tiempo | Acumulado |
|---|---|---|
| 0 — Herramientas | 1–2 sem | 2 sem |
| 1 — Matemática | 3–4 sem | 6 sem |
| 2 — Redes neuronales | 2–3 sem | 9 sem |
| 3 — Transformers/ViT | 3 sem | 12 sem |
| 4 — SSL y colapso | 3–4 sem | 16 sem |
| 5 — EBM y JEPA | 2–3 sem | 19 sem |
| 6 — World models/MPC | 2–3 sem | 22 sem |
| 7 — Teoría | 4–6 sem | 28 sem |

**En paralelo, no en serie:** los niveles 0–3 en ~3 meses a medio tiempo, y luego los niveles 4–6
mientras ya corres experimentos de Tesis 1 sobre los checkpoints liberados (no necesitas entender
todo para empezar a medir). El nivel 7 es el del Taller.

**Atajo legítimo:** los niveles 0, 1a y 3 los puedes comprimir mucho si ya los tienes de la carrera.
Lo que **no** se puede saltar es el **nivel 4** (colapso, stop-gradient, SIGReg): sin él, el paper
central no se entiende.
