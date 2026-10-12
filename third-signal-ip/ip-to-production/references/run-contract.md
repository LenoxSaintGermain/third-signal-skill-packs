# Resumable production contract

Use a dedicated versioned run directory, not another IP's production folder. Maintain `RUN.json` and `DECISIONS.md`; use the schema below as a record format, not evidence that any stage is complete.

```json
{
  "schema": "third-signal/ip-production-run/v1",
  "ip": {"slug": "example", "title": "Example"},
  "route": "reader-site",
  "source_paths": [],
  "audience": "",
  "installment": "",
  "authority": {
    "creative": {"scope": "", "evidence": ""},
    "asset_acceptance": {"scope": "", "evidence": ""},
    "deploy": {"scope": "", "evidence": ""},
    "release_audience": "private"
  },
  "dependencies": {},
  "stages": {},
  "selected_asset_ids": [],
  "deployments": [],
  "next_action": "Inspect source package"
}
```

Routes: `reader-site`, `signal-stage`, `both`. Track source, cast, script, art, source-acceptance, integration, QA, deployment and archive stages separately. Each stage records `state`, `inputs` (paths and hashes), `outputs` (paths and hashes), `evidence`, `blockers` and `updated_at`. States: `not-started`, `in-progress`, `awaiting-approval`, `blocked`, `approved`, `finalized`, `published`, `superseded`. Use only states supported by evidence; do not automatically promote every stage to published.

On resume, inspect existing RUN.json and actual outputs before generating anything. Recheck inputs and output hashes. Reuse valid stages, invalidate stale downstream outputs, and resume the earliest unmet dependency. Preserve superseded attempts. If deployment/post status is uncertain, inspect the existing remote result before retrying; no duplicate site/project creation as blind recovery.

For each accepted asset record ID, parent/reference IDs, source/tool evidence, binary path, size, dimensions, SHA-256, text policy, canon status, acceptance status and acceptance evidence. Unknown generation metadata stays unknown. Keep source paths and private evidence out of public site bundles.

Deployment receipts contain destination project identity, source commit when available, build/version/deployment IDs returned by tools, access audience, live URL, actual browser results, timestamp and limitations. Never store secrets or bearer preview URLs in public receipts.

A missing tool does not invalidate completed creative stages. Save their evidence and finish independent work; report the concrete missing deployment or source capability instead of claiming completion.
