# §6. Discusión (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 6 · 08-oct-2026*

---

## 6.1. El hallazgo tiene dos capas

La primera lectura de la matriz es una sola frase: **un umbral de `confidence` no viaja entre
implementaciones**. Pero el promedio no describe el fenómeno. Al mirar celda a celda aparecen **dos capas**
distintas, y confundirlas lleva a conclusiones opuestas (documentado en `docs/erratas_especificacion.md`, E2).

**Capa 1, la escala.** Dos definiciones pueden ordenar las decisiones **igual** y aun así estar en escalas
distintas. `C_max = p` y `C_Jev = (n·p − 1)/(n − 1)` inducen el mismo umbral en orden, de modo que existe un
mapa cerrado `ψ = φ⁻¹` entre ellas. El **número** no viaja (`|Δ|` mediano de 0.20 a 0.31 en el par
`pmax ↔ jev`), pero el **mapa** sí transfiere (0.0025). Es la diferencia entre copiar la cifra y traducirla.

**Capa 2, la forma.** Entre definiciones de **clases distintas** (`p_max`, entropía, margen) no existe ni
número ni mapa. `pmax → ent` tiene mediana de 0.77: es el caso en que la confianza "alta" de una definición y
la de la otra ordenan las decisiones de forma diferente, no solo con otra escala. Aquí no hay nada que
traducir y el porte directo es lisa y llanamente una extrapolación inválida.

La coexistencia de las dos capas es la razón de que el resultado no se pueda resumir con una media: la misma
tabla contiene identidades exactas (14 % de las celdas con `n = 2` transfieren bien) y desastres (celdas con
`Δ = 0.80` y cobertura 0).

## 6.2. Por qué el orden se preserva y el número no

Sea `f` una transformación creciente de `p_max`. Un umbral `τ` sobre `f(p_max)` selecciona el mismo conjunto
de decisiones que el umbral `f⁻¹(τ)` sobre `p_max`, porque `f` monótona no cambia el orden. Por eso
`C_Jev`, `C_max` y `C_mar` (fijado `n`) seleccionan lo mismo con el umbral traducido. Pero el **valor** de `f`
depende de `n` y de la definición, así que la misma cifra `0.7` significa coberturas distintas. Y cuando `f`
deja de ser una función de `p_max` (la entropía usa toda la distribución, no solo el máximo), ni siquiera
existe el mapa.

Esto es exactamente lo que predice la Proposición 1 y lo que mide el factor **104×**: el costo de confundir
"mismo orden" con "mismo número".

## 6.3. El umbral es una política, no un número suelto

En un sistema que decide, el umbral no es un parámetro cosmético: define cuándo el modelo actúa y cuándo se
abstiene. Un umbral trasladado sin mapa no solo cambia una métrica de calibración, cambia la **política de
abstención**. Las celdas de §5.6 lo muestran en su forma extrema: con `q = 0.80` puede terminar actuando en el
0 % de los casos. Para quien integra un modelo tipo Jev, la conclusión práctica es que el campo `confidence`
**no es un contrato entre implementaciones**: es un número local, válido dentro de la definición que lo
produjo.

Y sin embargo el ecosistema lo trata como si lo fuera. La revisión de implementaciones (Kev, Laya, AnyJev,
open-decision-ai) muestra que cada una publica su fórmula bajo el mismo nombre y que ninguna documenta la
relación con las demás. Ese vacío es el que este instrumento llena: no descubre que hay sobre-confianza (eso
ya se midió puertas adentro de varias implementaciones), sino que **cuantifica el error de trasladar el
umbral entre ellas** y entrega el mapa cuando existe.

## 6.4. Lo que esto dice de la calibración del ecosistema

La literatura reciente mide la calibración **dentro** de una definición (por ejemplo, ECE de Laya tal como se
distribuye). Este trabajo mide **entre** definiciones, que es una pregunta distinta y hasta ahora sin tabla.
Los dos resultados no se contradicen: un modelo puede estar bien calibrado respecto de su propia definición y
aun así ser inutilizable como fuente de umbral para otra. La cifra de §5.7 (el ECE cambia 2.7× según la
definición, sobre el mismo dato) ilustra que buena parte de las discrepancias que se atribuyen al modelo son,
en realidad, discrepancias del **medidor**.

## 6.5. Limitaciones

- **Cobertura de modelos.** Cinco configuraciones de hasta 0.8B, todas las que caben en 6 GB. Los modelos de
  4B a 9B del ecosistema quedan como extensión declarada.
- **Dos grupos ausentes.** `clinc150` en el checkpoint base de Laya (ventana de 512 tokens, 126 de 151
  opciones) y `kev-suites` (no carga en el Hub). Ninguno altera las conclusiones, pero acotan el alcance
  medido a 23 de 25 combinaciones.
- **El mapa existe dentro de clases y a cardinalidad fija.** Las celdas sin mapa (2.520 de 3.564) no son
  "fallos": son el resultado de que no haya traducción matemática posible. La matriz las marca como tales.
- **El control crudo infla el porte directo** en las celdas con empates de umbral (modelo sin entrenar,
  salidas saturadas). Por eso la comparación limpia excluye las celdas dominadas por empates y la de
  referencia es la de 948 celdas (104×).
- **Las definiciones opacas** (`act_probability`, `open-decision-ai`) quedaron fuera de la matriz por
  decisión de alcance, ya que no son funciones de la distribución.

## 6.6. Relación con los trabajos previos

Este resultado es un **instrumento**, y se sostiene aunque otro publique un hallazgo cercano. La calibración
de un modelo puntual (por ejemplo, la medición de Laya tal cual se distribuye) es un hallazgo fechado; la
matriz de transferencia y la librería que la reproduce son infraestructura. El instrumento no compite con esa
literatura: la cita, la usa como punto de partida y la extiende al eje que le faltaba, el eje entre
definiciones.

Las demás aristas del eje (por qué el término de RL no induce calibración, la ablación del objetivo de
entrenamiento, la cartografía del ecosistema, la coherencia frente a la negación) están ocupadas por trabajos
recientes y quedan **fuera** de esta tesis. Aquí lo medido es, deliberadamente, el hueco que quedaba abierto:
la transferencia de umbrales entre definiciones incompatibles del mismo campo.
