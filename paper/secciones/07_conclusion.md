# §7. Conclusión y artefactos (borrador)

*Tesis 1 · Ruta 1 · borrador de la sección 7 · 08-oct-2026*

---

## 7.1. Conclusión

El ecosistema abierto de modelos de decisión tipo Jev comparte un nombre de campo, `confidence`, y una
promesa: que sirve para fijar un umbral de actuación. La medición sobre **23 grupos, 65.185 decisiones y 3.564
celdas** muestra que esa promesa **no viaja entre implementaciones**. Sobre la **misma** distribución, la
definición de `confidence` más alta y la más baja difieren con mediana **0.288** y máximo **0.848**. Portar el
umbral tal cual (copiar la cifra) se equivoca del orden de **cien veces** más que portarlo con el mapa
matemático cuando este existe (0.2337 contra 0.0021, sobre las 312 celdas del nivel principal `raw` sin
empates dominantes). Y en las
celdas de peor caso, el porte directo pierde **toda** la cobertura: quien calibra al 80 % con una definición
puede terminar actuando en el 0 % con otra.

El resultado tiene dos capas. La **escala** hace que el número no viaje aunque el orden se preserve; la
**forma** hace que entre clases de definiciones distintas no exista ni número ni mapa. Dos pares que se creían
distintos resultan ser la **misma** fórmula (la `choice_confidence` de Kev es la de Jev; con `n = 2`,
`C_Jev` y el margen coinciden), lo que da transferencia exacta donde otros ven incompatibilidad.

El aporte no es el hallazgo de que las implementaciones discrepan, que era de esperar. El aporte es el
**instrumento** que permite cuantificar y corregir esa discrepancia, y que sigue valiendo aunque cada
premisa particular se cierre.

## 7.2. Artefactos entregados

| # | artefacto | dónde | estado |
|---|---|---|---|
| 1 | Especificación formal de las definiciones (DEF-1..DEF-8, Proposiciones 1 a 3) | `paper/03_especificacion_confidence.md` + erratas | hecho |
| 2 | Librería `jev-conf-metrics` | `src/jev_conf_metrics/` | hecho (36 tests) |
| 3 | Arnés de conformidad (tests T1..T8) | `tests/` | hecho |
| 4 | Matriz de transferencia de umbrales | `results/matrix/matriz_transferencia.csv` | medida (3.564 celdas) |
| 5 | Dataset de mediciones crudas | `results/crudos/*.jsonl` | medido (65.185 filas, con `row_hash`) |
| 6 | Scripts regeneradores | `src/matriz/{medir,matriz,figura,informe_matriz}.py` | hechos |
| 7 | Figuras (mapas de calor por dataset y cardinalidad) | `results/matrix/heatmap_*.png` / `.pdf` | hechas |
| 8 | Pre-registro con DOI | `paper/04_pre_registro.md` → Zenodo | publicado (10.5281/zenodo.23266795) |
| 9 | Repositorio | `github.com/Arbues/tesis1-jev-confidence` | privado; se abre con el MVP |

Todo el conjunto se regenera con `python -m pytest tests/ -q` seguido de los tres scripts de `src/matriz/`
(§4.5). Ninguna cifra del paper se escribe a mano: todas provienen del informe regenerable.

## 7.3. Trabajo futuro

El arco completo tiene tres etapas, y esta tesis cubre la primera.

- **Tesis 1 (este trabajo, medida).** El instrumento: medir y cuantificar la transferencia de umbrales entre
  las definiciones incompatibles del campo `confidence`.
- **Tesis 2 (mecanismo).** Una vez medido el problema, inducir calibración en el objetivo de entrenamiento,
  no solo por ajuste post-hoc. La pregunta heredada es por qué el término de RL de RLCD no bastó, que la
  literatura reciente ya exploró y que aquí se da por ocupada.
- **Taller de Tesis (teoría).** Las condiciones necesarias y suficientes para que una regla de puntuación
  estrictamente propia induzca un umbral que viaje entre definiciones.

Extensiones inmediatas del instrumento: medir los modelos de 4B a 9B en el Mac Mini, incorporar las
definiciones opacas cuando exista una forma de tratarlas, y repetir la matriz cuando aparezcan nuevas
implementaciones (el instrumento está diseñado para eso, no para un conjunto fijo de modelos).

## 7.4. Disponibilidad

Repositorio `github.com/Arbues/tesis1-jev-confidence` (privado en la versión de tesis; se hace público con
resultados). El pre-registro con el diseño congelado tiene DOI **10.5281/zenodo.23266795**. La librería se
publicará con licencia permisiva junto con la primera versión pública.
