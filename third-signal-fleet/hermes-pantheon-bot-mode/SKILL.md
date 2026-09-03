---
name: hermes-pantheon-bot-mode
description: Use when configuring Hermes v0.21.0 Pantheon rosters, named specialist bots, isolated bot memory, scoped permissions, or asynchronous A2A peer routing.
metadata:
  requires_tools: [terminal, file]
  fallback_for_tools: [terminal, file]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# Hermes Pantheon Bot Mode

## Level 0 — Overview

Use Hermes v0.21.0 Pantheon mode for persistent named specialists rather than repeatedly spawning anonymous workers. Each bot owns a durable namespace under `~/.hermes/bots/<bot_name>/`, receives only its approved tools, and communicates with peers through asynchronous A2A messages.

Never share a bot's memory directory, credentials, or unrestricted tool profile with another bot. Treat roster and permission changes as configuration changes requiring review.

## Level 1 — Runbook

1. Define a roster with stable names, roles, model/provider, memory namespace, and allowed tools.
2. Create each namespace with user-only permissions; do not copy the operator profile or secrets.
3. Configure scoped tool allowlists. Deny by default and grant the smallest set needed.
4. Register A2A peer routes with explicit sender, recipient, message schema, timeout, and retry policy.
5. Start one bot in foreground or headless mode and verify its identity, namespace, and denied tools.
6. Send a non-sensitive ping through A2A; verify delivery, correlation ID, and reply without assuming synchronous execution.
7. Record the roster revision and rollback configuration.

Example roster fields:

```yaml
bots:
  architect: {role: architecture, memory: ~/.hermes/bots/architect, tools: [file, terminal-read]}
  coder: {role: implementation, memory: ~/.hermes/bots/coder, tools: [file, terminal, test]}
  auditor: {role: verification, memory: ~/.hermes/bots/auditor, tools: [file, terminal-read]}
```

## Level 2 — Reference

A2A envelopes should include `message_id`, `sender`, `recipient`, `kind`, `created_at`, `payload`, and `reply_to`. Persist delivery state separately from bot memory. Retries must be idempotent and bounded. A bot may return `blocked` when a request exceeds its tool scope; the router must not silently escalate permissions.

## Common Mistakes

- Treating a named bot as a new session with no durable identity.
- Mounting `~/.hermes` broadly instead of one bot namespace.
- Letting A2A routes inherit ambient tools.
- Reporting a queued message as completed work.
- Recording secrets in shared peer transcripts.

## Verification

Confirm namespace ownership, effective tool policy, bot identity, A2A correlation, retry behavior, and clean shutdown. Keep a redacted roster snapshot for rollback.
