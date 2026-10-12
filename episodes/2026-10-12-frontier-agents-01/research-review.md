# Episode 01 — Research integrity and methodological audit

**Review date:** 12 October 2026. **Cutoff:** 12 October 2026.
**Review type:** AI-assisted editorial fact-check against original published source material, NOT independent human peer review or replication.
**Decision:** Correct the benchmark timeline in audio and transcript; release with caveats and claim-level evidence mapping. The episode is an educational conceptual synthesis, **not** an original experimental research study.

## Scope and search method

Targeted original-source search for OpenAI benchmark evaluations and later retractions, Anthropic agent architecture patterns, OpenAI agent tracing and evaluation documentation, academic agent benchmark methods and LLM-judge reliability. Key queries:
- `OpenAI February 2026 why no longer evaluate SWE-bench Verified contamination`
- `OpenAI July 2026 separating signal noise coding evaluations SWE-bench Pro`
- `Anthropic building effective agents December 2024 workflows vs agents`
- `OpenAI developers evaluate agent workflows traces graders datasets`
- `arxiv AgentJudgeBench 2026 tool calling judges`

**Selection:** Original papers or institutional technical reports and documentation that bear directly on each material claim. A vendor's own audit is labelled as a vendor-authored primary report, not independently validated evidence. Preprints are explicitly identified. News articles, public-relations paraphrases and unsupported social-media claims were not used as primary evidence.

**Important contrary development discovered:** The February 2026 critique of SWE-bench Verified is real, but a newer **8 July 2026** OpenAI analysis estimates approximately 30% of SWE-bench Pro public-split tasks have issues and retracts OpenAI's earlier endorsement of Pro. This materially changes the benchmark discussion. See primary source: https://openai.com/index/separating-signal-from-noise-coding-evaluations/

## Adversarial review findings

1. **Historical accuracy versus completeness:** A fact can be literally correct but misleading when a later retraction exists. The updated narration now gives the entire February-to-July benchmark sequence rather than stopping at the older finding.
2. **Author versus independent evidence:** OpenAI's 2026 benchmark audits are conducted and published by OpenAI. Their methods are reported, but the underlying findings have not been independently replicated in this production workflow. The transcript now says so.
3. **Conceptual claims versus tested hypotheses:** Architecture discussions often present reasoned engineering principles. Comparisons such as 'more agents may be worse' are framed as testable propositions, not universal measured facts.
4. **LLM evaluation caution:** Model-based grading is not interchangeable with independent functional tests or blinded expert evaluation. The episode does not claim it is.
5. **Frontier-lab language:** The phrase denotes the depth and experimental mindset of the tutorial, not sponsorship, employment, validation or review by an AI laboratory.

## Limitations

- This is **not** a systematic review, preregistered meta-analysis, or peer-reviewed paper. Search and synthesis were targeted, not exhaustive.
- Audio is a pedagogical synthesis built from a series of established ideas. It does **not** report completed new experiments or numerical improvements in any agent.
- Benchmark studies use different tasks, evaluation criteria and models; no cross-study causal comparisons are made here.
- Some sources are developer-authored accounts, living technical documentation, and preprints. They are authoritative about what their authors did or documented, not automatically proof of broad generalisation.
- Claims in the published transcript not mapped to a source are either obvious background statements, hypothetical examples or pedagogical advice; if a future edition uses numerical comparisons they require additional ledger entries.
- The independent editorial checks in this production are not blinded human peer review and cannot guarantee absence of factual errors.

## Reproducibility checklist for the featured experiment

- [x] Formal question: reactive versus initial versus revisable planning in a coding agent
- [x] Three intervention groups described
- [x] Model, tools, tasks and budgets identified as required controls
- [x] Primary endpoint: independently verified task completion
- [x] Secondary endpoints: cost, time, tests, edits, severe deviations
- [x] Trajectory and repository-version preservation recommended
- [x] Leakage and task contamination risks identified
- [x] Held-out evaluation set and repeated trials recommended
- [x] Limitation explicitly stated: a planned experiment, not an experiment run for this episode
- [ ] Actual implementation, preregistration, data, and confidence intervals: **not yet performed**

## Evidence ledger and release rule

See `evidence-ledger.json` for exact narrational excerpts, supporting source IDs, publication dates, classifications and specific limitations. This map is a transparent editorial aid, not an assertion that every supporting study has been independently reproduced.

**Release check:** Execute `python3 scripts/check_frontier_research.py episodes/2026-10-12-frontier-agents-01` plus publisher tests, XML checks and audio integrity verification. Red flags must block release.
