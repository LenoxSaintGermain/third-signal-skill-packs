---
name: ip-to-production
description: Take an original IP concept or existing source package through cast development, finished illustrated comics, a standalone reader website, and verified deployment. Use for an end-to-end production run or resuming that run; route Signal Stage graphic-novel harness requests to ip-to-signal-stage.
---

# IP to Production

Own the complete production loop in one task. A plan, cast sheet, packaged story, or successful build is an intermediate result. Completion means the requested finished comic and reader are accessible at a verified deployment, with source and release evidence preserved.

## Resolve the run

Read [the checkpoint contract](references/run-contract.md). Establish IP name/slug, concept or source paths, audience, bounded first installment, fixed canon versus creative freedom, output route, deployment destination, and release audience. Infer routine choices and record them; ask only for missing decisions that materially block work. Do not impose a six-page pilot on an already specified chapter.

- **Standalone reader:** continue below and read [reader release](references/reader-release.md).
- **Signal Stage / graphic-novel harness:** invoke `$ip-to-signal-stage`; follow this skill's shared production stages, then its Stage integration route instead of the standalone reader.
- **Both:** share the selected source masters, but keep separate package, QA, deployment and release receipts.

Record actual user authority for creative decisions, source selection, deployment and public release. Prior authority in the active task remains valid; do not request it again. The skill itself grants no authority. Private preview is the default when the release audience is unspecified.

## Resolve dependencies

Locate the publishing workspace from the active project. Resolve companion skills from this pack's sibling directories first, then the workspace's `skills/` and installed skill directories. Read their actual SKILL.md files, not merely this list:

- `$signal-recipe-engine` and its `references/publishing-pipeline.md`: narrative method and handoff.
- `$ip-continuation-desk`: reconstruct existing IP and previous run evidence before extending it.
- `$wind`: only when new world/character visual development needs it.
- An image-generation adapter actually available in this runtime: inspect reference-image support and original-file export. In Codex, use `$imagegen`; in other runtimes use the approved native/provider tool and record its real name. No tool is bundled here.
- `$signal-ip-publishing`: provenance and requested archive/sync destinations.

Use the available Sites skill/tools for Sites deployments; discover their actual current instructions. Do not hardcode a model version, site ID, deployment command, credentials or another IP's runtime. Missing dependencies must be reported precisely while independent work continues.

For Third Signal work apply its shared playbooks and default Linear tracking with Studio as the primary surface. Read the design routing playbook and applicable DESIGN.md before building UI. Do not apply unrelated canvas/concierge architecture to a comic reader.

## Shared production stages

1. **Source and decisions.** Inspect actual source text and image bytes. Recover the last confirmed state. Hash selected originals and record source hierarchy, conflicts, missing assets, and confirmed/proposed/unknown details. For a concept-only IP, build a concise premise and working bible under the user's creative authority. Preserve historical canon and originals; an adaptation's new choices are explicit.
2. **Cast and visual continuity.** Establish recognizable identity, ages, relationships, silhouettes, costume/prop rules, palette and geography from the sources. Inspect references before image generation. Produce references for the cast needed by this installment, expression/action tests, and a shared scene. Record selected reference IDs. Translate stylistic references into visual traits. Keep this IP's voice and visual identity.
3. **Comic script.** Choose the recipe; define installment arc, page/spread composition, panel jobs, eye path, dialogue, silence, reveals and ending. Make a readable script before generating page art. Adapt for sequential storytelling rather than decorating prose.
4. **Art and lettering.** Generate original art using the verified image-generation adapter and inspected cast references. Capture actual output bytes and available generation metadata immediately. Inspect every page for continuity, anatomy, prop custody, geography, panel order and text defects. Repair with versioned candidates. Keep clean masters and editable deterministic lettering or approved runtime text policy. Never represent a prompt, contact sheet or placeholder as finished art.
5. **Source acceptance.** Select exact asset IDs after visual QA. Record who/what authorizes acceptance: direct owner selection or explicit delegated editorial authority plus agent QA. Do not invent owner review. Export full-resolution masters, web derivatives, accessible transcripts, scripts, prompts, SHA-256 manifests and QA evidence. Lock accepted masters before downstream integration.
6. **Route and release.** Run the selected reader route. Preserve its own completion criteria; packaging is not deployment. Resolve defects, verify the actual live reader and archive requested outputs with readback evidence.

At each stage update the checkpoint. Continue through already authorized stages without an approval ritual. When a source master changes, invalidate dependent lettering, hashes, packages and reader QA; rebuild those derivatives before release.

## Finish

Return the live URL, finished installment and cast package paths, observed browser checks, release receipt, and actual limitations. If blocked, identify the last completed stage and one concrete next action; do not label the entire run complete. Social posting and ongoing schedules are separate outputs and require their own user request.


## Optional trailer adaptation

When explicitly requested, adapt accepted cast and story assets through [Manus integration](../manus-integration/SKILL.md) or another verified provider. Record a distinct motion run with source hashes, timed shot plan, cost scope and playback QA. Keep proposed trailer choreography separate from canon and website/public release. Exporting footage does not transfer the source provider's editable project.
