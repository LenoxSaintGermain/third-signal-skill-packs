---
name: poc-harness
description: Build or iterate a single-file clickable POC bundle that is backend-aware (per-screen API status and data labels), compares against a live app when one exists, and carries a built-in per-screen feedback harness whose export feeds the next iteration. Use when a product idea needs to be shown, reviewed screen by screen, and turned into issues, or when asked for a POC, clickable prototype, investor/owner review build, or "run the POC harness".
---

# poc-harness

Status: **skeleton, not yet validated.** Derived from the Signal Hunter POC (`signal-hunter-poc.html`). Evidence and defects: `docs/poc-harness/NOTES.md` in million-hunter-dashboard. Portable task for other agents: `docs/poc-harness/TASK.md`. Nothing here has been run end to end yet; the template build and scripts are listed as TODO.

## When to use
- A new idea needs a reviewable prototype with honest backend status.
- An existing live app needs a redesign reviewed as a diff against reality.
- A reviewer's per-screen feedback must come back in a form an agent can ingest.

Not for: production UI work, or demos that need live API calls.

## Inputs
Candidate block from `TASK.md` (idea, audience, live app URL or none, existing backend, known screens).

## Workflow
1. **Frame.** Fill the candidate block. If a live app exists, capture its screens read-only and stamp the capture date (`capture` step, TODO script). If not, say so in `BUILD.md`.
2. **Contract first.** Write `screens.json` (id, group, title, intent, api status, endpoint, dataLabel, liveCapture) validated by `contracts/screens.schema.json`. Generate `api-map.md` from it.
3. **Build.** One `poc.html`. Screen IDs, feedback chip on every screen, index, walkthrough (about 75 s, 5 steps), at least four rule-showing infographics, motion contract, tokens. Compare screen if a live app exists.
4. **Lint.** Fail on: screen without ID or API tag; numeric without a data label; any runtime network use; motion without a reduced-motion guard; blank-region risk (see below). (`lint` script TODO.)
5. **Verify.** Run the checklist in `TASK.md` for real: serve over localhost, walk every screen, export feedback, reduced-motion and 375 px passes. Report only what you ran.
6. **Review loop.** Reviewer uses the chip, exports `feedback.json`. Validate against `contracts/feedback.schema.json`. Turn each `changes` item into one issue per screen ID (see Third Signal Linear OS: docs = operating model, issues = one concrete change, comments = ship log). Revise, rebuild, new build id.

## Hard rules
1. Zero runtime network.
2. Every number labelled `LIVE · CAPTURED <date>`, `EXAMPLE DATA`, or `MOCK`. No fabricated customers, quotes, logos, metrics.
3. Every screen: stable ID, title, intent line, API status, endpoint.
4. No secrets in the bundle.
5. Label gaps honestly; never paper over one to look finished.
6. Live app exists means Compare screen is required.

## Motion contract
150-600 ms, `cubic-bezier(0.16, 1, 0.3, 1)`, CSS opacity/transform only, never blocks input, plays only on route change, 45 ms stagger capped at 540 ms in reading order, count-ups for hero numbers, one shared `[data-tip]` tooltip (hover, focus, tap, Esc), scrubbable charts, all off under `prefers-reduced-motion`.

## Known template defect to design out
In the source POC, blocks animate with `animation: rise ... both` and a per-block delay, so they sit at opacity 0 until the delay passes. In a narrow or throttled viewer this showed as about 500 px of blank space (Home) and an empty Compare page until interaction. Not reproduced at desktop width; cause unverified. Mitigation to test: start blocks visible and animate only transform, or cap delay and drop `both` fill, and include a 375 px foreground check in lint/verify.

## TODO (not built yet)
- `template/` source split (index.html, tokens.css, motion.js, viz.js, harness.js) and `build.mjs` emitting single-file `poc.html`.
- `scripts/capture.mjs`, `scripts/lint.mjs`, `scripts/ingest-feedback.mjs`.
- `references/` (motion, infographic patterns, tokens) distilled from NOTES.md.
- Validate by giving a fresh agent only this file plus a 3-screen `screens.json`.
