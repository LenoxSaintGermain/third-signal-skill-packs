# API v2 and bridge lifecycle

Verified 2026-10-14. Official sources: https://open.manus.ai/docs/v2/task.create and https://open.manus.im/docs/v2/task-lifecycle

API v2 uses the x-manus-api-key header. Keep the secret in secure runtime configuration, never prompts, receipts or public Git. Current task endpoints include POST /v2/task.create, GET /v2/task.detail?task_id=..., POST /v2/task.sendMessage and task.listMessages; inspect exact current parameter schemas before calling. A local wrapper may expose only a subset.

1. Record a task ID immediately after creation. If submission times out, inspect existing tasks before creating another.
2. Poll messages and task detail with bounded waits. Current lifecycle states are running, waiting, stopped and error. stopped alone is not completion: require has_running_background_jobs=false and inspect expected artifacts. A missing flag is unknown.
3. For waiting, distinguish an answer to a question from an action confirmation. Use sendMessage for questions and event-specific confirmAction schemas for confirmations. videoGenerate may request standard/premium; apiHighCreditNotice is a separate spending decision. Never blanket-approve either in a zero-paid-credit trial.
4. Resolve installed skill IDs with skill.list before enable_skills/force_skills. Preserve OAuth App ownership restrictions. Files attached to a message are not evidence of installation.
5. Download and inspect output files, log errors and observed costs, and retain the actual task URL/ID. A success message does not prove files, live deployment or completed background video jobs.

Hermes dispatch_manus_task currently uses an operator-only confirmation token proposal flow. Inspect its live contract. Agents must not read or manufacture the operator token or approve their own proposal. The bridge task route does not prove promotional entitlement or desktop timeline control. Prefer the signed-in Video UI for a UI-only offer unless API coverage is confirmed.
