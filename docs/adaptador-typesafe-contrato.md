# Contrato de la API directa de TypeSafe (System One / Jev) para el adaptador del pipeline

> **Insumo para el adaptador `typesafe-jev`** de la matriz de transferencia de umbrales (Ruta 1).
> Mide el **modelo real** por vía directa con clave de TypeSafe, **sin gateways** de terceros
> (Vercel / Netlify) ni revendedores.
>
> - **Fecha de consulta de todas las fuentes: 12-oct-2026** (America/Lima, UTC−05:00).
> - **Autor del documento:** agente (Hermes). Idioma: español. Regla **D4** del proyecto: cada cifra
>   con su fuente y cada fila marcada *medido aquí* o *auto-reportado*.
> - **Restricción cumplida:** no se escribió, solicitó ni usó ninguna clave; no se intentó
>   autenticar. Todo lo verificable sin clave viene de documentación **pública oficial** y del
>   **OpenAPI**; lo que exige una clave para confirmarse está aislado en **§8**.
> - **Estado global:** **parcialmente verificado**. §§1–7 = verificado en fuentes oficiales.
>   §8 = pendiente de una llamada autenticada.

---

## 0. Semáforo de verificación (qué está confirmado y qué no)

| # | Afirmación | Estado | Fuente (consulta 12-oct-2026) |
|---|---|---|---|
| 1 | URL base `https://api.typesafe.ai`, ruta `/v1/systemone` | ✅ verificado | OpenAPI `info`+`paths`; `docs.typesafe.ai/api` |
| 2 | Cabecera `Authorization: Bearer <API_KEY>` (esquema `HTTPBearer`) | ✅ verificado | OpenAPI `securitySchemes.HTTPBearer`; `docs.typesafe.ai/api` |
| 3 | Variable de entorno `TYPESAFE_API_KEY` | ✅ verificado | `docs.typesafe.ai/introduction/quickstart`; SDK `ENV` |
| 4 | Tres primitivas: `choice`, `score`, `noul` con sus campos de respuesta | ✅ verificado | OpenAPI `components.schemas`; páginas de primitivas |
| 5 | `choice` con `criteria` (mapa) y **≤255 opciones** | ✅ verificado (prosa) | `docs.typesafe.ai/primitives/choice` |
| 6 | `score` con `criteria` (array ordenado) y **2–10 niveles** | ✅ verificado (prosa) | `docs.typesafe.ai/primitives/score` |
| 7 | `noul` devuelve **solo** `noul` ∈ [0,1], **sin** `confidence` | ✅ verificado | OpenAPI `NoulAnswer`; `docs.typesafe.ai/primitives/noul` |
| 8 | `confidence` de `choice` = `(p_max − 1/n)/(1 − 1/n)` = `(n·p_max − 1)/(n−1)` | ✅ verificado | `docs.typesafe.ai/confidence` (§cálculo) |
| 9 | `confidence` de `score` usa **otra** fórmula (con `MAD_unif`, sensible a distancia) | ✅ verificado | `docs.typesafe.ai/confidence` |
| 10 | Estado compartido: un `state` por request; preguntas **en paralelo y aisladas** | ✅ verificado | `docs.typesafe.ai/concepts/state`; `primitives` |
| 11 | **No hay endpoint de lote**; el lote es el mapa `questions` | ✅ verificado | OpenAPI `paths` (solo 2 rutas) |
| 12 | Límites: 100 000 tok/s, 80 req/s, 64k contexto, 32k state+1 pregunta | ✅ verificado | `docs.typesafe.ai/models` |
| 13 | Errores `401 / 422 / 429 / 529` | ✅ verificado | `docs.typesafe.ai/api`; `help.typesafe.ai` |
| 14 | Versión del modelo en `response.model` (ID versionado, p.ej. `jev-1.13.0`) | ✅ verificado | `docs.typesafe.ai/models` |
| 15 | Precio 0.042 USD/Mtok entrada, salida gratis | ✅ verificado | `docs.typesafe.ai/models` |
| 16 | Valor real de `usage.output_tokens` en una llamada | ⚠️ **NO verificado** — la doc se contradice con el dato conocido del proyecto (ver §8-A) | OpenAPI ejemplo `=12`; `primitives/choice` ejemplo `=212` |
| 17 | Cadena exacta que devuelve `response.model` para `jev-latest` | ⚠️ **NO verificado** | requiere llamada autenticada |
| 18 | Forma del cuerpo JSON de `401` | ⚠️ **NO verificado** (la doc describe el status, no el cuerpo) | requiere llamada |
| 19 | ¿La API **rechaza** >255 opciones o >10 niveles? | ⚠️ **NO verificado** (el esquema no pone tope) | requiere llamada |
| 20 | ¿`model` acepta un ID versionado fijo (`jev-1.13.0`)? | ⚠️ **NO verificado** (la doc dice que sí) | requiere llamada |

**Cómo se obtuvo:** lectura de la documentación oficial en `docs.typesafe.ai`, descarga del contrato
máquina-legible `https://api.typesafe.ai/openapi.json` (HTTP **200**, 14 158 bytes, `info.version` =
`0.2.0`), y el centro de ayuda `help.typesafe.ai`. `console.typesafe.ai` **exige login** (un fetch
automatizado previo devolvió **403**; hoy devuelve la pantalla de acceso). Se consultaron además
espejos de la comunidad (`jevwiki.ai`, `jevai.guide`, `jevapi.dev`, `jevapi.org`) **solo para
contraste**; **no se usan como fuente de verdad** y donde divergen se indica.

---

## 1. URL base y versión del API

| Dato | Valor | Estado |
|---|---|---|
| URL base | `https://api.typesafe.ai` | ✅ verificado |
| Endpoint principal | `POST /v1/systemone` | ✅ verificado |
| Endpoint auxiliar | `GET /v1/models` | ✅ verificado |
| Versión de ruta | `v1` | ✅ verificado |
| Versión del documento OpenAPI | `info.version = 0.2.0`, `openapi = 3.1.0`, `info.title = "TypeSafe"` | ✅ verificado |
| `operationId` | `systemone_v1_systemone_post`, `models_v1_v1_models_get` | ✅ verificado |

> **Aviso de doble numeración:** la ruta es `v1` pero el documento OpenAPI se versiona aparte
> (`0.2.0`). Son números **independientes**. Para la trazabilidad de D4, la ruta `v1` es lo estable.

`GET /v1/models` es el descubridor de modelos: devuelve `name`, `description` y `release_date`
(`YYYY-MM-DD`) de los nombres aceptables en el campo `model`.

**No existe** ningún endpoint `/v1/batch`, ni `/preview/evaluation` (reemplazado por `/v1/systemone`)
ni `/v1/systemone/{id}`; el contrato público define **exactamente dos rutas**.

---

## 2. Autenticación

| Elemento | Valor exacto | Estado |
|---|---|---|
| Cabecera | `Authorization` | ✅ verificado |
| Forma del valor | `Bearer <API_KEY>` (esquema OpenAPI `HTTPBearer`: `type: http`, `scheme: bearer`) | ✅ verificado |
| Cabecera de contenido | `Content-Type: application/json` (única aceptada en el `POST`) | ✅ verificado |
| Variable de entorno | **`TYPESAFE_API_KEY`** (la leen ambos SDK; el HTTP directo la usa para construir la cabecera) | ✅ verificado |
| Variable de base URL (SDK) | `TYPESAFE_BASE_URL` (por defecto `https://api.typesafe.ai`) | ✅ verificado |
| Dónde se crea la clave | consola: `https://console.typesafe.ai` (ruta de claves **`/keys`**; escritos antiguos citan `/settings/keys`) | ✅ verificado (docs); ⚠️ `/keys` requiere login |
| Cabeceras extra que añaden los SDK | petición: `User-Agent`, `Accept`, `X-TypeSafe-SDK`, `X-TypeSafe-Runtime`, `X-TypeSafe-Retry-Count`; respuesta: `x-typesafe-request-id`, `retry-after`, `retry-after-ms`. **Ninguna es obligatoria** para el HTTP directo | ✅ verificado |

Forma de uso en el adaptador (**la clave nunca se escribe en el código ni en los crudos**, solo se
lee del entorno):

```bash
# La clave vive SOLO en el entorno del proceso que ejecuta el adaptador.
export TYPESAFE_API_KEY='<tu-clave>'      # no la pegues en el repo ni en logs
# El adaptador lee os.environ["TYPESAFE_API_KEY"] y arma: {"Authorization": f"Bearer {key}"}
```

Comprobación de presencia **sin mostrar el secreto** (el autor lo corre):

```bash
python3 -c "import os; print(bool(os.getenv('TYPESAFE_API_KEY')))"   # True = presente
```

Una clave ausente o inválida devuelve **`401 Unauthorized`**.

---

## 3. Las tres primitivas: request y response reales

### 3.0. Sobre del request (igual para las tres primitivas)

`POST https://api.typesafe.ai/v1/systemone`

```json
{
  "state": "Mi tarjeta fue cargada dos veces. Ayuda.",
  "model": "jev-1.13.0",
  "questions": {
    "<id-que-tú-eliges>": { "type": "noul|choice|score", "...": "..." }
  }
}
```

| Campo | Tipo | Obligatorio | Notas |
|---|---|---|---|
| `state` | `string \| object \| array` (no `null`) | **sí** | El contenido que **todas** las preguntas del request evalúan. Un `state` por request. |
| `model` | `string` | **sí** | Alias (`jev-latest`, `jev-preview`) **o** ID versionado (`jev-1.13.0`). |
| `questions` | `map<string, Question>` | **sí**, `minProperties: 1` | Las claves las eliges tú; **no** se envían al modelo ni se usan en la inferencia. La respuesta las reutiliza. |

> ⚠️ **Nombres de campo reales vs. nombres informales.** En el HTTP de TypeSafe el campo de
> opciones/niveles se llama **`criteria`** en las tres primitivas. Varios sitios de terceros
> (`jevai.guide`, `jevapi.dev`, `jevapi.org`) muestran `"options"` para choice y `"scale"` para
> score: **esos nombres no existen en el esquema oficial** y un `POST` con ellos sería inválido.
> Usar **`criteria`** siempre.

### 3.1. `choice` — elegir una de N opciones *sin orden*

**Request (campos reales):**

```json
{
  "state": "Ayuda: mi tarjeta fue cargada dos veces.",
  "model": "jev-1.13.0",
  "questions": {
    "department": {
      "type": "choice",
      "instructions": "¿Qué equipo debería atender esto?",
      "criteria": {
        "billing":   "Cargos, facturas, problemas de pago",
        "technical": "Bugs o problemas de integración",
        "sales":     "Precios o preguntas de cuenta"
      }
    }
  }
}
```

`criteria` de un `choice` es un **objeto/mapa** (nombre de la opción → descripción; un `null` deja
que el nombre hable por sí solo). **Máximo 255 opciones** (prosa oficial; el OpenAPI **no** fija
`maxProperties`).

**Response real (recortada a una pregunta):**

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "department": {
      "type": "choice",
      "choice": "billing",
      "confidence": 0.18,
      "probabilities": { "billing": 0.45, "technical": 0.28, "sales": 0.27 }
    }
  },
  "usage": { "input_tokens": 214, "output_tokens": 0 }
}
```

| Campo del answer | Tipo | Descripción |
|---|---|---|
| `type` | `"choice"` | Discriminante. |
| `choice` | `string` | La opción de **mayor probabilidad** (una de las claves de `criteria`). |
| `probabilities` | `map<string, number>` | Distribución completa sobre **todas** las opciones; "suman **aproximadamente** 1". |
| `confidence` | `number` 0–1 | Concentración de la distribución (ver §3.4). |

### 3.2. `score` — puntuar en una escala ordinal

**Request:**

```json
{
  "state": "El botón de exportar tumba la página de ajustes en Safari; en Chrome funciona.",
  "model": "jev-1.13.0",
  "questions": {
    "bug_severity": {
      "type": "score",
      "instructions": "¿Qué tan grave es el problema?",
      "criteria": [
        "Cosmético; sin impacto en la funcionalidad",
        "Funcionalidad degradada, pero hay forma de evitarlo",
        "Bloqueante; no hay forma de evitarlo"
      ]
    }
  }
}
```

`criteria` de un `score` es un **array ordenado** (de menor a mayor); la posición fija el nivel,
empezando en **0**. **2–10 niveles** (prosa oficial: "al menos dos… la API acepta hasta 10"; el
OpenAPI solo fija `minItems: 1`, **sin** `maxItems`).

**Response real:**

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "bug_severity": {
      "type": "score",
      "score": 1.43,
      "confidence": 0.35,
      "legend": {
        "0": "Cosmético; sin impacto en la funcionalidad",
        "1": "Funcionalidad degradada, pero hay forma de evitarlo",
        "2": "Bloqueante; no hay forma de evitarlo"
      },
      "probabilities": { "0": 0.0, "1": 0.57, "2": 0.43 }
    }
  },
  "usage": { "input_tokens": 178, "output_tokens": 0 }
}
```

| Campo del answer | Tipo | Descripción |
|---|---|---|
| `type` | `"score"` | Discriminante. |
| `score` | `number` | **Promedio ponderado por probabilidad** de los niveles; **puede caer entre niveles** (p. ej. 1.57). No es un entero. |
| `legend` | `map<string, string\|object\|array>` | Nivel (clave string `"0"`…`"n-1"`) → su descripción. |
| `probabilities` | `map<string, number>` | Probabilidad de cada nivel, **mismas claves que `legend`**; suman ≈ 1. |
| `confidence` | `number` 0–1 | Concentración, con la fórmula propia de `score` (ver §3.4). |

> **Detalle de serialización (HTTP):** en la respuesta HTTP de `score`, las claves de `probabilities`
> y `legend` son **strings** (`"0"`, `"1"`, …). En el SDK de Python se coercen a `int`. El adaptador
> que habla HTTP **debe ordenar por número**, no confiar en el orden del JSON.

### 3.3. `noul` — sí/no como probabilidad (SIN `confidence`)

**Request:**

```json
{
  "state": "Ayuda: mi tarjeta fue cargada dos veces.",
  "model": "jev-1.13.0",
  "questions": {
    "is_refund_request": {
      "type": "noul",
      "instructions": "¿El cliente pide un reembolso?",
      "criteria": {
        "true":  "Pide explícitamente que le devuelvan el dinero",
        "false": "No menciona un reembolso"
      }
    }
  }
}
```

`criteria` de `noul` es **opcional** (objeto con `true` y `false`). `instructions` describe la
afirmación a juzgar.

**Response real:**

```json
{
  "model": "jev-1.13.0",
  "answers": {
    "is_refund_request": { "type": "noul", "noul": 0.91 }
  },
  "usage": { "input_tokens": 96, "output_tokens": 0 }
}
```

| Campo del answer | Tipo | Descripción |
|---|---|---|
| `type` | `"noul"` | Discriminante. |
| `noul` | `number` 0–1 | Probabilidad de "sí". **No hay** `confidence`, ni `probabilities`, ni `legend`. |

> **Confirmado contra el proyecto:** el campo `confidence` de `choice` **no es** la probabilidad
> ganadora; es la concentración `(n·p_max − 1)/(n − 1)` (= `conf_jev`). El `noul` **no** trae
> `confidence`: la incertidumbre ya vive en el propio número (0.5 = indeciso).

### 3.4. Fórmulas de `confidence` (publicadas por TypeSafe)

TypeSafe **publica** las fórmulas exactas y aclara que son "una forma razonable, no la única":

- **`noul`** — *no* se devuelve `confidence`. Sustituto sugerido por la doc: `|2p − 1|`.
- **`choice`** (n opciones, p_max = prob. de la opción elegida):

  ```
  confidence = (p_max − 1/n) / (1 − 1/n)  =  (n·p_max − 1) / (n − 1)
  ```

  **Es exactamente la definición `jev` del proyecto** (concentración). Solo cuenta el máximo:
  `(0.6, 0.3, 0.1)` y `(0.6, 0.2, 0.2)` dan ambas 0.4.

- **`score`** (n niveles 0…n−1, m = nivel más probable): **fórmula distinta**, sensible a la
  distancia, con `MAD_unif = (1/n)·Σᵢ |i − (n−1)/2|`:

  ```
  confidence = max(0, 1 − Σᵢ pᵢ·|i − m| / MAD_unif)
  ```

  Ejemplo oficial: niveles `(0, 0.57, 0.43)`, m=1, spread 0.43, MAD_unif 2/3 → confidence ≈ **0.35**.
  Con tres niveles, `(0, 0.5, 0.5)`→0.25 y `(0.5, 0, 0.5)`→0; la fórmula de `choice` daría 0.25 a
  ambas.

> **Consecuencia directa para la tesis:** la `confidence` que devuelve el API es **`conf_jev` para
> `choice`** pero **una quinta definición para `score`** (no está en la lista del proyecto:
> `pmax, jev, ent, margin`). Para una fila `score`, el campo auto-reportado del API **no** equivale
> a `conf_jev`; hay que recalcular `conf_jev` desde `probabilities` si se quiere esa definición.

### 3.5. Sobre de la response (top-level, idéntico para las tres)

```json
{
  "model": "jev-1.13.0",
  "answers": { "<mismo-id>": { "type": "...", "...": "..." } },
  "usage":   { "input_tokens": 214, "output_tokens": 0 }
}
```

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `model` | `string` | sí | **ID versionado que realmente respondió**; puede diferir del alias enviado. Se registra (D4). |
| `answers` | `map<string, Answer>` | sí, `minProperties: 1` | Una entrada por pregunta, con tus claves; `type` coincide con la pregunta. |
| `usage.input_tokens` | `integer` | sí | Tokens de entrada **facturables**. |
| `usage.output_tokens` | `integer` | sí | Tokens de salida. **"Actualmente gratis"** (coste 0). ⚠️ El **conteo** no es necesariamente 0 — ver §8-A. |

---

## 4. Lote y estado compartido

**No hay endpoint de lote.** El "lote" **es el mapa `questions`**: en **un** `POST /v1/systemone`
se declaran N preguntas y vuelven N respuestas, como un solo request.

**Cómo se declara el estado compartido:** simplemente se pone **un** `state` en el request. **No hay
flag** `shared`/`context`: es implícito. La documentación oficial lo dice así: *"All questions see
the same state and are evaluated independently"* y *"Every question is evaluated in parallel and in
isolation against the same state in one go. … does not create context-rot."*

| Propiedad | Valor |
|---|---|
| Preguntas por request | `minProperties: 1`; **sin máximo documentado** (el tope real es el presupuesto de tokens de §5) |
| Tipos mezclables | Sí: `noul`, `choice` y `score` conviven en el mismo mapa |
| Estado por request | **Uno**; se comparte por todas las preguntas de ese request |
| Aislamiento | Cada pregunta se evalúa **independientemente**; **no** ve las respuestas de las otras |
| Distribución conjunta | **No existe** (coherente con el dato conocido del proyecto) |

**Implicación de diseño para el adaptador.** Como el `state` es único y cada ítem de un dataset es
un `state` distinto, medir N ítems = **N requests** (una pregunta `choice`/`score` por ítem). El
mapa `questions` ahorra *round-trips* solo cuando **varias preguntas comparten el mismo `state`**;
**no** permite empaquetar ítems independientes en un request. Consecuencia para el pendiente "costo
por 1 000 decisiones": ≈1 000 requests de entrada; el costo es ≈`1000 × (tokens_entrada_del_ítem) ×
0.042 USD / 1e6`, con salida gratis.

`GET /v1/models` no es de lote; solo lista modelos.

---

## 5. Límites oficiales y códigos de error

### 5.1. Límites (oficiales, `docs.typesafe.ai/models`, consulta 12-oct-2026)

| Límite | Valor | Notas |
|---|---|---|
| Contexto por request | **64 000 tokens** | Cubre `state` **+** todas las preguntas juntas. |
| Presupuesto `state` + 1 pregunta | **32 000 tokens** | `state` más la pregunta **más larga**. |
| Opciones por `choice` | **≤ 255** | Prosa oficial; el OpenAPI **no** fija `maxProperties` → validar el conteo del lado cliente. |
| Niveles por `score` | **2–10** | Prosa oficial ("al menos dos… hasta 10"); el OpenAPI solo `minItems: 1`, **sin** máximo. |
| Rate limit | **100 000 tokens/segundo** y **80 requests/segundo** | "Ajuste dinámico; puede cambiar sin aviso". Superar cualquiera devuelve `429`. |
| Entrada | **Solo texto**: `string`, objeto JSON o array de texto | Sin imagen/audio/vídeo. Inglés primario; otros idiomas (incl. CJK) con menor exactitud. |
| Precio | **$0.042 / Mtok** entrada; **salida gratis** | Coincide con el dato ya confirmado en el catálogo de Vercel. |

> ⚠️ **Divergencia de terceros.** Los sitios `jevai.guide` / `jevapi.org` publican "250k tok/s y
> 1200 req/min". **No coinciden** con la doc oficial (100k tok/s, 80 req/s). Se usa el valor
> **oficial**; el de terceros queda descartado.

### 5.2. Errores (código → causa)

| HTTP | Significado | ¿Documentado en el OpenAPI? | Notas |
|---|---|---|---|
| **401** `Unauthorized` | Clave ausente o inválida | Sí (referido por el esquema de seguridad) | Revisar la cabecera `Authorization`. |
| **422** `Unprocessable Entity` | El cuerpo no validó (campo faltante, pregunta malformada) | Sí | Cuerpo = `HTTPValidationError`: `{ "detail": [ { "loc": [...], "msg": "...", "type": "...", "input": ..., "ctx": ... } ] }`. Ej.: `loc:["body","questions","urgency","score","criteria"]`, `msg:"Field required"`, `type:"missing"`. |
| **429** `Too Many Requests` | Se superó un rate limit | No (solo prosa) | Honrar `Retry-After` / `retry-after-ms`; backoff exponencial. |
| **529** `Overloaded` | TypeSafe saturado temporalmente | No (solo prosa) | Reintentar con backoff; revisar el estado del servicio. |
| **403** | **No** documentado como error del API | — | El 403 observado fue de `console.typesafe.ai` (bloqueo anti-bot), **no** del API de datos. |

Reintentos recomendados por la doc: backoff exponencial en `429`/`529`; los SDK reintentan por
defecto en `{408, 429, 500–599}` y respetan `Retry-After`. `help.typesafe.ai` aclara la diferencia
**429 = rate limit** vs **529 = sobrecarga**.

---

## 6. Identificación de la versión del modelo (build medido) y regla D4

**Cómo saber qué build se midió:**

- El request lleva `model` = alias (`jev-latest`, `jev-preview`) **o** ID versionado (`jev-1.13.0`).
  El alias **mueve** cuando sale una release nueva → para reproducer, **fijar el ID versionado**.
- La **response** trae `model` = **ID versionado que respondió** (puede diferir del alias): *"May
  differ from the alias supplied in the request" … "log it to know which version answered."*
- `GET /v1/models` devuelve `name`, `description`, `release_date` (`YYYY-MM-DD`) de los alias
  disponibles para la cuenta. Los IDs versionados **se aceptan** aunque no aparezcan en la lista.
- **No** se expone hash de pesos, ni commit, ni `revision` del modelo (a diferencia de Laya/Kev en
  el Hub). El único identificador de build público es la **cadena de versión** (`jev-1.13.0`).

**Cómo registrarlo por fila (D4):** el adaptador, por cada respuesta, escribe en la fila del crudo:

| Columna del crudo | De dónde sale |
|---|---|
| `model` | handle fijo del adaptador, p. ej. `"typesafe/jev"` (para que la matriz lo agrupe igual que `laya`, `kev`, …) |
| `model_revision` | **`response.model`** (p. ej. `"jev-1.13.0"`). Es el build medido. |
| `output_tokens` | `response.usage.output_tokens` (ver §8-A) |
| `backend` | `"typesafe-api"` (vía directa, no gateway) |
| (opcional, D4) | `x-typesafe-request-id` de la response + `timestamp` UTC + el alias pedido, para trazabilidad fina |

Esto cumple la regla del proyecto: **cada fila declara el modelo y su versión**, y distingue lo
*medido aquí* (`conf_*`, calculadas de `probabilities`) de lo *auto-reportado* (`confidence_reported`).

---

## 7. Mapeo response TypeSafe → fila del proyecto

Esquema real de `results/crudos/*.jsonl` (verificado en el repo, 12-oct-2026): `id, config,
workflow, question, type, labels, probs, gold_label, y, n_options, correct, output_tokens,
answer_confidence, confidence_reported, act_probability, gold_score, pred_score, gold_probs,
conf_jev, conf_ent, conf_pmax, conf_margin, model, model_revision, dataset, backend, row_hash`.

El adaptador recibe `ans = response.answers["<id>"]` (con `response.usage` y `response.model`
adjuntos) y llama a `_fila(...)` de `src/matriz/medir.py`. Mapeo:

| Columna de la fila | Origen en la response TypeSafe | ¿Calculable con la respuesta directa? | Nota |
|---|---|---|---|
| `type` | `answers.<id>.type` | ✅ | `choice` / `score` / `noul` |
| `labels` | claves de `criteria` (choice) o claves de `legend`/`probabilities` (score) | ✅ | El adapter tolera nombres **o** índices `"0".."n-1"` con `legend` (ya previsto en `_fila`) |
| `probs` | `answers.<id>.probabilities` **ordenados** por `labels` | ✅ | **Renormalizar** a suma 1 (la doc dice "≈ 1") antes de `ent`/`jev` |
| `n_options` | `len(probs)` | ✅ | |
| `gold_label`, `y`, `gold_probs`, `gold_score` | **—** (vienen del dataset) | ❌ no están en la response | Los provee el caso/`gold_q` del dataset |
| `correct` | **—** | ❌ no está en la response | Se **calcula** local: `argmax(probs) == y`. La API nunca dice si acertó |
| `output_tokens` | `response.usage.output_tokens` | ✅ (con reserva) | Ver §8-A: la doc contradice el supuesto "= 0" |
| `confidence_reported` | `answers.<id>.confidence` | ✅ (choice/score) | **Auto-reportado**. Para `choice` = `conf_jev`; para `score` = fórmula propia; para `noul` = **null** |
| `answer_confidence` | **—** (TypeSafe no lo tiene; era de Laya) | ❌ | Dejar **null** |
| `act_probability` | **—** (TypeSafe no devuelve objeto `action`) | ❌ | Dejar **null** |
| `pred_score` | `answers.<id>.score` | ✅ (solo `score`) | Puede ser fraccionario |
| `conf_pmax` | `max(probs)` | ✅ | |
| `conf_jev` | `(n·p_max − 1)/(n−1)` sobre `probs` | ✅ | Para `choice` coincide con el `confidence` del API |
| `conf_ent` | `1 − H(probs)/log n` sobre `probs` | ✅ | |
| `conf_margin` | `p₍₁₎ − p₍₂₎` sobre `probs` | ✅ | Margen top-2 |
| `model` | handle del adaptador | ✅ | p. ej. `"typesafe/jev"` |
| `model_revision` | `response.model` | ✅ | El build medido, p. ej. `"jev-1.13.0"` |
| `dataset`, `backend`, `row_hash` | locales | ✅ | `row_hash` se calcula sobre la fila (igual que hoy) |

### 7.1. Definiciones que **NO** se pueden calcular con la respuesta directa

1. **Sobre un `noul`:** no hay `probabilities` → **ninguna** de `conf_pmax/jev/ent/margin` es
   calculable. Solo aplica la definición `noul = max(π, 1−π)` del proyecto.
2. **`correct` y todo el bloque `gold_*`:** **no** vienen en la response; requieren la etiqueta de
   oro del dataset (el `gold_q` de cada caso). Sin él, no hay accuracy ni ECE.
3. **Distribución conjunta entre preguntas:** **no existe**; las preguntas se evalúan aisladas.
   Cualquier métrica que asuma una conjunta queda fuera.
4. **`conf_jev` sobre un `score` usando el campo `confidence` del API:** **incorrecto**. El
   `confidence` de `score` es la fórmula con `MAD_unif`, **no** la concentración. Hay que
   **recalcular** `conf_jev` desde `probabilities`. El campo `confidence` del API, en `score`,
   constituye un **quinto** descriptor de incertidumbre, no una de las cuatro definiciones del
   proyecto.
5. **`answer_confidence` y `act_probability`:** no existen en TypeSafe → columnas **null** (no
   inferirlas del `confidence`).

---

## 8. Lo que NO se pudo verificar sin una clave + comandos `curl` para cerrarlo

Todo lo de abajo exige una **llamada autenticada**. No se ejecutó ninguna. Comandos listos para el
autor (usan **`$TYPESAFE_API_KEY`**, jamás la clave en claro; todos contra el contrato oficial):

```bash
# --- C1: descubrir modelos/alias que ve la cuenta (¿aparece jev-1.13.0?) ---
curl -sS https://api.typesafe.ai/v1/models \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" | python3 -m json.tool

# --- C2: noul mínimo (verifica envelope, noul sin confidence, y output_tokens real) ---
curl -sS -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"My card was charged twice.","questions":{"is_refund":{"type":"noul","instructions":"Does the customer request a refund?"}}}' | python3 -m json.tool

# --- C3: choice de 3 opciones (verifica que confidence == (n*pmax-1)/(n-1)) ---
curl -sS -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"My card was charged twice. Please help.","questions":{"department":{"type":"choice","instructions":"Which team should handle this?","criteria":{"billing":"Charges and payment problems","technical":"Bugs or integration problems","sales":"Pricing or account questions"}}}}' | python3 -m json.tool

# --- C4: score de 3 niveles (verifica que confidence sigue la fórmula MAD_unif, NO la de choice) ---
curl -sS -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"The export button crashes the settings page in Safari.","questions":{"severity":{"type":"score","instructions":"How severe is the issue?","criteria":["Cosmetic","Degraded but workaround exists","Blocking"]}}}' | python3 -m json.tool

# --- C5: fijar el ID versionado (confirma que 'model' acepta jev-1.13.0 y que response.model lo repite) ---
curl -sS -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"ping","questions":{"q":{"type":"noul","instructions":"Is this a test?"}}}' | python3 -m json.tool

# --- C6: forma del cuerpo 401 (OMITE la cabecera a propósito; no usa ninguna clave) ---
curl -sS -o - -w '\nHTTP %{http_code}\n' -X POST https://api.typesafe.ai/v1/systemone \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"ping","questions":{"q":{"type":"noul","instructions":"Is this a test?"}}}'

# --- C7: forma del cuerpo 422 (pregunta malformada: falta 'criteria' en un choice) ---
curl -sS -o - -w '\nHTTP %{http_code}\n' -X POST https://api.typesafe.ai/v1/systemone \
  -H "Authorization: Bearer $TYPESAFE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"jev-1.13.0","state":"ping","questions":{"department":{"type":"choice","instructions":"Which team?"}}}'
```

### 8.1. Preguntas concretas que cierran estos comandos

| # | Qué queda por confirmar | Comando |
|---|---|---|
| A | **Valor real de `usage.output_tokens`.** La doc se contradice con el dato del proyecto "output_tokens = 0 por construcción": el **ejemplo del OpenAPI** imprimía `output_tokens: 12` y la página de `choice` mostraba `output_tokens: 212` en su response de ejemplo. Puede que el **conteo** no sea 0 aunque el **costo** sí sea 0 ("output tokens are free"). Es el punto más crítico para la metrología del proyecto. | C2–C4 |
| B | **Cadena exacta de `response.model`** al pedir `jev-latest` (¿`"jev-1.13.0"`? ¿lleva prefijo?) | C2 (con `"model":"jev-latest"`) |
| C | **`model` acepta un ID versionado** y la respuesta lo repite | C5 |
| D | **Forma del cuerpo del `401`** (la doc describe el status, no el JSON) | C6 |
| E | **Forma del cuerpo del `422`** y que `detail[].loc` apunta al campo culpable | C7 |
| F | **¿Suma `probabilities` exactamente 1.0?** (la doc dice "aproximadamente") → decide si renormalizar | C3, C4 |
| G | **¿La API rechaza `>255` opciones en `choice` / `>10` niveles en `score`?** (el esquema no pone tope) | variante de C3 con 256 y 11 |
| H | **`GET /v1/models` real**: qué `name`s/alias ve la cuenta y si lista IDs versionados | C1 |
| I | **Cabeceras de rate limit** (`Retry-After`/`retry-after-ms`) y límites vigentes | C2 en bucle / `-D -` |
| J | **Campos extra no documentados** en la respuesta | C2–C4 |
| K | **¿Puede ocurrir `403`?** (el 403 visto fue de la consola, no del API) | C6 con clave inválida (no recomendado) |

---

## 9. Fuentes (todas consultadas el **12-oct-2026**)

**Oficiales / autoritativas**

| URL | Uso |
|---|---|
| `https://api.typesafe.ai/openapi.json` | **Contrato máquina-legible** (HTTP 200, 14 158 bytes; `openapi 3.1.0`, `info.version 0.2.0`) |
| `https://docs.typesafe.ai/api` | Endpoint, request/response, tabla de errores |
| `https://docs.typesafe.ai/models` | Precios, rate limits, contexto, alias, versiones |
| `https://docs.typesafe.ai/primitives` | Las tres primitivas, estado compartido |
| `https://docs.typesafe.ai/primitives/choice` | `choice` (≤255 opciones; ejemplo con `confidence`) |
| `https://docs.typesafe.ai/primitives/score` | `score` (2–10 niveles; `legend`) |
| `https://docs.typesafe.ai/primitives/noul` | `noul` (probabilidad, sin `confidence`) |
| `https://docs.typesafe.ai/confidence` | Fórmulas exactas de `confidence` (choice y score) |
| `https://docs.typesafe.ai/concepts/state` | `state` compartido, tipos admitidos |
| `https://docs.typesafe.ai/concepts/system-one` | Naturaleza del modelo (decisiones, no texto) |
| `https://docs.typesafe.ai/patterns/fan-out` | Fan-out especulativo (varias preguntas por llamada) |
| `https://docs.typesafe.ai/introduction/quickstart` | `POST /v1/systemone`, `$TYPESAFE_API_KEY`, curl |
| `https://docs.typesafe.ai/sdk/javascript/api/variables/ENV` | `TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL` |
| `https://help.typesafe.ai/articles/2769560962-what-is-the-difference-between-429-and-529` | Diferencia 429/529 y reintentos |
| `https://console.typesafe.ai` | Consola (exige login; `/keys` para crear clave) |

**No oficiales (solo contraste; descartadas donde divergen):** `https://jevwiki.ai/wiki/reference/http-api.md`,
`https://jevwiki.ai/wiki/reference/openapi-schemas.md`, `https://jevai.guide/guides/concepts/api-reference`,
`https://jevapi.dev/`, `https://jevapi.org/`. Divergencias anotadas: nombres `options`/`scale` (falsos),
rate limits 250k/1200 (no coinciden).

---

## 10. Receta de implementación (resumen operativo)

1. **Clave:** leer `TYPESAFE_API_KEY` del entorno; armar `{"Authorization": f"Bearer {key}"}`. Nunca
   escribirla en el repo, logs ni filas.
2. **Modelo:** fijar `model = "jev-1.13.0"` (no usar `jev-latest`, que se mueve).
3. **Por cada ítem:** construir el request con `state` = texto del ítem y `questions` =
   `{"<question>": {"type": ..., "instructions": ..., "criteria": ...}}` (`criteria` = mapa para
   `choice`, array ordenado para `score`, `{true,false}` opcional para `noul`).
4. **Enviar** `POST /v1/systemone` (idempotente por ítem; 1 request por ítem).
5. **Parsear:** `ans = response.answers["<question>"]`; adjuntar `response.usage` y `response.model`
   a `ans`; llamar `_fila(caso, question, ans, gold_q)`.
6. **Escribir** en `results/crudos/<modelo>__<dataset>.jsonl` con `model="typesafe/jev"`,
   `model_revision=response.model`, `backend="typesafe-api"`, y `row_hash`.
7. **Errores:** reintentar con backoff en `429`/`529` (honrar `Retry-After`); `401` = clave; `422` =
   cuerpo inválido.
8. **Copiar `usage` a cada fila**: `input_tokens` y `output_tokens` **tal como vienen** (en esta API
   `output_tokens` **no** es 0; ver §11). Registrar también el coste por fila si se quiere la tabla de
   costo por 1.000 decisiones.

---


## 11. Verificación en vivo (12-oct-2026, t440, sin GPU)

Con la clave del autor (`TYPESAFE_API_KEY` en `~/.env`, nunca impresa) se ejecutaron **6 llamadas reales**:
1 `GET /v1/models` y 5 `POST /v1/systemone`. Todas devolvieron `200`, ninguna `429`. Coste total < USD 0.0005.

| Punto del §0 | Resultado en vivo |
|---|---|
| A · `output_tokens` | **NO es 0**: 71 (3 preguntas), 58 (1 pregunta, n=5), 31 (1 pregunta, n=2). El contador de la API pagada cuenta algo de la respuesta serializada. Queda **medido**, no supuesto |
| B · catálogo | `GET /v1/models` → solo `jev-latest` y `jev-preview`; ambos alias, y también el ID versionado, se aceptan como entrada, y la respuesta devuelve siempre **`model: "jev-1.13.0"`** |
| D · estructura | Confirmada campo por campo en `choice`, `score` y `noul` |
| E · fórmula de `choice` | `confidence` `1.0` con `p=(1,0,0)` y `0.94` con `p=(0.05,0.95,0,0,0)`; el valor recalculado `(n·p_max−1)/(n−1)` = `0.9375` sobre las probabilidades **redondeadas** → coincide dentro de la rejilla |
| F · fórmula de `score` | `0.68` devuelto vs `0.68333` recalculado con `MAD_unif` sobre `p=(0.01,0.62,0.37,0,0)` → coincide dentro de la rejilla |
| G · `noul` | Sin campo `confidence` ✔ |
| H · coste | `input_tokens` 308–406 por ítem con 2–5 opciones → **≈ USD 0.013–0.017 por 1.000 decisiones** |

**Hallazgo metrológico nuevo (no estaba en la documentación): la API devuelve las probabilidades y la
confianza redondeadas a 2 decimales.** Todas las respuestas observadas traen valores como `0.95`, `0.62`,
`0.37`, `0.01`, `0.0`. Consecuencia para la matriz: en el brazo pagado la escala tiene una **rejilla de
0.01**, así que los **empates en el umbral** (columna `n_empates_tau`) serán mucho más frecuentes que en los
brazos de pesos abiertos, donde las distribuciones llegan con precisión completa. Hay que declararlo al medir
este brazo y no mezclarlo sin más con los demás.

**Lo que sigue sin verificar** (no se provocó a propósito): `401` con clave inválida, `422` con cuerpo
inválido, `429`/`529` bajo carga, y el comportamiento del límite de 255 opciones.

---

*Documento creado el 12-oct-2026. Cambios de este archivo deben reflejarse, en el mismo paso, en
`README.md` y `STATE.json` del proyecto (regla de mantenimiento del repo).*
