# Conversation source packages

## Contents

1. Purpose
2. Three independent state axes
3. Required artifacts
4. Asset DNA and lineage
5. Recovery rules
6. Capture-at-creation rule
7. Handoff boundary

## 1. Purpose

A creative conversation is evidence, not a durable asset repository. It may expose text, a rendered preview, an attachment reference, a temporary runtime path, or an internal file ID while withholding the original binary.

Build a recoverable source graph before Signal Stage ingestion. Preserve what is known, label what is inferred, and never regenerate a missing original merely to make a package look complete.

## 2. Three independent state axes

Record all three for every asset.

### Binary availability

- `verified-local`: original bytes exist at a verified local path and can be hashed.
- `downloadable`: an actual downloadable artifact is available.
- `preview-only`: a rendered chat preview is visible but original bytes are unavailable.
- `known-runtime-reference`: a historical path or file ID is known but not currently readable.
- `needs-export`: the original is believed to exist but must be recovered from its source system.
- `missing`: no usable binary or recovery handle is available.

### Approval

- `locked`, `finalized`, `approved`, `pending`, `rejected`, or `superseded`.

### Canon

- `locked`, `provisional`, `proposed`, `rejected`, `superseded`, or `not-applicable`.

Never infer one axis from another. A canon idea may have no approved visual. An approved concept image may be non-canon. A local file may still be rejected.

## 3. Required artifacts

For a thread-derived package, produce:

```text
00_PACKAGE_INDEX.md
01_IP_CANON_SNAPSHOT.md
02_DECISION_LEDGER.md
03_ASSET_INVENTORY.json
04_ASSET_LINEAGE.json
05_PROMPT_AND_GENERATION_LEDGER.md
06_RECOVERY_QUEUE.md
07_PRODUCTION_READINESS.md
08_PRODUCT_IDEAS_FOR_ASSET_OS.md  # only when the thread contains workflow/product concepts
```

Keep product/process ideas separate from story canon.

If the destination is writable, materialize the files and verify their paths. Otherwise return copy-ready contents or a real downloadable archive. Do not claim an export based only on a chat response.

## 4. Asset DNA and lineage

Assign each observed asset an immutable identifier such as `WITCH_ASSET_0001`. Never reuse an ID for regenerated or visually similar bytes.

Each inventory record should retain, when observed:

```json
{
  "id": "witch-character-sheet-0001",
  "asset_dna_id": "WITCH_ASSET_0001",
  "role": "character-design-sheet",
  "original_filename": "example.png",
  "binary_state": "needs-export",
  "approval_state": "pending",
  "canon_state": "provisional",
  "release_eligible": false,
  "origin": {
    "conversation_id": "...",
    "turn_id": null,
    "tool": "image generation",
    "file_id": null,
    "runtime_path": null
  },
  "lineage": {
    "parents": [],
    "relationships": []
  }
}
```

Allowed observed relationships include `generated-from-prompt`, `edited-from`, `derived-into`, `supersedes`, and `used-in`. Use `null`, `unknown`, or an empty list when evidence is absent.

## 5. Recovery rules

- Preserve original filenames and handles verbatim.
- Treat `/mnt/data/...` and similar paths as historical references unless readable now.
- Treat internal file IDs as recovery handles, not local files.
- Do not hash, dimension, or mark `verified-local` without actual bytes.
- Do not upscale, redraw, or screenshot a preview to impersonate the original.
- Keep rejected and superseded assets in the graph and outside release directories.
- Record exact prompts only when they appear verbatim; label all summaries as reconstructed.

## 6. Capture-at-creation rule

When an agent generates or receives a creative asset and the user has authorized a project destination, capture before the turn ends:

1. Original binary and original filename.
2. SHA-256, byte count, MIME type, and dimensions.
3. Conversation and turn IDs when available.
4. Exact prompt, model/tool, references, and seed only when exposed.
5. Asset DNA ID, parent IDs, approval state, and canon state.
6. A manifest entry even when the asset is rejected.

This is the durable thread-to-vault boundary. Later recovery is a fallback, not the primary workflow.

## 7. Handoff boundary

A conversation source package may advance to Signal Stage inspection only when at least one release candidate is `verified-local` or genuinely `downloadable`, its checksum can be recorded, and approval evidence exists.

Otherwise report `blocked-pre-ingestion`, preserve the recovery queue, and stop before runtime direction or publication.
