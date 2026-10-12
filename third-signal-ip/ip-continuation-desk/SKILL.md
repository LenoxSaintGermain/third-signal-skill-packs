---
name: ip-continuation-desk
description: Resume any Signal IP from any session or production stage. Reconstruct what is complete, pending, blocked, approved, superseded, or missing from canon dossiers, source threads, story packs, production reviews, checkpoints, manifests, assets, and publishing records; then return one clear next action and a weekly IP-library state summary.
---

# IP Continuation Desk

The IP Continuation Desk is the resume layer for Signal Publishing. It answers:

> What is this IP, where did we leave it, what is actually complete, what is still pending, and what should happen next?

It is an evidence-retrieval and handoff skill. It does not silently invent canon, mark work complete because a file exists, or treat a polished draft as approved.

## Invoke automatically when

Use this skill when the user says or implies:

- resume, continue, pick up, where did we leave off, what did we finish, what is pending, or what should I do next;
- kick off an IP, chapter, graphic-novel MVP, panel-spread run, visual-development sequence, or production pass;
- recap a session, recover work from another session, audit an IP, or prepare a weekly library report;
- compare active IPs, identify blockers, find the next approved artifact, or prepare a handoff.

Always invoke it before continuing an IP whose context is not fully present in the current conversation.

## Dependencies

For creative continuation, invoke `$signal-recipe-engine` first. Use [the publishing pipeline profile](../signal-recipe-engine/references/publishing-pipeline.md) to select the recipe and preserve the recipe handoff.

For Third Signal work, use the default Method shape: identify the surface, choose the durable artifact, and return observable evidence, remaining risk, and one next action.

## Evidence hierarchy

Read evidence in this order. A lower-ranked source may explain a higher-ranked one but cannot silently override it.

1. Explicit user decisions, approvals, locks, and release authority in the current or source session.
2. Canonical IP dossiers under `ip/<slug>/`.
3. Approved/finalized production handoffs, story-pack manifests, QA reviews, continuity ledgers, and release records.
4. Checkpoints, daily scoreboards, remaining-candidate files, and dated editorial notes.
5. Finalized dispatches and published reader/library manifests.
6. Source threads and attachments, when a thread reader or connected source is available.
7. Drafts, exploratory notes, rejected work, superseded artifacts, and filenames.

Filenames and folder placement are discovery hints only. Approval, canon, publication, and completion require evidence.

## State vocabulary

Use the controlled vocabulary in [state-schema.md](references/state-schema.md):

- `not-started`
- `in-progress`
- `awaiting-approval`
- `blocked`
- `approved`
- `finalized`
- `published`
- `superseded`

Keep three kinds of truth separate:

- **Complete:** an artifact or gate has explicit evidence of completion.
- **Pending:** the next required step is known but not complete.
- **Unknown:** the evidence needed to decide is missing or contradictory.

Unknown is not the same as pending, and pending is not the same as blocked.

## Continuation run

### 1. Identify the IP

Resolve the user's reference to one IP, series, chapter, or production package. Search `ip/`, `series/`, `source/`, `assets/`, and `outputs/`. If multiple candidates match, show the ambiguity and select the strongest evidence-backed match.

For a new or absent IP, create a provisional identity only. Do not create canon until a source dossier or explicit user lock exists.

### 2. Locate the last durable state

Find the most recent relevant evidence by meaning, not only modification time:

- canon dossier or README;
- latest dated checkpoint or scoreboard;
- latest approved development, production, lettering, QA, or release handoff;
- story-pack, export, ingestion, or publication manifest;
- pending/rejected/superseded record;
- asset/provenance record and missing-binary queue state;
- source-thread ID and session-specific decisions.

### 3. Build the evidence ledger

For every meaningful workstream, record:

| Workstream | State | Evidence | What is complete | What is pending | Blocker/risk |
|---|---|---|---|---|---|
| Canon/lore |  |  |  |  |  |
| Characters/world/system |  |  |  |  |  |
| Chapter/spine/panel plan |  |  |  |  |  |
| Art/source package |  |  |  |  |  |
| Lettering/text policy |  |  |  |  |  |
| QA/continuity |  |  |  |  |  |
| Runtime/library |  |  |  |  |  |
| Publication/archive |  |  |  |  |  |

Do not collapse a finished upstream stage into a finished downstream stage. Approved art is not a published story; a story pack is not a Signal Stage package; a finalized draft is not automatically canon.

### 4. Reconcile conflicts

When records disagree:

1. prefer explicit approval or lock over inference;
2. prefer the latest explicit state within the same authority level;
3. preserve the older state as superseded evidence;
4. report the contradiction instead of silently repairing it;
5. ask for a decision only when the contradiction changes the next action.

### 5. Return the resume brief

Use this order:

```text
IP / surface:
Current phase:
Overall state:
Last confirmed movement:

Completed:
- ...

Pending:
- ...

Blocked or unknown:
- ...

Evidence:
- [file or source] — [what it proves]

Recipe for the next move:
- primary:
- secondary:
- narrative job:

Next best action:
1. ...

Remaining risk:
- ...
```

The next best action must be singular, concrete, and observable. For example: “Draft the Chapter One page/spread spine from the approved lore dossier and mark new witchcraft rules as proposed,” not “continue developing the world.”

## Witches MVP continuation profile

When the user says “resume the witches MVP,” “start the witches graphic novel,” or similar:

1. Search for the witches dossier, source session, prior chapter outline, visual rules, character/faction notes, and any approved assets.
2. If the IP is not yet present in the publishing vault, state that clearly and build a source-bound intake brief rather than pretending prior work is available.
3. Invoke `$signal-recipe-engine` with **Sequential Reveal** as the likely primary recipe, **Situation-Forced Design** as the secondary recipe, and **Constraint-Bearing System** only where witchcraft rules must be dramatized.
4. Produce the Chapter One continuation brief: confirmed canon, proposed extensions, unresolved questions, chapter job, page/spread spine, panel jobs, text/lettering policy, and next handoff.
5. Do not generate final art until the source boundary, panel geometry, continuity anchors, and production authorization are explicit.

## Weekly IP-library report

The weekly report is a read-first operating summary, not a canon mutation. It should cover every active, recovered, or recently changed IP and include:

- current phase and state;
- movement since the previous report;
- completed gates;
- pending gates;
- blockers and missing evidence;
- approved, available-local, needs-export, superseded, and rejected assets;
- active recipe and next recommended action;
- changes to canon, proposed lore, and unresolved questions;
- one practical schedule for the coming week;
- one risk that could derail the next milestone.

Write the report to `reports/ip-library/weekly/YYYY-MM-DD.md` when the user authorizes a durable report. If the scheduler or report directory is unavailable, return the same report inline and state the gap once.

Recommended cadence: Monday morning after the daily publishing sync. The schedule is recorded in `AUTOMATION.md`.

## Safety and boundaries

- Read broadly; write only when the user requests a durable report, ledger update, or continuation artifact.
- Never promote proposed, inferred, rejected, superseded, or generated details to canon.
- Never infer approval from `final`, `v1`, timestamps, or a polished appearance.
- Never fabricate missing links, asset bytes, source sessions, or publication state.
- Preserve private IP boundaries and report unavailable connectors.
- End with one next action and the evidence that makes it the right next action.
