# MoA Council Qualification

**Status**: 🟢 PRODUCTION
**Version**: 1.2.0
**Category**: Multi-Model Orchestration & Cost Engineering

---

## Overview

Mixture-of-Agents (MoA) is the pattern where several models advise in parallel and one
aggregates their advice into the answer. Every serious agent stack is converging on some
version of it. Almost nobody engineers the roster.

**The Problem**: Model selection for a council is treated as a taste question — pick the
models at the top of a leaderboard, wire them up, ship. That produces councils that are
quietly broken in ways no test catches: advisors truncated mid-sentence, a "board of
advisors" that is one model talking to itself, a synthesizer weaker than the models it
referees, a roster naming models the API cannot actually call, and a bill nobody predicted
because unit price was confused with cost per finished task.

**The Solution**: A qualification protocol. Eight falsifiable laws, each of which contradicts
an intuition most teams hold, and a runbook that proves a roster before it ships. Every law
here was derived from a real defect — most caught during qualification, and three (2, 7, 8)
caught only after the roster had already shipped and passed review.

**Why this step matters**: a bad council does not fail loudly. It returns a plausible
answer, at a higher cost, with fewer real perspectives than you think you bought. The
failure mode is invisible by construction: you cannot tell from the output that one advisor
was cut off at its token cap, or that three of your four "independent" advisors were the
same model. Qualification is the only place these defects are detectable.

---

## The Eight Laws

| # | Law | The intuition it breaks |
|---|-----|-------------------------|
| **1** | **Catalog Law** — qualify against the API, not the storefront | A vendor's chat app and its developer API are different surfaces with different rosters. The flagship on the marketing page may `404` on the endpoint you bill against. |
| **2** | **Reasoning-Token Law** — output caps count invisible thinking | A cap named for output silently includes reasoning tokens. A reasoning model can spend its entire budget thinking and emit a truncated fragment as "advice". |
| **3** | **Recency Law** — newer is not better; verify per axis | Version *n+1* frequently regresses against *n* on real axes. This is not rare; expect it and check. |
| **4** | **Fan-Out Law** — know which primitive you have | Most delegation APIs resolve **one** credential bundle and hand the same model to every child. That is homogeneous fan-out. Building a "council" on it yields one model in N costumes. |
| **5** | **Unit-Price Law** — unit price ≠ cost per successful task | Two models can bill identically per token and differ 2× per finished task, because effort settings and verbosity drive spend more than rate does. |
| **6** | **Sensitivity Law** — classify data before ranking capability | Governance binds before benchmarks. The best model for a task is irrelevant if policy forbids that class of data reaching it. Sensitivity is a gate, not a tiebreaker. |
| **7** | **Context Law** — cost tracks **session age**, not question difficulty | Every advisor receives the whole conversation, so the same question costs more in week six than week one. Measured: **130:1** input-to-output from a 12-day session, **3.1:1** from a fresh one — the same question, **$1.18 vs $0.0144**. Escalate from a fresh session. |
| **8** | **Compression Law** — compression is **semantic**, not syntactic | You cannot beat the tokenizer by encoding more densely. Measured on one tokenizer: base64 **4.39×** the tokens of plain English, gzip+base64 **2.70×** — and gzip+base64 has **22% fewer characters**. Character count and token count are decoupled. Send less; never send denser. |

> **Laws 2 and 7 interact, and the interaction is the trap.** In an aged session output is a
> rounding error, so a *generous* output cap is nearly free — yet caps get set tight "to
> control cost", buying nothing and truncating advisors. Note the ratio inverts as sessions
> shorten: at 3:1 output *does* matter. Calibrate caps for quality either way; control cost
> by controlling context.

---

## Skillpack Signatures

| Skill | Trigger | Description |
|-------|---------|-------------|
| **Roster Qualification** | "Which models should advise?" | Runs the full protocol: catalog probe → role-matched ranking → token measurement → resolution proof → per-turn pricing. |
| **Cap Calibration** | "What should the token cap be?" | Measures reasoning-vs-visible token split per candidate and sets caps with measured headroom instead of a guessed constant. |
| **Fan-Out Audit** | "Can this actually run models in parallel?" | Determines whether the available primitive is homogeneous or heterogeneous before any architecture is designed around it. |
| **Council Pricing** | "What does one escalation cost?" | Converts measured token behaviour and published rates into a per-turn figure and a runway against current balance. |

---

## Role Determines The Metric

The single most common roster error is ranking every seat by "overall score". Advisors and
aggregators do different jobs and should be selected on different axes.

| Seat | What it actually does | Rank it on |
|------|----------------------|------------|
| **Advisor** | Produces one independent perspective. Never seen by the user. | Domain axes for the task; **lineage diversity** across the set |
| **Aggregator** | Follows the synthesis instruction, writes the user-visible answer, and **acts in the tool loop** | Instruction-following, language, and — if the loop uses tools — agentic capability |

A council of four models from one family buys correlated errors at 4× the price. Diversity
across the advisor set is a first-class selection criterion, not a nice-to-have. The
exception is genuine **specialists**: a coding-tuned sibling of a general model is a
different perspective; two general siblings are not.

---

## Anti-Patterns

- **Leaderboard-topping roster.** The top model on a board may be unreachable via your API, restricted by your governance, or priced for a different budget. Availability and policy are filters applied *before* ranking.
- **The weak synthesizer.** Putting a small fast model in the aggregator seat to save money inverts the whole pattern — you pay for frontier advice and then have it summarized by the weakest participant.
- **Guessed caps — and caps measured on toy prompts.** Any cap not derived from measurement *under representative context* is a truncation bug waiting for a real conversation.
- **Homogeneous "councils".** See Law 4. Verify the primitive.
- **Static rosters.** A qualified roster is qualified *as of a date*. Model catalogs move weekly. Re-run the protocol, and never hardcode a model id you have not probed.

---

## References

- [`references/qualification-protocol.md`](references/qualification-protocol.md) — the step-by-step runbook, with the failure each step catches
- [`references/field-notes-2026-08.md`](references/field-notes-2026-08.md) — a dated worked example: what the protocol caught on a real roster

---

## Provenance

Derived from production qualification of a live operator-agent council on the Hermes stack.
Every law corresponds to a defect this protocol met in production — including three it failed
to prevent on the first pass, documented in the field-notes postmortem rather than quietly
patched. The dated appendix will age; the laws will not.
