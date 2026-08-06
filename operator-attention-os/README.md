# Operator Attention OS

**Status**: 🟢 PRODUCTION
**Version**: 1.0.0
**Category**: Multi-Agent Interface Architecture

---

## Overview

Every agent dashboard is built on the same unexamined assumption: that showing the operator
more of what the agents are doing helps them stay in control. It does the opposite, and it
fails predictably at the exact moment the system becomes worth running — when there are
enough agents that watching them is no longer possible.

**The Problem**: agent activity scales with agent count. Operator attention does not. A
surface that renders activity uniformly spends a fixed budget on a growing pile, and past
some threshold the operator stops reading entirely. They do not announce this. They keep
the dashboard open, glance at it, and quietly stop trusting it — which is worse than not
having one, because the organisation still believes someone is watching.

**The Solution**: treat **operator attention as the scarce resource** and architect the
interface as a budget over it. Not compute, not context window, not tokens — attention.
Everything below follows from taking that seriously.

**North star**:

> The human should only ever see the queue of things that need a human, and everything else
> should be one deliberate step away — never zero steps away by default.

---

## The Six Laws

| # | Law | The pattern it rejects |
|---|-----|------------------------|
| **1** | **Attention Budget** — attention is the scarce resource, so spend it deliberately | "Show everything, let the operator filter." Filtering is work, and it is work that scales with agent count while the operator does not. |
| **2** | **Signals are not decisions** — consolidate raw events into things a human can *decide* | A feed of raw agent events. An operator's job is deciding, not triaging. Recurring proposals belong in one batch review, not N cards. |
| **3** | **Processes, not cards** — everything has a lifecycle, and resolution shows a **transition** | Items that silently vanish when resolved. Silence is the characteristic failure of agent systems; work that quietly didn't happen looks identical to work that did. |
| **4** | **One spine** — a single computed queue that every surface *reads* | Each view computing its own priority. N surfaces means N sources of truth, and they drift. One spine means the interface cannot disagree with itself. |
| **5** | **Deliberate depth** — non-urgent things are one intentional step away, never zero | The persistent side panel. Anything permanently on screen is permanently spending budget, whether or not it is needed right now. |
| **6** | **Bounded escape hatch** — "browse all" is opt-in and finite | An endless default grid. An unbounded default is an admission that the ranking was never trusted. |

> **Laws 1 and 3 are in tension, and the tension is the design.** Attention budget pushes
> toward showing less; visible transitions push toward showing *change* — including the
> change of something leaving. Resolve it by spending budget on **state transitions** rather
> than on **state**. A resolved item earns a moment of the operator's attention exactly
> once, then stops costing anything.

---

## Skillpack Signatures

| Skill | Trigger | Description |
|-------|---------|-------------|
| **Attention Audit** | "Why does nobody look at the dashboard?" | Measures how much of the surface is state vs. decisions, and what fraction of rendered items ever required a human. |
| **Signal Consolidation** | "We have too many cards" | Collapses raw agent events into decidable units; groups recurring proposals into batch reviews. |
| **Lifecycle Mapping** | "What states can this be in?" | Derives the process state machine and identifies which transitions are currently invisible. |
| **Spine Extraction** | "Which view is right?" | Finds surfaces computing independent priority and collapses them onto one computed queue. |

---

## The consolidation test

The cheapest diagnostic for whether a surface respects Law 2:

> Count the items on screen. Now count how many of them a human must **decide** something
> about. If the second number is much smaller than the first, the surface is spending
> attention on state rather than on decisions.

A production application of this pass took **35 raw signals to 25 operator decisions** and
removed a 38-item default wall, replacing it with bounded categories — gates, decisions,
review batches, anomalies — each carrying a count. Recurring proposals collapsed into batch
reviews rather than repeating.

The result is not a smaller dashboard. It is a dashboard where the number on screen means
something, because every item on it is a thing awaiting a person.

---

## Anti-Patterns

- **The comprehensive dashboard.** Completeness is the wrong goal. A surface that shows everything has made no decisions on the operator's behalf, which is the entire job.
- **Silent resolution.** An item that disappears without a transition teaches the operator that the surface is not trustworthy — they cannot distinguish "handled" from "lost."
- **Parallel priority.** Two views ranking the same items by their own logic will disagree, and the operator will learn to check both. You have now doubled the cost of the thing you were trying to reduce.
- **The permanent panel.** Persistent chrome is a standing charge against the budget. Make it summonable.
- **Notification-per-event.** One event, one alert is Law 2 failing at the notification layer instead of the visual one. Batch by decision, not by occurrence.
- **Screenshot-verified behaviour.** Laws 3 and 4 are behavioural claims. A screenshot cannot prove a transition animated or that two surfaces read one spine — those need contract tests.

---

## On verification

Most of these laws are invisible in a screenshot, which is why an attention-first interface
needs **contract verification rather than visual review**: assertions that resolution emits
a transition, that every surface reads the shared queue object, that a category's count
matches its contents, that the default view stays bounded.

The rule that makes it worth anything: **a check that cannot run must fail loudly, never
silently pass.** A skipped assertion reported as a pass is the same failure mode as a
silently resolved card — it teaches you to trust something that isn't reporting.

---

## Provenance

Derived from a production operator cockpit for agentic swarms. The laws are the governing
charter of that system, extracted here without implementation. Every one of them was
adopted after the pattern it rejects had already been built and found wanting.
