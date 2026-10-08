# Auditoría de saturación: decoupling MODELO vs HARNESS + evaluación a nivel de trayectoria
Fecha de corte de la búsqueda: 19 sep 2026. Fuentes: arXiv (búsqueda full-text y avanzada por rango de fechas),
Semantic Scholar, OpenAlex, web.

## 1. Conteos duros (arXiv)

| Consulta (frase exacta) | Total | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|
| "agent harness" | 243 (búsqueda simple) / ~289 (avanzada 2026) | ~0 | 1 | 3 (jul–dic) | ~240–289 |
| "agent scaffold" | 112 | ~0 | pocos | pocos | mayoría |
| "harness effect" | 10 | 0 | 0 | 0 | 10 |
| "trajectory-level evaluation" | 10 | 0 | 0 | 2 | 8 |

Semantic Scholar, consulta amplia `agent harness model scaffold decoupling evaluation`: 1,932 hits (ruidoso,
incluye dominios ajenos como *scaffolds* de ingeniería de tejidos).

**Lectura:** el término "agent harness" prácticamente NO existía antes de 2026. Es un campo de ~18 meses.
Estimación propia: **~40–60 papers** tocan genuinamente la atribución modelo-vs-harness; **~12–15** hacen
medición factorial controlada; **~10** son benchmarks/harnesses construidos específicamente para ello.

## 2. Sistemas y benchmarks existentes

- **Harbor** (framework + Harbor Adapters + Harbor-Index, arXiv:2609.04298): 80+ benchmarks portados,
  8 modelos × 54 benchmarks, cada modelo con Terminus-2 y 3 harnesses nativos. Harbor-Index = 82 tareas,
  ningún config supera 30% pass rate.
- **Exgentic** (arXiv:2602.22953): factorial completo 5 arquitecturas de agente × 5 LLMs × 6 benchmarks,
  150 configuraciones, coste declarado ~$20K. Open General Agent Leaderboard.
- **Harness-Bench** (arXiv:2605.27922): 106 tareas sandbox, 5,194 trayectorias, configuraciones harness×modelo.
- **Claw-SWE-Bench** (arXiv:2606.12344): OpenClaw × 9 modelos y 5 claws × 2 modelos; modelo mueve 29.4 pp,
  harness 27.4 pp; coste como eje de primera clase.
- **HarnessRisk** (arXiv:2608.17597): seguridad por fases del harness, 14 configs modelo×harness.
- **ClawProBench** (arXiv:2608.22510): scoring de trazas con calidad de proceso + eficiencia, 68 configs.
- **HarnessDev** (2609.01437), **Evo-Bench** (2608.09096), **EvoHarnessBench** (2609.04280),
  **HarnessOpt-Bench** (2608.06301), **VeRO-Bench** (2602.22480): benchmarks de *evolución* de harness.
- **HAL** (Holistic Agent Leaderboard, 2025), **Inspect**, **BrowserGym**, **CUBE**, **AgentBeats**.

## 3. Qué NO cubren

1. **Métricas de atribución a nivel de trayectoria estandarizadas y realmente estimadas.**
   arXiv:2605.23950 propone RR(k), Context Retention y Control Lag, pero declara explícitamente:
   *"We do not estimate these metrics on the 3×3 grid. Instead, we specify them as reporting requirements
   for future harness-aware evaluations."* → hueco abierto, citable, con la formulación ya dada.
2. **Modelos baratos / no-frontera como eje sistemático.** En los factoriales dominan modelos frontera;
   los modelos chinos baratos aparecen como "side cells" (deepseek-v3.2 en 2609.11987) o dentro de papers
   de evolución de harness (GLM-5, Qwen3.5, MiniMax M2.5). No hay un estudio factorial dedicado a la
   pregunta "¿el harness importa igual cuando el modelo es barato?".
3. **Dominios no-código.** El trabajo factorial es abrumadoramente SWE/terminal/coding. τ²-bench, deep
   research, office/customer service están sub-cubiertos.
4. **Bias de medición correlacionado** entre señales de proceso usadas para *entrenar* agentes y las usadas
   para *evaluarlos* (nombrado por el survey Horizon Gap, 2608.06663). Prácticamente virgen.
5. **Protocolos de potencia estadística / presupuesto de rollouts** para separar efecto-modelo de
   efecto-harness. Solo hay un preprint tangencial (Deployment Decision Reliability, S2 061ebefe...).
6. **Frontier coste–rendimiento (Pareto precio × tier de modelo × harness).** El coste se reporta, pero no
   se modela como frontera.
7. **Generalización fuera de inglés / fuera de EE.UU.** Nada.

## 4. Veredicto

**6/10.** Ver justificación en el informe final.

## 5. Plan de 3 etapas

Ver informe final.
