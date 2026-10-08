# EJE 1 — JEPA y *decision-metric alignment*: inventario completo de fuentes

> ## ❌ EJE DESCARTADO — 01-OCT-2026
> **Instrucción expresa del autor: no se trabajará sobre JEPA, LeWM, DINO ni sobre subrutas de este
> eje. El tema definitivo es el `eje-2-jev-opensource` (Jev y Laya — que no tienen ninguna relación
> con JEPA).** Las correcciones de abajo quedan solo como registro histórico de por qué se cerró.
>
> **Correcciones a este inventario:**
> 1. La afirmación "nadie ha barrido λ" es **falsa en general**: existen barridos de λ en otros
>    dominios (`eb_jepa`/CIFAR-10; ChronoJEPA/PEMS08, donde *placement* domina sobre λ). Lo que no
>    existe es el barrido medido contra alineación de decisión — y por eso ya no es la apuesta.
> 2. El hueco del eje 5 (Two-Room falla por dimensionalidad intrínseca) **ya está diagnosticado y
>    arreglado**: arXiv:2605.09241 (Sub-JEPA).
> 3. El puente "identificabilidad ↔ planificación" está parcialmente cerrado: arXiv:2605.26379 Thm 4
>    demuestra que la identificabilidad lineal habilita planificación óptima en latente para costes
>    ortogonalmente invariantes.
> 4. Entraron cuatro papers más al carril entre may y sep-2026: Sub-JEPA (2605.09241), SD-JEPA
>    (2605.31111), D-JEPA (2609.24749) y TD-JEPA (2607.25337). El carril "mejorar la geometría de
>    ranking de LeWM" está **saturado**.
> 5. Nuevo material verificado que sí queda abierto: el sesgo del BatchNorm del proyector de LeWM
>    (~300× en modo eval; rango efectivo 11.9→18.6 sin tocar pesos) y la ceguera de SIGReg al colapso
>    anisotrópico (‖∇‖ ≈ 2e-4 vs 1.25). Ver `README.md` §7-bis.

Tesis 1 · verificación HTTP de las 15 fuentes del eje · corte 25-sep-2026

---

## ⚠️ CORRECCIÓN CRÍTICA — leer antes que nada

Al verificar títulos encontré que **lo que te dije antes sobre el hueco está parcialmente mal.** Yo afirmé:

> *"El paper define la propiedad y construye el diagnóstico, pero NO da teoría: no dice cuándo se cumple
> ni cómo inducirla. Ese es el hueco."*

**Eso es falso.** El título completo de arXiv:2608.18746 lo delata:

> **"Decision-Metric Alignment in Latent World Models: Diagnostics *and Action-Conditioned Objectives*
> for MPC Planning"**

Y su resumen confirma que el paper ya entrega **las tres piezas** que yo te dije que faltaban:

| Lo que yo dije que faltaba | Lo que el paper ya hace |
|---|---|
| El diagnóstico | **Plan-Real Spearman** (acuerdo de rango latente-real sobre planes aleatorios) y **CEM-stage Spearman** (el mismo acuerdo mientras CEM concentra su propuesta) |
| Teoría de cuándo se cumple | **Analiza condiciones suficientes** bajo las cuales la distancia latente preserva el orden del coste real, identificando **tres cantidades de control: distorsión del encoder, error del rollout terminal y margen entre candidatos** |
| Un objetivo que la induzca | **DA-LeWM**: aumenta LeWM con cabezas de dinámica inversa y de acción-meta condicionada a demostraciones. Converge más rápido y logra mayor éxito online, **con puntuaciones de *probe* similares** |

Ese último detalle cierra el argumento que yo te presenté como abierto: *"la propiedad que falta es
geométrica, no informacional"* ya está demostrada empíricamente por ellos (el probe no cambia, la
geometría sí).

**Y hay un segundo paper, arXiv:2609.05461 (ARC-Bench), que hace la misma auditoría por otra vía:**

- Titulo: *"ARC-Bench: **Closed-Loop Replanning Masks Broken Action Ranking** in Frozen JEPA World Models"*
- Audita la misma suposición con un **protocolo sin fuga (*no-leak*) de candidatos fijos**
- Resultado: **la suposición falla de forma severa y estructural** — en las auditorías de manipulación
  con checkpoints oficiales, **el candidato mejor puntuado es casi siempre subóptimo**; la misma
  inversión aparece en dominios de laberinto
- Persiste al cambiar DINOv2 por encoders **V-JEPA 1 y V-JEPA 2 en escala ViT-L / ViT-G**
- Descarta procedencia, subentrenamiento, controles de backbone con presupuesto igualado y
  circularidad métrica
- **El hallazgo metodológico que más te afecta:** *el replanning en bucle cerrado lo enmascara*.
  Al reducir la frecuencia de replanning, el éxito se desploma. **Las tasas de éxito en bucle
  cerrado sobreestiman sistemáticamente la capacidad de ordenamiento de las representaciones latentes.**

### Qué significa esto para tu Tesis 1

**Dos papers de agosto 2026 ya ocupan el diagnóstico.** Tu Tesis 1 no puede ser "construir el
instrumento y caracterizar" — eso ya está hecho, dos veces, con protocolos distintos y checkpoints
liberados.

**Y ARC-Bench te da además una advertencia metodológica que invalida la mitad del protocolo que te
propuse:** yo te dije de medir la alineación en el bucle de planificación. ARC-Bench demuestra que
**eso es exactamente lo que oculta el defecto.** Cualquier medición en bucle cerrado que hagas
saldrá limpia y no significará nada.

### Lo que sigue genuinamente abierto

Ninguno de los dos papers hizo esto:

1. **¿Es el regularizador gaussiano (SIGReg) la causa de la distorsión métrica?**
   Aquí hay una **tensión entre dos resultados publicados y nadie la ha tocado**:
   - LeJEPA (may-2026) demuestra que la latente **gaussiana es necesaria y suficiente** para
     identificabilidad.
   - Estos dos papers demuestran que la **métrica del latente está rota de forma estructural**.
   → **¿La condición que garantiza la identificabilidad es la que rompe la alineación métrica?**
   Es una pregunta interna, matemática, falsable, y **el barrido de λ la responde directamente**.
   Ninguno de los dos papers barrió λ. DA-LeWM añade cabezas; no pregunta si el regularizador es la causa.

2. **Metrología: los dos instrumentos no han sido validados entre sí.** ARC-Bench usa candidatos
   fijos *no-leak*; 2608.18746 usa dos variantes de Spearman. **Nadie ha medido si miden lo mismo.**
   Existe una base racional para hacerlo: la corrección de Spearman por empates de Kendall y el
   efecto de la concentración de CEM sobre el rango son problemas estadísticos conocidos.

3. **Puente identificabilidad ↔ alineación sin explorar.** 2608.18746 nombra tres cantidades de
   control (distorsión, error terminal, margen) pero **no las conecta con las condiciones de
   identificabilidad de LeJEPA**. Si la desalineación correlaciona con la violación de las
   condiciones de identificabilidad, tienes un teorema.

4. **El régimen de horizontes no está barrido** como eje controlado, aunque el error de rollout
   terminal aparece como cantidad de control.

5. **Ni ARC-Bench ni 2608.18746 auditan V-JEPA 2.1** (features densas) más allá de la extensión
   controlada de backbone de ARC-Bench.

**La recomendación revisada y honesta:** el eje λ con medición **en bucle abierto** (siguiendo el
protocolo de ARC-Bench) para responder si el regularizador gaussiano causa la desalineación. Eso
conecta dos resultados publicados que hoy no se hablan, y es el tipo de pregunta interna que buscas.
Los detalles operativos están en `06_dossier_tesis1.md`, que **necesita revisión a la luz de esto.**

---

## 1. Fuentes del núcleo (todas verificadas HTTP 200)

### 1.1 Los dos papers que definen el eje

| Fuente | Qué es | Verificado |
|---|---|---|
| **[arXiv:2608.18746](https://arxiv.org/abs/2608.18746)** — *Decision-Metric Alignment in Latent World Models: Diagnostics and Action-Conditioned Objectives for MPC Planning* · Jiawei Wang, Ke Rui, Yushen Zuo, Yichun Feng, Minglei Li · 19-ago-2026 · cs.LG, cs.CV | **El paper fundacional del eje.** Define *decision-metric alignment*. Introduce Plan-Real Spearman y CEM-stage Spearman. Condiciones suficientes con tres cantidades de control. Propone DA-LeWM | ✅ 200 |
| **[arXiv:2609.05461](https://arxiv.org/abs/2609.05461)** — *ARC-Bench: Closed-Loop Replanning Masks Broken Action Ranking in Frozen JEPA World Models* · Zhengshu Zhang, Zhiyuan Li · cs.AI, cs.LG, cs.RO | El paper que **te obliga a medir en bucle abierto**. Protocolo *no-leak* de candidatos fijos. Demuestra que el defecto es estructural y que el replanning lo enmascara | ✅ 200 |

**Nota sobre los IDs:** el 2609.05461 tiene ID de septiembre-2026 pero fecha de publicación
2026-08-12. Puede ser una re-subida. Verifica el número de versión al citarlo.

### 1.2 El objeto de estudio: LeWM y su ecosistema

| Fuente | Qué es | Verificado |
|---|---|---|
| **[arXiv:2603.19312](https://arxiv.org/abs/2603.19312)** — *LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels* · Lucas Maes, Quentin Le Lidec, Damien Scieur, **Yann LeCun**, Randall Balestriero · 13-mar-2026 (v3 3-jun) · cs.LG, cs.AI | **El modelo objeto de estudio.** JEPA de ~15M desde píxeles, con objetivo de dos términos (predicción + SIGReg) sin stop-gradient ni EMA | ✅ 200 |
| **[github.com/lucas-maes/le-wm](https://github.com/lucas-maes/le-wm)** | Código oficial. ★4.466 · 657 forks · MIT · último push 26-may-2026 | ✅ 200 |
| **[le-wm.github.io](https://le-wm.github.io)** | Página del proyecto | ✅ 200 |
| **[github.com/galilai-group/stable-worldmodel](https://github.com/galilai-group/stable-worldmodel)** | Plataforma de entornos, planificación y evaluación. El arnés que usarás | ✅ 200 |
| **[github.com/galilai-group/stable-pretraining](https://github.com/galilai-group/stable-pretraining)** | Marco de entrenamiento mínimo y fiable | ✅ 200 |
| **[quentinll/lewm-pusht](https://huggingface.co/quentinll/lewm-pusht)** | Checkpoint liberado · Push-T | ✅ 200 |
| **[quentinll/lewm-cube](https://huggingface.co/quentinll/lewm-cube)** | Checkpoint liberado · OGBench-Cube | ✅ 200 |
| **[quentinll/lewm-tworooms](https://huggingface.co/quentinll/lewm-tworooms)** | Checkpoint liberado · Two-Room (el de dimensionalidad intrínseca baja) | ✅ 200 |
| **[quentinll/lewm-reacher](https://huggingface.co/quentinll/lewm-reacher)** | Checkpoint liberado · Reacher | ✅ 200 |

**Baselines con checkpoints** (Google Drive, referenciados por el repo de LeWM): PLDM, LeJEPA, IVL,
IQL, GCBC, DINO-WM, DINO-WM-noprop.

### 1.3 La familia JEPA (el linaje)

| Fuente | Qué es | Verificado |
|---|---|---|
| **[arXiv:2506.09985](https://arxiv.org/abs/2506.09985)** — *V-JEPA 2: Self-Supervised Video Models Enable Understanding, Prediction and Planning* · Mido Assran, Adrien Bardes, David Fan, Quentin Garrido, Russell Howes, Mojtaba Komeili, Matthew Muckley +22 · 11-jun-2025 · cs.AI, cs.CV, cs.LG, cs.RO | El modelo que popularizó los world models JEPA. 1.2B, planificación robótica zero-shot | ✅ 200 |
| **[arXiv:2603.14482](https://arxiv.org/abs/2603.14482)** — *V-JEPA 2.1: Unlocking Dense Features in Video Self-Supervised Learning* · Lorenzo Mur-Labadia, Matthew Muckley, Amir Bar, Mido Assran, Koustuv Sinha, Mike Rabbat, **Yann LeCun**, Nicolas Ballas · 15-mar-2026 | Pérdida predictiva densa, autosupervisión profunda, tokenizadores multimodales. Libera **ViT-B/L destilados (80M/300M)** — tu régimen de 6 GB | ✅ 200 |
| **[arXiv:2606.32026](https://arxiv.org/abs/2606.32026)** — *AdaJEPA: An Adaptive Latent World Model* · Ying Wang, Oumayma Bounou, **Yann LeCun**, Mengye Ren · 30-jun-2026 | World model latente que se adapta en tiempo de test. Relevante: ataca el mismo problema (latente que deja de servir) desde la adaptación, no desde la geometría | ✅ 200 |
| **[arXiv:2604.03208](https://arxiv.org/abs/2604.03208)** — *Hierarchical Planning with Latent World Models* · Wancong Zhang, Basile Terver, Artem Zholus, Soham Chitnis, Harsh Sutaria, Mido Assran, Randall Balestriero, Amir Bar +3 · 3-abr-2026 | Planificación jerárquica. Relevante porque el error de rollout terminal —una de las tres cantidades de control de 2608.18746— es justo lo que la jerarquía ataca | ✅ 200 |
| **LeCun 2022** — *A Path Towards Autonomous Machine Intelligence* | El documento fundacional del programa JEPA. Origen conceptual de todo el eje | — |

### 1.4 Teoría de identificabilidad (el puente al Taller)

| Fuente | Qué es |
|---|---|
| ***When Does LeJEPA Learn a World Model?*** · Klindt / LeCun / Balestriero · may-2026 | Identificabilidad lineal bajo latentes **gaussianos** + ruido aditivo estacionario + exploración amplia. **La gaussiana es necesaria de forma única ("si y solo si").** Pruebas **formalizadas en Lean 4**. Los datos dirigidos a objetivos (robótica real) **violan las condiciones** |
| **Cui et al.** · ruta espectral · jun-2026 | El objetivo JEPA ≡ **factorización de bajo rango** de una matriz de co-ocurrencia condicionada por acción |
| **stable-worldmodel benchmark** · Maes et al. · Mila + LeCun · may-2026 | Robustez 50% → **12%** (cambia color del agente) → **6%** (cambia fondo). **La precisión de predicción es un proxy pobre del éxito de planificación.** El campo estaba tan fragmentado que un mismo algoritmo se reimplementó en ≥5 papers |

> Estos tres son la materia prima del **Taller**: son los únicos resultados que tienes con
> demostración matemática o verificación mecánica. **La tesis conceptual es conectar las condiciones
> de identificabilidad con la alineación métrica de decisión.**

### 1.5 Evidencia de competitividad al costo

| Dato | Fuente |
|---|---|
| 2B (V-JEPA 2.1 ViT-G) supera a DINOv3 de 7B en profundidad NYUv2 (0.307 vs 0.309 RMSE) | benchmark V-JEPA 2.1 |
| Backbone V-JEPA 2 en **350.000 dashcams**, superando a un rival de píxeles con **~91× menos parámetros** | despliegue industrial reportado |
| Planificación **10× más rápida** (128 → 8 pasos de simulación; >100 s → 10.6 s) | V-JEPA 2 |
| AMI Labs: seed de **$1.030M** a valuación **$3.500M**, ~12 empleados, sin producto | prensa |

---

## 2. Cómo usar este inventario

| Si necesitas… | Ve a |
|---|---|
| El planteamiento formal del problema | 2608.18746 §intro y definición |
| El protocolo de medición que **debes** copiar (bucle abierto, candidatos fijos) | 2609.05461 |
| El modelo sobre el que trabajar | 2603.19312 + checkpoints `quentinll/lewm-*` |
| Saber qué se puede afirmar con garantía teórica | *When Does LeJEPA Learn a World Model?* |
| El estado de la discusión de vanguardia | AdaJEPA y Hierarchical Planning |
| El marco conceptual | LeCun 2022 |

**Nota sobre `arquitectura_y_ruta.html`:** los 6 diagramas SVG siguen válidos para entender la
mecánica de JEPA y de LeWM. El diagrama 5 (*decision-metric alignment*) **necesita actualizarse**:
dibuja las inversiones de ranking como el objeto del diagnóstico de tu tesis, cuando en realidad
el diagnóstico ya lo aportan otros dos papers. Hay que añadir el eje λ como el objeto propio.
