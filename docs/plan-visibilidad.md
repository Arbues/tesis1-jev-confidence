# Plan de visibilidad del artefacto — Tesis 1

**Qué es este documento.** Cómo hacer que el instrumento de la Tesis 1 (*metrología y transferencia del campo
`confidence` en modelos de decisión tipo Jev*) sea **encontrable, instalable y citable** por gente que no es el
autor. No propone ciencia nueva: propone **distribución**.

| | |
|---|---|
| Autor del plan | 🤖 agente (Hermes), a partir de `README.md` §10-bis, `STATE.json`, `docs/guia-cierre-pendientes.md` (FASE 5), `eje-2-jev-opensource/FUENTES.md` y `08_estudio_ecosistema.md` |
| Destinatario | ✋ Arbués Enrique Pérez V. (FC-UNI, ORCID `0009-0004-7605-6569`) |
| Fecha | **20-oct-2026** (todas las cifras de línea base medidas ese día; ver Anexo F) |
| Estado del repo | `main` en `40b7f42` (13-oct-2026); el árbol de trabajo tiene cambios en curso sobre `conf_score` (pendiente n=3), hechos por otro proceso |
| Coste total del plan | **USD 0** (PyPI, GitHub, Zenodo, Software Heritage, Hugging Face, arXiv, foros: todos gratuitos) |
| Hardware | ThinkPad T440 sin GPU + navegador. **Ninguna acción de este plan necesita GPU ni cómputo** |
| Restricción dura | El paper en inglés (`paper/en/`) **está bloqueado** hasta que el autor apruebe el borrador español §1–§7. El plan está partido en dos por esa línea |

**Orden de lectura, si no se quiere leer todo:** §1 (decidir, 2 min) → §2 (diagnóstico medido) → §4 (las tres fases
con checklist) → §3 (el detalle de cada canal, solo del canal que se vaya a ejecutar) → §6–§7 (riesgos y métricas)
→ Anexos (plantillas y comandos listos para copiar).

---

## 1. Resumen para decidir (una página)

### 1.1 El diagnóstico en una frase

**El artefacto existe, está medido y está fechado con tres DOI — pero hoy no se puede instalar, no aparece en
ningún índice del ecosistema y su registro de software no está en OpenAIRE.** La tesis está *reservada*; no está
*distribuida*. Reservar protege la prioridad; distribuir es lo que produce citas.

### 1.2 Las cinco puertas, y cuántas están abiertas

```
QUIÉN BUSCA                        PUERTA                         ESTADO HOY (20-oct-2026)
──────────────────────────────────────────────────────────────────────────────────────────
practicante que quiere medir   →   pip install jev-conf-metrics   →   ❌ HTTP 404: no existe en PyPI
dev del ecosistema             →   GitHub topics / búsqueda       →   ❌ 0 topics, descripción en español
curador de awesome-jev         →   PR a categories/…              →   ❌ no hay entrada (54 en esa categoría)
investigador                   →   OpenAIRE / arXiv / Scholar     →   ⚠️ preprint en Zenodo; software NO indexado; sin arXiv
revisor / comité               →   DOI / SWHID                    →   ✅ los tres DOI y el SWHID resuelven
```

Cuatro de cinco puertas cerradas. Las tres primeras necesitan, antes que nada, **una sola cosa**: que el paquete
se pueda instalar. Eso es lo que ordena este plan.

### 1.3 Las cuatro decisiones que el autor debe tomar (§9 las detalla)

| # | Decisión | Recomendación del agente | Coste de equivocarse |
|---|---|---|---|
| D-1 | ¿Publicar `jev-conf-metrics` en PyPI **ahora**, con versión `0.2.0` y CLI `jevconf`? | **Sí.** El nombre está libre (verificado 404) y el paquete ya construye wheel y sdist sin dependencias | Alto: si otro registra el nombre, el DOI del instrumento apunta a un repo que no se instala |
| D-2 | ¿La CLI mínima va en **este** repo o se espera al repo `decision-calibration-bench`? | **En este repo**, 5 subcomandos offline (`defs`, `conf`, `ece`, `umbral`, `transfer`). La CLI completa (`medir`, `matriz`, `informe`) sigue siendo del framework | Medio: esperar al framework retrasa la puerta principal 2–4 semanas sin ganar nada |
| D-3 | ¿Subir la matriz (2,2 MB) y las 65.185 mediciones (120 MB) a Hugging Face como *dataset*? | **Sí**, con la matriz primero y los crudos después | Bajo, pero se pierde el canal donde el ecosistema ya busca datos (`LocalLLaMA/typed-decisions` vive ahí) |
| D-4 | ¿Pedir el endosso de arXiv ya, o cuando exista `paper/en/`? | **Cuando exista el borrador en inglés.** Un endosante tiene que poder juzgar el texto | Bajo: pedirlo antes obliga a pedirlo dos veces |

### 1.4 Lo que se puede hacer esta semana sin inglés y sin aprobación

| Orden | Acción | Quién | Tiempo | Cierra cuando |
|---|---|---|---|---|
| 1 | `gh repo edit` con descripción, 12 topics y homepage = DOI (§3.4) | 🤖 | 15 min | la API devuelve los topics y el DOI |
| 2 | `cli.py` + `[project.scripts]` + README de paquete en inglés (§3.2) | 🤖 | 2–3 h | `jevconf conf --p 0.7,0.1,0.1,0.1` imprime la tabla |
| 3 | Cuenta PyPI + token + 2FA (§3.2) | ✋ | 10 min | el token existe y está en `~/.env`, no en el repo |
| 4 | TestPyPI y luego PyPI (§3.2) | 🤖 publica, ✋ autoriza | 20 min | `pip install jev-conf-metrics` en venv limpio |
| 5 | Dataset en Hugging Face (§3.6) | ✋ cuenta + 🤖 sube | 1 h | `hf download` devuelve el CSV |

Nada de esto toca el paper, ni el pre-registro, ni requiere aprobación de nadie más que el autor.

---

## 2. Diagnóstico

### 2.1 La línea base, medida (no estimada)

Todo lo de esta tabla se obtuvo el **20-oct-2026** con los comandos del Anexo F. Si una cifra no está aquí, no
existe.

| Señal | Valor hoy | Qué significa |
|---|---|---|
| `pypi.org/pypi/jev-conf-metrics/json` | **HTTP 404** | El nombre está libre; nadie puede instalar el instrumento por `pip` |
| `pypi.org/pypi/jevconf/json` | **HTTP 404** | El nombre del comando también está libre |
| GitHub: estrellas / forks / issues | **0 / 0 / 0** | Sin tráfico orgánico ni señal social |
| GitHub: `topics` | **`[]`** | Invisible en la búsqueda por tema, que es como se navega este ecosistema |
| GitHub: `description` | en español, sin cifras | Un visitante anglófono no sabe qué mide ni cuánto |
| GitHub: `homepage` | **`null`** | El botón "About" no lleva al DOI |
| GitHub: Discussions | **desactivadas** | No hay dónde preguntar sin abrir un issue |
| Tráfico 14 días: vistas / clones | **14 (1 único) / 345 (156 únicos)** | El clonado es del propio autor y sus agentes; no hay terceros |
| Zenodo software `…23330647` | **2 vistas, 2 descargas** | Prácticamente nadie ha abierto el registro |
| Zenodo preprint `…23329431` | 2 vistas, 5 descargas | Ídem |
| Zenodo pre-registro `…23266795` | 4 vistas, 1 descarga | Ídem |
| OpenAIRE, DOI del **software** | **total = 0** | No está cosechado: el índice académico no lo ve |
| OpenAIRE, preprint y pre-registro | **total = 1** cada uno | El cosechador funciona; el registro de software se quedó atrás |
| Software Heritage, revisión `39a6856…` | **resuelve** (200, con autor y fecha) | Archivo independiente correcto |
| Build del paquete (`uv build`) | **wheel 21.549 B + sdist 32.201 B**, 0 dependencias | **Se puede publicar hoy**: ya construye |
| Wheel: `entry_points` | **ninguno** | No hay comando; no hay CLI |
| `python -m jev_conf_metrics` | **falla** (`No module named …__main__`) | No hay punto de entrada alternativo |
| Metadata del wheel: `Summary` | en español | Todo el ecosistema publica en inglés (Laya, Kev, Nimble, SemIf, los arneses del índice): un resumen en español no se encuentra buscando en inglés |
| Metadata del wheel: descripción larga | **27.654 bytes del `README.md` interno** (el `METADATA` completo son 27.941 caracteres) | En PyPI se vería la bitácora del proyecto, no una portada del instrumento |
| Tests | **52 en `main`; 63 en el árbol de trabajo** | 11 nuevos de `conf_score` en curso (pendiente n=3) |

### 2.2 Qué tiene el artefacto a su favor (y no está usando)

| Activo | Dónde está | Por qué vale para visibilidad |
|---|---|---|
| Tres DOI publicados y verificados | Zenodo: pre-registro, software v1.0.1, preprint | Un enlace con DOI es lo que convierte un post en citable |
| SWHID | `swh:1:rev:39a685679905b7445b1a455d812b416f1acb9ef0` | Archivo independiente del proveedor; los archivos de software lo valoran |
| 65.185 decisiones y 3.564 celdas | `results/crudos/` (120 MB) y `results/matrix/` (2,2 MB) | Es el dato que nadie más tiene; es *subible* a un dataset público |
| 8 figuras listas | `paper/figures/` | Material directo para un post; la fig. 4 (por par) es la que se entiende sin leer nada |
| Librería stdlib puro, 0 dependencias | `src/jev_conf_metrics/` | Instalación sin fricción: el argumento más fuerte para PyPI |
| `CITATION.cff` válido con 6 identificadores | raíz del repo | Botón "Cite this repository" en GitHub |
| Cifras titulares cerradas y defendibles | `results/matrix/RESUMEN_MATRIZ.md` | Permiten un anuncio con números, sin adjetivos |

### 2.3 Qué falta, en orden de bloqueo

```
   (falta) CLI + metadata  ──►  PyPI  ──►  README público  ──►  foros  ──►  citas
        │                         │
        └── bloquea todo          └── bloquea los anuncios (sin paquete, el enlace es muerto)

   paper ES aprobado  ──►  paper/en/  ──►  endosso  ──►  arXiv  ──►  visibilidad académica
        (✋, pendiente n=1)                     (✋, externo)
```

Hay dos cadenas, no una. **La cadena de arriba no depende del inglés ni de la aprobación del paper**: por eso es
la que se ejecuta primero. La de abajo sí, y es la única parte del plan que puede tardar meses.

### 2.4 Cómo encaja con la FASE 5 de `docs/guia-cierre-pendientes.md`

La guía de cierre dice *qué* hace falta; este documento dice *cómo*, *dónde* y *cómo se comprueba*. Mapeo directo:

| FASE 5 (guía) | Canal aquí | Qué añade este plan |
|---|---|---|
| 1. README del framework en inglés con cita y DOI | **C2** + **C1** | Estructura de 9 secciones, ejemplo verificado, y el aviso de que hoy la descripción larga de PyPI sería la bitácora interna |
| 2. `CITATION.cff` en el framework + "Cómo citar" | **C2**, **C3** | `preferred-citation` al preprint y el botón de GitHub |
| 3. Metadatos: keywords, classifiers, description con cifras, topics | **C1**, **C3** | Los valores literales, campo por campo |
| 4. Anuncio en los foros de `FUENTES.md`, siempre con DOI | **C5** | URL por foro, regla del foro, formato de entrada y criterio de cierre |
| 5. Versión corta divulgativa: 1 figura + tabla por par | **C6** | Qué figura, qué tabla, longitud y dónde vive |

Lo que este plan **no** hace: cambiar el orden de las fases de la guía, ni proponer tocar el paper, ni el
pre-registro, ni la matriz sellada.

---

## 3. Canales priorizados

### 3.1 Tabla maestra

Retorno y esfuerzo en escala 1–5 (5 = máxima). El orden de ejecución **no** es el del ratio: `C3` va primero
porque cuesta 15 minutos y no depende de nada; `C1` va segundo porque **desbloquea a C5 y C6**.

| # | Canal | Retorno | Esfuerzo | Depende de | Coste | Quién | Cierra cuando |
|---|---|---|---|---|---|---|---|
| **C3** | GitHub: descripción, topics, homepage, Discussions | 3 | 1 | — | $0 | 🤖 | la API devuelve 12 topics y `homepage` = DOI |
| **C1** | PyPI `jev-conf-metrics` + CLI `jevconf` | 5 | 3 | D-1, D-2 | $0 | 🤖 + ✋ (cuenta) | `pip install` limpio + `jevconf` responde |
| **C2** | README de paquete en inglés + `CITATION.cff` + "Cómo citar" | 4 | 2 | C1 | $0 | 🤖 | el README de PyPI tiene ejemplo ejecutable |
| **C4** | Catálogos: OpenAIRE, Zenodo (grafo), SWH (re-visita), Scholar | 2 | 1 | C1 | $0 | 🤖 | OpenAIRE devuelve `total ≥ 1` para el DOI del software |
| **C6** | Nota divulgativa: 1 figura + tabla por par (ES y EN) | 3 | 2 | C1 | $0 | 🤖 + ✋ (revisa) | publicada y enlazada desde el README |
| **C5** | Foros del ecosistema (awesome-jev, r/LocalLLaMA, HF, issues) | 4 | 3 | C1, C2, C6 | $0 | 🤖 redacta / ✋ publica | entrada mergeada + ≥3 hilos con dato |
| **C7** | Paper en inglés → arXiv | 5 | 5 | aprobación §1–§7 y endosso | $0 | ✋ envía / 🤖 prepara | `arxiv.org/abs/…` responde 200 |

### 3.2 C1 — PyPI: el paquete que hoy no existe

**Por qué es la puerta.** En este ecosistema, "¿esto se instala?" se responde con `pip install`. Un repo con 400
líneas de README y sin paquete se lee como un ejercicio; un paquete con un comando se lee como una herramienta.
Además, PyPI es el único canal que **no exige inglés en el paper**: solo pide que la portada del paquete esté en
inglés, y eso es metadata, no la tesis.

**Lo que ya está verificado que funciona.** El paquete construye hoy, sin tocar nada:

```bash
cd /home/arbues/paper-tesis1
uv build --out-dir /tmp/dist          # -> jev_conf_metrics-0.1.0-py3-none-any.whl (21.549 B) + .tar.gz
# el wheel instala en un venv limpio y expone 33 nombres
```

**Lo que hay que arreglar antes de publicar** (todo en `pyproject.toml` y en archivos nuevos):

| # | Problema medido | Arreglo | Archivo |
|---|---|---|---|
| 1 | `readme = "README.md"` apunta a la bitácora interna (27.654 bytes, en español) | Crear `README-pypi.md` (~120 líneas, inglés, portada del instrumento) y apuntar `readme` ahí | `pyproject.toml`, `README-pypi.md` |
| 2 | `Summary` en español | `"Measure and transfer the confidence field across Jev-type decision models"` | `pyproject.toml` |
| 3 | Sin `classifiers` | Los 6 de la tabla de abajo | `pyproject.toml` |
| 4 | `license = { text = "Apache-2.0" }` (forma antigua) | `license = "Apache-2.0"` + `license-files = ["LICENSE"]` (PEP 639: exige subir `setuptools>=68` a **`>=77`** en `[build-system]`, o el build falla) | `pyproject.toml` |
| 5 | Sin `[project.scripts]` | `jevconf = "jev_conf_metrics.cli:main"` | `pyproject.toml` |
| 6 | No hay `cli.py` ni `__main__.py` | 5 subcomandos offline (tabla siguiente) | `src/jev_conf_metrics/cli.py` |
| 7 | 4 `Project-URL` y ninguno apunta al DOI del software | Añadir `Instrumento (DOI)`, `Documentación` (preprint) y `Changelog` | `pyproject.toml` |
| 8 | Versión `0.1.0` sin release pública | Subir a **`0.2.0`** (añadir CLI es *feature*) y tag `v0.2.0` | `pyproject.toml` |

**Metadata propuesta, campo por campo** (copiable):

| Campo | Valor |
|---|---|
| `name` | `jev-conf-metrics` |
| `version` | `0.2.0` |
| `summary` | `Measure and transfer the confidence field across Jev-type decision models` |
| `keywords` | `confidence calibration, threshold transfer, decision models, jev, expected calibration error, selective prediction` |
| `classifiers` | `Development Status :: 4 - Beta` · `Intended Audience :: Science/Research` · `License :: OSI Approved :: Apache Software License` · `Programming Language :: Python :: 3 :: Only` · `Topic :: Scientific/Engineering :: Artificial Intelligence` · `Typing :: Typed` (solo si se añaden anotaciones) |
| `requires-python` | `>=3.10` (ya está) |
| `dependencies` | `[]` (ya está; **no añadir numpy**: es la ventaja competitiva) |
| `project.urls` | `Homepage` = repo · `Repository` = repo · `Documentation` = DOI del preprint · `Pre-registro (DOI)` = `10.5281/zenodo.23266795` · `Instrumento (DOI)` = `10.5281/zenodo.23330647` · `ORCID` |

**La CLI mínima** (5 subcomandos, stdlib puro, sin GPU, sin red):

| Subcomando | Qué imprime | Ejemplo literal | Criterio de aceptación |
|---|---|---|---|
| `jevconf defs` | Las definiciones DEF-1…DEF-5 con fórmula, rango y clase (escala o forma) | `jevconf defs` | 5 filas, sin cifras inventadas: se leen del módulo |
| `jevconf conf` | Las 4 definiciones de **una** distribución, y la brecha máxima−mínima | `jevconf conf --p 0.7,0.1,0.1,0.1` | imprime `0.3216 … 0.7` y `brecha 0.3784` |
| `jevconf ece` | ECE (ancho y masa), Brier, AUROC, cobertura a `q` | `jevconf ece --csv m.csv --conf pmax` | funciona sobre un CSV de 2 columnas (`conf,correcto`) |
| `jevconf umbral` | τ para cobertura `q`, cobertura y precisión resultantes | `jevconf umbral --csv m.csv --conf ent --q 0.80` | devuelve 3 números y el `n` |
| `jevconf transfer` | Δ del porte directo y Δ con mapa entre dos definiciones, sobre las mismas filas | `jevconf transfer --csv m.csv --desde pmax --hasta ent --q 0.80` | devuelve los dos Δ y el `n` de la celda; es el comando del Anexo E |

El ejemplo de `conf` es el más importante: **es la tesis en un comando**. Con la misma distribución de 4 opciones,
`pmax` dice 0.70 y `ent` dice 0.3216 — una brecha de 0.378. Verificado contra la librería instalada el 20-oct-2026.

**Publicación, paso a paso:**

```bash
# 1) construir
cd /home/arbues/paper-tesis1 && rm -rf dist && uv build --out-dir dist

# 2) ensayo en TestPyPI (gratis, se puede repetir)
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TESTPYPI_TOKEN" dist/*

# 3) instalación de prueba DESDE TestPyPI, en venv limpio
uv venv /tmp/vtest            # ojo: un venv de uv NO trae pip; se instala con uv pip
uv pip install --python /tmp/vtest/bin/python \
  --index-url https://test.pypi.org/simple/ jev-conf-metrics
/tmp/vtest/bin/jevconf conf --p 0.7,0.1,0.1,0.1

# 4) producción (irreversible: PyPI no deja borrar, solo yank)
uv publish --token "$PYPI_TOKEN" dist/*
```

| | |
|---|---|
| ✋ Autor | Crear cuenta en `https://pypi.org/account/register/`, activar 2FA, crear token en `https://pypi.org/manage/account/token/` (alcance: solo el proyecto, no global) y dejarlo en `~/.env` como `PYPI_TOKEN`. **Nunca al repo** |
| 🤖 Agente | Todo lo demás, incluido el ensayo en TestPyPI |
| Coste | **USD 0** |
| Tiempo | ✋ 10 min (una vez) · 🤖 3 h (código + metadata + README) + 20 min (publicar y verificar) |
| Cierre | `https://pypi.org/project/jev-conf-metrics/` responde 200; en un venv limpio `pip install jev-conf-metrics && jevconf --version` funciona; el README de PyPI muestra el ejemplo |
| Trampa | Un *placeholder* vacío para "reservar el nombre" es peor que no tener nada: PyPI **no permite borrar**, solo *yank*, y un paquete vacío queda en el historial para siempre |

### 3.3 C2 — README de paquete en inglés, `CITATION.cff` y "Cómo citar"

**Aviso de alcance, para que no haya confusión:** este README es **metadata del software**. No es `paper/en/`, no
traduce la tesis, no necesita aprobación de nadie y **no desbloquea ni condiciona** el paper en inglés. Son dos
cosas distintas que comparten el idioma.

**Estructura propuesta (9 secciones, 90–130 líneas):**

| # | Sección | Contenido exacto | Líneas |
|---|---|---|---|
| 1 | Título + una frase | Qué mide, en una línea, sin adjetivos | 3 |
| 2 | The problem | "The same field `confidence` means different things; a threshold calibrated in one definition means nothing in another" | 5 |
| 3 | What this gives you | 4 viñetas: definiciones, métricas, transferencia, CLI | 8 |
| 4 | Install | `pip install jev-conf-metrics` | 3 |
| 5 | Four lines that show the point | El ejemplo de abajo, con su salida | 10 |
| 6 | What was measured | Tabla con las cifras titulares y su DOI | 10 |
| 7 | The two layers | Escala vs forma, en 4 líneas | 6 |
| 8 | Cite | `CITATION.cff` + DOI del software y del preprint | 6 |
| 9 | License / scope | Apache-2.0 código, CC-BY-4.0 texto; qué **no** hace | 6 |

**El ejemplo de la sección 5, con su salida real** (verificado instalando el wheel el 20-oct-2026):

```python
from jev_conf_metrics import all_confidences

p = [0.70, 0.10, 0.10, 0.10]          # one distribution, four options
all_confidences(p)
# {'jev': 0.6, 'ent': 0.3216, 'pmax': 0.7, 'margin': 0.6}
```

Cuatro líneas, una brecha de 0.378, cero configuración. Ese es el gancho: si el lector no entiende el problema
después de esto, no lo va a entender con el paper.

**`CITATION.cff`**: el del repo ya está validado con 6 identificadores; el del paquete debe ser el mismo archivo
más un bloque `preferred-citation` que apunte al **preprint** (`10.5281/zenodo.23329431`) con `type: article`. Con
eso, GitHub muestra el botón *Cite this repository* y quien cite el software acaba citando el paper.

**Sección "Cómo citar" en el `README.md` del repo** (hoy no existe: verificado, no hay ninguna coincidencia de
"cómo citar" ni "cite this"): tres líneas con el DOI del instrumento, el del preprint y el `BibTeX` mínimo.

| | |
|---|---|
| 🤖 Agente | Redactar `README-pypi.md`, el `CITATION.cff` del paquete y la sección de cita del repo |
| ✋ Autor | Leer 5 minutos y corregir el tono (una sola pasada) |
| Coste | $0 · Tiempo: 2 h 🤖 + 10 min ✋ |
| Cierre | El README de PyPI renderiza el ejemplo y los DOI; `CITATION.cff` valida contra el esquema (0 errores) |

### 3.4 C3 — GitHub: que la portada diga qué es y cuánto mide

Hoy la portada del repo es una bitácora de tesis en español, con `topics` vacío y sin homepage. Para un visitante
que llega desde un foro, la información utile —qué mide, cuánto, dónde está el DOI— está en la línea 340 de un
documento de 407.

**Cambios, con comando literal:**

```bash
gh repo edit Arbues/tesis1-jev-confidence \
  --description "Metrology and threshold transfer for the confidence field in Jev-type decision models: 65,185 decisions, 23 groups, 3,564 cells. Median gap 0.288; 0.2337 vs 0.0021 with map (109x)." \
  --homepage "https://doi.org/10.5281/zenodo.23330647" \
  --add-topic jev --add-topic confidence-calibration --add-topic calibration \
  --add-topic threshold-transfer --add-topic decision-models --add-topic metrology \
  --add-topic model-evaluation --add-topic reproducibility --add-topic research-software \
  --add-topic python --add-topic open-weights --add-topic thesis \
  --enable-discussions
```

| Qué | Valor propuesto | Por qué ese |
|---|---|---|
| Descripción | la de arriba (≈ 220 caracteres) | Lleva las cifras del titular: es lo único que se ve en un resultado de búsqueda |
| Homepage | DOI del **instrumento** (concepto `…23328988` si se prefiere el puntero móvil) | Un clic desde GitHub al registro citable |
| Topics | 12 | `jev`, `confidence-calibration`, `calibration`, `threshold-transfer`, `decision-models`, `metrology`, `model-evaluation`, `reproducibility`, `research-software`, `python`, `open-weights`, `thesis` |
| Discussions | activadas | Da un sitio para preguntar sin abrir un issue; hoy está en `false` |
| Social preview | PNG 1280×640 con la fig. 4 (por par) + el titular | Es la miniatura que aparece al pegar el enlace en un foro |
| Release destacada | `v1.0.1` ya es *Latest* | Ya está bien; no tocar |
| Issue templates | 2: "reportar una cifra que no reproduce" y "proponer una definición" | Convierte un visitante en colaborador |

El **social preview** es el único paso que no tiene comando: se sube a mano en
`https://github.com/Arbues/tesis1-jev-confidence/settings` → *Social preview* → *Edit* → *Upload an image*.
🤖 genera el PNG desde `paper/figures/fig4-por-par.png` + una banda con el titular.

| | |
|---|---|
| 🤖 Agente | Comando `gh repo edit`, generar el PNG, redactar las plantillas de issue |
| ✋ Autor | Subir la imagen (30 s) |
| Coste | $0 · Tiempo: 20 min 🤖 + 1 min ✋ |
| Cierre | `gh api repos/Arbues/tesis1-jev-confidence --jq '{topics,homepage,description}'` devuelve los 12 topics y el DOI; Discussions aparece en la barra |

### 3.5 C4 — Catálogos académicos: qué falta de verdad

Aquí hay que ser honesto: **la mayor parte ya está hecha**, y lo que falta es más pequeño de lo que parece.

| Catálogo | Estado real (20-oct-2026) | Acción | Cierre |
|---|---|---|---|
| **Zenodo** | 3 depósitos publicados y verificados por API | (a) Cerrar el grafo de relaciones (pendiente n=4, cosmético, 15 min): `isSupplementedBy` del pre-registro al software y `isSupplementedBy`/`references` entre software y preprint. (b) Al publicar `v0.2.0`, el Release crea una **versión nueva** con DOI propio, sin romper el de concepto | el registro muestra las relaciones y el DOI de concepto apunta a `0.2.0` |
| **Software Heritage** | Revisión archivada, SWHID resuelve | Re-visitar el repo **después** del repo nuevo del framework (`https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://github.com/Arbues/tesis1-jev-confidence`); el SWHID nuevo va al `CITATION.cff` | el SWHID del commit del release nuevo resuelve |
| **OpenAIRE** | **Preprint y pre-registro: indexados (total = 1). Software: NO (total = 0)** | (a) Re-consultar la API en 15 y 30 días. (b) Revisar que el registro de DataCite tenga `subjects` y `relatedIdentifiers` completos. (c) Si a 30 días sigue en 0, escribir al soporte de OpenAIRE con el DOI (gratis) | `https://api.openaire.eu/search/publications?doi=10.5281/zenodo.23330647&format=json` devuelve `total ≥ 1` |
| **Google Scholar** | Sin verificar (depende de la cosecha de DataCite/Zenodo) | Buscar el título exacto a las 2–6 semanas; si aparece, el enlace se añade al README | aparece al buscar el título entre comillas |
| **ASCL** | **No presentado, y recomiendo no presentarlo** | ASCL indexa software de **astronomía y astrofísica**; este instrumento no lo es. El encaje es débil y una entrada rechazada no aporta nada | — (se deja fuera; ver §7) |
| **ORCID** | 3 works | Añadir el DOI del paquete `0.2.0` como cuarto *work* cuando exista (3 min, ✋) | la API pública de ORCID devuelve 4 works |

**Sobre OpenAIRE, que es el hallazgo nuevo de este diagnóstico.** Que el preprint esté y el software no sugiere
**retraso de cosecha**, no un error de metadata: los dos registros salieron el mismo día y con el mismo publicador.
Por eso la acción es *esperar y verificar*, no *arreglar*. Lo que sí conviene arreglar es el grafo de Zenodo, porque
un registro sin relaciones es más difícil de enlazar por un cosechador.

| | |
|---|---|
| 🤖 Agente | Consultas, revisión de DataCite, edición del grafo en Zenodo (con ✋ delante de "Publicar"), correo al soporte si toca |
| ✋ Autor | Publicar los cambios de metadatos en Zenodo (la interfaz no deja hacerlo por API sin token) y añadir el work en ORCID |
| Coste | $0 · Tiempo: 1 h 🤖 + 10 min ✋ |
| Cierre | OpenAIRE `total ≥ 1` para el DOI del software; ORCID con 4 works |

### 3.6 C5 — Foros y comunidades del ecosistema

**Regla que gobierna todo este bloque:** no se anuncia nada hasta que `pip install jev-conf-metrics` funcione y el
DOI esté en el texto. Un anuncio con enlace muerto quema el canal una sola vez y no se recupera.

| Comunidad | URL literal | Qué se publica | Regla del lugar | Cierra cuando | Riesgo |
|---|---|---|---|---|---|
| **awesome-jev** (índice curado) | `https://github.com/yibie/awesome-jev` → PR a `categories/calibration-research.md` | **Una** viñeta de una frase: dominio + método + cifra, con el DOI | Verificado en su `CONTRIBUTING.md`: una entrada, una categoría, **una sola frase**, sin prosa larga; rechazan repos "cuya documentación pesa más que su código" | la entrada está mergeada y la línea del índice dice 55 entradas | **Medio-alto**: el repo es mayoritariamente documentación de tesis. Mitigación: entrar **después** de C1, citando el paquete y el comando, no la tesis |
| **r/LocalLLaMA** | `https://www.reddit.com/r/LocalLLaMA/` | Post de texto: 1 figura (fig. 4), 5 líneas, DOI, comando de instalación | Revisar la barra lateral antes de publicar (autopromoción limitada, sin enlaces repetidos). Un post, una vez | 72 h vivo con ≥ 1 comentario técnico respondido | Medio: sin cuenta con historial, el filtro antispam lo puede comer |
| **Hugging Face (dataset)** | `https://huggingface.co/new-dataset` → `Arbues/jev-confidence-transfer-matrix` | La matriz (2,2 MB, 21 columnas) + los 23 `.jsonl` crudos en un segundo repo, con *dataset card* en inglés | Gratis; la card necesita YAML (`license: apache-2.0`, `tags: [jev, calibration, metrology]`) | `hf download Arbues/jev-confidence-transfer-matrix` funciona y aparece en la búsqueda de datasets por "jev" | Bajo. Es el canal natural: `LocalLLaMA/typed-decisions` ya vive ahí |
| **Issues técnicos en los proyectos del ecosistema** | `NandhaKishorM/laya`, `jaredpalmer/kev`, `bespokelabsai/nimble`, `TheoLeeCJ/SemIf-OpenJev`, `Gestalt-Lab/jeff` | Un issue con **un dato que les afecta** y el enlace al DOI. Ej.: a Laya, "tu `confidence` es `1−H/log k`; medimos cuánto se degrada un umbral portado desde `pmax`: celda X, Δ = Y" | Dato, no promoción. Nada de "mira mi repo" sin número | ≥ 3 issues abiertos con cifra y respuesta o cierre razonado | Medio: un issue promocional se cierra en 10 minutos y deja mala fama |
| **X / Twitter** | cuenta del autor | Hilo de 6 tuits: fig. 4, la tabla por par, DOI, `pip install` | — | ≥ 1 cita de un tercero (no se persigue) | Bajo |
| **Show HN** | `https://news.ycombinator.com/submit` | Título "Show HN: …" + el comando + el DOI | Un solo envío; sin pedir votos | ≥ 10 puntos en 24 h (si no, no se repite) | **Alto**: invisible sin tracción previa. Hacerlo solo si C1 y C5-awesome-jev ya dieron señal |
| **dev.to / blogs del ecosistema** | `https://dev.to/new` | La nota divulgativa de C6, en inglés | — | publicado con enlace al DOI | Bajo |
| **jevals.com** | `https://jevals.com` | Preguntar si acepta un arnés de metrología (no un modelo) | No verificado que acepte envíos | respuesta del mantenedor | Bajo |

**La viñeta para awesome-jev, redactada** (una frase, con cifras que el PDF sostiene):

> **Metrology:** measures the same `confidence` field under four incompatible definitions across 65,185 decisions
> and reports how far a threshold travels between them — median gap 0.288, and 109× smaller error when the map is
> applied instead of the raw threshold ([DOI](https://doi.org/10.5281/zenodo.23330647)).

Si el mantenedor pide "uso de Jev" y no metrología, la respuesta honesta es que el instrumento **mide salidas de
Jev y de sus reimplementaciones**, no integra Jev en un producto. Si eso no encaja en su criterio, no se insiste:
el índice no es el único canal y forzarlo cuesta credibilidad.

| | |
|---|---|
| 🤖 Agente | Redactar la viñeta, los issues, el hilo y el post; preparar el dataset y su card |
| ✋ Autor | Publicar con su cuenta (Reddit, X, HN) y enviar el PR; responder comentarios |
| Coste | $0 · Tiempo: 3 h 🤖 + 1,5 h ✋ repartidas en dos semanas |
| Cierre | Entrada mergeada en awesome-jev + dataset descargable + ≥ 3 hilos con dato abiertos |

### 3.7 C6 — La nota divulgativa: 1 figura y la tabla por par

El paper tiene 12 páginas; un lector de foro lee 40 segundos. Hace falta una pieza intermedia: **600–900 palabras,
una figura y una tabla**, en español y en inglés.

| Elemento | Cuál exactamente | Por qué |
|---|---|---|
| Figura | `paper/figures/fig4-por-par.png` | Es la que muestra que el promedio engaña: la distribución es bimodal |
| Tabla | La tabla **por par** de `RESUMEN_MATRIZ.md` §3b, recortada a 8 filas | Es el titular real de la tesis, no la media global |
| Cifras permitidas | 65.185 · 23 grupos · 3.564 celdas · mediana 0.288 (p90 0.434, máx 0.848) · 0.2337 vs 0.0021 = 109× · ECE 0.216 (pmax) vs 0.577 (ent) | Todas están en el PDF y en el informe regenerable |
| Cifras **prohibidas** | Cualquier ECE de Jev medido por el autor (el brazo pagado no se ha corrido), "Jev está descalibrado", "el umbral nunca transfiere" | El PDF no las sostiene; la segunda capa (forma) sí falla, la primera (escala) **sí** transfiere con mapa |
| Título propuesto | «El mismo campo, el mismo dato: el umbral que no viaja» / *"Same field, same data: the threshold that does not travel"* | Frase nominal, sin promesas |
| Dónde vive | `docs/nota-divulgativa.md` (ES) y `docs/nota-divulgativa.en.md` (EN), enlazadas desde el README | Un archivo del repo se puede citar y versionar; un post de foro no |

| | |
|---|---|
| 🤖 Agente | Redactar las dos versiones, generar el recorte de la tabla desde el CSV |
| ✋ Autor | Revisar el tono y aprobar las cifras (20 min) |
| Coste | $0 · Tiempo: 3 h |
| Cierre | ambas notas en el repo, enlazadas desde el README, con las cifras cuadrando contra `RESUMEN_MATRIZ.md` |

### 3.8 C7 — Paper en inglés y arXiv (bloqueado)

**Este canal no se toca hasta que el autor diga, por escrito, que el PDF IEEE lo representa** (pendiente n=1, es
lo último que cierra la Tesis 1). Todo lo demás del plan es independiente.

| Paso | Qué | Quién | Requisito | Cierre |
|---|---|---|---|---|
| C7.1 | `paper/en/secciones/` con **la misma numeración** §1–§7; un solo `02_referencias.bib` compartido | 🤖 | aprobación §1–§7 | los 7 archivos existen y el `.bib` no se duplica |
| C7.2 | Figuras en inglés desde `src/figuras_paper.py` → `paper/figures/en/` | 🤖 | C7.1 | 8 figuras con ejes y leyendas en inglés |
| C7.3 | PDF en inglés, con la línea "English version of the Spanish original (DOI 10.5281/zenodo.23329431)" | 🤖 | C7.1 | `main.pdf` compila, sin citas sin resolver |
| C7.4 | Endosso: identificar 3 candidatos entre los autores que el paper ya cita y que sí publican en arXiv; enviar la solicitud desde el **primer envío** de arXiv (el sistema da el enlace) | ✋ | C7.3 | el código de endosso introducido, o 2 negativas → se replantea |
| C7.5 | Envío a arXiv: `cs.LG` primaria, `cs.CL` cruzada; licencia arXiv no exclusiva + CC-BY-4.0 declarada | ✋ envía / 🤖 prepara | C7.4 | `arxiv.org/abs/XXXX.XXXXX` responde 200 |
| C7.6 | Actualizar: badge de arXiv en el README, `relatedIdentifiers` en Zenodo (`isVersionOf`/`isSupplementTo`), 5.º work en ORCID, y **un solo** post de seguimiento en los foros | 🤖 + ✋ | C7.5 | el registro de Zenodo muestra la relación con arXiv y ORCID tiene 5 works |

**Sobre el endosso, con precisión.** La página oficial (`https://info.arxiv.org/help/endorsement.html`) describe
dos vías: (a) correo institucional + reclamar trabajos propios, y (b) **endosso personal** de un autor establecido
en la categoría. Con 0 papers en arXiv y sin coautores, la vía real es (b). El contexto del proyecto añade que
desde **ene-2026** el correo institucional ya no basta; conviene verificarlo en el momento del envío, porque la
política se mueve. Consecuencia práctica: **el endosso es el único paso del plan que no controla el autor**, y por
eso no puede bloquear nada de las fases A y B.

**Por qué no se puede adelantar el envío.** arXiv pide la versión completa en inglés (contexto del proyecto,
feb-2026). Enviar un abstract en inglés con el cuerpo en español no es una opción; enviar el PDF en español a
`cs.LG` es un rechazo casi seguro y un antecedente malo para el endosso.

---

## 4. Plan en tres fases

**Convención de nombres:** los **canales** son `C1`–`C7` (§3); las **acciones** son `A1`–`A10` (fase de 7 días),
`B1`–`B9` (fase de 2–4 semanas) y `P1`–`P6` (*paper*: la fase que espera la aprobación). Así `C1` nunca significa
dos cosas.

### 4.1 Fase A — 0 a 7 días: "el paquete existe y se instala"

Objetivo de la fase: **que `pip install jev-conf-metrics` funcione y que la portada del repo diga qué es.** Nada
de esta fase necesita inglés del paper, aprobación, GPU ni cuenta nueva salvo PyPI y Hugging Face.

| # | Acción | Quién | Dónde | Coste | Tiempo | Cierre verificable |
|---|---|---|---|---|---|---|
| A1 | `cli.py` con 5 subcomandos + `__main__.py` | 🤖 | `src/jev_conf_metrics/` | $0 | 2 h | `python -m jev_conf_metrics conf --p 0.7,0.1,0.1,0.1` imprime 4 líneas y la brecha |
| A2 | Metadata del paquete (tabla §3.2) + `README-pypi.md` en inglés | 🤖 | `pyproject.toml`, `README-pypi.md` | $0 | 2 h | `uv build` sin warnings y `unzip -p dist/*.whl '*/METADATA'` muestra `Summary` en inglés y `entry_points` |
| A3 | Cuenta PyPI + 2FA + token de proyecto en `~/.env` | ✋ | `https://pypi.org/manage/account/token/` | $0 | 10 min | `grep -c PYPI_TOKEN ~/.env` = 1 y `git grep -l PYPI_TOKEN` en el repo no devuelve nada |
| A4 | Ensayo en TestPyPI + instalación de prueba | 🤖 | comando §3.2 | $0 | 15 min | `jevconf --version` responde desde el venv de TestPyPI |
| A5 | Publicación real en PyPI | 🤖 | `uv publish` | $0 | 5 min | `https://pypi.org/project/jev-conf-metrics/` = 200 y `pip install` limpio funciona |
| A6 | GitHub: descripción, 12 topics, homepage, Discussions, plantillas de issue | 🤖 | `gh repo edit` (§3.4) | $0 | 20 min | `gh api … --jq .topics` devuelve 12 y `.homepage` el DOI |
| A7 | Social preview (PNG 1280×640) | 🤖 genera / ✋ sube | *Settings → Social preview* | $0 | 15 min | la miniatura aparece al pegar el enlace en un chat |
| A8 | Dataset en Hugging Face: matriz primero (2,2 MB), crudos después (120 MB) | ✋ cuenta / 🤖 sube | `https://huggingface.co/new-dataset` | $0 | 1 h | `hf download Arbues/jev-confidence-transfer-matrix` devuelve el CSV de 21 columnas |
| A9 | Nota divulgativa ES + EN (§3.7) | 🤖 | `docs/nota-divulgativa*.md` | $0 | 3 h | ambas enlazadas desde el README; cifras cuadran con `RESUMEN_MATRIZ.md` |
| A10 | Verificación de OpenAIRE y del grafo de Zenodo | 🤖 + ✋ | §3.5 | $0 | 40 min | OpenAIRE `total ≥ 1` (o ticket abierto con fecha) y relaciones visibles |

**Checklist de cierre de la fase A** (todo debe ser sí):

- [ ] `pip install jev-conf-metrics` funciona en un venv recién creado, en una máquina distinta del repo.
- [ ] `jevconf conf --p 0.7,0.1,0.1,0.1` imprime una brecha de 0.3784.
- [ ] La página de PyPI muestra el ejemplo y los DOI, no la bitácora de la tesis.
- [ ] El `README.md` del repo tiene una sección "Cómo citar" con los tres DOI.
- [ ] `topics` = 12 y `homepage` = DOI en la API de GitHub.
- [ ] El dataset se descarga con un comando.
- [ ] Ningún archivo nuevo contiene una clave; `git grep -i "pypi-"` no devuelve nada.

### 4.2 Fase B — 2 a 4 semanas: "el artefacto entra en los circuitos del ecosistema"

Objetivo: **que terceros lo encuentren sin que el autor les escriba.** Requisito de entrada: fase A cerrada.

| # | Acción | Quién | Dónde | Coste | Tiempo | Cierre verificable |
|---|---|---|---|---|---|---|
| B1 | PR a `awesome-jev` → `categories/calibration-research.md` | ✋ envía / 🤖 redacta | `https://github.com/yibie/awesome-jev` | $0 | 45 min | entrada mergeada; el índice pasa de 54 a 55 en esa categoría |
| B2 | 3–5 issues técnicos con dato en Laya, Kev, Nimble, SemIf, Jeff | 🤖 redacta / ✋ abre | repos de `FUENTES.md` §3 | $0 | 1,5 h | ≥ 3 issues abiertos con cifra y DOI |
| B3 | Post en r/LocalLLaMA (fig. 4 + comando + DOI) | ✋ | `https://www.reddit.com/r/LocalLLaMA/` | $0 | 30 min | 72 h vivo y ≥ 1 comentario respondido |
| B4 | Hilo de 6 tuits + post en dev.to con la nota de C6 | ✋ | cuenta del autor | $0 | 40 min | publicados con enlace al DOI |
| B5 | Release `v0.2.0` → versión nueva en Zenodo con DOI propio | ✋ OK / 🤖 `gh release create` | `docs/release-v0.2.0.md` | $0 | 30 min | DOI nuevo publicado y enlazado desde el README y el `CITATION.cff` |
| B6 | ORCID: cuarto *work* con el DOI de `0.2.0` | ✋ | `https://orcid.org/my-orcid` | $0 | 5 min | la API pública devuelve 4 works |
| B7 | Endosso de arXiv: 3 candidatos + solicitud preparada (sin enviar el paper todavía) | ✋ | `https://arxiv.org/a/` y el flujo de envío | $0 | 40 min | el código de endosso existe o hay 2 negativas registradas |
| B8 | Medición a 30 días: repetir el Anexo F y comparar con la línea base | 🤖 | §7 | $0 | 30 min | tabla de métricas actualizada con fecha |
| B9 | *Opcional*: Show HN, solo si B1 y B3 dieron señal | ✋ | `https://news.ycombinator.com/submit` | $0 | 20 min | ≥ 10 puntos en 24 h |

**Checklist de cierre de la fase B:**

- [ ] Al menos un índice de terceros lista el artefacto (awesome-jev u otro).
- [ ] Al menos tres hilos abiertos por terceros o por el autor **con respuesta**.
- [ ] El dataset tiene ≥ 1 descarga que no sea del autor (se comprueba en el contador de HF).
- [ ] Existe un DOI de `0.2.0` y el de concepto apunta a esa versión.
- [ ] La solicitud de endosso está hecha o se sabe por qué no.

### 4.3 Fase C — tras la aprobación del paper: "arXiv y consolidación"

**Puerta de entrada, literal:** el autor escribe que el PDF `paper/ieee/main.pdf` lo representa. Sin eso, esta
fase no empieza. Esta fase puede empezar en 2 semanas o en 3 meses; las fases A y B no la esperan.

| # | Acción | Quién | Dónde | Coste | Tiempo | Cierre verificable |
|---|---|---|---|---|---|---|
| P1 | `paper/en/` §1–§7 con la misma numeración, un solo `.bib` | 🤖 | `paper/en/secciones/` | $0 | 3–5 días | 7 archivos; `diff` de estructura contra `paper/secciones/` sin huecos |
| P2 | Figuras en inglés | 🤖 | `paper/figures/en/` | $0 | 2 h | 8 figuras con leyendas en inglés |
| P3 | PDF en inglés con la nota de versión y el DOI del original | 🤖 | `paper/en/ieee/` | $0 | 1 día | compila, 0 citas sin resolver, declara el DOI español |
| P4 | Endosso concedido | ✋ | flujo de arXiv | $0 | variable | código válido |
| P5 | Envío a arXiv (`cs.LG` + `cs.CL`) | ✋ envía | `https://arxiv.org/submit` | $0 | 2 h | `arxiv.org/abs/…` = 200 |
| P6 | Consolidación: badge, `relatedIdentifiers` en Zenodo, 5.º work en ORCID, un post de seguimiento | 🤖 + ✋ | repo, Zenodo, ORCID | $0 | 1 h | las tres cosas visibles y enlazadas |

**Checklist de cierre de la fase C:**

- [ ] El abstract de arXiv enlaza al preprint en español como versión original.
- [ ] El registro de Zenodo del software declara la relación con el arXiv id.
- [ ] ORCID tiene 5 works.
- [ ] Un solo post de seguimiento en los foros (no repetir el anuncio original).

---

## 5. Dependencias: qué bloquea qué

```
                        ┌──────────────────────────────┐
                        │ D-1 nombre + D-2 dónde la CLI│   (✋ decide, 10 min)
                        └──────────────┬───────────────┘
                                       ▼
   ┌───────────────┐        ┌──────────────────┐        ┌─────────────────┐
   │ A1 cli.py     │───────►│ A2 metadata+README│──────►│ A4/A5 PyPI      │
   │ (🤖, 2 h)     │        │ (🤖, 2 h)         │        │ (✋ token, 🤖)   │
   └───────────────┘        └──────────────────┘        └────────┬────────┘
                                                                 │
        ┌────────────────────────────────────────────────────────┤
        ▼                        ▼                               ▼
 ┌─────────────┐         ┌──────────────┐               ┌──────────────────┐
 │ A6/A7 GitHub│         │ A8 HF dataset│               │ C5 foros (B1–B4) │
 │ (🤖, 35 min) │         │ (✋+🤖, 1 h)  │               │ (✋ publica)      │
 └─────────────┘         └──────────────┘               └──────────────────┘
                                                                 │
                                                                 ▼
                                                        ┌──────────────────┐
                                                        │ B5 release 0.2.0 │
                                                        │ → DOI nuevo      │
                                                        └──────────────────┘

   APROBACIÓN §1–§7 (✋)  ──►  paper/en/ (🤖)  ──►  endosso (✋ externo)  ──►  arXiv
        ↑
        └── única puerta de la fase C; no bloquea A ni B
```

**Tres reglas de orden que se desprenden del grafo:**

1. **Nada se anuncia antes de A5.** Los foros (C5) consumen la credibilidad una sola vez.
2. **A8 (dataset) no espera a A5**, pero sí a que exista la tabla por par publicable; puede ir en paralelo con A6.
3. **B5 (release 0.2.0) va después de B1–B4**, no antes: el DOI de la versión nueva se emite cuando el paquete
   ya está anunciado y su CLI probada. Si el paso a inglés cambia algo del paquete, se emite una `0.3.0`; no se
   gastan versiones por adelantado.

---

## 6. Riesgos y trampas

| # | Riesgo | Prob. | Impacto | Mitigación | Señal de alerta |
|---|---|---|---|---|---|
| R1 | **Anunciar antes de que el paquete exista** → enlaces muertos en foros | Alta si se improvisa | Alto (quema el canal) | Regla dura: ningún post antes de A5; el texto del anuncio incluye un `pip install` que se prueba ese mismo día | alguien responde "404" |
| R2 | **Publicar en foros sin el DOI a mano** | Media | Alto (deja de ser citable) | Plantilla de anuncio (Anexo B) con los tres DOI y el comando; revisión antes de enviar | el post no tiene enlace a `doi.org` |
| R3 | **Prometer cifras que el PDF no tiene** (p. ej. "Jev está descalibrado") | Media | Alto (credibilidad) | Lista blanca de cifras en §3.7 y §8; el titular es la tabla por par, no la media | una cifra del post no aparece en `RESUMEN_MATRIZ.md` |
| R4 | **Tocar el pre-registro** (`paper/04_pre_registro.md`) | Baja | **Muy alto** (rompe la reserva) | El archivo no se edita; cualquier cambio va como errata en `docs/erratas_especificacion.md` | `git log -- paper/04_pre_registro.md` con un commit posterior al 09-oct |
| R5 | **Otro registra el nombre `jev-conf-metrics` en PyPI** | Baja | Alto | Publicar en fase A; los nombres son únicos y permanentes | `pypi.org/pypi/jev-conf-metrics/json` deja de dar 404 |
| R6 | **La descripción larga de PyPI es la bitácora interna** | Alta si no se corrige | Medio (mala primera impresión) | `README-pypi.md` propio; verificar en la página de PyPI, no solo en el wheel | la página de PyPI habla de "Tesis 1" y de fases |
| R7 | **Rechazo en awesome-jev por "documentación > código"** | Media | Medio | Entrar después de A5, citando el comando y el paquete; aceptar el no sin insistir | el PR se cierra sin comentario |
| R8 | **OpenAIRE no cosecha el software** | Media | Bajo | Re-consultar a 15/30 días; completar `subjects`/`relatedIdentifiers`; escribir al soporte | `total` sigue en 0 a los 30 días |
| R9 | **Endosso de arXiv denegado por todos los candidatos** | Media | Alto para la fase del paper, nulo para A/B | Pedirlo a 3 candidatos a la vez; plan alternativo: versión EN en Zenodo (ya se puede) y arXiv cuando se consiga | 2 negativas |
| R10 | **El release 0.2.0 se publica con metadatos malos y ya no se puede corregir** | Media | Medio | Zenodo: los **archivos** solo se cambian en los primeros 45 días; el DOI es irreversible. Ensayar todo en TestPyPI | el ZIP de Zenodo trae el `README.md` equivocado |
| R11 | **Claves en el repo** | Baja | **Muy alto** | `PYPI_TOKEN` y `HF_TOKEN` solo en `~/.env`; `.gitignore` ya cubre `.env`; `git grep` antes de cada commit | `git grep -iE -e "pypi-" -e "hf_"` devuelve algo |
| R12 | **Autopromoción repetida en Reddit/HN** | Media | Medio (sombra) | Un anuncio por canal y fase; el seguimiento va en los mismos hilos, no en hilos nuevos | el post se elimina sin explicación |
| R13 | **El plan se lee como sustituto de la Tesis 2 / del cierre** | Baja | Bajo | Este documento no cierra pendientes académicos: cierra distribución. El cierre de la Tesis 1 sigue siendo la lectura del §1–§7 | alguien propone "ya que estamos, medir 4B–9B" |

**La trampa que más caro sale, y por eso va aparte:** confundir *visibilidad* con *impacto*. Un repo con 300
estrellas y cero citas no vale más que uno con 5 estrellas y una cita. Las estrellas se compran con espectáculo;
las citas, con un DOI que resuelve y una tabla que otro necesita.

---

## 7. Métricas de éxito observables

**No hay objetivos numéricos honestos posibles**: nadie puede prometer 50 estrellas. Lo que sí se puede fijar son
**umbrales de movimiento** y la forma de leerlos. Toda la columna "cómo se lee" es un comando o una URL.

| Métrica | Cómo se lee | Línea base 20-oct-2026 | "Está funcionando" a 30 días | A 90 días | Qué NO significa |
|---|---|---|---|---|---|
| Descargas PyPI | `https://pypistats.org/packages/jev-conf-metrics` | **no existe el paquete** | > 0 sin contar las del autor | ≥ 20/mes sostenidas | No distingue CI de humanos |
| Estrellas del repo | `gh api repos/Arbues/tesis1-jev-confidence --jq .stargazers_count` | **0** | ≥ 3 | ≥ 15 | Las estrellas no citan |
| Forks | ídem `.forks_count` | **0** | ≥ 1 | ≥ 3 | Un fork puede ser un backup |
| Issues de terceros | `gh issue list --repo Arbues/tesis1-jev-confidence --state all --search "-author:Arbues"` | **0** | ≥ 1 | ≥ 3 | Un issue puede ser una queja (también sirve) |
| Vistas del repo (14 d) | `gh api repos/…/traffic/views` | **14 (1 único)** | ≥ 100 (≥ 20 únicos) | ≥ 300 | Los bots inflan vistas |
| Clones (14 d) | `gh api repos/…/traffic/clones` | **345 (156 únicos)** | proporción de únicos ≥ 20 % | ídem | Hoy son del propio autor |
| Vistas Zenodo (software) | `https://zenodo.org/api/records/23330647` → `stats.unique_views` | **2** | ≥ 10 | ≥ 40 | — |
| Descargas Zenodo (software) | ídem `stats.unique_downloads` | **2** | ≥ 5 | ≥ 20 | — |
| Presencia en índices | `curl -s "https://api.openaire.eu/search/publications?doi=…&format=json"` | **software: 0**; preprint y pre-registro: 1 | software ≥ 1 | ≥ 1 en dos índices | — |
| Citas del DOI | `https://api.datacite.org/dois/10.5281/zenodo.23330647` → `relationships.citations` y Google Scholar | **0** | 0 (es pronto) | ≥ 1 mención externa | Una mención no es una cita formal |
| Entradas en índices curados | README de `yibie/awesome-jev` | **0** | ≥ 1 | ≥ 1 | — |
| Dataset descargado | contador del repo HF | **no existe** | ≥ 1 distinta del autor | ≥ 10 | — |
| arXiv | `arxiv.org/abs/…` | **no enviado** | — | — (fase C) | — |

**Cómo se recoge todo en 5 minutos** (🤖, una vez al mes): repetir el bloque del Anexo F y anotar la fecha. Sin
serie temporal, las métricas no dicen nada; con dos puntos separados 30 días, dicen casi todo.

**Lectura honesta a 90 días.** Con un artefacto de nicho, un dominio de 2.400 estrellas en el índice de referencia
y 54 entradas en la categoría de calibración, lo razonable es **decenas de descargas, una o dos citas y una entrada
en un índice**. Si a 90 días hay 0 descargas y 0 menciones, el problema no es el plan: es que el artefacto no
resuelve el problema de nadie y hay que revisar el encuadre (esa es una decisión de tesis, no de marketing).

---

## 8. Lo que este plan NO hace

| No | Por qué |
|---|---|
| No toca `paper/04_pre_registro.md` | Es el texto depositado con DOI; los cambios van como errata |
| No traduce el paper fuera de `paper/en/` | El paper en inglés está bloqueado hasta la aprobación del §1–§7 |
| No anuncia cifras nuevas | El brazo pagado no se ha corrido; el ECE de Jev medido por el autor no existe todavía |
| No dice "`output_tokens = 0`" en general | En la API de pago está medido que no lo es (71 / 58 / 31) |
| No promete transferencia universal fallida | La capa de **escala** sí transfiere con mapa (Δ ≈ 0.0021); la de **forma** no. El post debe decir las dos |
| No publica un paquete vacío para "reservar" el nombre | PyPI no borra, solo yank; un placeholder queda para siempre |
| No abre cuentas ni crea credenciales | Cada cuenta la crea el autor (PyPI, HF, Reddit, X, HN); el agente solo prepara el material |
| No usa el correo institucional como prueba de identidad en arXiv | Desde ene-2026 no basta (contexto del proyecto); el endosso es personal |
| No toca `results/matrix/` ni los crudos | Son el artefacto sellado; el dataset de HF es una **copia**, no un reemplazo |
| No mete `numpy` como dependencia | La instalación sin dependencias es parte del argumento |
| No propone Tesis 2 | Otro alcance (pendiente n=8) |

---

## 9. Decisiones abiertas (para el autor)

| # | Decisión | Opciones | Recomendación | Qué se pierde si se elige la otra |
|---|---|---|---|---|
| D-1 | Nombre en PyPI | `jev-conf-metrics` (libre) · otro | **`jev-conf-metrics`**: coincide con el nombre que ya usa el DOI y el `CITATION.cff` | Coherencia entre el paquete y el registro citado |
| D-2 | Dónde vive la CLI | Este repo (mínima) · repo del framework (completa) | **Las dos**: mínima aquí ya; completa en `decision-calibration-bench` | Publicar hoy, sin esperar 2–4 semanas al framework |
| D-3 | Dataset en HF | Solo matriz (2,2 MB) · matriz + crudos (120 MB) | **Matriz primero**, crudos en un segundo repo | El dato pesado es el que más se cita en este campo |
| D-4 | Cuándo pedir el endosso | Ahora · Con `paper/en/` listo | **Con el borrador EN listo**, para que el endosante pueda juzgar | Tiempo, si el endosante tarda |
| D-5 | Versión a publicar | `0.1.0` (la actual) · `0.2.0` | **`0.2.0`**: añadir CLI es *feature*, y una versión nueva deja el DOI de `v1.0.0`/`v1.0.1` intacto | Claridad del historial |
| D-6 | Show HN | Sí · No | **Solo si B1 y B3 dieron señal** | Nada; HN castiga el envío sin tracción |
| D-7 | ASCL | Presentar · No presentar | **No presentar**: es de astronomía | Nada relevante |
| D-8 | Idioma de la nota divulgativa | Solo ES · ES + EN | **ES + EN**: la comunidad del ecosistema es anglófona y la nota no es el paper | Alcance del anuncio |

Ninguna de estas ocho decisiones bloquea el resto del plan salvo D-1 y D-2, que son la puerta de la fase A.

---

## Anexo A — Comandos literales

```bash
# ---------- LÍNEA BASE (repetir el 20 de cada mes) ----------
curl -s -o /dev/null -w "%{http_code}\n" https://pypi.org/pypi/jev-conf-metrics/json
gh api repos/Arbues/tesis1-jev-confidence \
  --jq '{stars:.stargazers_count,forks:.forks_count,issues:.open_issues_count,topics:.topics,homepage:.homepage}'
gh api repos/Arbues/tesis1-jev-confidence/traffic/views  --jq '{views:.count,unicos:.uniques}'
gh api repos/Arbues/tesis1-jev-confidence/traffic/clones --jq '{clones:.count,unicos:.uniques}'
curl -s https://zenodo.org/api/records/23330647 | python3 -c \
  "import sys,json;d=json.load(sys.stdin)['stats'];print(d['unique_views'],'vistas',d['unique_downloads'],'descargas')"
for d in 10.5281/zenodo.23266795 10.5281/zenodo.23329431 10.5281/zenodo.23330647; do
  printf "%s -> " "$d"
  curl -s "https://api.openaire.eu/search/publications?doi=$d&format=json" \
    | python3 -c "import sys,json;print('total',json.load(sys.stdin)['response']['header']['total']['\$'])"
done

# ---------- FASE A ----------
# A1/A2: construir y comprobar la metadata sin publicar
cd /home/arbues/paper-tesis1 && rm -rf dist && uv build --out-dir dist
unzip -p dist/*.whl '*/METADATA' | head -25          # Summary en inglés, licencia, Project-URL
unzip -p dist/*.whl '*/entry_points.txt'             # debe listar jevconf

# A4: ensayo en TestPyPI
uv publish --publish-url https://test.pypi.org/legacy/ --token "$TESTPYPI_TOKEN" dist/*
uv venv /tmp/vtest
uv pip install --python /tmp/vtest/bin/python \
  --index-url https://test.pypi.org/simple/ jev-conf-metrics
/tmp/vtest/bin/jevconf conf --p 0.7,0.1,0.1,0.1

# A5: producción
uv publish --token "$PYPI_TOKEN" dist/*
python3 -m venv /tmp/vprod && /tmp/vprod/bin/pip install -q jev-conf-metrics \
  && /tmp/vprod/bin/jevconf --version          # prueba final en venv limpio

# A6: GitHub
gh repo edit Arbues/tesis1-jev-confidence \
  --description "Metrology and threshold transfer for the confidence field in Jev-type decision models: 65,185 decisions, 23 groups, 3,564 cells. Median gap 0.288; 0.2337 vs 0.0021 with map (109x)." \
  --homepage "https://doi.org/10.5281/zenodo.23330647" \
  --add-topic jev --add-topic confidence-calibration --add-topic calibration \
  --add-topic threshold-transfer --add-topic decision-models --add-topic metrology \
  --add-topic model-evaluation --add-topic reproducibility --add-topic research-software \
  --add-topic python --add-topic open-weights --add-topic thesis \
  --enable-discussions

# A8: dataset en Hugging Face (la cuenta la crea el autor)
# el repo debe existir ANTES de subir: https://huggingface.co/new-dataset -> Arbues/jev-confidence-transfer-matrix
hf auth login                                   # token en ~/.cache/huggingface, nunca en el repo
hf upload Arbues/jev-confidence-transfer-matrix \
  results/matrix/matriz_transferencia.csv matriz_transferencia.csv --repo-type dataset
hf upload Arbues/jev-confidence-transfer-matrix results/matrix/RESUMEN_MATRIZ.md RESUMEN_MATRIZ.md --repo-type dataset

# B5: release 0.2.0 (publica solo en Zenodo)
git tag -a v0.2.0 -m "v0.2.0 - CLI jevconf y metadata de paquete"
git push origin v0.2.0
gh release create v0.2.0 --notes-file docs/release-v0.2.0.md

# higiene antes de cada commit
git grep -nE "pypi-[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}" || echo "sin claves"
```

---

## Anexo B — Plantilla de anuncio (foro / Reddit / X)

**Español (120 palabras):**

> **El mismo campo, el mismo dato: el umbral que no viaja.**
> En el ecosistema tipo Jev, `confidence` significa al menos cuatro cosas distintas: `(n·p_max−1)/(n−1)`,
> `1−H/log k`, `p_max` y margen. Medimos 65.185 decisiones en 23 grupos (Laya, Kev, control crudo) y 3.564 celdas
> de transferencia de umbral. Dos resultados: entre definiciones de la misma clase el **número** no viaja (aplicar
> el umbral tal cual se equivoca 0.2337 de media) pero el **mapa** sí (0.0021, 109× menos); entre clases distintas
> (`pmax` ↔ entropía) no viaja ni el número ni el mapa. La mediana de la brecha entre la definición más alta y la
> más baja de la **misma** distribución es 0.288.
> `pip install jev-conf-metrics` · instrumento: https://doi.org/10.5281/zenodo.23330647 · paper (ES): https://doi.org/10.5281/zenodo.23329431

**Inglés:**

> **Same field, same data: the threshold that doesn't travel.**
> In the Jev-style ecosystem, `confidence` means at least four different things. We measured 65,185 decisions
> across 23 groups and 3,564 threshold-transfer cells. Within a class, the number doesn't transfer (mean absolute
> error 0.2337) but the map does (0.0021, 109× better); across classes (`pmax` ↔ entropy) neither does. Median gap
> between the highest and lowest definition of the same distribution: 0.288.
> `pip install jev-conf-metrics` · instrument: https://doi.org/10.5281/zenodo.23330647 · paper (ES): https://doi.org/10.5281/zenodo.23329431

**Reglas del anuncio:** cifras solo de esta lista; nunca decir "Jev está descalibrado"; decir siempre "paper en
español, versión en inglés en preparación"; un enlace a `doi.org`, no a Zenodo directo.

---

## Anexo C — Plantilla de solicitud de endosso (arXiv)

> Asunto: **Endorsement request — cs.LG (metrology of confidence fields in decision models)**
>
> Estimado/a [nombre]:
>
> Le escribo porque [motivo concreto: cita su trabajo X / su implementación Y aparece medida en mi matriz].
> Soy Arbués Enrique Pérez V., estudiante de Ciencia de la Computación en la Universidad Nacional de Ingeniería
> (Perú), ORCID 0009-0004-7605-6569. Mi primer envío a arXiv es un artículo de metrología: mide cómo se comporta
> el campo `confidence` entre definiciones incompatibles en modelos de decisión tipo Jev, sobre 65.185 decisiones,
> y publica el instrumento con DOI (10.5281/zenodo.23330647).
>
> El preprint en español está aquí: https://doi.org/10.5281/zenodo.23329431 — la versión en inglés es la que
> enviaría. Si considera que el trabajo encaja en cs.LG, el enlace de endosso que arXiv me ha generado es:
> [enlace]. Si prefiere no endosar, se lo agradezco igual; no volveré a pedirlo.
>
> Gracias por su tiempo.

**Reglas:** 3 candidatos a la vez, nunca en bloque; mencionar el trabajo concreto de esa persona; incluir el enlace
de endosso que da arXiv al iniciar el envío; aceptar el no sin insistir.

---

## Anexo D — Esquema de `README-pypi.md`

```
# jev-conf-metrics
One sentence: what it measures.                      (3 líneas)
## The problem                                        (5)
## What this gives you                                (8, 4 viñetas)
## Install                                            (3)
## Four lines that show the point                     (10, código + salida)
## What was measured                                  (10, tabla + DOI)
## The two layers (scale vs shape)                    (6)
## Cite                                               (6)
## License and scope                                  (6)
```

Regla de estilo: inglés técnico, sin adjetivos, todas las cifras con su DOI al lado, y el ejemplo **ejecutable tal
cual** (probado en el venv de TestPyPI antes de publicar).

---

## Anexo E — Plantilla de issue técnico para un proyecto del ecosistema

> **Título:** `confidence` is `1−H/log k` in this repo — here is how far a threshold from `p_max` drifts when ported
>
> We measured threshold transfer between the confidence definitions used in the Jev ecosystem (65,185 decisions,
> 23 model/dataset groups, including this checkpoint). Porting a threshold calibrated on `p_max` into the
> entropy-based confidence here gives a mean absolute coverage/precision error of **[Δ de la celda concreta]** at
> q = 0.80; applying the affine map instead reduces it to **[Δ_mapa]**.
>
> Raw cell: `modelo=…, dataset=…, n=…, A=pmax, B=ent, q=0.80` in https://doi.org/10.5281/zenodo.23330647
> Code: `pip install jev-conf-metrics` (reproduce with `jevconf transfer --csv … --desde pmax --hasta ent`).
> Not a bug report — a measurement you may want to link from the model card.

Regla: una celda concreta, un número, un comando. Sin "mira mi repo".

---

## Anexo F — Registro de verificación (20-oct-2026)

| Comprobación | Comando | Resultado |
|---|---|---|
| Nombre libre en PyPI | `curl -s -o /dev/null -w "%{http_code}" https://pypi.org/pypi/jev-conf-metrics/json` | **404** |
| Nombre de comando libre | ídem `jevconf` | **404** |
| Metadatos de GitHub | `gh api repos/Arbues/tesis1-jev-confidence` | `stars 0 · forks 0 · issues 0 · topics [] · homepage null · discussions false · license Apache-2.0 · created 2026-10-08 · pushed 2026-10-13` |
| Tráfico | `gh api …/traffic/views` y `/clones` | 14 vistas (1 único) · 345 clones (156 únicos) |
| Zenodo software | `curl -s https://zenodo.org/api/records/23330647` | `status published · 2 vistas · 2 descargas · resourceType Software` |
| Zenodo preprint / pre-registro | ídem `23329431` / `23266795` | 2/5 y 4/1 |
| OpenAIRE (software) | `api.openaire.eu/search/publications?doi=…23330647` | **total 0** |
| OpenAIRE (preprint, pre-registro) | ídem | **total 1** cada uno |
| Software Heritage | `archive.softwareheritage.org/api/1/revision/39a6856…/` | 200; autor y fecha correctos |
| Build del paquete | `uv build --out-dir` en copia limpia | wheel 21.549 B + sdist 32.201 B; 0 dependencias |
| Instalación del wheel | `uv venv` + `uv pip install dist/*.whl` | 33 nombres exportados; `__version__` 0.1.0 |
| Punto de entrada | `python -m jev_conf_metrics` | **falla**: no hay `__main__` |
| `entry_points` del wheel | `unzip -l dist/*.whl` | **ninguno** |
| Descripción larga del wheel | `unzip -p dist/*.whl '*/METADATA'` | 27.654 bytes del `README.md` interno (27.941 caracteres de `METADATA`) |
| Ejemplo de la librería | `all_confidences([0.7,0.1,0.1,0.1])` | `{'jev': 0.6, 'ent': 0.3216, 'pmax': 0.7, 'margin': 0.6}` |
| Tests | `.venv/bin/python -m pytest -p no:cacheprovider` | **52 en `main`, 63 en el árbol de trabajo** |
| Índice del ecosistema | `gh api repos/yibie/awesome-jev` | 2.422 estrellas; `CONTRIBUTING.md` presente; categoría `categories/calibration-research.md` con 54 entradas |
| Política de endosso | `info.arxiv.org/help/endorsement.html` | dos vías: correo institucional + reclamar trabajos, o endosso personal |
| ASCL | `ascl.net/code/submit` | admite envíos con moderación; **ámbito astronomía** → no aplica |

---

## Anexo G — Glosario

| Término | Significado en este documento |
|---|---|
| **PyPI** | *Python Package Index* (`pypi.org`). El índice del que `pip` instala. Publicar es gratuito; un nombre es único y no se reutiliza |
| **TestPyPI** | Ensayo de PyPI (`test.pypi.org`). Sirve para probar el paquete antes de publicar de verdad; se puede repetir cuantas veces haga falta |
| **wheel / sdist** | Los dos formatos que se suben: `.whl` es el paquete instalable; `.tar.gz` el código fuente empaquetado |
| **entry point** | El campo del `pyproject.toml` que crea un comando en el sistema (`jevconf`). Sin él, instalar no da ningún comando |
| **CLI** | *Command Line Interface*: el programa que se usa escribiendo en la terminal |
| **DOI de versión / de concepto** | El primero identifica un depósito concreto (v1.0.1); el de concepto apunta siempre a la última versión |
| **SWHID** | Identificador intrínseco de Software Heritage: identifica una revisión de código por su contenido, no por una URL |
| **OpenAIRE** | Agregador europeo de literatura y software científico. Cosecha Zenodo; se consulta por API. Que un registro esté en Zenodo no garantiza que OpenAIRE ya lo tenga |
| **DataCite** | El registro de metadatos que usa Zenodo (los DOI de datos y software viven ahí, no en Crossref) |
| **ASCL** | *Astrophysics Source Code Library*: catálogo de software de astronomía. Fuera de ámbito aquí |
| **Endosso (arXiv)** | Aval de un autor establecido que permite a un primer enviante publicar en una categoría de arXiv |
| **arXiv id** | Identificador del preprint (`arXiv:XXXX.XXXXX`), distinto del DOI |
| **ECE** | *Expected Calibration Error*: distancia media entre la confianza declarada y la precisión observada |
| **cobertura** | Fracción de casos que el modelo decide responder al aplicar un umbral; su pareja es la precisión sobre lo respondido |
| **tabla por par** | La tabla A→B de `RESUMEN_MATRIZ.md` §3b: el error de portar el umbral de una definición a otra. Es el titular, porque la media global engaña (la distribución es bimodal) |
| **mapa** | La transformación afín entre dos definiciones de la misma clase; portar con mapa reduce el error de 0.2337 a 0.0021 |
| **JSONL** | Un JSON por línea; el formato de `results/crudos/` (23 archivos, 65.185 filas) |
| **dataset card** | El `README.md` con YAML de un repositorio de datos en Hugging Face (licencia, tareas, etiquetas) |
| **2FA** | Segundo factor de autenticación; PyPI lo exige para publicar |
| **token** | Credencial de publicación de PyPI. Vive en `~/.env`, nunca en el repo |
| **yank** | Retirar una versión de PyPI sin borrarla (PyPI no permite borrar) |
