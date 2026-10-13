# Publicar en Zenodo: guía literal + diagnóstico del caso `tesis1-jev-confidence`

**Fecha de verificación de todos los datos de este documento:** 12-oct-2026, 20:34 (−05, America/Lima) = 13-oct-2026, 01:34 UTC.
**Método:** consulta directa a la API pública de Zenodo y de GitHub (sin credenciales, sin iniciar sesión) + documentación oficial de Zenodo.

---

## 0. LA RESPUESTA CORTA (léela antes que nada)

**No falló nada. El depósito existe y YA está publicado con DOI.**

| Dato | Valor verificado |
|---|---|
| **DOI de la versión v1.0.0** | **10.5281/zenodo.23328989** |
| **DOI del concepto** (todas las versiones) | **10.5281/zenodo.23328988** |
| Tipo de recurso | `Software` |
| Versión | `v1.0.0` |
| Licencia | `apache2.0` |
| Archivo depositado | `Arbues/tesis1-jev-confidence-v1.0.0.zip` (16.899.810 bytes ≈ 16,9 MB) |
| Autor | Pérez Villegas, Arbués Enrique — *Facultad de Ciencias, Universidad Nacional de Ingeniería (FC-UNI), Lima, Perú* — ORCID 0009-0004-7605-6569 |
| Vínculo con GitHub | `isSupplementTo` → `https://github.com/Arbues/tesis1-jev-confidence/tree/v1.0.0` |
| **Creado en Zenodo** | **2026-10-13T00:59:43Z** (a las 19:59:43 del 12-oct en Lima) |
| **Estado** | **`published`** (no es borrador) |
| Página del registro | https://zenodo.org/records/23328989 |
| Redirección por DOI | https://doi.org/10.5281/zenodo.23328989 |

**La prueba de que la integración GitHub→Zenodo funcionó:** el Release de GitHub se publicó a las **00:59:36Z** y el registro de Zenodo se creó **7 segundos después, a las 00:59:43Z**. Zenodo tomó el ZIP del release, lo archivó y le asignó DOI. No hay ningún borrador esperando: el registro nació ya publicado.

> **Por lo tanto:** no hay que pulsar ningún «Publicar», no hay que hacer nada más, y el DOI **10.5281/zenodo.23328989** ya es citable hoy.

Lo que probablemente confundió al autor es que **buscaba botones de una versión vieja de Zenodo que ya no existe** (ver §2). La frase «Zenodo → Upload → GitHub» describe una interfaz retirada en octubre de 2023.

---

## 1. LO PRIMERO QUE HAY QUE MIRAR: ¿existe el depósito?

### 1.1 Si se tiene sesión iniciada (lo que debe hacer el autor)

1. Entrar en **https://zenodo.org** e iniciar sesión.
2. En la barra superior, pulsar el menú **`My dashboard`** (ya **no** existe una pestaña llamada «Uploads»).
   - URL directa: **https://zenodo.org/me/uploads**
3. Se abre la lista **`My uploads`**. Ahí deben aparecer **dos** registros del autor, ambos en estado publicado:
   - *Metrología y transferencia del campo confidence (pre-registro)* → DOI `10.5281/zenodo.23266795`
   - *Metrología y transferencia del campo confidence en modelos de decisión de pesos abiertos tipo Jev* → **`v1.0.0`** → **DOI `10.5281/zenodo.23328989`** ← **este es el que creó GitHub**
4. Qué buscar en pantalla:
   - Los registros **ya publicados** aparecen en la lista **sin** etiqueta de estado.
   - Un **borrador** aparecería con una etiqueta naranja/roja del tipo **`Draft`** y con botones a la derecha **`Edit`** / **`Delete`** en vez de **`Edit`** / **`View`** (o `New version`).
   - **En este caso NO hay ningún borrador**: la lista no muestra ningún ítem en estado `Draft`.

### 1.2 Verificación SIN iniciar sesión (la que se usó para este informe)

Abre en el navegador esta URL (es una API pública, no pide cuenta):

```
https://zenodo.org/api/records/23328989
```

Debe devolver un JSON con:
- `"status": "published"`
- `"doi": "10.5281/zenodo.23328989"`
- `"conceptdoi": "10.5281/zenodo.23328988"`
- `"version": "v1.0.0"`
- `"resource_type": {"type": "software"}`

Y esta otra para confirmar que forma parte de la cadena de versiones del proyecto:

```
https://zenodo.org/api/records/23328989/versions
```

### 1.3 Verificación del lado de GitHub (estado del Release)

Abre:

```
https://api.github.com/repos/Arbues/tesis1-jev-confidence/releases
```

Resultado verificado: el release `v1.0.0` tiene **`"draft": false`**, **`"prerelease": false`**, **`"published_at": "2026-10-13T00:59:36Z"`**. Es decir, **el Release NO es un borrador ni un pre-release** — es un release público válido, que es exactamente lo que Zenodo necesita.

### 1.4 Página del webhook / historial de releases en Zenodo

Con sesión iniciada:

```
https://zenodo.org/account/settings/github/repository/Arbues/tesis1-jev-confidence
```

Ahí se ve la lista de releases procesados por Zenodo para ese repositorio, con su estado (`Processing`, `Published` o una pestaña **`Errors`** si falló). En este caso debe figurar **`v1.0.0` → `Published`** con enlace al DOI `10.5281/zenodo.23328989`.

---

## 2. POR QUÉ NO VE «Upload», «GitHub» NI «Publicar»

Esta es la causa raíz de la confusión. **Zenodo cambió su interfaz el 13 de octubre de 2023** (migración a InvenioRDM) y las etiquetas que buscaba el autor **desaparecieron**:

| Lo que buscaba | ¿Existe en Zenodo (2026)? | Dónde está hoy realmente |
|---|---|---|
| Pestaña/botón **«Upload»** | ❌ **No existe.** Fue eliminada | Menú **`My dashboard`** en la barra superior (reemplaza a la antigua pestaña «Uploads») |
| Botón **«Upload»** para subir un archivo | ❌ **No existe** con ese nombre | Icono **`+`** (menú *Quick actions*) arriba a la derecha → opción **`New upload`** |
| Pestaña **«GitHub»** en el menú principal | ❌ **No existe** ahí | Menú del **perfil** (avatar, arriba a la derecha) → **`GitHub`** |
| Botón **«Publicar» / «Publish»** en un depósito de GitHub | ❌ **No existe** para depósitos de GitHub | **No hace falta**: el Release de GitHub publica el DOI automáticamente |

### 2.1 La barra de navegación REAL de Zenodo hoy (2026)

De izquierda a derecha, en la cabecera:

1. **`Search`** — buscador (campo de texto, arriba).
2. **`Communities`** — explorar comunidades.
3. **`My dashboard`** — **aquí están «My uploads», «My communities», «My requests»**.
4. **`Inbox`** — solicitudes pendientes (revisiones, invitaciones, etc.).
5. **`+`** — menú de *quick actions* → **`New upload`** / **`New community`**.
6. **Menú del perfil** (tu nombre/avatar, extremo derecho) → **`Profile` · `Change password` · `Notifications` · `Security` · `Linked accounts` · `Applications` · `GitHub`**.

**La ruta literal para llegar a la integración con GitHub es, por tanto:**

```
zenodo.org  →  (avatar, arriba a la derecha)  →  GitHub
```

URL directa equivalente: **https://zenodo.org/account/settings/github/**

### 2.2 Por qué en un depósito de GitHub no hay botón «Publicar»

**En el Zenodo actual, crear un Release en GitHub ES la publicación.** Zenodo descarga el ZIP del tag, lo archiva y **publica el registro con DOI en segundos**, sin paso de aprobación y sin dejar borrador. No hay «Submit»/«Publish» que pulsar en ese flujo.

Esto se confirma con dos hechos verificados hoy:
- El registro `23328989` tiene fecha de creación **00:59:43Z**, 7 segundos después del Release (**00:59:36Z**), y ya nace con `"status": "published"`.
- Informe independiente de otro proyecto (2026) con el mismo comportamiento: *«Creating the `paper-v1.2.0` GitHub release minted `10.5281/zenodo.21997434` five seconds later. There was no draft and no approval step.»* — https://github.com/Silentpartnercoding/minority-prophet/pull/102

> ⚠️ Consecuencia importante: **el DOI de un Release de GitHub es irreversible**. Una vez creado el Release, el DOI existe y no se puede «despublicar». Por eso hay que revisar los metadatos **antes** de crear el Release (o corregirlos después con `Edit`, que no cambia el DOI).

---

## 3. SI EL DEPÓSITO NO EXISTIERA: causas y cómo arreglarlo

*(En este caso **no aplica** — el depósito existe y está publicado — pero queda como guía por si en el futuro se publica una versión nueva y no aparece.)*

El orden de comprobación, de la causa más probable a la menos:

1. **El repositorio no estaba «enabled» (interruptor apagado) cuando se creó el Release.**
   - Síntoma: el release existe en GitHub pero no aparece en Zenodo.
   - Regla dura de Zenodo: **no archiva retroactivamente releases anteriores a la activación del interruptor.**
   - Arreglo: activar el interruptor (§3.1) y **crear un Release NUEVO** (aunque sea un tag nuevo como `v1.0.1`). Editar el release viejo normalmente no basta.

2. **El Release se creó como `Draft` o como `Pre-release`.**
   - Un release en borrador **no dispara** el webhook.
   - Verificar: si en la página del release en GitHub hay una etiqueta **`Pre-release`** o el release solo es visible para quien tiene permiso, no se archivará como versión normal.
   - Arreglo: editar el release → desmarcar **`Set as a pre-release`** → **`Publish release`**; o crear un release definitivo nuevo.

3. **El repositorio es privado.** Zenodo solo lee repositorios **públicos**. (`Arbues/tesis1-jev-confidence` es público — verificado: `"private": false`.)

4. **Eres miembro, no *Admin*, de una organización de GitHub.** El repositorio debe estar bajo tu cuenta personal (es el caso aquí) o debes tener permiso **Admin** sobre él. Para repos de organización hay que aprobar el acceso de la app OAuth en GitHub → *Settings → Applications → Zenodo → Organization access* → **Grant**, y luego pulsar **`Sync now`** en Zenodo.

5. **El webhook no se instaló o se cayó.** Con sesión, ve a `https://github.com/Arbues/tesis1-jev-confidence/settings/hooks` y comprueba que existe un webhook hacia Zenodo (en *Recent Deliveries* verás el código de respuesta; `202` = aceptado, `400`/`50x` = error).

6. **Metadatos inválidos** (`CITATION.cff` o `.zenodo.json` mal formados): el release aparece pero con estado de **error**.
   - Diagnóstico: en `https://zenodo.org/account/settings/github/repository/Arbues/tesis1-jev-confidence`, abrir el release fallido → pestaña **`Errors`**.
   - Errores típicos: *«Extra metadata load failed»* (el `.zenodo.json` es inválido) o *«Citation metadata load failed»* (el `CITATION.cff` es inválido). Si el repo tiene **los dos** archivos, Zenodo usa **solo** el `.zenodo.json` e ignora el `CITATION.cff`.
   - Arreglo: corregir el archivo y **volver a crear el release**.

### 3.1 Cómo activar («enable») el repositorio y forzar el depósito

**Ruta literal:**

1. Entra en **https://zenodo.org** e inicia sesión.
2. Pulsa el **avatar/menú de perfil** (arriba a la derecha) → **`GitHub`**.
   (URL directa: https://zenodo.org/account/settings/github/ )
3. Si es la primera vez: pulsa **`Connect`** y autoriza en GitHub (**`Authorize Zenodo`**). Ya está hecho en este caso.
4. Pulsa el botón **`Sync now`** (arriba de la página) para refrescar la lista de repositorios.
5. Busca en la lista **`GitHub repositories`** el repositorio **`Arbues/tesis1-jev-confidence`**.
6. Mueve a **ON** el **interruptor (toggle)** que está a su derecha. (Si ya estaba en ON, apágalo y vuélvelo a encender para reinstalar el webhook.)
7. **Recarga la página** (F5) para que la lista de repositorios activados se actualice.
8. Comprobación: junto al repositorio debe aparecer ahora una **insignia/DOI** enlazando al registro, y el repositorio queda «enabled».

**Para forzar la creación del depósito:**

1. Vuelve a **GitHub** → `https://github.com/Arbues/tesis1-jev-confidence/releases/new`
2. Crea un **tag nuevo** (p. ej. `v1.0.1`), un título y las notas.
3. **`Publish release`** (nunca «Save draft»; deja sin marcar «Set as a pre-release»).
4. Espera entre unos segundos y unos minutos. Aparecerá el nuevo registro/versión en Zenodo con DOI nuevo.

---

## 4. ALTERNATIVA MANUAL COMPLETA (subir el PDF o el ZIP a mano)

Sirve, por ejemplo, para depositar el **PDF del paper IEEE** (`paper/ieee/main.pdf`) como publicación, o el ZIP del código sin depender de GitHub.

### Paso a paso literal

1. Inicia sesión en **https://zenodo.org**.
2. Abre el formulario de depósito:
   - **Pulsando la interfaz:** icono **`+`** (arriba a la derecha) → **`New upload`**.
   - **Por URL directa:** **https://zenodo.org/uploads/new**
3. **Sube el archivo:** pulsa el botón **`Upload files`** (o arrastra el archivo a la zona de soltar). Límites: **100 archivos / 50 GB**.
   - Para código: sube **un único** `.zip` del código fuente (si eliges `Software`, Zenodo exige **un solo archivo comprimido**; si no, el registro no se envía a Software Heritage).
   - Para el paper: sube el `main.pdf`.
4. **DOI:** en el bloque *Digital Object Identifier*, a la pregunta «¿ya tienes DOI?» responde **`No`** y pulsa el botón **`Get a DOI now!`** (en algunas vistas aparece como **`Reserve DOI`**).
   - Esto **reserva** el DOI para poder imprimirlo en el PDF, pero **todavía no lo publica**.
   - ⚠️ Si borras el borrador, el DOI reservado se pierde.
5. **`Resource type`** (obligatorio): elige del desplegable.
   - Para el paper → **`Publication`** → y dentro **`Preprint`** (o `Journal article` si corresponde).
   - Para el código → **`Software`**.
6. **`Title`** (obligatorio): título completo, sin abreviar.
7. **`Publication date`** (obligatorio): la fecha en que se publica, por defecto hoy.
8. **`Creators`** (obligatorio): pulsa **`Add creator`**.
   - Tipo **`Person`**. Añade apellido y nombre: **`Pérez Villegas`** / **`Arbués Enrique`**.
   - **Name identifier:** `0009-0004-7605-6569` (ORCID).
   - **Affiliation:** `Facultad de Ciencias, Universidad Nacional de Ingeniería (FC-UNI), Lima, Perú` (se autocompleta desde ROR; elige la opción sugerida, no texto libre).
9. **`Description`** (recomendado): pega el resumen/abstract.
10. **`License`** (recomendado, necesario para una buena práctica): **`Apache-2.0`** para el código, **`CC-BY-4.0`** para el texto del paper.
11. **`Version`** (opcional pero recomendado para software): `v1.0.0`.
12. **`Language`** (opcional): `Spanish` / `English` según el contenido.
13. Revisa con **`Preview`** si quieres ver cómo quedará la página.
14. **PUBLICAR: pulsa el botón `Publish`.**
    - Aparecerá un aviso de que **no podrás añadir, modificar ni borrar archivos** después de publicar.
15. Confirma pulsando **`Publish`** otra vez en el diálogo.
16. **Obtén el DOI:** al terminar, la página del registro muestra el DOI (`10.5281/zenodo.XXXXXXXX`) y el enlace **`https://doi.org/...`**. Cópialo. Es el DOI definitivo, ya registrado.

> Nota: para editar metadatos de un registro ya publicado: en la página del registro pulsa **`Edit`**, cambia lo que quieras y vuelve a pulsar el botón verde **`Publish`**. **Esto NO cambia el DOI.**

---

## 5. TABLA DE SÍNTOMAS → CAUSA → SOLUCIÓN

| Síntoma que reporta el usuario | Causa | Solución literal |
|---|---|---|
| «No veo ninguna opción **Upload**» | La pestaña/бotón «Uploads» **se eliminó** en Zenodo (oct-2023) | Usa **`My dashboard`** (cabecera) o el icono **`+` → `New upload`** |
| «No encuentro **GitHub** en el menú» | GitHub **nunca** estuvo en el menú principal; está en el menú de perfil | Pulsa el **avatar** (arriba a la derecha) → **`GitHub`** → https://zenodo.org/account/settings/github/ |
| «No me aparece el repo en la lista» | No se ha pulsado **`Sync now`**, o falta permiso Admin / acceso de la organización en GitHub | Pulsa **`Sync now`**, recarga la página. Si es de una organización: GitHub → *Settings → Applications → Zenodo → Organization access* → **Grant**, y luego **`Sync now`** |
| «El depósito no se creó (no aparece nada)» | El repo no estaba **enabled** al crear el Release, o el Release era **draft/pre-release**, o el webhook falló | Activa el **toggle** del repo (§3.1) y **crea un Release NUEVO** (Zenodo no archiva releases anteriores a la activación) |
| «El depósito se creó pero con **errores**» | `CITATION.cff` o `.zenodo.json` inválidos | Abre el release en `.../account/settings/github/repository/Arbues/tesis1-jev-confidence` → pestaña **`Errors`**; corrige el archivo y **crea un Release nuevo** |
| «No encuentro el botón **Publicar**» | En depósitos de GitHub **no existe**: el Release ya publicó el DOI. Y en subida manual el botón se llama **`Publish`**, no «Publicar» | No hay nada que pulsar: el DOI ya existe. Para subida manual, el botón es **`Publish`** (abajo y arriba del formulario) |
| «Está en borrador y no sé cómo soltarlo» | Un depósito manual guardado con **`Save draft`** | Entra en **`My dashboard` → `My uploads`** → busca la etiqueta **`Draft`** → pulsa **`Edit`** → completa los campos con estrella roja → **`Publish`** |
| «El DOI no resuelve / no está registrado» | Se usó **`Get a DOI now!`** (reserva) y **nunca se pulsó `Publish`** | Date de alta en el borrador y pulsa **`Publish`**; el DOI solo se registra al publicar |

---

## 6. ADVERTENCIA CLAVE: SIN PUBLICAR, EL DOI NO EXISTE

- En **subida manual**, el botón **`Get a DOI now!`** / **`Reserve DOI`** solo **reserva** el identificador. **El DOI NO queda registrado hasta que se pulsa `Publish`.**
- Si borras el borrador, **el DOI reservado se pierde**.
- Un borrador **no es visible** para nadie salvo tú y **no es citable**: un DOI reservado que nunca se publica **no resuelve**.
- En el flujo **GitHub→Zenodo**, en cambio, **no hay botón Publicar**: al crear el Release el DOI se emite y se publica solo, en segundos. En este caso concreto **ya está hecho**: `10.5281/zenodo.23328989`.
- Y es **irreversible**: un registro publicado en Zenodo no se puede «despublicar». Los metadatos sí se pueden corregir con **`Edit` → `Publish`** (el DOI no cambia); los **archivos** solo se pueden tocar por ti durante los primeros **45 días** y luego solo vía soporte.

---

## 7. FUENTES CONSULTADAS (URL + fecha)

Todas consultadas el **12-oct-2026** (Lima).

**Datos del caso (API pública, sin sesión):**
1. `https://api.github.com/repos/Arbues/tesis1-jev-confidence/releases` — release `v1.0.0`, `draft:false`, `prerelease:false`, `published_at: 2026-10-13T00:59:36Z`.
2. `https://api.github.com/repos/Arbues/tesis1-jev-confidence` — `private:false`, `license: Apache-2.0`.
3. `https://zenodo.org/api/records/23328989` — registro **publicado**, DOI `10.5281/zenodo.23328989`, concepto `10.5281/zenodo.23328988`, `Software`, `v1.0.0`, `created 2026-10-13T00:59:43Z`, licencia apache2.0, archivo `Arbues/tesis1-jev-confidence-v1.0.0.zip`, `isSupplementTo …/tree/v1.0.0`.
4. `https://zenodo.org/api/records/23328989/versions` — 1 versión, `published`.
5. `https://zenodo.org/api/records/23266795` — pre-registro publicado (sin afiliación en el creador, sin archivo relacionado con GitHub).

**Documentación oficial de Zenodo (interfaz 2026):**
6. https://help.zenodo.org/docs/get-started/navigating-zenodo/ — nombres reales de la cabecera: `Search`, `Communities`, **`My dashboard`**, `Inbox`, **`+` (Quick actions)**, **Profile** (con `GitHub` dentro).
7. https://help.zenodo.org/docs/about/whats-changed/ — *«The Uploads header menu item has been removed in favour of a new My dashboard menu item.»*
8. https://help.zenodo.org/docs/deposit/create-new-upload/ — **«Click the plus icon in the header, and select New upload»**; botón `Upload files`; `Get a DOI now!` reserva el DOI; **«The DOI will only be registered once the record is published»**.
9. https://help.zenodo.org/docs/get-started/quickstart/ — 3 pasos: `Upload` → `Describe` → **`Publish`**.
10. https://help.zenodo.org/docs/deposit/manage-records/ — `My dashboard` → `My uploads` muestra publicados **y borradores**; `Edit` y botón verde **`Publish`** para cambios que **no afectan al DOI**.
11. https://help.zenodo.org/docs/github/enable-repository/ — menú de perfil → **`GitHub`** → **`Sync now`** → **toggle**; «Refresh the page to update the list of enabled repositories».
12. https://help.zenodo.org/docs/github/archive-software/github-upload/ — flujo del Release; depuración en pestaña **`Errors`**.
13. https://help.zenodo.org/docs/github/archive-software/manual-upload/ — `Resource type` = `Software`; **un solo ZIP es obligatorio** para Software Heritage.
14. https://help.zenodo.org/docs/deposit/describe-records/creators/ — `Add creator`, `Person`/`Organization`, ORCID y afiliaciones vía ROR.
15. https://help.zenodo.org/docs/deposit/describe-records/descriptions/ — campo `Description` (recomendado).
16. https://help.zenodo.org/docs/deposit/manage-versions/ — `New version`, `Import files`, `My uploads`, botón **`View all versions`**.
17. https://support.zenodo.org/help/en-gb/24-github-integration/51-why-does-my-github-organisations-repositories-not-show-up — repos de organización: permiso **Admin** + *Organization access* en GitHub + **`Sync now`** (publicado 26-03-2026).
18. https://support.zenodo.org/help/en-gb/24-github-integration/204-why-does-my-github-release-fail-with-an-error — errores `Extra metadata load failed` / `Citation metadata load failed` (publicado 28-01-2026).

**Comportamiento no-retroactivo y auto-publicación (evidencia externa):**
19. https://github.com/zenodo/zenodo/issues/2420 — *«it seems to work if you create the github release after having turned on the github repo in zenodo, but zenodo does not detect an already existing github release»*.
20. https://github.com/Silentpartnercoding/minority-prophet/pull/102 — *«Creating the release minted `10.5281/zenodo.21997434` five seconds later. **There was no draft and no approval step.**»*

**URL del formulario manual:** `https://zenodo.org/uploads/new` (confirmada como el depósito actual de Zenodo).

---

## 8. HALLAZGOS ADICIONALES ÚTILES PARA EL PROYECTO

1. **Cerrar el pendiente del `.hermes.md` §7 nº 1 y 2:** el registro de **software** `10.5281/zenodo.23328989` **ya trae** la afiliación `FC-UNI` y el **ORCID** `0009-0004-7605-6569`. El que **no** tiene afiliación es el **pre-registro** `10.5281/zenodo.23266795` (creador sin `affiliation`) — ahí sigue abierto el arreglo (se hace con **`Edit` → `Publish`**, sin cambiar el DOI).
2. **Dos DOIs que conviene distinguir al citar:**
   - **Concept DOI** `10.5281/zenodo.23328988` → «el software», siempre resuelve a la última versión. **Usa este** en la cita general.
   - **Version DOI** `10.5281/zenodo.23328989` → solo la `v1.0.0` congelada. Úsalo cuando cites exactamente esa versión.
3. **`.hermes.md` §7 y `README.md` §10-ter todavía no registran** el depósito de software `10.5281/zenodo.23328989` (solo listan el pre-registro `23266795`). Conviene añadirlo en la misma pasada en que se toque `README.md`/`STATE.json` (regla de mantenimiento del proyecto).
4. **Recordatorio operativo para la próxima versión:** como el DOI se emite **al publicar el Release** y es **irreversible**, conviene verificar el `CITATION.cff` / `.zenodo.json` **antes** de pulsar `Publish release` en GitHub; si algo sale mal, el único arreglo limpio es **crear otro release** (`v1.0.1`).
