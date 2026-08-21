---
name: signal-stage-library
description: Ingest approved or finalized visual-story assets—especially WIND spreads and Signal Comics story packs—into a validated Signal Stage library package. Use when Codex needs to audit asset approval and provenance, convert a final art package into a Signal Stage ingestion spec, design beat/shot/anchor/cue metadata, prepare immutable runtime derivatives, validate a story manifest, or hand off assets to the Signal Stage reader without regenerating approved art.
---

# Signal Stage Library

Treat ingestion and production as separate gates:

`approved source package → ingestion spec → directed runtime spec → library pack`

Never turn an asset into a runtime scene merely because a file exists. Approval, identity, integrity, and direction are separate facts.

## Core law

Preserve approved pixels. Generate only derivatives, crops, metadata, and runtime choreography. Do not redraw, AI-unletter, clean up, extend, or repair approved art during ingestion.

If the source needs visual repair, stop and return it to its originating production workflow.

## Workflow

### 1. Establish the source boundary

Find the controlling approval record, Story Pack manifest, final asset directory, and narrative source. Prefer the manifest over filenames. Do not infer approval from `v1`, `final`, a recent modification date, or placement in an approved-looking folder. If the asset package has no manifest, author one from [references/source-package-template.json](references/source-package-template.json) using only observed facts; leave approval pending until evidence exists.

Require:

- explicit package approval or finalization evidence;
- one locally available release image;
- source path, dimensions, byte size, and SHA-256;
- text policy: `dynamic`, `hybrid`, or `baked-editorial`;
- a clear canonical/private/release boundary.

Read [references/ingestion-contract.md](references/ingestion-contract.md) before authoring or editing an ingestion spec. For WIND, also read [references/wind-profile.md](references/wind-profile.md).

### 2. Inspect without mutating

Run:

```bash
python3 scripts/signal_stage_library.py inspect \
  --source /absolute/path/to/story-pack-manifest.md \
  --property wind \
  --output /absolute/path/to/<story-id>-signal-stage-ingestion.json
```

Use `--asset-root` only when manifest paths are relative to a different verified root. Use `--approval approved|finalized|locked` only when the user or a named approval artifact supplies that state. Record the evidence with `--approval-evidence`.

The command may emit a blocked spec. That is useful: preserve its blockers rather than weakening the gate.

### 3. Choose the text policy

- `dynamic`: use an approved text-free master; put dialogue/captions in cues.
- `hybrid`: preserve approved diegetic/editorial text in the image; keep dialogue or performance copy in cues.
- `baked-editorial`: treat all approved typography as image content; use cues only for supplemental performance, never duplicate baked wording.

Never use a static lettered master as `dynamic`. Never remove baked text with a generative edit.

### 4. Direct the experience

Complete `runtime.story` and `runtime.beats` in the ingestion spec. The primitive is a beat, not a page.

For every beat, define:

- one of `focus`, `sequence`, `stage`, `mosaic`, `drift`, or `break`;
- the approved `asset_id`;
- desktop and mobile crop behavior;
- named focal anchors and safe radii;
- shots only when a guided sequence or mosaic needs them;
- cues anchored to named subjects or safe text zones;
- one dominant motion class;
- direction and reduced-motion behavior;
- lock state: art is normally `locked`; choreography may be `guided`.

Use mechanical crops of the approved image. Never invent off-canvas content. A mobile crop may omit an object only when that omission is intentional and documented.

### 5. Validate production readiness

Run:

```bash
python3 scripts/signal_stage_library.py validate \
  --spec /absolute/path/to/<story-id>-signal-stage-ingestion.json \
  --production-ready
```

Fix every error. Warnings require an explicit judgment in the handoff; do not silently ignore them.

### 6. Package the library entry

Run:

```bash
python3 scripts/signal_stage_library.py package \
  --spec /absolute/path/to/<story-id>-signal-stage-ingestion.json \
  --output /absolute/path/to/signal-stage-library/<story-id>-v1
```

The packager copies immutable sources into `source/`, creates a merge-ready public library subtree, resolves `asset_id` references, and emits:

- `ingestion.json`
- `provenance.json`
- `source/`
- `public/library/<story-id>/story.json`
- `public/library/<story-id>/assets/`

It refuses to overwrite an existing package. Create a new versioned output directory for revisions.

### 7. Integrate separately

Loading the package into a live reader, changing a site library index, deploying, publishing, assigning canon, or changing access is a separate authorization boundary. Do not infer those permissions from ingestion.

## Hard gates

Block production when any of these is true:

- approval evidence is absent or pending;
- the selected asset is rejected, superseded, a QA proof, or missing locally;
- a recorded checksum or dimension does not match the file;
- dynamic text is requested without a clean approved master;
- anchors refer to subjects outside the approved canvas;
- a cue references a missing anchor;
- mobile behavior depends on generative outpainting;
- rejected evidence is marked release-eligible;
- the source master would be overwritten;
- runtime copy contradicts approved wording or silently rewrites canon.

## Daily Desk lessons carried forward

- Lock panel geometry as structure. A four-panel strip cannot become stacked panels or a 2×2 page during preparation.
- Keep generated text out of clean masters. Use deterministic lettering or runtime cues.
- Track identity, background topology, prop custody, handedness, device orientation, and crop/occlusion state.
- Treat missing hands, duplicated props, pseudo-text, altered symbols, and identity drift as source-production failures—not runtime polish tasks.
- Keep phone proofs and rejected candidates as evidence only.
- Hash every accepted source and derivative.
- Preserve the release boundary. A valid pack is not automatically published.

## Handoff result

Report:

- ingestion state and any blockers;
- selected source master and text policy;
- beat/mode count;
- package path and manifest paths;
- validation result;
- actions intentionally not taken, such as deployment or canon assignment.
