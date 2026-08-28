# Portable contracts

Use `third-signal-agent-workforce@1` as the control-plane manifest schema. The example under `assets/hq-manifest.example.json` is intentionally executable by any adapter.

## Role

A role survives provider replacement. Required fields:

- `role_id`, `department`, and `mission`;
- `capabilities` and `prohibited`;
- `approval_policy`;
- `default_adapter` and `fallback_adapters`;
- `required_skills`.

## Adapter

An adapter declares current execution capability, not institutional authority. Required fields:

- `adapter_id`, `kind`, and `state`;
- `trust_boundary` and `capabilities`;
- `credentials_ref` containing only a symbolic reference, never a secret.

Allowed states: `offline | shadow | active | degraded | retired`.

## Task envelope

Required fields:

- `task_id`, `swarm_trace_id`, and `role_id`;
- `capability`, `classification`, and `public_impact`;
- `approval_policy`;
- `input_refs` and `output_contract`;
- `allowed_tools` and `denied_tools`;
- `preferred_adapters` and `fallback_adapters`;
- `idempotency_key`, `lease`, and `status`.

Allowed task states: `queued | claimed | running | approval-required | blocked | completed | failed | cancelled`.

Allowed classifications: `public | internal | confidential | restricted`.

External mutation tasks must use `operator_required` or `preauthorized_exact_packet`. `preauthorized_exact_packet` still requires action-time confirmation when the active agent environment requires it.

## Approval packet

Bind approval to:

- immutable `action_id` and task id;
- exact action type;
- destination and account;
- content and asset hashes;
- authorizer and authorization timestamp;
- expiration;
- rollback or correction path;
- consumed status.

Changing content, destination, account, asset bytes, or expiration invalidates the packet. Promotion authorization, campaign approval, and action-time public execution approval are separate gates.

## Receipt

Required fields:

- `receipt_id`, `task_id`, `run_id`, and `attempt`;
- `swarm_trace_id`, `role_id`, `adapter_id`, and `runtime_node_id`;
- `status`, `input_hashes`, and structured `outputs`;
- `mutations`, `approvals_used`, and `validation`;
- `started_at`, `finished_at`, and `next_action`.

Allowed receipt states: `ok | partial | noop | blocked | failed`.

Receipt filenames and identities must be append-only and include `task_id`, `run_id`, and `attempt`; a date-only name is not unique. Every output hash is a full lowercase SHA-256. Every external mutation lists the approval consumed and the observed destination evidence. Missing metrics are `not_observed`, not zero. A receipt is a claim until the control plane verifies its references.

Do not run authorization tests by mutating production sidecars and relying on a `finally` rollback. Test against isolated copies, because crashes and concurrent jobs can expose temporary state.
