# Erratas de la especificación de `confidence`

*Registro de contradicciones internas encontradas en `paper/03_especificacion_confidence.md` al
implementar la librería `jev-conf-metrics` (08-oct-2026). Cada errata: texto original, por qué es
contradictorio, resolución aplicada y su efecto.*

---

## E1 — El umbral `τ_A` estaba definido con `≤ 1 − q`

**Texto original** (`paper/03_especificacion_confidence.md` §5, paso 1):

> `τ_A = min { τ : (1/|S_cal|)·Σ_{i∈S_cal} 𝕀[C_A(i) ≥ τ] ≤ 1 − q }`

**Por qué es contradictorio.** Los pasos 3 y 4 de la misma sección definen
`cobertura = fracción de ítems con C ≥ τ` y la celda de la matriz como `Δ(A→B) = q − cobertura_B`,
con objetivo de cobertura `q`. Con `q = 0.80`, la condición `≤ 1 − q = 0.20` seleccionaría el umbral
que deja **20 %** de los ítems por encima, no 80 %. El signo está invertido.

**Resolución aplicada.** Se conserva la lectura de los pasos 3–4 (que es la que da sentido a la
matriz y a la noción de «cobertura objetivo»):

> `cobertura(τ) = #{i ∈ S_cal : C_A(i) ≥ τ} / |S_cal|`, decreciente en `τ`
> `τ_A(q) = min { τ ∈ valores observados de C_A : cobertura(τ) ≤ q }`

**Efecto.** Ninguno sobre las mediciones del paso 0 (no usan umbrales). Afecta solo a la matriz, que
aún no se ha medido. **Acción (aplicada el 09-oct-2026):** corregir la línea en la especificación.

---

## E2 — El porte del umbral: ¿el número o el mapa?

**Texto original** (§5, paso 2, y §5, cierre):

> 2. Aplicar `τ_B := τ_A` **tal cual** (sin re-ajuste) al destino.
>
> «Por Proposición 1, las celdas dentro de una clase de equivalencia (y todo `n = 2`) deben salir
> `Δ = 0` salvo ruido de empates»

**Por qué es contradictorio.** Las dos afirmaciones no pueden ser ciertas a la vez. `jev` y `pmax`
son equivalentes en orden vía `φ(x) = (n·x − 1)/(n − 1)`, que es **afín pero no la identidad**: están
en escalas distintas. Si se porta el número `τ` tal cual, un `τ_jev = 0.14` aplicado a `pmax` (que
vive en `[1/n, 1]`) no selecciona el mismo conjunto — en el propio `--selftest` del paso 0 se ve:
`τ_jev = 0.1404` da 80,05 % de cobertura en `jev`, y su espejo `φ⁻¹(τ) = 0.4270` es el que da 80,05 %
en `pmax`. El número **no** transfiere; el **mapa** sí.

De hecho las dos lecturas ya convivían en el repo: §5 paso 2 describe el porte directo, y el
`selftest` de `src/paso0_go_no_go.py` verifica la transferencia «exacta» aplicando `φ⁻¹`.

**Resolución aplicada.** Se reportan **los dos portes**, etiquetados, porque responden a preguntas
distintas y las dos son informativas:

| Columna | Definición | Qué mide | Papel |
|---|---|---|---|
| `delta` | `q − cobertura_B(τ_A)` | lo que le pasa a quien **copia el número** de un sistema a otro (lo que hace el ecosistema) | **métrica principal** de la matriz |
| `delta_mapa` | `q − cobertura_B(ψ(τ_A))`, con `ψ` el mapa cerrado A→B | si la **información** sobrevive cuando se conoce la definición | verifica la Proposición 1 (`Δ = 0`) |

`delta_mapa` solo existe cuando hay mapa (misma clase de equivalencia **y** misma cardinalidad). Al
cruzar `n` no existe (§4.2 de la especificación), y la celda queda sin esa columna — que es,
precisamente, la frontera que la Proposición 1 declara.

**Consecuencia para el claim (y es una buena noticia).** El hallazgo se afila en dos capas:

1. **Capa de escala.** Ni entre definiciones equivalentes en orden transfiere el número: hay que
   aplicar el mapa. Esto es cuantificable celda a celda y no lo dice la anécdota de los 30 tickets.
2. **Capa de forma.** Entre clases distintas (`pmax ↔ ent`, `pmax ↔ margen`) no existe mapa
   estricto: no hay número **ni** mapa que transfiera. Aquí está el peligro real.

**Efecto.** Ninguno sobre el paso 0. La matriz gana una columna y pierde una expectativa mal puesta.
**Acción (aplicada el 09-oct-2026):** corregir el cierre de §5 en la especificación y añadir esta tabla al
marco teórico del paper (§3) como parte del enunciado de la Proposición 1.

---

## E3 (menor) — `noul` no está en `CONFIDENCES`

`paper/03_especificacion_confidence.md` §4.5 lista `C_noul` dentro de las clases de equivalencia,
pero `conf_noul` opera sobre un escalar `π` (primitiva binaria), no sobre una distribución, así que
no puede entrar en el diccionario `CONFIDENCES` de la librería. **Resolución:** `conf_noul` se expone
como función propia, separada de las cuatro analíticas.

**Corrección (28-oct-2026).** La versión original de esta errata añadía «y entra en la matriz solo en el
bloque `n = 2`, comparada contra `p_max`». **Eso no ocurre:** la matriz tiene exactamente cuatro
definiciones (`DEFS = [pmax, jev, ent, margin]` en `src/matriz/matriz.py`, 12 pares) y `noul` no aparece en
ninguna celda ni en ninguna fila cruda. No hace falta medirla: a `n = 2` es idéntica a `p_max`
(`max(π, 1−π) = p_max`), así que el bloque de `n = 2` ya la representa. El paper lo decía mal en §4.3
(`.md` y `.tex`) y se corrigió en el mismo paso.

---

## E4 — `output_tokens = 0` no era una afirmación sobre el contador

**Texto original** (`paper/03_especificacion_confidence.md` §1, `paper/01_marco_teorico.md` §10,
`paper/secciones/04_metodo.md` §4.1, `paper/secciones/05_resultados.md` §5.2 y `paper/04_pre_registro.md`):

> «no genera texto, luego `output_tokens = 0`» · «`output_tokens = 0` **por construcción**».

**Por qué estaba mal.** La premisa (no hay bucle de decodificación, la inferencia termina con un
*readout* de logits) es correcta y **medida** en los brazos de pesos abiertos: `output_tokens = 0` en
las 65.185 filas de `results/crudos/` y en `results/raw/`. Lo que **no** se sigue de la premisa es el
valor del **contador** del proveedor de pago. La documentación oficial de TypeSafe solo garantiza que
la salida **no se cobra** y sus ejemplos publican `output_tokens` 12 (OpenAPI `Usage`) y 212 (página
`primitives/choice`) — ver `docs/adaptador-typesafe-contrato.md` §0, punto A.

**Resolución (12-oct-2026).** Se separa el mecanismo del contador: el paper afirma que **no se genera
texto** y reporta `output_tokens = 0` **solo donde se midió** (brazos de pesos abiertos). El contador de
la API de TypeSafe se reporta cuando exista una llamada real (brazo pagado). `paper/04_pre_registro.md`
**no se toca**: es el texto depositado con DOI (10.5281/zenodo.23266795) y su frase se refiere, con
razón, a los pesos abiertos.

**Medido el 12-oct-2026 (t440, 6 llamadas reales a `api.typesafe.ai`).** El contador de la API pagada
**no es 0**: `output_tokens` = **71** (3 preguntas), **58** (1 pregunta, n=5) y **31** (1 pregunta, n=2);
`input_tokens` 308–406 por ítem. La decisión de separar mecanismo y contador queda **confirmada por
medición**, no por prudencia. Añadido en `docs/adaptador-typesafe-contrato.md` §11.

**Corrección (28-oct-2026).** La frase de la sección «Por qué estaba mal» —«`output_tokens = 0` en las
65.185 filas de `results/crudos/` **y en `results/raw/`**»— es **falsa en su segunda mitad**: en
`results/raw/` el paso 0 midió para Kev `output_tokens_total = 869.310`
(`results/raw/paso0_summary_kev_kev-latest.json`). Lo que vale 0 es `results/crudos/` (la corrida
confirmatoria), porque **su adaptador no propaga el campo** (`medir.py` lee `usage.output_tokens` y los
backends de pesos abiertos no lo rellenan): ese 0 **no es una medición del contador**. El paper se ajustó
en el mismo paso: §4.1 ya no afirma «todas con `output_tokens = 0` verificado», la tabla de §5.1 lleva una
nota sobre la columna y §5.7 atribuye el 869.310 al **paso 0**, no a la corrida confirmatoria.


---

## E6 (menor) — la fecha del pre-registro y su archivo depositado

**Texto original** (`paper/04_pre_registro.md`, cabecera): «Estado: **PUBLICADO**. DOI: **10.5281/zenodo.23266795**
(Zenodo, 08-oct-2026)». La regla del propio archivo es que, una vez publicado, **no se modifica**.

**Qué se encontró (verificado contra la API de Zenodo, 12-oct-2026).** El registro declara
`publication_date = 2026-10-09` y `created = 2026-10-09T16:58Z`; la edición posterior (afiliación) subió la
revisión a 5 pero **no** tocó ni la fecha ni el DOI. Además, el archivo **depositado** es una revisión previa a
la publicación: dice «Estado: listo para subir», no contiene su propio DOI y difiere del local **solo** en esa
cabecera de estado (el método es idéntico; 109 líneas en ambos).

**Resolución.** El archivo **no se toca** (su inmutabilidad es justamente lo que el pre-registro promete) y **no**
se crea una versión nueva del registro solo por la cabecera. La discrepancia queda registrada aquí y en
`STATE.json`. Lo único que se corrige es lo que se afirma **fuera** del archivo: la fecha canónica del
pre-registro es **09-oct-2026** (la que declara Zenodo).

---

## E5 — `score` y `choice` no comparten la fórmula de `confidence`

**Texto original** (`paper/03_especificacion_confidence.md` §1, tabla de primitivas): `choice` y `score`
aparecían devolviendo ambos «`confidence`», sin distinguir la fórmula.

**Por qué está mal.** La documentación oficial de TypeSafe (`docs.typesafe.ai/confidence`, consultada el
12-oct-2026) da **dos** fórmulas para el mismo campo según la primitiva:

```
choice:  confidence = (p_max − 1/n) / (1 − 1/n)                  ← es C_jev (solo cuenta el máximo)
score:   confidence = max(0, 1 − Σᵢ pᵢ·|i − m| / MAD_unif)       ← ordinal, sensible a la distancia
         con MAD_unif = (1/n)·Σᵢ |i − (n−1)/2|
noul:    no devuelve `confidence`; la doc sugiere |2p − 1| = 2·max(p, 1−p) − 1
```

Con tres niveles, `(0, 0.5, 0.5)` da 0.25 y `(0.5, 0, 0.5)` da 0 con la fórmula de `score`, mientras
que la de `choice` daría 0.25 a las dos.

**Resolución.** Se documenta como una **quinta definición** del campo (dispersión ordinal) y se anota que
la `score_confidence` de Kev pertenece a esa misma familia — lo que confirma que Kev espeja el adaptador
de referencia de TypeSafe.

### E5-bis — decisión del autor (19-oct-2026): entra como EXTENSIÓN DECLARADA

El autor decidió que `conf_score` **sí entra**, porque comparar la definición de Jev con las de los modelos
locales es parte del objetivo del paper. Se implementó sin tocar nada sellado:

| Qué | Dónde | Nota |
|---|---|---|
| Función y constante | `src/jev_conf_metrics/definiciones.py` → `conf_score`, `score_mad_unif`, `CONFIDENCES_EXT` | `CONFIDENCES` sigue con las cuatro del pre-registro; `all_confidences(p)` no cambia de salida |
| Tests | `tests/test_conf_score.py` (11) | ejemplo oficial de TypeSafe + no-invariancia a permutación + suelo en 0 |
| Medición | `src/matriz/extension_conf_score.py` → `results/matrix/EXTENSION_CONF_SCORE.md` y `.csv` | 5.505 decisiones de `sst5`, 5 configuraciones |
| Alcance | solo `sst5` (5 niveles ordinales) | `wanli`, `banking77`, `clinc150`, `typed-decisions` son nominales: no se inventa la escala |
| Verificación en vivo | la API real devuelve exactamente `conf_score`: `probs=[0.43,0.57,0,0,0]` → `confidence_reportada = 0.64`, fórmula = 0.6417 | 20-oct-2026, brazo pagado |

**Cifras (19-oct-2026):** brecha mediana entre la definición más alta y la más baja de la misma
distribución: **0.272** con cuatro definiciones → **0.290** con cinco. ECE global de la corrida:
`score` 0.241 · `margin` 0.237 · `pmax` 0.204 · `ent` 0.199 · `jev` 0.184.
La quinta definición **cambia de signo según el modelo**: en el control crudo Qwen es la más pesimista en
el 70.3 % de las filas; en Laya-multilingual, la más optimista en el 92.6 %.


---

## E8 — `precision()` devolvía la confianza media, no el acierto

**Qué se encontró (28-oct-2026).** `precision(confs, correct, tau)` en
`src/jev_conf_metrics/transferencia.py` devolvía `sum(confianzas seleccionadas) / nº seleccionados`, es
decir, la **confianza media** de los ítems con `C ≥ τ`, en lugar del **acierto** entre esos ítems que define
la especificación (§5, paso 3: `precisión_B = Σ 𝟙[C_B ≥ τ]·a_i / #{C_B ≥ τ}`). El argumento `correct`
llegaba a la función y no se usaba.

**Efecto.** `precision_A` y `precision_B` de las **3.564 celdas** de `results/matrix/matriz_transferencia.csv`
(7.128 valores) y de la tabla §4 de `RESUMEN_MATRIZ.md` son confianza media, no precisión: en
`Qwen/banking77` la tabla publicaba **0.204** donde la accuracy del modelo es **0.0156**. El PDF del paper
no imprime esas columnas (sus tablas dan `Δ`, cobertura e IC), pero §3.5 promete medir «la cobertura y la
precisión», y el CSV es un artefacto publicado.

**Resolución (aplicada el 28-oct-2026).**
1. Función corregida (`sel = [a for c, a in …]`) y **dos tests de regresión** en `tests/test_transferencia.py`
   (el caso mínimo `precision([.9,.8,.7,.2],[1,0,1,0],.7) = 0.667` y la coherencia con `celda`).
2. `informe_matriz.py` **recalcula la precisión desde los crudos** para la tabla que publica
   (`precisiones_raw`, nivel `raw`, `q = 0.80`) y la imprime con una nota que remite a esta errata.
3. El **CSV sellado no se reescribe**: recalcular esas dos columnas exige volver a correr la matriz completa
   y el nivel `L0` cuesta ~44 min por grupo con 77 clases (~19 h en total). Se corrigen en la próxima
   regeneración completa del artefacto. `Δ`, `τ`, IC y `p` **no dependen** de `precision`, así que el resto
   del CSV se regenera byte a byte idéntico y **ninguna cifra del paper cambia**.
4. §4.5 del paper declara la excepción donde antes prometía que cualquier diferencia es un bug.
