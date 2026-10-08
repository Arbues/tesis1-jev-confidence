# §1. Introducción (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 1 · 04-oct-2026*
*Estilo: IEEE · citas con `\cite{clave}` (las claves viven en `paper/02_referencias.bib`).*

---

Los modelos de lenguaje grandes responden **generando texto**: la secuencia de tokens *es* la respuesta y su
longitud es el costo. En septiembre de 2026 apareció una familia distinta. Los **modelos de decisión** —o
modelos *System One*— reciben una pregunta y un conjunto **cerrado y etiquetado** de opciones, y responden
con **una opción y una probabilidad**, sin emitir texto: terminan la inferencia con un *readout* de logits en
la posición de cada etiqueta permitida \cite{jev2026blog,jev2026docs}. Su costo de salida es **cero tokens**
por construcción, su latencia es de decenas de milisegundos, y se ofrecen como el componente que decide
«qué hacer» dentro de un sistema mayor: clasificar, enrutar, verificar, abstenerse.

Jev, de TypeSafe, abrió la categoría el 18 de septiembre de 2026 \cite{jev2026blog}. En menos de un mes
floreció un ecosistema **open-source** de pesos abiertos que replica su contrato: **Laya** (421M, la única
implementación que publica el bucle de entrenamiento RLCD completo) \cite{layaRepo}, **Kev** como familia
entrenable \cite{kevRepo}, y una decena de derivados (Nimble, SemIf, Jeff, jev-lite, AnyJev, entre otros)
\cite{nimble,semif,jeff,jevLite,anyjev}. Todos exponen el mismo campo: **`confidence`**.

Ese campo es el que hace útil al modelo. Un despliegue típico no usa la etiqueta a secas: fija un **umbral**
sobre `confidence` y decide *actuar*, o *escalar a un humano* cuando el modelo no está seguro
\cite{chow1970,geifman2017}. El umbral, por tanto, **es** la política. Y aquí está el problema. Aunque el
campo se llame igual en todo el ecosistema, **su definición no es la misma**:

- Jev lo define como **concentración**: `(n·p_max − 1)/(n − 1)`, no como la probabilidad ganadora
  \cite{jev2026docs}. Laya lo define como **entropía normalizada**: `1 − H(p)/log k` \cite{layastudio}.
  Para `noul`, Laya usa `max(p, 1−p)` \cite{layastudio}; `jev-lite` usa directamente `p_max` \cite{jevLite};
  otros usan un prior aprendido.

El efecto es inmediato: una sola distribución sobre tres opciones, `(0.0118, 0.4629, 0.5253)`, produce **tres
valores distintos** de `confidence` — `0.288` con la fórmula de Jev, `0.3199` con la entropía de Laya y
`0.5253` con `p_max` \cite{rohitghumare}. Es el mismo dato; el número cambia según quién lo calcule. Un umbral
calibrado sobre una definición, portado a otra, **no significa lo mismo** — y el ecosistema los porta entre
modelos como si fueran intercambiables.

La afirmación cualitativa «los umbrales no transfieren» ya circula en anécdotas \cite{jebadiah}. Lo que **no
existe** es la medición sistemática: **cuánto** se degrada la cobertura y la precisión del umbral al portarlo
entre definiciones, modelos y datasets. Esa tabla es la que este trabajo construye.

**Contribuciones.**

1. Una **especificación formal** de cada definición de `confidence` en uso, como función de la distribución
   devuelta y de la cardinalidad `n` (dominio, rango, monotonía), con una **proposición** que separa las
   definiciones que son *equivalentes en orden* (transferencia exacta de umbral) de las que no.
2. La librería **`jev-conf-metrics`**, que implementa todas las definiciones y las métricas de calibración y
   discriminación, con **tests de conformidad** contra salidas publicadas.
3. La **matriz de transferencia de umbrales** (definición origen × definición destino × modelo × dataset), el
   **dataset de mediciones crudas** con versión y hash por fila, y el **script regenerador** que la produce
   con un comando.
4. El **pre-registro** de la cobertura objetivo, las definiciones y los datasets antes de la corrida principal.

El trabajo no reporta un hallazgo sobre si la calibración «viaja» o no: entrega el **instrumento con el que se
mide**. Es el patrón de \cite{guo2017}, que no descubrió que las redes modernas están des-calibradas, sino que
dio la métrica y la corrección que el campo entero cita. La aportación sobrevive al hueco: cualquiera que
afirme que los umbrales no transfieren tendrá que **citar la matriz**, no reemplazarla.

**Organización.** La Sección 2 sitúa el trabajo frente a la calibración, las reglas de puntuación propias, la
predicción selectiva y el ecosistema Jev-OSS. La Sección 3 fija el marco teórico: definiciones, calibración
frente a discriminación, la proposición de equivalencia en orden y la definición formal de la transferencia de
umbrales. Las Secciones 4 y 5 describen el método y los resultados.
