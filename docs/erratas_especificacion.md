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
como función propia y entra en la matriz solo en el bloque `n = 2`, comparada contra `p_max` (con
quien es idéntica: `max(π, 1−π) = p_max`). Ya estaba así en la práctica; se documenta para que no
parezca un olvido.

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
de referencia de TypeSafe. Que entre o no en la librería y en la matriz **después** del pre-registro es
decisión del autor (afecta artefactos sellados). Detalle del contrato: `docs/adaptador-typesafe-contrato.md`.

