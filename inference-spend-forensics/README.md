# Inference Spend Forensics

**Status**: 🟢 PRODUCTION
**Version**: 1.0.0
**Category**: Operator Cost Control

---

## Overview

An inference bill arrives that is several times what you expected. You know your systems.
You form a hypothesis — *it must be the chat feature, users have been busy* — and you start
optimising there.

**You are almost certainly wrong, and the bill contains the evidence to prove it.**

**The Problem**: a 30-day bill of **$1,234.06** across two projects, attributed to "input
tokens" and "image output tokens." The operator's instinct was that the customer-facing app
was responsible. It was not. **74% of the spend came from scheduled background jobs inside
an agent runtime the operator believed was running locally.** It had been billing a cloud
API on every turn for months. Nothing was broken, no alert fired, and every internal cost
estimate read `$0.00` for the single most expensive model in the system.

**The Solution**: treat the bill as a crime scene with fingerprints already on it. **Model
identifiers are globally unique strings.** Before theorising, grep every codebase and config
for the exact model names on the invoice. The one that appears in only one system *is* the
culprit, and the attribution is not a guess — it is a proof.

> This is [`operator-attention-os`](../operator-attention-os) applied to money. There, the
> scarce resource is attention and the failure is noise. Here the scarce resource is spend
> and the failure is **invisibility** — cost that no dashboard reports because the code was
> written to report it as zero.

---

## The Seven Laws

| # | Law | The instinct it corrects |
|---|-----|--------------------------|
| **1** | **Attribute by model string, not by intuition** — model IDs are unique fingerprints; the culprit is the system where that exact string appears | "It's probably the chat feature." Grep first. A model string present in exactly one codebase ends the argument. |
| **2** | **"Local" is a claim, not a fact** — verify the resolved default model of every agent runtime you call local | "Hermes is our local lane." Its config default was a cloud API model. Every "local" turn was metered. |
| **3** | **Unpriced is not free** — a `0/0` entry in a price catalog makes spend structurally invisible | "Our cost dashboard shows nothing." It shows nothing *because* the expensive model is priced at zero, not because it's cheap. |
| **4** | **Scheduled beats interactive** — unattended work compounds; interactive work is self-limiting because a human is waiting | "We barely used it this month." Cron was 74% of calls. Nobody watches cron. |
| **5** | **Baseline and spikes have different owners** — plot daily before you theorise | "It's all one problem." A flat plateau and a $325 spike were two unrelated systems. The spike day was the *quietest* day for the baseline system. |
| **6** | **A subscription you own is not a lane you use** — credential pools default to whatever metered key is present | "We pay for ChatGPT already." The OAuth provider was never authenticated; the metered API key was, so every call took the expensive path. |
| **7** | **Flat-rate has a trapdoor** — auto-recharge silently converts a subscription back into metered billing | "Route the load to the flat-rate plan." With auto-recharge enabled, overflow bills your card instead of throttling. Check before you migrate. |

---

## The discriminating test

For any cost you are about to optimise, ask:

> **Did I measure this, or infer it?** If inferred — stop. The cheapest measurement in this
> entire discipline is `grep` for a model string.
>
> **If this line went to zero, would the bill actually drop by that much?** If you cannot
> answer from data, you are optimising a story.

A fix that is not anchored to a measured line item is a guess wearing a commit message.

---

## The diagnostic sequence

Run in order. Each step is cheap and eliminates whole branches.

| # | step | what it settles |
|---|------|-----------------|
| **1** | **Grep every repo and config for the exact model strings on the invoice** | Attribution. A string in one system only is proof, not hypothesis. |
| **2** | **Plot daily spend** | Whether you have one problem or two. Plateaus and spikes rarely share an owner. |
| **3** | **Find the runtime's own usage ledger before building one** | Mature agent runtimes record per-call tokens locally. Query it; do not instrument blind. |
| **4** | **Split that ledger by session origin** (cron / interactive / API) | Whether humans or schedulers are spending. Usually schedulers. |
| **5** | **Divide calls by runs** | Per-run efficiency. A job averaging 40+ model turns is malfunctioning, not merely expensive. |
| **6** | **Check for a hard turn ceiling and count runs that hit it** | Runaway jobs. Runs pinned exactly at the cap never finished — they were truncated. |
| **7** | **Verify which credential each provider actually resolves to** | Whether you are paying twice for capacity you already own. |

**Trust token counts, not the ledger's own cost column.** Every runtime examined had a
`estimated_cost_usd` field that was mostly zeros, for exactly the Law 3 reason. Tokens and
call counts are ground truth; derived cost inherits every gap in the price table.

---

## What the numbers looked like

Recorded so the shape is recognisable, not because your numbers will match.

| signal | value | what it meant |
|---|---|---|
| cron share of agent calls | **74%** | the scheduler, not the human, was the customer |
| model turns per scheduled run | **~23 avg** | each "one" job was 23 billed round-trips |
| runs pinned at the turn ceiling | **13% of runs → 34% of calls** | a small tail of runaways dominated |
| per-call overhead, unscoped vs scoped toolsets | **24,680 → 6,394 tokens** | 74% of every call was capability the job never used |
| generated artifacts never opened | **67 files, atime == mtime** | output nobody consumed, billed daily |

That last row is the cheapest audit in this document. **Compare access time to modification
time on anything an agent generates on a schedule.** If they are identical, the artifact has
been written and never read, and you are paying a model to talk to a disk.

---

## Anti-Patterns

- **Theorising before grepping.** Law 1. The invoice names the model. The model names the system.
- **Trusting a cost dashboard built on your own price table.** If the table has `0/0` rows, the dashboard is a confidence generator, not a measurement.
- **Migrating load to a "flat-rate" plan without reading its overflow policy.** Law 7. A plan with auto-recharge and a $30/month grant cannot absorb a $700/month workload; it will simply bill you differently.
- **Assuming per-call overhead belongs to the vendor you just adopted.** Measured: the overhead was the *host runtime* loading every toolset and 88 skills, not the new provider. The same trivial prompt cost 24,680 tokens through the runtime and 6,945 through the vendor CLI directly.
- **Capping turns to control a runaway.** A truncated run wastes every turn it spent and delivers nothing. Fix why it loops; a cap only bounds the blast radius.
- **Pausing a job without mapping what reads its output.** Generators sit upstream of briefings and syncs. Pause the leaf nodes; the roots need a product decision.
- **Deleting a key before proving which project minted it.** A decommission removed the project that had issued the app's API key. The app broke silently; the *other* system's key survived and kept billing.

---

## The trap, stated plainly

Every individual decision here was reasonable when it was made. A default model was set
once and never revisited. A preview model was added to a catalog before pricing existed, so
it got `0/0` as a placeholder. Jobs were scheduled one at a time, each cheap in isolation.
A subscription was purchased and its provider left unconfigured because the metered key
already worked.

**None of these is a bug. Together they are a bill.**

The failure mode is not carelessness — it is that **cost is the only system property with no
natural feedback signal.** Latency you feel. Errors page you. Wrong output embarrasses you.
Spend accumulates in silence for thirty days and then arrives as a single number with no
stack trace.

The remedy is to give it a feedback signal on purpose: a usage ledger written from the call
sites that already hold the token counts, a daily ceiling that fails closed on the most
expensive lane first, and unpriced models reported as **unknown** rather than as zero.

---

## Provenance

Derived from a live investigation of a $1,234.06 / 30-day inference bill spanning an agent
runtime and a web application, 2026-08-13. Every figure was measured against the runtime's
own usage database and the deployed bundle.

Two of the investigation's own conclusions were overturned mid-flight and are recorded here
rather than quietly dropped:

- **The first mechanism was wrong.** Scheduled-job cost was attributed to a session-attachment
  setting believed to re-send accumulated history. Reading the scheduler source showed the
  setting mirrors output into a chat and does nothing of the kind, and only one job had it
  set. The *conclusion* (cron dominates) survived; the *mechanism* did not. Law 1 exists
  because the corrected version was found by reading source, not by reasoning about it.
- **The overhead was blamed on the wrong layer.** A 24,680-token per-call overhead was
  attributed to the newly-adopted vendor's skill context, and trimming it was recommended.
  Direct measurement showed the vendor's own CLI cost 6,945 tokens for the same prompt, and
  that scoping the *host runtime's* toolsets cut the call to 6,394. The recommendation would
  have produced no saving at all.

If an audit never overturns one of its own findings, it probably stopped measuring once it
found a story it liked.
