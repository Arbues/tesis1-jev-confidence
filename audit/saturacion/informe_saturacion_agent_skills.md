# Auditoría de saturación: SEGURIDAD Y VERIFICACIÓN DE "AGENT SKILLS"
Fecha de corte: 2026-09. Corpus recolectado: 683 papers únicos (arXiv, vía MCP paper_search), + evidencia web de industria y estándares.

## 0. Advertencia metodológica
Los conteos provienen de búsquedas por relevancia en arXiv (no de un índice exhaustivo), por lo que son **cotas inferiores**. Se deduplicó por paper_id. Las cifras de industria provienen de blogs/vendor docs (Snyk, Cisco, CSA, Adversa, SkillFed, Trail of Bits) y deben leerse como evidencia gris.

## 1. Conteo por año
| Categoría | 2024 | 2025 | 2026 (ene–sep) |
|---|---|---|---|
| A. Seguridad de *agent skills* como artefacto (vulns, threat models, scanners, auditorías) | 0 | 0 | **56** |
| B. Seguridad de la capa MCP/tools (tool poisoning, servidores MCP) | 0 | 11 | **30** |
| C. Artefactos skill + verificación/testing/fuzzing | 0 | 2 | **62** (17 con foco explícito en título) |
| D. Modelos de permisos/capacidades para skills | 0 | 0 | **29** |

**Hecho decisivo:** el formato SKILL.md se publicó en octubre de 2025. En ~9 meses (2026) hay ~56 papers de seguridad de skills y ~17 de verificación/benchmarking. No existe literatura 2024 porque el artefacto no existía.

## 2. Los 12+ trabajos clave
1. **2601.10338** (2026) Agent Skills in the Wild — 42.447 skills, 31.132 analizadas con SkillScan, **26,1%** vulnerables, 14 patrones, precisión 86,7%/recall 82,5%; banda declarada 23–30%.
2. **2602.12430** (2026) Survey (el citado por el estudiante).
3. **2603.16572** (2026) Context Matters — **238.180 skills**; scanners reportan 3,79%–41,9% según herramienta; solo **0,12%** de skills comunes marcadas por los 5 scanners; con contexto de repositorio solo **0,52%** quedan sospechosas. Dice explícitamente que los datasets anotados prometidos por trabajos previos **no fueron localizables**.
4. **2605.11770** (2026) Behavioral Integrity Verification (BIV) — 49.943 skills; **80,0%** desvía del comportamiento declarado; 81,1% por negligencia, 18,9% intención adversarial; F1 0,946.
5. **2605.23951** (2026) Formal Verification of Agent Skills — retícula de 4 niveles (unverified/declared/tested/formal) + **prueba de contención de capacidades** por interpretación abstracta y tipos de refinamiento. *Cierra el desafío abierto #5 del survey.*
6. **2606.03024** (2026) SkillGuard — framework de permisos centrado en skills, doble plano (influencia de contexto + efectos), cubre 99,93% de objetos protegidos en 1.260 skills. *Cierra el desafío #4.*
7. **2606.00925** (2026) SkillVetBench — benchmark de detección + verificación en runtime; baselines semánticos/firma fallan hasta 89%.
8. **2608.19901** (2026) MaliciousSkillBench — 9.740 skills (7.505 maliciosas / 2.235 benignas), consolida 13 fuentes, 4.588 familias estructurales.
9. **2608.10906** (2026) GitSkills — dataset de **3.797.117 SKILL.md** de 282.200 repos (SQLite autocontenido).
10. **2607.02357** (2026) Cloak and Detonate — SkillCloak evade scanners por ofuscación estructural + detección dinámica.
11. **2609.17274** (2026) After the Party — estudio longitudinal de ClawHub/OpenClaw: crecimiento, gobernanza y fiabilidad del scanning.
12. **2605.13044** (2026) Sefz — *semantic fuzzing* para violaciones de especificación (skill rompe sus propias reglas sin ataque).
13. **2508.14925** (2025) MCPTox — 45 servidores MCP vivos, 353 tools, 1.312 casos; ASR hasta 72,8%.
14. **2607.11086** (2026) MCPZoo — 64.611 servidores MCP únicos; scanners reportan 96,89% "riesgosos" vs realidad medida.
15. **2605.21404** (2026) What Twelve LLM Agent Benchmark Papers Disclose — auditoría de divulgación de benchmarks (score medio 0,38); precedente metodológico directo para una auditoría de benchmarks de skills.

## 3. ¿Se replicó el 26,1%?
**No.** Nadie lo replicó de forma limpia y los números independientes divergen:
- 2601.10338 (skills.rest + skillsmp.com): 26,1% (banda 23–30%).
- Tercero sobre ClawHub+skills.sh: 13,4% crítico.
- Sobre 40.285 skills de skills.sh: 9%.
- 2602.06547: 157 skills confirmadas maliciosas de 98.380 (**0,16%**).
- 2603.16572: fail rates 3,79%–41,9% según scanner; **0,52%** tras análisis con contexto de repositorio.
- SkillFed (67.453 versiones): solapamiento máximo entre scanners 10,4%; acuerdo de los tres 0,69%; kappa de Cohen 0,045–0,082.
- Adversa.ai (8 scanners, MalSkillBench 7.797 muestras): **ningún scanner supera la línea base "marcar todo"** (F1 0,655); mejor real 0,551.
- Trail of Bits (jun 2026): evadieron *todos* los scanners (ClawHub, Cisco, Gen, Socket, Snyk); 3 de 4 bypass en <1 hora.
- CSA (jun 2026): Snyk degradó alertas a "Medium" ante ofuscación split-stream; Socket no emitió ningún Critical/High.
- Además: 2603.16572 reporta que los datasets prometidos **no se pudieron encontrar** → crisis de reproducibilidad explícita.

Conclusión: la prevalencia real de vulnerabilidades en skills **no está establecida**; lo que está establecido es que la medición es no fiable.

## 4. Corpora y datasets públicos
- **GitSkills** (2608.10906): 3.797.117 SKILL.md / 282.200 repos, SQLite, jul 2026.
- **MaliciousSkillBench** (2608.19901): 9.740 skills etiquetadas; 13 fuentes consolidadas.
- **MalSkillBench** (Adversa.ai, industria): 7.797 muestras (4.000 benignas reales) — con defectos conocidos: 13% directorios vacíos y fuga de etiqueta vía `_meta.json`.
- **SkillAtlas** (2609.13353): 3.014 casos, 6.589 trazas, 151.131 pasos, 233 skills, 8 categorías.
- **SkillVetBench** (2606.00925): skills maliciosas confirmadas de OpenClaw incl. campaña ClawHavoc.
- **Skill-Inject** (2602.20156): 202 pares inyección-tarea.
- **SKILL-DEP** (2607.01136): benchmark de dependencias de skills.
- **MCPZoo** (2607.11086): 64.611 servidores MCP únicos (113.927 totales), 37.288 dinámicamente analizables.
- **MCPTox** (2508.14925): 45 servidores vivos / 353 tools / 1.312 casos.
- **SkillFed ClawHub Security Signals**: 67.453 versiones con veredicto ClawScan + VirusTotal + NVIDIA SkillSpector.
- **OASB** (Open Agent Skill Benchmark): leaderboard público (con set benigno sesgado a configs MCP cortas).
- **Marketplaces/registros**: ClawHub/OpenClaw (49.592 skills abr-2026; ~49.943 usadas en BIV), skills.sh, SkillsMP (170.226 artefactos), skills.rest, SkillsAuth, pluginsmp, aiskillstore; MCP: registro oficial, Smithery, glama.ai, PulseMCP, mcp.so.
- **GitHub**: anthropics/claude-plugins-official (~35.840 stars), trailofbits/skills, UnboundCompute/security-agent-skills, kalshamsi/claude-security-skills.

## 5. Frameworks y escáneres existentes (el área NO está vacía)
**Estándares:** OWASP **Agentic Skills Top 10 (AST10)** — 10 riesgos + propuesta de *Universal Skill Format* con `permissions.files/network/shell`, `risk_tier`, `signature`, `content_hash`, `scan_status`. OWASP **MCP Top 10**, OWASP **AISVS v1.0**, **AIVSS**, OWASP Top 10 Agentic Applications 2026. NIST AI Agent Standards Initiative (feb 2026), RFI NIST/CAISI (ene 2026), EU AI Act, ISO 42001.
**Académicos:** SkillGuard (permisos), BIV (integridad conductual), retícula de verificación formal (2605.23951), VASO (contratos formales), Sefz (fuzzing semántico), SkillFuzz, SkillVetBench, MaliciousSkillBench, SkillTester (skilltester.ai), ACES (evaluación continua de skills), ChainGuard, ColluSkill/CompoSkill (ataques de composición), SCR-Bench.
**Industria/comercial:** **Snyk Agent Scan** (ex-Invariant mcp-scan, ~2.000+ stars, escanea skills y MCP), **Cisco mcp-scanner** (Apache 2.0) y skill-scanner, **Socket**, **Gen** (skills.sh), **NVIDIA SkillSpector** (64 patrones/16 categorías), **Akto** (comercial), **VirusTotal**, ClawScan, más skills de auditoría de Trail of Bits.

## 6. Veredicto: 8/10 (muy trabajado)
Las tres etapas del plan propuesto ya tienen 3–10 papers cada una, y dos de los "siete desafíos abiertos" del survey (permisos por capacidades, verificación/testing) fueron cerrados por trabajos de mayo–junio 2026 que el propio survey (feb 2026) no alcanzó a citar. No es 10 porque no existe ground truth humano público, ningún benchmark de skills ha sido auditado independientemente, la portabilidad semántica de permisos entre runtimes no se ha medido, y los fallos *benignos* de composición (deadlocks, no-terminación, cascadas) siguen casi vírgenes.

## 7. Lo que sí queda para un académico
1. **Metrología / auditoría de la medición** (el hueco más limpio): no hay ground truth con acuerdo inter-anotador, los datasets prometidos no son localizables, los benchmarks tienen fugas de etiqueta y sets benignos sesgados, y ningún escáner supera a "marcar todo". La industria no puede llenar esto (conflicto de interés + sin ground truth).
2. **Portabilidad de propiedades de seguridad entre runtimes** (desafío #1 × #4): ¿sobrevive el modelo de permisos al portar SKILL.md → skill.json → manifest.json?
3. **Fallos benignos de composición**: liveness/deadlocks/contradicciones entre skills (la literatura de composición es casi toda de ataque).
4. **Verificación de la capa de instrucciones en lenguaje natural**: 2605.23951 sólo cubre el lado script; la semántica NL sigue sin garantías.
5. **Drift longitudinal** y **coste/economía de los pipelines de verificación**.

## 8. Plan de 3 etapas (reposicionado para ser defendible)
### ETAPA 1 — Tesis 1: "Auditoría de la medición" (no otra medición de prevalencia)
Construir un **ground truth humano** (300–500 skills, ≥2 anotadores, kappa de Cohen) muestreado de GitSkills/MaliciousSkillBench/ClawHub congelado; correr 6–8 escáneres existentes (Snyk Agent Scan, Cisco skill-scanner, NVIDIA SkillSpector, regex estático propio, LLM-as-judge barato) sobre la misma muestra; reportar precisión/recall/FPR vs ground truth, acuerdo inter-escáner, y auditar la calidad de los benchmarks publicados (fuga de etiquetas, artefactos vacíos, validez de constructo) usando el esquema de 2605.21404. Entregable: harness reproducible + snapshot congelado + set etiquetado + paper de validez de medición.
*Coste: 50–200 USD (etiquetado LLM) + tiempo humano. Sin GPU.*

### ETAPA 2 — Paper 1: Modelo de permisos por capacidades, evaluado empíricamente
No proponer otro framework (SkillGuard y OWASP Universal Skill Format ya existen): **medir** la expresividad y la aplicación del esquema de permisos sobre corpus reales. Cuantificar el "consent gap" declarado-vs-real (estático + sandbox dinámico), la cobertura de expresividad por esquema (¿cuántas skills pueden siquiera declarar su conjunto real de capacidades?), e implementar un monitor de referencia en 2 runtimes para medir aplicación efectiva; contrastar con el 99,93% que reclama SkillGuard. Eje novedoso: **portabilidad semántica de permisos** entre runtimes.
*Coste: 200–500 USD (sandbox + extracción con LLM). Sin GPU (Docker basta).*

### ETAPA 3 — Paper 2: Verificación automatizada con garantías
Extender la contención de capacidades (2605.23951, lado script) a la **capa de instrucciones NL** mediante un subconjunto mecánicamente chequeable de SKILL.md (anotaciones de efecto tipadas extraídas de NL, verificadas contra el manifiesto); añadir una **suite de tests negativos** para violaciones de especificación y liveness de composiciones; y evaluar adversarialmente la solidez de la suite. Encuadre: "solidez y límites de la verificación de skills", no "otro detector".
*Coste: 300–800 USD. GPU opcional (RTX 4050 6 GB corre un juez local 7–8B 4-bit; no imprescindible).*

**Total: ~550–1.500 USD. GPU: no requerida.**

## 9. Advertencias honestas
- El survey 2602.12430 tiene **~7 meses** y su lista de "siete desafíos abiertos" ya está parcialmente obsoleta; no debe usarse como mapa de huecos.
- El escaneo de skills ya es **categoría comercial** (Snyk, Cisco, Socket, Gen, NVIDIA, Akto). "Escanear skills" no es aporte académico por sí mismo.
- Cualquier medición de prevalencia caduca en meses: la ventaja académica está en la **validez y la reproducibilidad**, no en el número.
