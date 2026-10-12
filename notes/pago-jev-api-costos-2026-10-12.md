# Camino de pago mínimo para medir Jev por API — economía de la corrida mínima

**Fecha de verificación:** 12-oct-2026 · **Autor:** agente (subagente de investigación) · **Idioma:** español
**Documento que revisa:** `contexto/00_veredicto_jev_typesafe.md` §3.1, §3.2, §6, §7 (no modificado).
**Fuentes primarias hoy:** catálogo vivo `GET https://ai-gateway.vercel.sh/v1/models` (HTTP 200, **458 modelos**),
`docs.typesafe.ai/models`, `openrouter.ai/typesafe/jev-1.13`, `docs.netlify.com`, y los datasets ya en el repo.

---

## 0. Veredicto operativo (leer esto primero)

1. **La cifra de uso no es el problema: el mínimo de cobro del proveedor sí.** El estudio completo
   (5 datasets, tamaño completo, 12.677 decisiones) cuesta **USD 0,33** a la tarifa de Jev. Con 3 semillas: **USD 0,99**.
2. **Corrección crítica al veredicto local:** en Vercel AI Gateway, **`typesafe-ai/jev` NO es elegible para el
   crédito gratuito de \$5/mes**. El catálogo vivo lo declara `"availableToFreeTier": false`. Por tanto el crédito
   gratuito **no** cubre a Jev — hay que **comprar créditos** (y eso exige tarjeta).
3. **Camino de pago mínimo (cash) encontrado:** **Netlify AI Gateway, plan Free** — 300 créditos/mes ≈ **USD 1,67**
   de uso de IA, **sin tarjeta** (plan "nunca se te cobra"), y Jev está listado. La suite completa usa **~20 %** de ese crédito.
   ⚠️ No lo verifiqué creando una cuenta: **"no verificado"** in situ (ver §5).
4. **Con tarjeta, el más barato es OpenRouter: USD 5,80** de compra mínima (5 USD + 0,80 de comisión mínima) para
   cubrir ~0,33 USD de uso. Vercel queda en segundo lugar (mín. de compra no confirmado). TypeSafe directo ya **no
   tiene lista de espera**, pero **tampoco da crédito gratuito** a cuentas nuevas.
5. **Plan B a USD 0 real, ya probado por el proyecto:** **Laya** (pesos abiertos, y además servida **gratis**
   —\$0/M— en el propio Vercel AI Gateway), Kev, tinyjev, Jeff-1.

---

## 1. Confirmación / corrección de las cifras del veredicto local

| # | Afirmación en `00_veredicto_jev_typesafe.md` | Estado hoy (12-oct-2026) | Veredicto |
|---|---|---|---|
| 1 | `typesafe-ai/jev` listado en el gateway; `id` + `owned_by` OK | Confirmado en `GET /v1/models` (catálogo ahora de **458** modelos, no 372) | ✅ Confirma |
| 2 | `pricing input 0.000000042` → **\$0,042/M** | Confirmado exacto (mismo valor hoy) | ✅ Confirma |
| 3 | `output 0` → salida gratis | Confirmado (`output_tokens = 0`) | ✅ Confirma |
| 4 | `zdr: all` | **El catálogo dice `zdr: "some"`** y `no_training: "all"` | ❌ **Corrige** |
| 5 | Free tier Vercel "\$5/mes ... **acceso a todos los modelos**" | **El free tier es un SUBCONJUNTO**, no el catálogo completo | ❌ **Corrige** |
| 6 | "\$0,042/M ... **el estudio completo cabe en el crédito gratuito**" | **Falso: Jev tiene `"availableToFreeTier": false`** | ❌ **Corrige** (clave) |
| 7 | Free tier "\$5/mes ... **con método de pago registrado**" | Confirmado: sin método de pago → error `403 customer_verification_required` | ✅ Confirma |
| 8 | "Directo TypeSafe → **lista de espera**, límites 250k tok/s y 1.200 req/min" | **Sin lista de espera** desde 27-sep-2026 ("ANYONE CAN SIGN UP"). Los docs oficiales hoy: **100K tok/s y 80 req/s**; el 250k/1.200 sólo aparece ya en un **revendedor no oficial** | ❌ **Corrige** |
| 9 | Crédito gratuito Vercel "\$5/mes" | Sigue existiendo, pero **sólo para modelos del subconjunto**; además, comprar créditos lo **elimina** (pasas a plan de pago) | ⚠️ Matiza |
| 10 | Ventana de contexto / especificación | Docs TypeSafe: **64k por petición, 32k para `state` + pregunta más larga**. Catálogo Vercel: `context_window 32000`. `supported_specifications: ["v4"]` | ✅ Confirma |
| 11 | "límites de tasa free tier (429) ... R5" (riesgo) | Confirmado y **peor**: hay hilos de la comunidad con **403/429 persistentes en Jev** y un equipo **suspendido por sospecha de abuso** (ver §4, riesgo) | ⚠️ Agrava |

**Detalle del hallazgo #6 (el que cambia el presupuesto).** El payload de `vercel.com/ai-gateway/models?freeTier=true`
incrusta, por modelo, la bandera `availableToFreeTier`. Extracto literal hoy:

```
typesafe-ai/jev               availableToFreeTier = false
openai/gpt-6-luna-decisions   availableToFreeTier = false
liquid/d1                     availableToFreeTier = false
microsoft/microsoft-decision-1 availableToFreeTier = false
convaiinnovations/laya        availableToFreeTier = true   <-- gratis
convaiinnovations/laya-free   availableToFreeTier = true   <-- gratis
```

Es decir: **ningún modelo de decisión "de pago" entra en el crédito gratuito de Vercel; sólo Laya (gratis) sí.**

---

## 2. Tabla comparativa — TODAS las rutas encontradas hacia `Jev`

Precio de Jev verificado hoy = **\$0,042 / millón de tokens de entrada · \$0 salida**. La salida nunca se cobra
(`output_tokens = 0`).

| # | Ruta | URL oficial | Modelo exacto | Precio verificado in / out | ¿Exige tarjeta? | ¿Tier gratuito? | ¿Jev disponible? |
|---|---|---|---|---|---|---|---|
| 1 | **Vercel AI Gateway** | https://vercel.com/ai-gateway/models/typesafe-ai/jev | `typesafe-ai/jev` | \$0,042/M · \$0 | **Sí** (sin tarjeta el crédito ni se activa) | \$5/mes **pero Jev NO es elegible** → hay que comprar créditos | ✅ Listado hoy |
| 2 | **TypeSafe directo** | https://docs.typesafe.ai/models · https://console.typesafe.ai | `jev-1.13.0` (alias `jev-latest`) | \$0,042/M · \$0 | **Sí** (hay que añadir fondos) | **No** desde 27-sep-2026 | ✅ Nativo |
| 3 | **OpenRouter** | https://openrouter.ai/typesafe/jev-1.13 | `typesafe/jev-1.13` | \$0,042/M · \$0 | **Sí** (crédito prepago) | No para Jev | ✅ Listado |
| 4 | **Netlify AI Gateway** | https://docs.netlify.com/build/ai-gateway/overview | `jev-1.13.0` / `jev-latest` | list price del proveedor (\$0,042/M) facturado a créditos Netlify | **No** en plan Free ("nunca se te cobra") | **Sí: 300 créditos/mes ≈ \$1,67 de uso IA** | ✅ Listado (changelog 28-sep) |
| 5 | **Cloudflare Workers AI** | https://developers.cloudflare.com/workers-ai/models/jev/ | `typesafe/jev` | — | — | — | ❌ **ELIMINADO** ("deprecated/not found" hoy) |
| 6 | **Amazon Bedrock** | https://builder.aws.com | — | — | — | — | ❌ No es modelo de Bedrock (sólo "sidecar" vía Lambda) |
| 7 | **Azure AI Foundry / Vertex** | — | — | — | — | — | ❌ No listado |
| 8 | **jevtypesafeai.com ("Jev AI")** | https://jevtypesafeai.com | `jv_live_...` | **\$0,42/M** (≈ **10× el precio real**) | prepago | playground gratis | ⚠️ **NO OFICIAL / con sobreprecio — evitar** |
| 9 | **BYOK en Vercel** | https://vercel.com/docs/ai-gateway | `typesafe-ai/jev` + tu clave TypeSafe | tarifa TypeSafe | Sí | No | ⚠️ Requiere créditos igual (BYOK se bloquea a saldo \$0) |
| 10 | **LiteLLM pass-through** | https://docs.litellm.ai | `typesafe` | tarifa TypeSafe | según tu proxy | No | ✅ (sólo proxy) |

**Plan B — pesos abiertos (USD 0, sin API):**

| Modelo | Repo/URL | Base | Licencia | Nota |
|---|---|---|---|---|
| **Laya** | https://huggingface.co/convaiinnovations/laya | ModernBERT-large 421M | Apache-2.0 | **También gratis por API en Vercel** (`convaiinnovations/laya`, \$0/M, free-tier) o `laya-free` |
| **Kev** | https://huggingface.co/jaredpalmer/kev-0.5b | Qwen2.5-0.5B + LoRA | Apache-2.0 | Réplica del contrato `/v1/systemone` |
| **tinyjev** | https://huggingface.co/AnkitAI/tinyjev-0.6b | Qwen3-0.6B + head | MIT | Temperatura fija 1,46 |
| **Jeff-1** | https://huggingface.co/GestaltLabs/Jeff-1 | LoRA sobre Qwen3-4B | Apache-2.0 | `jgeuter/Jeff-1.0-Large` = Gemma-4-31B, **CC BY-NC** y 80 GB → descartado por entorno |
| **OpenJev 9B** | https://huggingface.co/iFurySt/openjev | Qwen3.5-9B + head | Apache-2.0 | Requiere más VRAM |

> Comparadores de decisión de pago en el mismo gateway (no-Jev, mismos \$0,042/M in y \$0 out):
> `microsoft/microsoft-decision-1` (zdr `all`) y `liquid/d1` (\$0,04/M). Útiles como brazos extra.

---

## 3. Economía de la corrida mínima publicable

El estudio necesita **≥ 200 ítems por dataset etiquetado**. Cardinalidades del proyecto: **{2,4,5}** (typed-decisions),
**3** (WANLI), **5** (SST-5), **77** (Banking77), **151** (CLINC150) — coincide exactamente con el conjunto
`(2,3,4,5,77,151)` del enunciado.

### 3.1 Tokens de entrada por ítem (medidos sobre el payload real del proyecto)

No estimado a ojo: reconstruí la petición exacta que arma `src/matriz/adaptadores.py` (estado + `instructions` en
español + `criteria` con la lista de etiquetas) y conté tokens con `tiktoken` (cl100k_base como proxy estándar;
el tokenizador real de Jev no es público, de ahí que sea una **estimación calibrada**, no una medición de Jev).

| Dataset | Nº etiquetas | tok/ítem (media) | rango (mín–máx) | Texto de estado real |
|---|---|---|---|---|
| typed-decisions | 2 / 4 / 5 | **576,6** | 452 – 913 | JSON de traza de agente (estado + 5 preguntas) |
| SST-5 | 5 | **77,6** | 60 – 103 | reseña corta |
| WANLI | 3 | **125,8** | 101 – 158 | `Premisa: …\nHipótesis: …` (+ descripciones largas de las 3 etiquetas) |
| Banking77 | 77 | **931,8** | 925 – 946 | consulta corta + **77 etiquetas** |
| CLINC150 | 151 | **1.300,4** | 1.295 – 1.314 | consulta corta + **151 etiquetas** |

> El costo lo domina **la lista de etiquetas repetida en el prompt**: con 2–5 opciones el ítem pesa 60–160 tokens;
> con 77/151 opciones pesa ~900–1.300 tokens aunque el texto sea corto.

### 3.2 Costo real (Jev: \$0,042/M entrada · \$0 salida)

| Dataset | n completo | **USD @ 200 ítems** | **USD @ tamaño completo** | **USD / 1.000 decisiones** |
|---|---|---|---|---|
| typed-decisions | 400 | 0,00484 | 0,00969 | 0,0242 |
| SST-5 | 1.101 | 0,00065 | 0,00359 | 0,0033 |
| WANLI | 5.000 | 0,00106 | 0,02641 | 0,0053 |
| Banking77 | 3.076 | 0,00783 | 0,12038 | 0,0391 |
| CLINC150 | 3.100 | 0,01092 | 0,16931 | 0,0546 |

### 3.3 Acumulado para 1, 2 y 5 datasets

**Escenario A — mínimo publicable: 200 ítems por dataset**

| Datasets | n | tokens | USD | USD / 1.000 dec |
|---|---|---|---|---|
| **1** (typed-decisions) | 200 | 115.311 | **0,00484** | 0,0242 |
| **2** (+ SST-5) | 400 | 130.837 | **0,00550** | 0,0137 |
| 3 (+ WANLI) | 600 | 155.992 | 0,00655 | 0,0109 |
| 4 (+ Banking77) | 800 | 342.358 | 0,01438 | 0,0180 |
| **5** (+ CLINC150) | 1.000 | 602.428 | **0,02530** | 0,0253 |

**Escenario B — suite al tamaño completo (recomendado para el paper)**

| Datasets | n | tokens | USD | USD / 1.000 dec |
|---|---|---|---|---|
| **1** (typed-decisions) | 400 | 230.623 | **0,00969** | 0,0242 |
| **2** (+ SST-5) | 1.501 | 316.094 | **0,01328** | 0,0088 |
| 3 (+ WANLI) | 6.501 | 944.944 | 0,03969 | 0,0061 |
| 4 (+ Banking77) | 9.577 | 3.811.253 | 0,16007 | 0,0167 |
| **5** (+ CLINC150) | 12.677 | 7.842.338 | **0,32938** | **0,0260** |

**Multiplicadores de robustez (suite completa):** ×3 semillas = **USD 0,99** · ×5 = **USD 1,65** · ×10 = **USD 3,29**.

### 3.4 Conclusión económica

> El uso es **despreciable** frente a cualquier mínimo de compra. Con \$5 de crédito cabrían **~39,7 M de tokens =
> ~64.000 decisiones de la suite completa**; a \$0,33 por pasada, el crédito de \$5 paga **~15 barridos completos**.
> La restricción real es **la tarjeta y el mínimo de compra del proveedor**, no el costo por token.

| Ruta | Desembolso mínimo real | ¿Cubre la suite (\$0,33)? | Comentario |
|---|---|---|---|
| **Netlify Free** | **\$0** (300 créditos/mes ≈ \$1,67) | ✅ (usa ~20 %) | Sin tarjeta, "nunca se te cobra" — **camino de pago mínimo** |
| **OpenRouter** | **\$5,80** (5 USD + 0,80 comisión mínima; 5,5 %) | ✅ de sobra | Comisión efectiva ~16 % por el piso de \$0,80 |
| **Vercel AI Gateway** | compra de créditos (MCP acepta **1–1000 USD**; hay reporte de **mínimo \$10**) → **no verificado** | ✅ | Jev **no** entra en el \$5 gratuito |
| **TypeSafe directo** | "añadir fondos" (mínimo no publicado) → **no verificado** | ✅ | Sin crédito gratuito para cuentas nuevas |
| **Plan B pesos abiertos** | **\$0** | ✅ | Laya/Kev/tinyjev/Jeff-1 en local; **Laya también \$0/M por API en Vercel** |

---

## 4. Riesgos y avisos que cambian la decisión

- **Jev no está en el crédito gratuito de Vercel** (§1 #6). Cualquier plan que asumiera "\$5 gratis cubre Jev" **está mal**.
- **Compra de créditos Vercel = pierdes el \$5/mes** para siempre (pasas a plan de pago). Añadir tarjeta **no** basta si
  el modelo no es elegible: hace falta **comprar**.
- **Inestabilidad documentada de Jev en Vercel AI Gateway.** Hilos de la comunidad (sep-2026) reportan `403 ACCESS_DENIED`
  y `429 "No access to this model at this time"` con créditos disponibles, incluso en cuentas nuevas; y **un equipo
  fue suspendido por sospecha de abuso** ("This block cannot be removed"). Un usuario describió un lote de 131 preguntas
  tardando **~1,5 h** por límites del free tier, frente a 81 s en la API propia de TypeSafe. → **No pongas la corrida
  confirmatoria sólo en Vercel.**
- **Cloudflare Workers AI quedó fuera**: `typesafe/jev` ya no existe allí (verificado hoy). Si tu plan dependía de esa
  ruta, hay que reasignarla.
- **Revendedor no oficial con 10× de sobreprecio:** `jevtypesafeai.com` ("Jev AI") cobra **\$0,42/M** (diez veces los
  \$0,042/M reales) y se presenta como si fuera la vía oficial. Su cifra de límites (250k tok/s, 1.200 req/min) es la que
  contamina el veredicto local §3.1. **No es TypeSafe. Evitar.**
- **Convención de nombres del proyecto:** el veredicto cita `NandhaKishorM/laya` (GitHub); el repo de pesos es
  `convaiinnovations/laya` (HF). Es el mismo proyecto (Apache-2.0, 421M).

---

## 5. Datos que **NO** pude verificar (declarados honestamente)

1. **Que el plan Free de Netlify realmente sirva a Jev sin tarjeta y sin verificación de identidad** para una cuenta nueva.
   Verifiqué la aritmética de créditos (180 créditos/\$1) y que Jev está listado en Netlify AI Gateway, **pero no creé cuenta**.
2. **Mínimo exacto de compra** en Vercel AI Gateway (el esquema de la herramienta MCP dice `1–1000`; un comentario de
   maintainer menciona `$10`; un usuario compró `$10`). **No confirmado.**
3. **Mínimo de compra** de TypeSafe directo: la ayuda oficial dice "introduce la cantidad que quieras", sin mínimo publicado.
4. **Disponibilidad real de signup** en `console.typesafe.ai` desde mi entorno: devuelve **403** (Cloudflare). La afirmación
   "sin lista de espera" se apoya en el post del CEO (27-sep) y en catálogos independientes, no en un alta observada.
5. **Tokenizador real de Jev:** los tokens/ítem son con `tiktoken` cl100k_base, no con el tokenizador de Jev. Puede haber
   una desviación de ±10–20 %. Las **cardinalidades y los textos de opciones sí son exactos** (salen de los datos del repo).
6. **Precio/cifras del revendedor `jevtypesafeai.com`:** lo trato como NO oficial; no verifiqué su servicio.

---

## 6. Pasos exactos: qué hace el autor a mano y qué hace el agente

### 6.1 Camino de pago mínimo (Netlify Free — recomendado)

| # | Paso | Quién | Detalle |
|---|---|---|---|
| 1 | Crear cuenta en netlify.com (plan **Free**) | **Autor** | Sin tarjeta. Decisión de autoría: ¿aceptar el plan Free con tope duro de 300 créditos/mes? |
| 2 | `npm i -g netlify-cli` y `netlify login` | Agente | Automatizable en local (`netlify dev` da acceso al AI Gateway sin desplegar) |
| 3 | Escribir el runner que llama a Jev dentro de Netlify Functions / `netlify dev` con `@typesafe-ai/sdk` | Agente | Las env vars (`TYPESAFE_API_KEY`, `TYPESAFE_BASE_URL`) las inyecta Netlify; **el agente nunca escribe la clave** |
| 4 | Correr la suite completa (12.677 decisiones, ~\$0,33 de uso = ~20 % del crédito Free) | Agente | Registra `usage.input_tokens` por ítem |
| 5 | Análisis ECE/Brier/curvas + figuras | Agente | Reutiliza `src/jev_conf_metrics` del repo |

### 6.2 Si se prefiere pagar (una sola compra)

| # | Paso | Quién | Detalle |
|---|---|---|---|
| 1 | Decidir ruta: **OpenRouter** (\$5,80 fijos) o **Vercel** (comprar créditos) o **TypeSafe directo** | **Autor** | Decisión de autoría (método de pago) |
| 2 | Crear cuenta y **añadir la tarjeta** (OpenRouter/Vercel) o fondos (TypeSafe) | **Autor** | El agente **no** toca datos de tarjeta |
| 3 | Generar la API key en el panel del proveedor | **Autor** | Ver §6.3 |
| 4 | Poner la clave en `~/.env` | **Autor** | El autor la escribe; el agente sólo lee el **nombre** de la variable |
| 5 | Correr la suite con el runner existente apuntando al endpoint elegido | Agente | `response.model` registrado para fijar `jev-1.13.0` |
| 6 | Verificar gasto real (`GET /v1/credits` en Vercel, o `usage.cost` en OpenRouter) | Agente | Trazabilidad D4 |

### 6.3 Variables de entorno por ruta (el autor las define; el agente sólo ve el nombre)

| Ruta | Variable | Endpoint |
|---|---|---|
| Vercel AI Gateway | `AI_GATEWAY_API_KEY` | `https://ai-gateway.vercel.sh/v1/evaluate` (o `/typesafe/v1/systemone`) |
| TypeSafe directo | `TYPESAFE_API_KEY` | `https://api.typesafe.ai/v1/systemone` |
| OpenRouter | `OPENROUTER_API_KEY` | Decisions API de OpenRouter |
| Netlify | (inyectada por Netlify) | AI Gateway de Netlify |

> **Nota de cumplimiento:** el agente **no escribe ni solicita claves**. El procedimiento es: el autor deja la clave en
> `~/.env` y el agente lee únicamente el nombre de la variable vía entorno.

---

## 7. URLs verificadas (12-oct-2026)

- Catálogo vivo: `GET https://ai-gateway.vercel.sh/v1/models` (HTTP 200; `typesafe-ai/jev` presente)
- Free tier (bandera por modelo): https://vercel.com/ai-gateway/models?freeTier=true
- Precios/tiers Vercel: https://vercel.com/docs/ai-gateway/pricing · https://vercel.com/docs/ai-gateway/faq
- Getting started / tarjeta: https://vercel.com/docs/ai-gateway/getting-started
- Ficha Jev (Vercel): https://vercel.com/ai-gateway/models/typesafe-ai/jev
- TypeSafe modelos y precio: https://docs.typesafe.ai/models · https://docs.typesafe.ai/introduction/quickstart
- TypeSafe facturación: https://help.typesafe.ai/articles/7771619341-how-do-i-add-credits
- OpenRouter Jev: https://openrouter.ai/typesafe/jev-1.13 · comisiones: https://openrouter.ai/docs/faq · https://openrouter.ai/terms
- Netlify AI Gateway: https://docs.netlify.com/build/ai-gateway/overview · precios IA: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/pricing-for-ai-features/
- Netlify planes/créditos: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/credit-based-pricing-plans/
- Cloudflare (Jev eliminado): https://developers.cloudflare.com/workers-ai/models/jev/
- Bedrock/Azure/Vertex (no listado): https://jev-ai.pro/where-to-run-jev · https://www.factualminds.com/blog/jev-typesafe-ai-aws-guide-2026/
- Estado de acceso TypeSafe (independiente): https://shaduf.ai/p/jev-catalog/
- Revendedor NO oficial (evitar): https://jevtypesafeai.com/pricing
