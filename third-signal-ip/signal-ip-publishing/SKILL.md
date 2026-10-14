---
name: signal-ip-publishing
description: Archive creative source packages, accepted masters and release evidence with separate canon, availability and publication states. Portable edition for cross-agent IP production and verified repository or Drive delivery.
---

# Signal IP Publishing — portable edition

Read [the recipe handoff](../signal-recipe-engine/references/publishing-pipeline.md). This portable edition carries the archival contract; it does not install the owner's vault, browser session, Drive mount or harvesting infrastructure.

1. Resolve the user-authorized source package and destination. Inspect actual bytes and approval records. Keep raw research, rejected attempts, superseded art and accepted masters distinguishable. Do not infer canon or publication from filenames.
2. Build an append-only inventory: asset ID, relative path, byte size, SHA-256, dimensions, parent/reference IDs, tool/prompt metadata when actually exposed, binary availability, acceptance evidence, canon state and release eligibility. Unknown values stay unknown.
3. Capture new originals immediately with [capture_at_creation.py](../signal-stage-library/scripts/capture_at_creation.py). A screenshot is not an original. If an original is missing, save its observed source handle and recovery action in a recovery queue; do not fabricate bytes or claim recovery.
4. Preserve versioned source masters and mechanical delivery derivatives separately. Changed masters invalidate dependent hashes, packages and QA. Never overwrite or silently prune earlier evidence.
5. Verify repository identity and access audience before a scoped commit/push. Public skill repositories contain reusable workflows only; private IP, credentials, account identifiers and private source records belong in the authorized private destination.
6. For Drive, resolve the destination through its actual folder ID or a verified managed mount. A similarly named local mirror is not proof of cloud delivery. Check copied bytes with read-back hashes; record local verification and remote synchronization separately.
7. Record website release only from a successful provider receipt plus observed live reader checks. Retain version/build/deployment IDs, source revision, audience, URL, timestamp and limitations. Archive completion and release completion are separate facts.
8. Resume idempotently: reconcile existing output IDs and hashes before new generation, upload or deployment. Ambiguous remote results require inspection before retry.

The private installation may supply extra vault reconciliation, source recovery and catalog tools. Discover and verify those interfaces there; this public pack intentionally does not include its private catalog, hardcoded mounts or authentication adapters. A portable file inventory is not a claim of vault ingestion. Social posting and recurring schedules require separate task authority and are not part of an archive operation.
