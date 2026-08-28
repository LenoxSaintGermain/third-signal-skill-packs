# Portable contracts

Use `third-signal-agent-workforce@2` as the control-plane manifest schema. The example under `assets/hq-manifest.example.json` is intentionally executable by any adapter.

The manifest includes provider-neutral `runtime_nodes`, `skills`, `schedules`, `approvals`, `artifacts`, `receipts`, and control-plane `events`. Every skill record declares whether its SHA-256 covers `SKILL.md` or the packaged bundle, provides a package-local path, and validates the declared hash against those bytes. Provider conversations and browser sessions are never substitutes for these registries.

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
- optional `last_heartbeat_at` as an observation, not an assurance of current access.

Allowed states: `offline | shadow | active | degraded | retired`.

## Runtime node

A runtime node is the observed execution or verification host. It carries `runtime_node_id`, `authority`, nullable `adapter_id`, `state`, `trust_boundary`, and capabilities. Adapter nodes belong to their adapter. Provider-neutral verification nodes belong to the control plane and explicitly declare `receipt.verify`. Leases, events, receipts, and verification records must resolve to registered nodes.

## Task envelope

Required fields:

- `task_id`, `swarm_trace_id`, and `role_id`;
- `capability`, explicit `effect`, `operating_mode`, `classification`, and `public_impact`;
- `approval_policy`;
- `input_refs` and `output_contract`;
- `allowed_tools` and `denied_tools`;
- `preferred_adapters` and `fallback_adapters`;
- `idempotency_key`, `resume_policy`, `replay_safety`, `lease`, and `status`.

Allowed task states: `queued | claimed | running | approval-required | blocked | completed | failed | cancelled`.

Allowed classifications: `public | internal | confidential | restricted`.

External mutation tasks must use `operator_required` or `preauthorized_exact_packet`. `preauthorized_exact_packet` still requires action-time confirmation when the active agent environment requires it.

`effect` is `read | draft | mutate`; do not infer mutation risk from a capability name. `operating_mode` is `shadow | active`. `resume_policy` is `restart_current_inputs | resume_exact_snapshot | block_for_operator`. `replay_safety` is `read_only | idempotent | non_repeatable`.

A lease carries `generation`, `holder_adapter`, `runtime_node_id`, `fencing_token`, `claimed_at`, and `expires_at`. Every claim increments the generation and issues a new token. Only an assigned, healthy-enough adapter that declares the capability may hold it. Late successful receipts and all mutations must match the current generation and token.

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

The portable approval record includes `task_id`, `action_type`, `destination`, `account`, `content_hash`, full `asset_hashes`, exact `scope`, `rollback_or_correction`, authorization and expiration timestamps, status, and consumed state. Consumption binds one approval to one receipt with `consumed_by_receipt_id` and `consumed_at`; reuse fails closed. Each mutation declares its own `approval_id`, and one one-use approval covers exactly one mutation. The approval must remain valid through mutation completion. A mutation receipt must match those fields exactly.

Changing content, destination, account, asset bytes, or expiration invalidates the packet. Promotion authorization, campaign approval, and action-time public execution approval are separate gates.

## Receipt

Required fields:

- `receipt_id`, `task_id`, `run_id`, `attempt`, `lease_generation`, and `fencing_token`;
- `swarm_trace_id`, `role_id`, `adapter_id`, and `runtime_node_id`;
- `status`, `input_hashes`, and structured `outputs`;
- `mutations`, `approvals_used`, `validation`, and independent `verification`;
- `started_at`, `finished_at`, control-plane `received_at`, and `next_action`.

Allowed receipt states: `ok | partial | noop | blocked | failed`.

Receipt filenames and identities must be append-only and include `task_id`, `run_id`, and `attempt`; a date-only name is not unique. Empty `mutations` and `approvals_used` arrays are valid for read-only and `noop` work. Every output references a registered artifact and carries its full lowercase SHA-256. Every external mutation lists the one-use approval consumed, exact scope, current fencing data, and observed destination evidence. Missing metrics are `not_observed`, not zero. A receipt is a claim until the provider-neutral control plane verifies its references from a runtime distinct from the executor; completed work requires a verified `ok` or `noop` receipt bound to the same task, trace, role, adapter assignment, generation, and fence.

## Control-plane event

When an adapter disappears, the control plane—not the missing worker—records the interruption. Required fields are `event_id`, `event_type`, `task_id`, `lease_generation`, `recorded_at`, `source`, and `status`. A `lease.expired` event also binds the prior holder adapter, runtime node, and fence, and must be independently verified. A failover to generation N requires that event for generation N-1, recorded before the fallback starts. A receipt received after its bound lease-expiration event is rejected, including late `partial` reports. Preserve the prior adapter as a `retired` tombstone or atomically change role defaults; never leave dangling provider references.

Do not run authorization tests by mutating production sidecars and relying on a `finally` rollback. Test against isolated copies, because crashes and concurrent jobs can expose temporary state.
