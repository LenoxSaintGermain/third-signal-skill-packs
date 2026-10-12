---
name: ip-to-signal-stage
description: Produce an original IP as a finished graphic novel and integrate it into the Signal Stage graphic-novel harness, including directed beats, immutable art, validated library packaging, browser QA and verified deployment. Use for concept-to-Signal-Stage runs or adapting existing approved comic assets into that harness.
---

# IP to Signal Stage

This is the Signal Stage route of `$ip-to-production`, not an alternative art generator or a new reader invented from scratch.

## Start from the shared run

Read `../ip-to-production/SKILL.md` and its checkpoint contract. Resolve that sibling in the publishing workspace if the installed skill paths are not adjacent. Set route to `signal-stage` (or `both` when requested). Run shared source, cast, script, art and source-acceptance stages as needed. For existing accepted art, verify it and reuse it; do not regenerate it solely to fit the harness.

Then invoke `$signal-stage-library` and read its `references/ingestion-contract.md`. Use its actual current scripts/schema. Record direct owner authority or explicitly delegated acceptance and exact selected asset IDs; never infer that approval covers every recovered artifact. Production authority already supplied in the current task is valid evidence and should not prompt redundant approval requests.

## Locate the real graphic-novel harness

Find the actual Signal Stage repository and its current graphic-novel reader, library index, package loader, manifest schema, build commands and deployment identity. Record paths and source revision in RUN.json. Inspect a working entry and its rendered behavior before extending the library. The ingestion packager is not the runtime harness. A design plan is not proof of an implemented harness.

Use an isolated checkout/output directory where needed, preserve unrelated changes, and keep existing library entries intact. Prefer compatible library ingestion over forking the reader. If a dedicated site is requested, reuse the verified harness in a new project with this IP's own identity. If the harness cannot be located or accessed, finish the validated package and record the integration blocker; do not silently substitute a static gallery or claim the requested experience exists.

## Ingest and direct

- Preserve accepted pixels, geometry and wording. Visual repairs return to upstream art production as a new version; ingestion performs only permitted mechanical derivatives and direction.
- Capture stable Asset DNA, lineage, dimensions and hashes. Use `capture_at_creation.py` for new-generation capture when applicable, following its documented contract.
- Select `dynamic` only for an accepted text-free master; use `hybrid` or `baked-editorial` for accepted embedded text. Avoid duplicating baked dialogue with runtime cues.
- Generate ingestion with the resolved `signal-stage-library/scripts/signal_stage_library.py` command and its documented arguments. Keep approval evidence explicit; inspect `--help` if the installed interface differs.
- Direct the story in beats. Preserve page/panel reveal order and narrative jobs. Supported contract modes include focus, sequence, stage, mosaic, drift and break; verify current runtime compatibility. Define anchors, safe radii, desktop/mobile crops, shots where needed, cue timing, dominant motion and reduced-motion behavior. Do not reveal a later panel early just to animate it.
- Run the library validator with `--production-ready`; resolve errors and document warning judgments. Package to a new versioned directory. A valid library pack is an intermediate deliverable.

## Integrate and deploy

Merge the generated `public/library/<story-id>/` subtree into the verified harness using its actual library-index convention. Keep `source/`, `ingestion.json`, `provenance.json`, private paths and approval records outside the public bundle. Preserve existing stories and unique IDs. If an adapter is needed, keep the source package unchanged, document the mapping and validate the resulting runtime contract.

Build and inspect the actual experience on desktop and phone. Verify entry from the library, complete beat progression, anchors/crops, cue legibility, no doubled dialogue, chapter navigation, reduced motion and a readable static/transcript alternative. Test the implemented controls and record actual viewports; do not equate schema validation with visual QA.

Deploy through the available authorized provider and verify the live story route as well as the library entry. Honor recorded private/public scope. Record source revision, package hashes, deployment ID/URL, browser evidence and limitations. Archive the package and log the ship through the shared production workflow.

Done means a complete comic, validated directed package, and verified working Signal Stage graphic-novel experience at the intended live destination. If only packaging succeeded, report packaged—not deployed.
