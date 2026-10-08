# JEPA: estado real (sep-2026), competitividad al costo y huecos internos

Documento de actualización · 19-sep-2026 · corrige el re-ranking según la perspectiva CC

---

## 1. En qué quedó JEPA

**La familia avanzó fuerte, y el avance es interno (arquitectura y objetivo), no de escala.**

### V-JEPA 2.1 (marzo 2026) — el salto

Cuatro ingredientes nuevos, todos **internos**:

1. **Dense Predictive Loss** — objetivo de enmascaramiento donde *todos* los tokens (contexto visible y enmascarados) contribuyen a la pérdida → anclaje espacial y temporal explícito
2. **Deep Self-Supervision** — el objetivo auto-supervisado se aplica **jerárquicamente en varias capas intermedias del encoder**
3. **Multi-Modal Tokenizers** — entrenamiento unificado sobre imágenes y video
4. Escalado de modelo y datos

Modelos liberados: **ViT-g/G (1B/2B)** y **dos variantes destiladas ViT-B/L (80M/300M)**.

### Resultados (frozen backbone)

| Tarea | V-JEPA 2.1 | Referencia previa |
|---|---|---|
| Ego4D anticipación de interacción | **7,71 mAP** | ~35% mejor que el SOTA previo |
| EPIC-KITCHENS-100 action anticipation | **40,8 R@5** | nuevo SOTA absoluto |
| SSv2 (reconocimiento de acción) | **77,7%** | nuevo SOTA |
| Profundidad NYUv2 (linear probe) | **0,307 RMSE** | **supera a DINOv3 de 7B** |
| VOC semántica | 85,0 mIoU | competitivo |
| Navegación Tartan Drive | 5,687 ATE | SOTA |
| **Planificación** | **128 → 8 pasos de simulación** | **>100 s → 10,6 s (10× más rápido)** |
| Grasping en robot real | **+20%** sobre V-JEPA 2-AC | — |

### El resto del ecosistema (2026)

- **"When Does LeJEPA Learn a World Model?"** (mayo 2026, Klindt/LeCun/Balestriero): prueba **identificabilidad lineal** — LeJEPA recupera las variables latentes verdaderas hasta una transformación lineal. Condiciones: latentes **gaussianos** + dinámica de **ruido aditivo estacionario** + exploración amplia del espacio de estados. **La gaussiana es necesaria de forma única** (resultado "si y solo si"). Pruebas formalizadas en **Lean 4**. *Problema:* los datos dirigidos a objetivos —los que usa la robótica real— **violan las condiciones**, así que la garantía no aplica.
- **stable-worldmodel benchmark** (mayo 2026, Maes et al., Mila + LeCun): los world models actuales son **frágiles**. Éxito ~50% en condiciones limpias → **~12%** si cambia el color del agente → **~6%** si cambia el fondo. Y lo más importante: **la precisión de predicción es un proxy pobre del éxito de planificación**. El campo estaba tan fragmentado que un mismo algoritmo de planificación había sido reimplementado en ≥5 papers.
- **Cui et al.** (junio 2026): enmarca el preentrenamiento JEPA como **aprendizaje espectral condicional en grafos**; el objetivo JEPA **equivale a una factorización de bajo rango** de una matriz de co-ocurrencia condicionada por acción. Deriva un trade-off entre error de aproximación y error de muestra en función de la dimensión latente.
- **AMI Labs**: seed de **$1.030 millones** a valuación pre-money de $3.500M (la mayor ronda semilla europea), ~12 empleados, sin producto, hoja de ruta de años. LeCun dice explícitamente: *"no trabajen en LLMs; los avances en world models vienen de la academia"*.

---

## 2. ¿Son suficientes los resultados y competitivos al costo? — SÍ

Tres evidencias de costo-competitividad, que es justamente la tesis central de JEPA:

1. **2B vence a 7B**: V-JEPA 2.1 ViT-G (2B) supera a **DINOv3 de 7 mil millones** en profundidad (0,307 vs 0,309 RMSE) y a DINOv3 ViT-7B en detección de objetos de próxima interacción.
2. **91× menos parámetros en producción real**: un modelo de predicción de colisiones con backbone V-JEPA 2 afinado se desplegó en **350.000 dashcams** y superó a un modelo mucho mayor que predice en espacio de píxeles, usando **~91 veces menos parámetros**.
3. **10× más rápido en planificación**: los pasos de simulación interna bajaron de 128 a 8.

**Conclusión:** JEPA pasó de ser una apuesta filosófica a tener resultados SOTA con ventaja de eficiencia medible. **Vale la pena mejorarlo internamente**, y el espacio de mejora interna está abierto y activo.

---

## 3. Los tres huecos INTERNOS (y son de matemática y código, no de comparación)

### Hueco A — Identificabilidad fuera del régimen gaussiano

El teorema es un "si y solo si": **la gaussiana es la única distribución latente para la que la garantía vale**. Pero el mundo real no tiene latentes gaussianos y los datos de robótica son dirigidos a objetivos, no exploratorios. **Pregunta abierta y matemática:** ¿qué garantías de identificabilidad sobreviven para clases más amplias de entornos? Cui et al. abrieron la ruta espectral (grafo de co-ocurrencia); extenderla a dinámicas no estacionarias o no gaussianas es trabajo de **teoría pura**, con Lean 4 disponible como herramienta de verificación.

### Hueco B — Decision-metric alignment (el hueco más limpio y más nuevo)

**arXiv:2608.18746 (agosto 2026)** formaliza exactamente lo que faltaba:

> "Fuerte decodificación de variables de tarea no garantiza que este coste particular ordene las secuencias de acciones candidatas por progreso real. Llamamos a esta última propiedad **decision-metric alignment**."
>
> "La pregunta dominante que se le hace a un world model latente —'¿qué codifica el latente?'— es por tanto **incompleta** para planificación. La propiedad que falta es **geométrica, no informacional**."

Formalizan la distinción **suficiencia informacional** (¿se pueden decodificar las cantidades de tarea del latente?) vs **alineación métrica de decisión** (¿el coste latente ordena los planes consistentemente con sus resultados reales?). Construyen sobre **LeWM** (Maes et al. 2026), usan CEM con N=64 secuencias de acciones, y comparan costes latentes vs reales por pares.

**Esto es matemática + código interno**, y el paper tiene **un mes de vida**: nadie ha construido todavía la teoría de cuándo el latente es métricamente alineado, ni un objetivo de entrenamiento que lo induzca.

### Hueco C — Mecánica interna del objetivo y del predictor

Los ingredientes que hicieron funcionar a V-JEPA 2.1 (Dense Predictive Loss, Deep Self-Supervision en capas intermedias, tokenizers multimodales) se introdujeron **empíricamente**, sin teoría de por qué funcionan. Y la prevención de colapso (stop-gradient, maestro EMA) sigue siendo un mecanismo heurístico. Ahí hay intervención a nivel de código y de objetivo.

---

## 4. Corrección de perspectiva (tenías razón)

Tu objeción es correcta: **CC se enfoca en lo interno — matemática, código, mecanismos — no en comparaciones externas.** Mi recomendación anterior (T-B, "modelo vs. harness") era un **estudio comparativo**, y por eso no es núcleo de CC aunque fuera barato y tuviera hueco. Bajo tu criterio correcto, el re-ranking cambia:

| Tema | Tipo de aporte | Encaje CC real |
|---|---|---|
| **JEPA internals** (huecos A/B/C) | **Matemática + mecánica del objetivo** | **Núcleo CC** |
| ZO apuntando a A3 (estimadores generativos) | Algoritmo nuevo + teoría | **Núcleo CC** |
| Doc 03 T1 (fidelidad de formalización) | Lógica y semántica formal | **Núcleo CC** |
| Doc 03 T4 (contratos semánticos) | Semántica de implementaciones | **Núcleo CC** |
| T-B (modelo vs. harness) | Comparación / metrología | Plus, no núcleo |
| T-C (seguridad de skills) | Auditoría de medición | Plus, no núcleo |

---

## 5. Recomendación revisada

**JEPA internals es tu mejor opción** bajo el criterio CC, y ahora tiene una base mucho mejor que hace dos semanas:

- **Tu idea original se publicó.** El "audit de ordenabilidad de acciones" que habíamos diseñado es ahora *decision-metric alignment* (arXiv:2608.18746, ago-2026), construido sobre **LeWM** — el mismo modelo de tu plan original. Eso **no te quita el tema: te da la definición formal** y te deja el espacio de seguimiento completo (teoría de cuándo se cumple + objetivo que lo induzca).
- **Tu hardware alcanza y sobra.** V-JEPA 2.1 liberó variantes destiladas **ViT-B/L (80M/300M)**; LeWM es de 15M. El hueco A/B se trabaja con esos modelos, no con el ViT-G.
- **El costo es prudente**: auditar ViT-B/L local; rentar nube solo si quieres el ViT-G como referencia.
- **Y la ventaja de costo está demostrada** (2B > 7B, 91× menos parámetros, 10× más rápido), así que "seguir mejorándolo internamente" es una apuesta defendible, no una fe.

**Tesis 1 concreta:** formalizar y medir **decision-metric alignment** en modelos JEPA pequeños — derivar condiciones bajo las cuales el coste latente ordena los planes correctamente, construir el diagnóstico (que el paper deja como herramienta, no como teoría), e intervenir sobre el objetivo para inducir alineación.
**Tesis 2:** extender la identificabilidad más allá del régimen gaussiano (ruta espectral de Cui et al.).
**Taller:** un objetivo de entrenamiento métricamente alineado, verificado.

---

## Fuentes

**JEPA / V-JEPA:** arXiv:2603.14482 (V-JEPA 2.1, dense features) · arXiv:2506.09985 (V-JEPA 2) ·
github.com/facebookresearch/vjepa2 · ai.meta.com/blog/v-jepa-2-world-model-benchmarks ·
arXiv:2606.32026 (AdaJEPA, LeCun) · arXiv:2604.03208 (HWM, hierarchical latent MPC) ·
arXiv:2608.18746 (**decision-metric alignment**) · arXiv:2609.05461 (ARC-Bench) ·
Klindt/LeCun/Balestriero, "When Does LeJEPA Learn a World Model?" (mayo 2026, Lean 4) ·
Maes et al., stable-worldmodel benchmark (mayo 2026, Mila) · Cui et al. (junio 2026, espectral) ·
arXiv:2602.23643 (SAI, Goldfeder/Wyder/LeCun).

**Contexto AMI Labs:** MIT Technology Review (ene-2026, entrevista a LeCun) · TechCrunch /
TechTimes (jun-2026) · startuphub.ai (ago-2026).
