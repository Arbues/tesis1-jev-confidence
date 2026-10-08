# Dossier Tesis 1 — Decision-metric alignment en world models JEPA pequeños

Documento de trabajo · 19-sep-2026 · objetivo: dejar listo el instrumento que el Taller convertirá en matemática

---

## 0. Cómo se encaja con tu plan de tres etapas

| Etapa | Qué aporta | Tipo de contribución |
|---|---|---|
| **Tesis 1** | **El instrumento + la caracterización empírica**: medir cuándo el latente ordena bien los planes, y barrer los ejes internos que lo controlan | Empírica / de medición |
| **Tesis 2** | **El mecanismo**: un objetivo de entrenamiento que induzca alineación, o una corrección en el espacio latente | Algorítmica |
| **Taller** | **Las bases matemáticas**: condiciones necesarias/suficientes para la alineación métrica; extender la identificabilidad fuera del régimen gaussiano | **Teórica** (Lean 4) |

Tú mismo lo dijiste: Tesis 1 pasa siempre, y el Taller es el que tiene que demostrar bases matemáticas. Entonces **Tesis 1 se diseña como la pista de aterrizaje del Taller**: no inventa teoría, pero produce exactamente la evidencia empírica que la teoría necesitará explicar. Cada eje que barras en Tesis 1 es una hipótesis que el Taller demostrará.

---

## 1. El problema, formalizado

**arXiv:2608.18746 (19-ago-2026)** — *Decision-Metric Alignment in Latent World Models*:

> "Fuerte decodificación de variables de tarea no garantiza que este coste particular ordene las secuencias de acciones candidatas por progreso real. Llamamos a esta última propiedad **decision-metric alignment**."
>
> "La pregunta dominante que se le hace a un world model latente —'¿qué codifica el latente?'— es por tanto **incompleta** para planificación. La propiedad que falta es **geométrica, no informacional**."

La definición operativa: un espacio latente está alineado respecto a un coste de planificación `c_lat` si, para todo par de secuencias de acciones candidatas `a⁽ⁱ⁾`, `a⁽ʲ⁾` con costes reales `c_real⁽ⁱ⁾`, `c_real⁽ʲ⁾`:

```
si   c_real⁽ⁱ⁾ < c_real⁽ʲ⁾     entonces     c_lat⁽ⁱ⁾ < c_lat⁽ʲ⁾
```

Es decir: **la relación de orden inducida por el coste latente debe coincidir con la del entorno real.** Es una propiedad de la *estructura métrica* del latente, no de su contenido informacional. El paper la define y construye el diagnóstico, pero **no da teoría**: no dice bajo qué condiciones se cumple, ni cómo inducirla.

**Eso es el hueco.** Y es exactamente el tipo de hueco que deja trabajo para tres etapas: medirlo (Tesis 1) → inducirlo (Tesis 2) → demostrarlo (Taller).

---

## 2. Objeto de estudio: LeWM en detalle

**LeWorldModel (LeWM)** — arXiv:2603.19312, Maes, Le Lidec, Scieur, **LeCun**, Balestriero (Mila/NYU/Samsung SAIL/Brown).
Código: `github.com/lucas-maes/le-wm`. Construye sobre `stable-worldmodel` (entornos, planificación, evaluación) y `stable-pretraining` (entrenamiento).

**Por qué es el objeto ideal:** ~15M parámetros, **entrenable en una sola GPU en pocas horas**, y **checkpoints liberados** para los cuatro entornos — así que Tesis 1 no necesita entrenar desde cero.

### Arquitectura interna (importa al detalle)

```
Encoder:    ViT-tiny (~5M)          patch 14 · 12 capas · 3 cabezas · hidden 192
            z_t = [CLS] token de la última capa
            → proyector: MLP de 1 capa + BatchNorm   ← necesario porque el
              LayerNorm final del ViT impide optimizar el objetivo anti-colapso

Predictor:  transformer (~10M)      6 capas · 16 cabezas · dropout 10%
            historial de N frames → ẑ_{t+1} autoregresivo
            enmascaramiento causal temporal (no ve el futuro)
            acción a_t entra por AdaLN, con parámetros inicializados en CERO

Objetivo:   L_LeWM = L_pred + λ · SIGReg(Z)
            SIGReg fuerza latentes gaussianos · M = 1024 proyecciones · λ = 0.1
            SIN stop-gradient · SIN EMA · end-to-end · 1 solo hiperparámetro efectivo

Planifica:  CEM sobre distancia latente al goal
            cada frame = 1 token de 192 dims (~200× menos tokens que DINO-WM)
            ~1 s vs 47 s de DINO-WM  →  48× más rápido
```

### Entornos y checkpoints disponibles

| Entorno | Tarea | Checkpoint |
|---|---|---|
| **Push-T** | manipulación 2D, empujar bloque a configuración objetivo | `quentinll/lewm-pusht` |
| **OGBench-Cube** | manipulación 3D con brazo robótico | `quentinll/lewm-cube` |
| **Two-Room** | navegación 2D | `quentinll/lewm-tworooms` |
| **Reacher** | brazo de 2 articulaciones | `quentinll/lewm-reacher` |

Baselines con checkpoints (Google Drive): **PLDM, LeJEPA, IVL, IQL, GCBC, DINO-WM, DINO-WM-noprop**.

### Dato clave que ya sugiere la hipótesis del Taller

El propio paper de LeWM reporta que **falla en el entorno más simple (Two-Room)**, y su explicación es reveladora:

> "sospechamos que se debe a que la **dimensionalidad intrínseca de la tarea es demasiado baja**, lo que puede impedir que el **regularizador gaussiano** produzca un espacio latente bien estructurado."

Eso conecta directamente con el teorema de LeJEPA (la gaussiana es **necesaria de forma única** para la identificabilidad). **Hay una tensión estructural entre el regularizador gaussiano y la calidad métrica del latente, y nadie la ha medido.** Ese es el corazón científico de Tesis 1.

---

## 3. El instrumento: coeficiente de alineación métrica de decisión

**Núcleo de Tesis 1.** Implementar el diagnóstico sobre el harness existente:

1. **Muestrear M estados iniciales** por entorno (distribución de estados del dataset de evaluación).
2. En cada estado, **muestrear N = 64 secuencias de acciones candidatas** (como el paper).
3. Para cada secuencia, calcular:
   - `c_lat⁽ⁱ⁾` = ‖rollout del predictor → latente final − z_goal‖ (coste latente)
   - `c_real⁽ⁱ⁾` = coste real ejecutando la secuencia en el entorno
4. Sobre los **N(N−1)/2 pares** por estado, calcular:
   - **Spearman ρ** y **Kendall τ** entre el ranking latente y el real
   - **Tasa de inversión** (fracción de pares mal ordenados)
   - **Top-k agreement**: ¿el argmin latente está en el top-k real?
5. Agregar sobre estados con intervalos de confianza bootstrap.

**Aporte:** el paper introduce la definición y reporta el diagnóstico como herramienta; **nadie ha publicado el barrido sistemático** sobre los ejes que controlan la alineación.

---

## 4. Los cinco ejes internos que hay que barrer (esto es lo que hace la tesis)

Esto es lo que la distingue de "una comparación": cada eje **interviene sobre la mecánica interna del modelo**.

### Eje 1 — Horizonte de rollout
Alineación vs número de pasos k del rollout autoregresivo. **Predicción:** decae por error acumulado. **Valor:** establece el horizonte máximo confiable — resultado útil y directamente citable.

### Eje 2 — Regularizador gaussiano λ (el eje central)
**Intervención interna real:** reentrenar LeWM barriendo λ ∈ {0.01, 0.05, 0.1, 0.5, 1.0} y medir la alineación.
**Hipótesis fuerte:** existe una **tensión** entre la regularización gaussiana (necesaria para la identificabilidad según el teorema de LeJEPA) y la alineación métrica de decisión. Si λ grande mejora la estructura global pero degrada el ordenamiento local de planes, tienes un **trade-off fundamental medido** — y ese es el resultado que el Taller convertirá en teorema.
**Coste:** 5 entrenamientos de 15M en 4050. Es la parte más cara y sigue siendo factible.

### Eje 3 — Dimensión del latente
Ablación de la dimensión de embedding (192 → 64, 128, 256, 512) vs alineación. El paper solo reporta que "el rendimiento satura pasado cierto umbral" para *control*, no para *alineación*.

### Eje 4 — Localización de la desalineación: encoder vs predictor
Congelar el predictor y variar el encoder (ViT vs ResNet-18, que el paper ya validó) y viceversa. **¿La desalineación nace en la geometría del encoder o en la dinámica del predictor?** Nadie lo ha separado.

### Eje 5 — Régimen de datos y dimensionalidad intrínseca
Push-T (alta dim) vs Two-Room (baja dim, donde LeWM falla). Conectar con el teorema: la condición gaussiana es un "si y solo si" para identificabilidad, así que **debería haber un régimen de dimensionalidad intrínseca donde la alineación se rompe estructuralmente**. Ese cruce teoría-medición es el puente al Taller.

### Eje transversal — Reproducir el benchmark de robustez
Combinar con las perturbaciones del *stable-worldmodel benchmark* (color del agente, fondo, distractores) y medir si **la alineación cae antes que el éxito de planificación**. Eso daría un diagnóstico más sensible que la tasa de éxito — y explicaría el hallazgo "predicción ≠ planificación".

---

## 5. Entregables de Tesis 1

| # | Entregable | Por qué vale |
|---|---|---|
| 1 | **Harness reproducible** (fork de `stable-worldmodel`) con el diagnóstico implementado | El artefacto que otros citan; el Taller lo reutiliza |
| 2 | **Dataset público** de pares (coste latente, coste real) por entorno × horizonte × λ | Datos crudos = base para trabajos futuros |
| 3 | **Caracterización empírica**: cuándo se alinea y cuándo no, con los 5 ejes | El resultado principal |
| 4 | **El trade-off λ ↔ alineación** (si se confirma) | La hipótesis que el Taller demostrará |
| 5 | **Pre-registro con DOI** antes de correr | Hace creíble cualquier desenlace, incluido el negativo |

---

## 6. Cómputo y costo (todo en tu laptop)

| Componente | Coste |
|---|---|
| Evaluación con checkpoints liberados (4 entornos) | **Horas, no días.** CEM con N=64 sobre latentes de 192 dims y predictor de 10M es trivial |
| Reentrenar LeWM barriendo λ (eje 2) | ~5 corridas × pocas horas en la 4050 |
| Obtener `c_real` | El coste real es simular el entorno (2D/3D), no la GPU. Push-T y Two-Room baratos; Cube más caro |
| V-JEPA 2.1 ViT-B/L destilados (opcional) | Encoder congelado + embeddings cacheados → barato |
| **Costo monetario** | **~$0** salvo nube opcional para el ViT-G como referencia (~$30–60) |

**GPU: sí la usas, y alcanza.** 15M de parámetros y ViT-tiny son exactamente el régimen donde una 4050 de 6 GB trabaja cómoda.

---

## 7. Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| arXiv:2608.18746 (o su sucesor) publica el barrido primero | Publicar **pre-registro + harness** temprano; el valor del instrumento sobrevive aunque el barrido se publique |
| El eje 2 (λ) requiere reentrenar y el dataset PushT pesa 43 GB | Usar Two-Room y Reacher para el barrido completo (baratos) y PushT solo para el λ óptimo y ±1 |
| La alineación sale alta en todos los regímenes (resultado "aburrido") | **No es un fracaso:** un resultado negativo bien medido sobre un diagnóstico de un mes de vida es publicable y cierra la pregunta. El eje 2 y el 5 son los que más probablemente den estructura |
| El harness `stable-worldmodel` tenga fricción de instalación | Es un repo mantenido y activo (Mila); el fork de LeWM ya lo usa |

---

## 8. Qué deja Tesis 1 para el Taller (la matemática)

1. **Condiciones necesarias/suficientes para la alineación métrica de decisión** — hoy no existen. Tesis 1 da la evidencia de qué variables importan (λ, dimensionalidad intrínseca, horizonte), que es el punto de partida para derivar el teorema.
2. **Identificabilidad fuera del régimen gaussiano** — el "si y solo si" de LeJEPA es el ancla; la ruta espectral de Cui et al. (junio 2026) es la vía abierta.
3. **Un objetivo de entrenamiento que induzca alineación** — la parte algorítmica (Tesis 2), que el Taller puede acompañar con garantías.
4. **Formalización en Lean 4** — el precedente ya existe: el teorema de identificabilidad de LeJEPA se verificó mecánicamente. Ese es el estándar al que apuntar en el Taller.

---

## Fuentes

**Núcleo:** arXiv:2608.18746 (decision-metric alignment) · arXiv:2603.19312 (LeWorldModel) ·
github.com/lucas-maes/le-wm · github.com/galilai-group/stable-worldmodel ·
github.com/galilai-group/stable-pretraining · le-wm.github.io.

**Teoría:** "When Does LeJEPA Learn a World Model?" (Klindt/LeCun/Balestriero, mayo 2026, Lean 4) ·
Cui et al., ruta espectral (junio 2026) · Maes et al., stable-worldmodel benchmark (mayo 2026) ·
LeCun, "A Path Towards Autonomous Machine Intelligence" (2022).

**Familia JEPA:** arXiv:2603.14482 (V-JEPA 2.1) · arXiv:2506.09985 (V-JEPA 2) ·
arXiv:2606.32026 (AdaJEPA) · arXiv:2604.03208 (HWM, MPC jerárquico latente).
