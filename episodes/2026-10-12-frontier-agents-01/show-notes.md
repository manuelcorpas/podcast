# Frontier Agents — Episode 01

**Title:** How Agentic AI Actually Works: The Frontier Lab Mindset
**Format:** Approximately 30-minute technical masterclass, single-voice narration
**Produced:** 12 October 2026
**Voice disclosure:** The narration is synthetic and AI-generated.
**Intended audience:** AI researchers, engineers, technical scientists, and advanced AI practitioners.

## Podcast description

What separates using an AI assistant from thinking like a frontier-lab researcher working on autonomous agents? This episode builds a rigorous mental model of agentic AI: the agent loop, tool interfaces, runtimes and harnesses, context engineering, test-time computation, multi-agent coordination, safety boundaries, evaluation design, and the economics of verifiable outcomes.

An autonomous coding agent serves as the running example. The episode finishes with a controlled experiment you can actually reproduce: comparing reactive execution, fixed planning, and revisable planning, while controlling for compute budget, test leakage and evaluation variance.

The central message: **Agentic capability is not demonstrated by a persuasive final answer. It is demonstrated by verified behaviour in an environment, under explicit constraints.**

## Topics

- What distinguishes an agent from an ordinary model call or fixed workflow
- Model policy, action loops, observations and stopping conditions
- Agent harnesses, tool schemas, sandboxed execution and traces
- Context engineering versus genuine learning
- Planning and inference-time compute
- Single-agent versus multi-agent architecture trade-offs
- Reproducible agent benchmarks, independent checks and benchmark leakage
- Failure-first evaluation, prompt injection and reward hacking
- Cost per verified outcome and resource-bounded autonomy
- A reproducible three-condition coding-agent experiment

## Research and technical references

1. OpenAI, [Agents SDK documentation](https://developers.openai.com/api/docs/guides/agents/sdk) — agent runtimes, tools, handoffs, guardrails and orchestration.
2. OpenAI, [Integrations and observability](https://developers.openai.com/api/docs/guides/agents/integrations-observability) — traces, tool calls, guardrails and instrumented workflows.
3. Anthropic, [Building effective agents](https://www.anthropic.com/research/building-effective-agents) — simple compositional patterns and workflow-versus-agent distinctions.
4. Anthropic, [Common workflow patterns](https://claude.com/resources/articles/common-workflow-patterns-for-ai-agents-and-when-to-use-them) — sequential, parallel and evaluator-optimizer patterns.
5. OpenAI, [Why we no longer evaluate SWE-bench Verified](https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/) — a February 2026 discussion of benchmark contamination and test validity.

## Lab experiment summary

**Question:** Does planning materially improve autonomous coding performance on unfamiliar maintenance tasks?

**Conditions:** (A) reactive agent; (B) agent with initial plan; (C) agent with revisable plan after contradictory evidence.

**Controls:** same model, same tools, matching task distribution, comparable inference budget, recorded model version and repository commit, independent grading.

**Measure:** held-out task success, regressions, unintended edits, token and tool-call counts, runtime, severity-weighted failures, and repeated-trial variance.

**Interpretation:** Report what changes, on which task classes, at what resource cost. Do not infer causal improvement if budgets or environments differ.

---

*Educational content. Narration generated with an AI voice. No clinical advice, and no claim of human-voice narration.*
