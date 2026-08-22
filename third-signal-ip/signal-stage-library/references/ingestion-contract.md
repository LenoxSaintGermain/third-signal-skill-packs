# Signal Stage ingestion contract

## Contents

1. Contract layers
2. Required top-level fields
3. Asset records
4. Runtime records
5. State machine
6. Approval and mutation rules
7. Minimal directed example

## 1. Contract layers

The ingestion spec is the stable handoff between an IP production workflow and Signal Stage. It separates:

1. **Source truth** — what was observed, where it came from, which file bytes are authoritative, and which originals still need recovery.
2. **Editorial policy** — canon, privacy, text ownership, and allowed derivative operations.
3. **Direction** — beats, crops, anchors, cues, motion, and reduced-motion behavior.
4. **Runtime output** — a Signal Stage story manifest and copied browser assets.

The current schema identifier is:

```json
"third-signal/signal-stage-ingestion/v1"
```

The packager emits a current reader manifest with:

```json
"third-signal/signal-stage/v1"
```

The packaged `public/` subtree is merge-ready for a Signal Stage site's public directory:

```text
public/library/<story-id>/story.json
public/library/<story-id>/assets/*
```

Keep `ingestion.json`, `provenance.json`, and `source/` outside the deployed public subtree because they contain private source paths and approval evidence.

## 2. Required top-level fields

```text
schema
package
approval
policy
assets
runtime
gates
state
blockers
```

`package` identifies the source story. `approval` records the actual approval state and evidence. `policy` controls mutation and text ownership. `assets` is the complete provenance registry. `runtime` is the directed story. `gates` records machine-checkable results.

For conversation-born material, preserve `source_conversations`, Asset DNA, lineage, binary availability, asset approval, and canon state from the source package. See [conversation-source-packages.md](conversation-source-packages.md).

## 3. Asset records

Every locally available file record uses:

```json
{
  "id": "text-free-master",
  "asset_dna_id": "WIND_ASSET_0001",
  "role": "text-free-master",
  "source_path": "/absolute/source/path.png",
  "filename": "source-path.png",
  "mime": "image/png",
  "width": 2135,
  "height": 460,
  "bytes": 1899313,
  "sha256": "...",
  "status": "passed",
  "binary_state": "verified-local",
  "approval_state": "approved",
  "canon_state": "locked",
  "contains_lettering": false,
  "release_eligible": true,
  "immutable": true
}
```

Rules:

- Keep absolute source paths in the private ingestion spec; the packaged runtime manifest contains only browser paths.
- Never substitute a preview, screenshot, historical runtime path, or internal file ID for original bytes.
- Preserve observed origin and lineage fields. Unknown parentage remains unknown.
- Record rejected and superseded files for provenance, but set `release_eligible` to `false`.
- Never select `phone-qa-*`, `rejected-candidate`, prompt records, or QA reports as runtime art.
- Prefer a clean reader derivative or text-free master for `dynamic` text.
- Preserve a baked-text WIND spread only under `hybrid` or `baked-editorial`.

## 4. Runtime records

`runtime.story` carries the story header and direction profile. `runtime.beats` contains the experience.

Each beat must contain:

```text
id, order, scene, pages, title, mode, lock, scroll_screens,
asset_id, alt, motion, desktop, mobile, shots, anchors, cues,
direction, reduced_motion
```

Supported modes:

```text
focus, sequence, stage, mosaic, drift, break
```

Supported motion classes:

```text
ambient, narrative, editorial, silence
```

Anchors use percentages relative to the approved image:

```json
{
  "id": "hero-face",
  "label": "Hero face",
  "x": 34,
  "y": 42,
  "mobile_x": 50,
  "mobile_y": 40,
  "safe_radius": 10
}
```

Cues must reference an anchor in the same beat. Valid trigger progress is `0.0–1.0`. Cue order should rise with trigger progress.

The current reader expects this audio compatibility shape. Leave it off by default unless the property profile explicitly supports it:

```json
{
  "id": "ambient-disabled",
  "label": "Ambient sound",
  "type": "generated-rain",
  "default_on": false
}
```

## 5. State machine

```text
blocked
  └─ resolve source/approval/integrity blockers
ready-for-direction
  └─ author complete runtime beats
production-ready
  └─ package and validate
packaged
```

Do not collapse `ready-for-direction` into `production-ready`. Approved art can be ready for ingestion while its performance design remains unfinished.

## 6. Approval and mutation rules

- `approval.state` must be `approved`, `finalized`, or `locked` for production.
- `approval.evidence` must name an approval artifact, user instruction, or canonical manifest field.
- A post-package approval must identify the selected inventory or Asset DNA IDs. Apply the approval as an ingestion overlay; do not rewrite the immutable source-package snapshot or promote every observed asset.
- `policy.approved_pixels_immutable` must be `true`.
- `policy.derivatives_only` must be `true`.
- `policy.allow_generation` must be `false`.
- `policy.text` must be `dynamic`, `hybrid`, or `baked-editorial`.
- Packaging may copy and mechanically encode an image. It may not erase, repaint, outpaint, recomposite, or redraw it.

## 7. Minimal directed example

```json
{
  "runtime": {
    "story": {
      "id": "wind-seventeen-seconds",
      "title": "WIND",
      "chapter": "Spread 01 · Seventeen Seconds",
      "subtitle": "The first event the world noticed.",
      "credit": "A Third Signal production",
      "profile": {
        "id": "wind",
        "label": "Forensic pressure",
        "accent": "#d7b56d",
        "surface": "#07090a",
        "text": "#f0eadf",
        "motion_doctrine": "Observation before explanation; evidence activates only when the reader reaches it."
      },
      "audio": {
        "id": "ambient-disabled",
        "label": "Ambient sound",
        "type": "generated-rain",
        "default_on": false
      }
    },
    "beats": [
      {
        "id": "seventeen-seconds",
        "order": 1,
        "scene": "Goma livestream",
        "pages": "Spread 01",
        "title": "Seventeen Seconds",
        "mode": "mosaic",
        "lock": "locked",
        "scroll_screens": 2.8,
        "asset_id": "wind-spread-master",
        "alt": "A livestream and forensic frames reveal an ordinary rider becoming impossible to move.",
        "motion": {"dominant": "editorial", "ambient": [], "intensity": 1},
        "desktop": {"object_position": "50% 50%", "start_scale": 1.0, "end_scale": 1.04},
        "mobile": {"object_position": "20% 50%", "start_scale": 1.12, "end_scale": 1.22},
        "shots": [
          {"id": "live", "label": "The livestream", "object_position": "18% 50%", "mobile_position": "18% 50%", "function": "establish public evidence"},
          {"id": "foot", "label": "The foot", "object_position": "50% 50%", "mobile_position": "50% 50%", "function": "isolate the anomaly"}
        ],
        "anchors": [
          {"id": "rider", "label": "Delivery rider", "x": 20, "y": 50, "mobile_x": 50, "mobile_y": 45, "safe_radius": 12}
        ],
        "cues": [],
        "direction": "Begin as evidence, not spectacle; activate the forensic frames after the livestream holds.",
        "reduced_motion": "Use the static spread with a moving focus border."
      }
    ]
  }
}
```
