# Skill Routing Economics

**Status**: 🟢 PRODUCTION
**Version**: 1.0.0
**Category**: Agent Capability Management

---

## Overview

Skill libraries grow monotonically. Nobody deletes a skill, because deleting one has an
obvious cost (a capability disappears) and no visible benefit. So they accumulate, and the
assumed price is tokens — the always-on descriptions in the system prompt.

**That assumption is wrong, and it is wrong in a way that misdirects the entire pruning
effort.**

**The Problem**: measured on a production agent with ~100 skills, the always-on skill block
was ~11,500 tokens per turn — but prompt-cache hit rate ran **87%**, making the real spend
roughly a fifth of nominal, on the order of $20/month. Meanwhile 18% of skills had never
been invoked once, and a third had been invoked exactly once.

Token cost was never the constraint. **The constraint is the model's routing attention.**

**The Solution**: treat the skill block as a **routing table**, not a library. Every
description is a candidate answer in a multiple-choice question the model answers on every
turn. Adding a skill does not merely add tokens — it **adds a wrong answer**. Prune for
discriminability, not for size.

> This is [`operator-attention-os`](../operator-attention-os) with a different consumer.
> There, the scarce resource is the human's attention. Here it is the model's. Same law.

---

## The Five Laws

| # | Law | The instinct it corrects |
|---|-----|--------------------------|
| **1** | **Routing attention, not tokens** — a skill's real cost is being a distractor in every routing decision | "Trim the verbose descriptions." Measure cache hit first; if it is high, description length is nearly free and you are optimising the wrong axis. |
| **2** | **Cost is the count, not the outliers** — descriptions converge on a uniform size | "Find the bloated ones." Measured: median 332 chars, min 300, max 374 across 100 skills. There are no outliers. Only *fewer* helps. |
| **3** | **Never-invoked is worse than unused** — it is an active wrong answer, not dead weight | "It costs almost nothing to leave it." It costs a share of every routing decision, forever. |
| **4** | **Overlap is the harm** — two descriptions a model could confuse damage each other | "More coverage is better." Two similar skills are worse than one good one: the same correlated-error problem as staffing a council with one model family. |
| **5** | **Gates only pay when platforms differ** — a precondition that is always satisfied is not a filter | "Gate everything with a dependency." Verify the gate can actually fail before counting the saving. |

---

## The discriminating test

For each skill, ask two questions:

> If this description vanished, would the model still reach the skill when it is genuinely
> needed? **If yes — redundant.**
>
> Would the model route to it *wrongly*, in situations it does not serve? **If yes — it is
> a distractor**, and it is costing you turns, not tokens.

A skill that is neither redundant nor a distractor earns its place regardless of how rarely
it fires.

---

## Five operations, each with a measurable trigger

| operation | trigger | note |
|---|---|---|
| **KILL** | `use_count == 0` over a meaningful window, no unique capability | pure distractor, zero return |
| **MERGE** | two descriptions above a confusability threshold | overlap *is* the damage — one sharp entry beats two blurry ones |
| **SPLIT** | one skill invoked across genuinely divergent intents | its description cannot discriminate; sharpen both halves |
| **GATE** | declares a precondition **that can actually fail** | the only operation with zero capability loss — but see Law 5 |
| **DEMOTE** | used, but rarely, and highly specific | keep it installed and reachable by name; remove it from the routing block |

**DEMOTE is the underused one.** The awkward cohort is not the never-invoked skills — those
are easy. It is the ones invoked *exactly once* over months. Killing them destroys real
capability; leaving them in the routing block taxes every turn. Demotion resolves the
tension: reachable by explicit name, absent from the routing decision.

---

## Structure: English, JSON, or something else?

Skills are written *for agents, by agents*, which invites the question of whether prose is
the right encoding at all. Measured against one production tokenizer, same information:

| encoding | vs plain English |
|---|---|
| minified JSON | **0.58×** |
| terse / telegraphic | 0.62× |
| plain English | 1.00× |
| gzip + base64 | 2.70× |
| base64 | 4.39× |

Encoding more densely **backfires** — gzip+base64 has 22% fewer *characters* and 170% more
*tokens*. But the interesting result is that even the winners are the wrong optimisation:

**A description's job is semantic matching, not data transfer.** The model reads it to
decide "is this my situation?" Compressing it to save 40% of an already-cached block, while
degrading the model's ability to discriminate, trades pennies for turns.

### The answer: split by consumer

Not English *or* structured. **Both, divided by who evaluates them.**

| content | consumer | encoding | reaches the prompt? |
|---|---|---|---|
| preconditions — required tools, platforms, capabilities | the **runtime** | structured data | **never** |
| semantic trigger — when this situation applies | the **model** | natural language | only when preconditions pass |

Machine-checkable facts should be evaluated before the prompt is assembled. A browser skill
should not be a routing candidate in a session with no browser — not because it is
expensive, but because it is a *wrong answer that cannot be right*.

Natural language is correct for the half the model reads, because semantic matching is what
models do. Structured data is correct for the half the runtime reads, because determinism is
what runtimes do. Most skill formats collapse both into prose and hand the whole thing to
the model — which is how you end up asking a language model to evaluate a boolean.

---

## Anti-Patterns

- **Pruning by description length.** Law 2. The distribution is flat; there is nothing to trim.
- **Counting a gate before proving it can fail.** An audit found ~62% of skills declared a gateable dependency — but the platforms in use shared nearly identical toolsets, so almost every gate would have fired *never*. The headline saving was imaginary. Verify against the actual platform matrix.
- **Treating `use_count == 1` as alive.** One invocation in six months is a demotion candidate, not a justification.
- **Adding a skill for a case an existing skill nearly covers.** You have not added coverage; you have added ambiguity to both.
- **Optimising the block before measuring cache hit.** If the block is cached, its size is close to free and the whole exercise is misdirected.

---

## Provenance

Derived from an audit of a production agent's ~100-skill routing block. Every number here
was measured, including the ones that overturned the audit's own initial conclusions — the
44% gating saving that turned out to be near-zero once the platform matrix was checked is
recorded above as an anti-pattern rather than quietly dropped.
