---
name: frontier-agents-learning
description: Produce a technically rigorous, continuously updated 25–35 minute agentic AI masterclass for Manuel's personal learning; create AI-narrated MP3, transcript, cited notes, reproducible lab and publication-ready assets; publish to Personal Genomics Zone only with explicit approval.
---

# Frontier Agents: continuing technical AI learning podcast

## Trigger
Use this skill when asked for the next *Frontier Agents* episode, a frontier-lab learning podcast, an update of an earlier AI masterclass, or continuation of agentic-AI education in audio.

## Mission and scope
Develop Manuel's **technical literacy in frontier agentic AI**, with mastery measurable by his ability to implement and evaluate systems. This is **not** a genomics or PRS teaching podcast. Genomics is acceptable only as an optional application after the general AI concept has been explained technically.

The series runs *inside* the existing **Personal Genomics Zone** feed (repository: `manuelcorpas/podcast`, deployed at `https://manuelcorpas.github.io/podcast/`, RSS `feed.xml`). "Frontier Agents" is a series name, not a new RSS feed.

Read the canonical `SOUL.md` at `~/dev/AGENTIC-AI/00-CORE-MEMORY/STRATEGY/SOUL.md` where available, then read the parent project's `SOUL.md`. Cognitive augmentation is the ultimate goal; agentic genomics is the means of proving it. Respect the doctrine's explicit per-publication human-approval gate.

## Personal AGENTIC-AI project as the learning compass

**Before researching or choosing any episode**, use the live project at ~/dev/AGENTIC-AI as a source of learning needs, not as material automatically cleared for public release. Do NOT rely on stale memories or a guessed current state.

1. Read the governing ~/dev/AGENTIC-AI/00-CORE-MEMORY/STRATEGY/SOUL.md, then the project's SOUL.md and the current-state and personal-AI-proof documents. The ultimate objective is measurable cognitive augmentation, not content output for its own sake.
2. Run python3 scripts/frontier_learning_context.py to construct a LOCAL, PRIVATE, read-only source map of the most recent project work. It collects bounded Git subjects and measurement gaps from AGENTIC-AI and related local repositories. Read the local private file at ~/.local/share/frontier-agents/private-learning-context.md. Never upload or commit that private brief. If the computer or project is unavailable, state the evidence gap and use only the user-approved or currently visible context.
3. Check recent relevant code paths, traces, PRs, benchmarks and experiments only as needed for a specific curriculum question. Examples of relevant ongoing engineering: agent orchestration, Codex/MCP/GBrain retrieval, persistent state, tool failure recovery, RoboTerri and other agent coordination, ClawBio/ClawBench evaluation, and trustworthy scientific autonomy. Work on these systems informs *what to learn*, not the general audience episode's whole subject.
4. Identify **one frontier-AI technical knowledge gap**, independently of any biomedical or PRS task. Examples: trace-grounded retrieval and context selection; state persistence vs model memory; idempotent retry and failure recovery; multi-agent handoff overhead; benchmark design; measuring actual human attention saved.
5. Link that gap to two or more independent pieces of external original research and create a lab exercise using PUBLIC or SYNTHETIC examples. Publish no operational project details, unfinished hypotheses, sensitive personal information, medical/patient data, credentials, private logs, staff names, internal systems or unpublished results without explicit separate disclosure approval.
6. Maintain **two deliverables**: (A) a publishable neutral technical podcast, and (B) a PRIVATE application brief naming the relevant project components, testable change, relevant local traces, expected result and 1–2 next actions. Only A enters the public podcast repository.
7. Capture five active-recall questions and one executable coding/evaluation task for the listener. At the next episode, measure whether the previous gaps were closed; adapt difficulty and revisit misconceptions. Learning is assessed by correct explanations, successful reproducible experiments, and fewer verified failure modes, NOT listening counts, Git commit counts or a self-declared top-1% percentile.
8. An operational success claim must be checked against actual verified outcomes and the project's personal-AI-proof measurement gates; do not interpret unverified attention savings or high activity as demonstrated gains.

**Curriculum prioritisation:** frontier conceptual importance 30%, evidence gap demonstrated in AGENTIC-AI 30%, quality of original external research 25%, ability to test in an hour 15%. Override this formula only with explicit documented rationale. Keep one coherent technical theme per episode; do not become a daily news bulletin.

## Inputs
- `topic` (optional; choose the highest-learning-value agentic AI concept if unspecified).
- `continuation_of` (optional, episode number or prior transcript).
- `new_developments_since` (optional; otherwise use previous episode publication date).
- `duration_minutes` (default 30, target 29–31).
- `publish` (default false; **must** be explicitly authorised for *this* episode).

## Workflow
1. **Recall first.** Refresh the private AGENTIC-AI learning-context brief described above, establish the live proof gaps, and read latest episodes in `feed.xml`, the Frontier Agents transcripts and `episodes/frontier-agents/series.json` if present. Identify the next number, known prior concepts, unanswered questions, repetitions, and a learning objective. Do not recycle the earlier episode as "new".
2. **Research current evidence.** Use dated primary sources: official research papers, technical documentation, benchmark code, arXiv papers with caveats, and changes from OpenAI, Anthropic, Google DeepMind, METR, and independent evaluation groups. Cross-check details and event dates. Distinguish published research, engineering claims, benchmark results, speculation, and your own hypotheses. Do not invent citations or rely on a press release alone for a quantitative result.
3. **Pick a technical question, not a news roundup.** Prioritise concepts such as agent policy and harness, tool use, MCP, planning, memory/context, long-horizon reliability, inference-time compute, RL for agents, verifiers, agent security, environments, simulation, benchmarks, or multi-agent coordination. Prefer a topic with an actionable experiment. Use relevance (30), novelty versus prior episodes (25), evidence strength (25), and experimental tractability (20), each scored with written rationale; normally require 80/100 before production.
4. **Write for audio, not for slides.** Approximately 4,200–5,100 spoken words for a half-hour, calibrated against synthesis duration. Open with a concrete research question; explain architecture and mechanisms; give one running general-purpose AI systems example; compare alternatives; cover real failure modes and evidence; specify a reproducible experiment; finish with technical takeaways and what the next episode builds on. Use natural British-English scientific delivery; no padded motivational slogans or invented expert conversations. Explain notation in spoken English.
5. **Technical and editorial review.** Verify every time-sensitive claim against sources; validate numbers; make clear what is known and unknown. Check repeated material against transcripts. Avoid representing generated narration as Manuel's natural voice or claiming experiments were run unless there are stored artefacts. Maintain a source map and the exact primary citations in show notes. Reject unexplained jargon, advice-only content, weak sources and unsubstantiated frontier-lab claims.
6. **Audio production.** Prepare an immutable UTF-8 transcript. Run `python3 scripts/render_frontier_agents.py --script INPUT --output OUTPUT --target-minutes 30` (with `OPENAI_API_KEY` already configured in the authorised runtime) using the tested natural HD synthetic voice. Never print, log or commit credentials. Encode clean MP3, check integrity with `ffmpeg -v error -i MP3 -f null -`, verify duration with `ffprobe`, and inspect quality. Default voice: OpenAI `tts-1-hd` / `onyx` (the successful Episode 01 voice); replace only after listening and confirming a real improvement. No macOS `say` fallback and no silent substitution to another voice.
7. **Release preparation.** Create `episodes/YYYY-MM-DD-frontier-agents-NN/transcript.txt`, `show-notes.md`, citations with URLs, next episode questions, an MP3 under `audio/`, and a compact manifest containing episode number, date, topic, source dates, voice/model, duration, source SHA-256 and audio SHA-256. Keep project files inside the existing podcast repo. Validate existing feeds and site before and after running `scripts/add_episode.py`. Prevent duplicate GUIDs.
8. **Publication gate.** External release is forbidden without explicit user approval of **that exact episode**. When approved: run existing publishing script; execute unit tests and RSS/XML/MP3 checks; stage **only** episode artefacts, the feed, the index and relevant skill changes; commit to the existing podcast repository; push to `main` if it is fast-forward safe; verify live `feed.xml` and HTTP delivery of the MP3. Do not claim Apple/Spotify ingestion until independently observed: podcast directories poll feeds asynchronously.
9. **Learning feedback.** After each episode, record a 5-question oral challenge, a small practical experiment and the user's feedback/knowledge gaps. Use these to select the next episode and adjust the difficulty. Record what was *learned*, not merely listened to.

## Non-negotiable research-methods gate
Before script finalisation, construct evidence-ledger.json with entries for **every material empirical, comparative, numerical, dated, technical, or safety-related claim**. Each entry contains an exact transcript excerpt, source identifiers, evidence classification, audit disposition, and concrete limitations. Each source has institution, date, original URL, specific supporting finding and limitations.

- **Prioritise original evidence:** inspect primary papers, methods, supplementary information, benchmark code, or standards. Press releases and secondary reporting are context, not independent efficacy confirmation. Developers' own research reports are primary accounts, not independent replications.
- **Recency and contradiction:** search up to production date for corrections, retractions, revised benchmark findings, replications, or adverse results; apply the later evidence even when an older statement is historically correct (as with February versus July 2026 SWE-bench findings).
- **Search log:** retain queries, search dates, inclusion/exclusion rationale, contrary evidence, and reasons for selecting cited papers. Separate peer-reviewed papers, preprints, vendor-authored reports, official docs, hypothesis and speculation.
- **Statistical integrity:** report relevant sample sizes and splits, metrics, uncertainty if provided, baselines, confounders, model versions, tool/environment details, missingness and benchmark leakage risk. Never invent results or generalise a demo into a validated empirical improvement.
- **Adversarial review:** independently inspect key claims' original sources, actively search for contradictory evidence, and test for unsupported causal inference, benchmark gaming, and omitted limitations. Produce a research-review.md with limitations and reproducibility checklists. AI review is not human peer review.
- **Falsifiable lab:** use predefined primary endpoint, baseline, controlled model/tool budget, evaluation set isolation, repeats where feasible, failure analysis and independent verification. Distinguish planned from actually completed experiments.
- **Hard fail:** execute python3 scripts/check_frontier_research.py EPISODE_DIRECTORY before rendering or release. Checks ensure evidence structure, NOT epistemic truth. Human editorial review remains required. Unverifiable claims should be withheld or conspicuously qualified.
- **Audio/version integrity:** transcript, audio, notes, feed, and evidence map must reference one frozen version. For significant corrections, release versioned audio and update podcast enclosure without altering the episode's stable GUID. Include correction notice.
- Never call an episode peer-reviewed, independently replicated, or production verified without exact matching evidence; source/vendor claims cannot be recast as objective ground truth.

## Quality gates
- Episode must teach how a frontier agentic-AI system works under the hood and what to test.
- Technical accuracy, citation provenance and reproducible lab come before novelty.
- At least one falsifiable experiment and meaningful baseline.
- 29–31 minutes verified, intelligible narration, consistent volume, complete final audio.
- Clear AI narration disclosure; no implication that the audio is Manuel speaking.
- No automatic public release on recurring scheduling without explicit episode-specific approval.
- If sources are inadequate, produce a research brief and questions rather than a fabricated episode.

## Continuation curriculum (adapt to new evidence)
1. Episode 01 — Agent architecture, harness, context, evaluation (published only when approved).
2. Episode 02 — Agents as sequential decision-makers: policies, action/observation loops, stopping, uncertainty and budgets.
3. Episode 03 — Context engineering versus persistent memory: retrieval, compaction, state reconstruction and contamination.
4. Episode 04 — Evaluation at the frontier: trajectories, graders, task distributions, benchmark gaming and held-out tests.
5. Episode 05 — Tool-use reliability: schemas, privilege boundaries, prompt injection, MCP and runtime design.
6. Episode 06 — Test-time compute and agent planning: baselines, search, self-correction and cost-quality frontiers.
7. Episode 07 — Multi-agent coordination: parallelism, independence, correlated errors and supervision.
8. Episode 08 — Training agent behaviour: reinforcement learning, tool feedback and verifiable rewards.

The series should change when new advances make the prior ordering obsolete. Each episode must advance mastery beyond the last.

## Repository tools
- `scripts/render_frontier_agents.py`: voice synthesis, normalisation, duration verification, optional dry-run.
- `scripts/add_episode.py`: existing RSS and index insertion.
- `scripts/test_add_episode.py`: existing publisher tests.
- `episodes/2026-10-12-frontier-agents-01/`: baseline script and show notes.
