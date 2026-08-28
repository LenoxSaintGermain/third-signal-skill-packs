# Operating model

## Decision

Third Signal owns the workforce. Providers supply execution.

```text
Third Signal HQ / Admin OS / Orbital
  role registry
  task graph and leases
  skill registry and hashes
  approval ledger
  artifact vault
  receipt ledger
  adapter health and routing
        |
        +-- GrokBot adapter
        +-- Hermes adapter
        +-- Codex adapter
        +-- Claude adapter
        +-- Gemini adapter
        +-- future adapter
```

The control plane may be implemented locally first and projected into `thirdsignal.ai/#admin`. The public/admin site is a cockpit, not the only system of record.

## Ownership boundary

The control plane owns:

- role identity and mission;
- capabilities and prohibitions;
- task state, dependencies, lease, and idempotency;
- approval policy and exact action packets;
- schedules and event triggers;
- skill identity and hashes;
- artifacts and provenance;
- adapter health, budget, and failover;
- traces and verified receipts.

Adapters own:

- provider-native planning and execution;
- provider browser or computer sessions;
- temporary working files;
- provider telemetry needed to create a receipt.

Adapters do not own canon, rights, durable approvals, permanent staff identity, or institutional memory.

## Minimum control-plane operations

```text
submit(task)
claim(adapter, capability, lease)
heartbeat(runtime_node)
report(receipt)
request_approval(action_packet)
approve(action_packet)
release(task)
```

`publish`, `deploy`, `send`, `delete`, permission changes, purchases, and credential changes are capabilities executed only after an exact action packet is approved.

## Failover semantics

- Every task has an idempotency key.
- Every claim has an expiring lease.
- Missing heartbeats expire leases; they do not mark work complete.
- Outputs are content-addressed where practical.
- A fallback adapter revalidates inputs and partial outputs before resuming.
- Mutation tasks must check for an existing destination receipt before retrying.
- Provider conversations and browser sessions are never required to resume the job.

Run a failover drill before declaring a permanent role portable: disable the preferred adapter, claim one representative task with the fallback, and produce an equivalent receipt without changing the role or task identity.

## Projection into Admin OS

The cockpit should show:

- persistent role and current adapter;
- capability and task state;
- lease and heartbeat freshness;
- source artifacts and output receipts;
- approval required;
- cost and model routing;
- degraded, stale, or failover state.

Use a closed component catalog. Agents select allowed cards and actions; they do not generate arbitrary privileged UI.
