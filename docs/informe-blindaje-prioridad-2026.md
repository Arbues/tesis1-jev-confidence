# Blindaje de prioridad y crédito verificable — mecanismos **gratuitos** (octubre 2026)

**Contexto:** entregable de software + paper + dataset. Pre-registro ya publicado con DOI
`10.5281/zenodo.23266795` (08-oct-2026). Autor: Arbués Enrique Pérez V., FC-UNI.
Restricción: **costo 0 USD**, **sin anotación manual** del autor. Fecha del informe: 12-oct-2026.

> **Regla de lectura.** Todo dato aquí fue verificado contra la documentación oficial viva (no de memoria)
> el 12-oct-2026. Donde algo **no** está garantizado por la fuente, se marca con **⚠️ NO DAR POR HECHO**.

---

## 0. Resumen en una frase

Lo único que da **prioridad demostrable ante un tercero** hoy, gratis, es: **DOI de Zenodo (DataCite) + tag/Release de GitHub sobre repo público + SWHID de Software Heritage**; arXiv es el sello de mayor prestigio científico **pero está bloqueado por el sistema de *endorsement*** (riesgo #1).

---

## 1. Tabla maestra

| Mecanismo | Qué reserva exactamente | Qué exige exactamente | Costo | Tiempo | URL oficial |
|---|---|---|---|---|---|
| **Zenodo — DOI de versión** | Un DOI por cada publicación de archivos; queda ligado a la versión exacta | Publicar el registro (metadata mínima). Al publicar **por primera vez** se emiten **2 DOIs**: el de *versión* y el de *concepto* (todos los versiones) | $0 | Inmediato al publicar | https://zenodo.org/help/versioning · https://help.zenodo.org/docs/deposit/about-records/ |
| **Zenodo — nueva versión** | Nuevo DOI de versión, ligado a la anterior (`isNewVersionOf`/`isPreviousVersionOf`) | Página del registro → botón verde **New version** (solo con permiso de edición) → metadata + **Import files** → publicar. **Solo si cambian los ARCHIVOS**; editar metadatos (título/autores) **no** genera versión nueva | $0 | Minutos | https://help.zenodo.org/docs/deposit/manage-versions/ |
| **Zenodo — reserva de DOI** | Un DOI para incrustarlo en el PDF antes de publicar | En un *draft*: campo DOI → "No" → **Get a DOI now!**. Si borras el draft, el DOI reservado **se pierde**; el DOI solo se registra al publicar | $0 | Inmediato | https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/ |
| **Software Heritage — Save Code Now** | Copia preservada del repo + **SWHID** intrínseco (SHA-1) de revisiones/snapshots | Ir a Save Code Now, elegir VCS (`git`) y pegar la **URL de clonado**; o extensión **UpdateSWH** (1 clic); o API/webhook | $0 | Forjas conocidas (GitHub): **sin aprobación, horas** (típ. minutos según tamaño). Origen desconocido: cola de moderación **días** | https://www.softwareheritage.org/how-to-archive-reference-code/ · https://docs.softwareheritage.org/user/faq/index.html |
| **GitHub — tag + Release** | Un tag inmutable + un objeto Release (ZIP/tarball, notas) | Permiso de colaborador/escritura. Tag nuevo o existente + publicar Release | $0 | Inmediato | https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository |
| **Zenodo ↔ GitHub** | DOI **por cada Release** del repo habilitado | Repo **PÚBLICO** + cuenta GitHub↔Zenodo (OAuth) + habilitar el repo + permisos (webhooks; org debe autorizar la app). **No archiva releases previos** | $0 | Minutos–horas por release | https://help.zenodo.org/docs/github/enable-repository/ · https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content |
| **CITATION.cff** | Cita canónica en GitHub + metadata para Zenodo | Nombre exacto `CITATION.cff`, en raíz, YAML 1.2, válido según schema **1.2.0** | $0 | Inmediato | https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md · https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files |
| **arXiv** | `arXiv:YYMM.NNNNN` + fecha de anuncio en listas públicas | **ENDORSEMENT** para el primer envío a la categoría + versión completa **en inglés** | $0 | **Indeterminado** (depende de un tercero) | https://info.arxiv.org/help/endorsement.html · https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/ |
| **OSF Preprints** | DOI + URL persistente | Subir preprint; pasa **pre-moderación** (pending privado) | $0 | Servidores comunitarios: **≥2 semanas**; servidor general OSF: ~1–2 días hábiles | https://help.osf.io/article/376-preprints-home-page |
| **Zenodo tipo "publication/preprint"** | DOI de preprint | Subir PDF como `publication` + subtipo `preprint` (sin comité científico) | $0 | Inmediato | https://developers.zenodo.org/ |
| **ResearchGate** | DOI propio `10.13140/RG…` | Solo para trabajos **no publicados** (preprint/tesis) con full-text público; **no editable** después | $0 | Inmediato | https://help.researchgate.net/research-and-publications/researchgate-dois |

---

## 2. Detalle por mecanismo

### (a) Zenodo — DOI por versión, metadatos, concepto vs versión

**Dos DOIs desde el primer publish** (no hay que hacer nada extra) [[FAQ versioning](https://zenodo.org/help/versioning)]:
- **DOI de versión** → la versión concreta de tus archivos (el que se cita normalmente).
- **DOI de concepto** → "todas las versiones"; resuelve siempre a **la última**.

> **⚠️ Aplicado a este proyecto:** `10.5281/zenodo.23266795` es el DOI de la **versión 1** (el pre-registro).
> El **DOI de concepto** es un número distinto. Hay que **anotar el concepto** para citar "el pre-registro
> como línea de trabajo" y el de versión para citar exactamente lo depositado el 08-oct.

**Nueva versión (paso a paso)** [[manage-versions](https://help.zenodo.org/docs/deposit/manage-versions/)]:
1. Abrir la *landing page* del registro publicado.
2. Clic en **New version** (verde; solo aparece si tienes permiso de edición) → se crea un *draft*.
3. Rellenar metadata y **Import files** (no duplica archivos) y subir/cambiar lo que haga falta.
4. **Publicar** → nuevo DOI de versión, ligado a las demás.

**Cuándo NO crear versión:** cambiar título/autores/descripción se hace **editando** el registro → **no** hay DOI nuevo. Solo se versiona si cambian los **archivos**. Correcciones menores de archivos dentro de **30 días** publicados sin nuevo DOI; fuera de eso, solo casos justificados (soporte). Un *draft* de nueva versión debe publicarse en **45 días**.

**Metadatos** [[describe records](https://help.zenodo.org/docs/deposit/describe-records/)]:
- **Obligatorios (estrella roja):** Título · Creadores/autores (con **ORCID** — clave para crédito) · **Tipo de recurso** · Fecha de publicación · **Licencia**.
- Recomendado: **Descripción/abstract**.
- **Tipo de recurso** (vocabulario DataCite) [[resource-type](https://help.zenodo.org/docs/deposit/describe-records/resource-type/)]:
  paper → `publication` + subtipo `preprint` (o `article`); código → `software`; mediciones crudas → `dataset`
  [[lista oficial](https://developers.zenodo.org/)].

### (b) Software Heritage — Save Code Now / API, tiempos y SWHID

Tres vías [[how-to-archive](https://www.softwareheritage.org/how-to-archive-reference-code/)]:
1. **Save Code Now** (formulario): https://archive.softwareheritage.org/save/ → elegir `git` → pegar **URL de clonado** → Submit.
2. **Extensión de navegador UpdateSWH** (Chrome/Firefox): 1 clic desde la página del repo GitHub.
3. **API / webhook:** endpoint `POST /api/1/origin/save/` (categoría *Request archival*), o webhook oficial de GitHub
   [[API](https://docs.softwareheritage.org/_modules/swh/web/save_code_now/api_views.html)].

**Tiempos** [[FAQ oficial](https://docs.softwareheritage.org/user/faq/index.html)]: para **forjas conocidas (GitHub)** "se guardan sin aprobación → no más de unas horas" (en la práctica, minutos). Origen **desconocido** → **cola de moderación humana**, "días".

**SWHID** [[especificación](https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html)]:
- Forma `swh:1:<tipo>:<sha1>`; tipos `snp`, `rel`, `rev`, `dir`, `cnt`.
- Se obtiene en la interfaz del archivo (pestaña **permalinks**); es **verificable por cualquiera** con `swh-identify` (paquete `swh.model` en PyPI).
- Resolutor: `https://archive.softwareheritage.org/<swhid>`. **ISO/IEC 18670** y sitio **swhid.org**.
- Para citar en el paper: usar el SWHID del **revision** del tag (p. ej. `swh:1:rev:<hash-del-commit>`), con calificadores `;origin=…;visit=…` [[guía SWH](https://www.softwareheritage.org/software-hash-identifier-swhid)].

> **⚠️ NO DAR POR HECHO:** el SWHID **no es un DOI** ni un sello de tiempo de autoridad. Software Heritage
> declara explícitamente que su foco es **reproducibilidad, "no dar crédito a autores"** y su *timestamp* es la
> **fecha del propio commit** (que controla el autor). Sirve como prueba de *contenido exacto*, no de *prioridad legal*.

### (c) GitHub — tag/Release, enlace al DOI y depósito automático

- **Release requiere permiso de escritura** en el repo; el tag es inmutable y el ZIP/tarball se genera por release.
- **El enlace DOI↔Release lo hace Zenodo, no GitHub:** al habilitar la integración, **cada Release** genera un registro Zenodo nuevo (o una **nueva versión**) con su DOI; el estado se ve en el Release (panel Zenodo) y en `External resources > Archived in`.
- **Requisitos** [[GitHub Docs](https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content)]: repo **público** (Zenodo "solo puede acceder a repositorios públicos"); conectar GitHub↔Zenodo; permisos que pide Zenodo = **gestionar webhooks** (instala el webhook en repo público) + **leer organizaciones** (para repos de org; la **org debe autorizar la app Zenodo**) [[FAQ permisos](https://support.zenodo.org/help/en-gb/24-github-integration/127-which-github-permissions-do-you-request-and-why)].
- **En habilitar el repo:** profile menu → **GitHub** → **Sync now** → toggle del repo → refrescar [[enable-repository](https://help.zenodo.org/docs/github/enable-repository/)].

> **⚠️ NO DAR POR HECHO / trampas verificadas:**
> - **No hay archivo retroactivo:** un Release creado **antes** de habilitar el repo **no** se archiva.
> - **No se puede pre-reservar DOI** para un Release de GitHub (sí para un upload manual) [[FAQ](https://support.zenodo.org/help/en-gb/24-github-integration/73-can-i-pre-reserved-a-doi-before-a-github-release)].
> - **No se puede enlazar** un repo GitHub a un **registro Zenodo ya existente** (ni al DOI de concepto del pre-registro).

### (d) CITATION.cff — validación y campos obligatorios

[[schema-guide 1.2.0](https://github.com/citation-file-format/citation-file-format/blob/main/schema-guide.md)] · [[GitHub Docs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files)]:
- Debe llamarse **`CITATION.cff`** (respetando mayúsculas), en la **raíz**, ser **YAML 1.2** y **válido según schema 1.2.0**.
- **Obligatorios:** `cff-version` · `message` · `authors` (≥1) · `title`.
  **`date-released` es OPCIONAL** en 1.2.0 (era obligatorio en el viejo 1.0.3 — no confundir).
- **Validación oficial:** `cffconvert` (el propio Zenodo lo usa) y el validador/creador del proyecto CFF. GitHub **valida** y muestra aviso si es inválido; la cita aparece como **"Cite this repository"** (APA/BibTeX) en la portada del repo.
- Útiles para este proyecto: `type: software` (o `dataset`), `identifiers:` con **DOI de concepto** y **DOI de versión** (`type: doi`) y **`type: swh`** para el SWHID, y `preferred-citation:` para apuntar al **paper**.
- **Soporte de `swh` en CFF:** confirmado en la guía del schema (ejemplo con `type: swh`).

> **⚠️ NO DAR POR HECHO — conflicto CITATION.cff ↔ .zenodo.json:** si el repo tiene **ambos**, **Zenodo ignora por completo el CITATION.cff** y usa solo el `.zenodo.json` [[Zenodo](https://help.zenodo.org/docs/github/describe-software/zenodo-json/)].
> GitHub sí sigue usando `CITATION.cff` para la caja de cita. Y un `CITATION.cff` **inválido** hace que **el release FALLE** en Zenodo con `"Citation metadata load failed."` [[FAQ](https://support.zenodo.org/help/en-gb/24-github-integration/204-why-does-my-github-release-fail-with-an-error)].

### (e) arXiv — RIESGO CLAVE: endorsement y política de idiomas

**¿Necesita endorsement un autor que nunca envió a arXiv?** **SÍ. Y desde 21-ene-2026 es más difícil.**
- Política vigente [[blog 21-ene-2026](https://blog.arxiv.org/2026/01/21/attention-authors-updated-endorsement-policy/), [help](https://info.arxiv.org/help/endorsement.html)]: **ya no basta el correo institucional**. Dos caminos:
  1. **Correo institucional académico** **Y además** autoría previa en un paper **aceptado al mismo "endorsement domain"**.
  2. **Endorsement personal** de un autor establecido de arXiv **del mismo dominio**.
- Con **0 papers en arXiv**, el autor **no cumple el camino 1** → **NECESITA endorsement personal**.
- **Cómo se consigue** (camino 2): iniciar nuevo envío y elegir la categoría → llega un correo con **código de 6 caracteres** → encontrar endorsers en papers afines (enlace *"Which authors of this paper are endorsers?"* al pie de cada abstract) → enviarles el código. **Al menos un endorsement positivo por categoría.** No es apropiado escribir a muchos a la vez ni insistir al mismo.
- **Tiempo:** **NO GARANTIZADO.** Depende de que un tercero acepte. ⚠️ **Planificar con semanas de antelación.**
- **Si no lo tiene:** el envío **no se anuncia** (bloqueado). **arXiv staff NO puede dar endorsement ni saltarse el requisito.** No hay atajo dentro de arXiv.
- **Idiomas** (política vigente desde **11-feb-2026**): [[FAQ multilang](https://info.arxiv.org/help/faq/multilang.html), [blog](https://blog.arxiv.org/2026/01/13/non-english-paper-submission-guidelines/)]
  - **Obligatorio** incluir la **versión completa en inglés** (no basta el abstract), y debe ir **PRIMERO**.
  - Se acepta **traducción automática** si es fiel. Se anota idioma en el campo *Comments*.
  - ⚠️ El metadata **admite pocos caracteres no-ASCII** (tildes/ñ en el abstract → precaución).
- **Publicar antes de la sustentación:** ≥ **NO DAR POR HECHO** que "se puede sin más". arXiv **no prohíbe** publicar un preprint antes de sustentar, **pero**: (i) la licencia es **irrevocable**; (ii) arXiv **no retira** el artículo si luego un venue prohíbe distribución previa, y arXiv **recomienda no enviar** si no estás seguro de no querer publicarlo después en un venue restrictivo [[submittal agreement](https://info.arxiv.org/help/policies/submission_agreement.html)]. La decisión "preprint antes o después de sustentar" es **institucional/de comité**, no la resuelve arXiv → **preguntar al asesor**.
- Licencia: se elige en el envío y es **irrevocable**; opciones CC BY / CC BY-SA / CC BY-NC-SA / CC BY-NC-ND / arXiv no-exclusiva / CC0 [[license](https://arxiv.org/help/license)]. CC BY permite reuso comercial → puede chocar con algunos venues.

### (f) Alternativas de preprint **sin endorsement** y su valor probatorio

- **Zenodo `publication/preprint`:** DOI **inmediato**, sin comité científico. Es la vía más rápida y controlada; **ya es la casa del pre-registro**. (Mismo sistema de DOIs de versión/concepto.)
- **OSF Preprints:** red de servidores; **pre-moderación** (pending privado hasta que un moderador acepte/rechace) → al aceptar da **DOI + URL persistente** [[376](https://help.osf.io/article/376-preprints-home-page), [178](https://help.osf.io/article/178-submitting-to-a-moderated-preprint-service), [691 políticas](https://help.osf.io/article/691-preprint-moderation-policies)]. Licencias recomendadas CC0 / CC-BY 4.0.
  ⚠️ **OSF muestra un aviso de "Project Transition"** (oct-2025) → **verificar continuidad del servicio** antes de depender de él.
- **ResearchGate:** genera DOI propio `10.13140/RG…` **solo para trabajos no publicados** (preprint/tesis/dataset) con full-text público; una vez generado, **el ítem no se puede editar** [[RG DOIs](https://help.researchgate.net/research-and-publications/researchgate-dois)].
  ⚠️ **Valor probatorio BAJO**: es la plataforma comercial, no un repositorio de preservación ni registro de prioridad reconocido. **No usarlo como sello de prioridad.**

### (g) Qué sello da cada uno y cuál implica **prioridad demostrable**

| Mecanismo | Sello que emite | ¿Prioridad demostrable ante tercero? |
|---|---|---|
| **Zenodo (DOI)** | DOI registrado en **DataCite** + fecha de publicación en metadata | **El más fuerte de los gratuitos.** Registro de tercero, resoluble, citable. (La fecha la **declara el autor**, no es timestamp criptográfico.) |
| **GitHub tag/Release** | Hash SHA-1 del commit + fecha del Release en la API | Media. Evidencia buena, pero fecha/hora las fija **GitHub/el autor**. |
| **Software Heritage (SWHID)** | Identificador **intrínseco** (hash) + visita registrada | Fuerte para *"este contenido exacto existía"*; **no** es DOI ni autoridad de sellado. |
| **arXiv** | `arXiv:YYMM.NNNNN` + **fecha de anuncio** pública | Fuerte en la **comunidad científica**, pero **bloqueado por endorsement**. |
| **OSF** | DOI + fecha de publicación al aceptar | Comparable a Zenodo, con pre-moderación. |
| **ResearchGate** | DOI propio `10.13140/RG…` | **Débil**; no lo cuentes como prioridad. |

> **⚠️ Advertencia global.** **Ninguno** de los gratuitos emite un *sello de tiempo* de autoridad de sellado
> (tipo **RFC 3161 / TSA**). Si se necesitara "existencia en fecha X" ante un tercero hostil, habría que añadir
> un sello gratuito tipo **OpenTimestamps** sobre el **hash del commit**. No es necesario para el objetivo
> actual (crédito y trazabilidad), pero **no se debe afirmar** que un DOI "prueba" una fecha de autoría.

---

## 3. Orden recomendado de ejecución

1. **Cerrar el repo**: `LICENSE` (Apache-2.0), `LICENSE-docs` (CC-BY-4.0), `CITATION.cff` **válido** (`cffconvert`), y `.zenodo.json` **solo si** se necesitan `grants`/`communities`. Commit.
2. **Conectar Zenodo↔GitHub y habilitar el repo** (público) **ANTES** de crear el release.
3. **Crear tag `v1.0.0` + Release** en GitHub → Zenodo archiva y emite **DOI de versión**; **guardar el DOI de concepto**.
4. **Añadir el DOI de concepto** a `CITATION.cff`/`README` en un commit **posterior** (⚠️ no se puede pre-reservar DOI para un release).
5. **Save Code Now** sobre el commit/tag → obtener **SWHID** → pegarlo en `CITATION.cff` (`identifiers: type: swh`).
6. **Publicar el paper** como `publication/preprint` en **Zenodo** (DOI) y/o en **OSF Preprints**.
7. **arXiv (opcional/decisión del autor):** iniciar el **endorsement con semanas de antelación**; preparar **versión inglesa completa primero**.
8. **ORCID** `0009-0004-7605-6569`: importar los DOIs como *works* (crédito verificable).

---

## 4. Errores típicos que invalidan un release (los 3 que más rompen)

1. **Release sin depósito real.** Release creado **antes** de habilitar Zenodo (o sin tag propio) → **no hay DOI**; Zenodo **no archiva retroactivamente** ni permite pre-reservar el DOI.
2. **DOI sin metadatos útiles / confundir versión con concepto.** DOI sin licencia, sin tipo de recurso, sin ORCID ni relación al paper → existe pero no es "citable de verdad"; y citar el **DOI de versión** cuando se quería el **de concepto** (o viceversa) genera citas divergentes.
3. **Licencia o cita mal puestas.** `CITATION.cff` **inválido** → **el release FALLA** en Zenodo (`"Citation metadata load failed."`, no se archiva nada); y si hay `CITATION.cff` **y** `.zenodo.json`, Zenodo **ignora el CITATION.cff** (alinear ambos). Añadir la licencia *dentro* de la metadata hace que Zenodo no interprete el archivo `LICENSE`.
4. **Extra:** enviar a arXiv el paper **solo en español** (rechazo por política de idioma) o **sin endorsement** (no se anuncia).

---

## 5. Fuentes (URLs consultadas el 12-oct-2026)

**Zenodo:** help/versioning · about-records · manage-versions · manage-files · reserve-doi · resource-type · describe-records · github/enable-repository · github/describe-software · github/describe-software/zenodo-json · github/archive-software/github-upload · support FAQ GitHub integration (permisos · pre-reserva DOI · fallo de release) · developers.zenodo.org · zenodo.org/help/versioning
**Software Heritage:** how-to-archive-reference-code · docs FAQ · api_views (origin/save) · persistent-identifiers · software-hash-identifier-swhid · FAQ general · updateswh (extensión)
**GitHub:** managing-releases-in-a-repository · referencing-and-citing-content · about-citation-files
**CITATION.cff:** schema-guide (1.2.0) · schema.json · cffr / cffconvert
**arXiv:** endorsement · blog 21-ene-2026 (endorsement) · FAQ multilang · blog 13-ene-2026 (guidelines) · blog 21-nov-2025 (cambio de política) · moderation · submit · license · submission_agreement · translations
**OSF:** help 376 · help 178 · help 691
**ResearchGate:** help/researchgate-dois
