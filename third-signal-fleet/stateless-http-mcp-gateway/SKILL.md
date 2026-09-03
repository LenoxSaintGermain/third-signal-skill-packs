---
name: stateless-http-mcp-gateway
description: Use when building or standardizing custom MCP servers on the 2026-07-28 stable spec with Streamable HTTP, header routing, MCP Apps, or Tasks.
metadata:
  requires_tools: [terminal, file]
  fallback_for_tools: [terminal, file]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# Stateless HTTP MCP Gateway

## Level 0 — Overview

Use stateless Streamable HTTP for horizontally deployable custom MCP servers. Route requests using explicit `Mcp-Method` and `Mcp-Name` headers, expose MCP Apps UI extensions only through declared capabilities, and use Tasks for long-running work without storing session state in the gateway.

Stateless means each request carries enough context to authenticate, authorize, validate, and continue; it does not mean unaudited shared storage is acceptable.

## Level 1 — Runbook

1. Pin the 2026-07-28 stable MCP specification and define supported methods, names, versions, and content types.
2. Accept Streamable HTTP requests only over authenticated TLS; validate `Mcp-Method` and `Mcp-Name` against an allowlist.
3. Route to a handler using the headers plus validated JSON-RPC/body data; never infer a tool from an untrusted display name.
4. Return protocol-compliant errors and correlation IDs without leaking credentials or internal stack traces.
5. Advertise MCP Apps UI extensions only when the client and server capability negotiation succeeds.
6. Create and poll Tasks for bounded asynchronous work; authorize every poll and make cancellation idempotent.
7. Test duplicate delivery, missing headers, replay, timeout, cancellation, and unsupported capability paths.

## Level 2 — Reference

Keep transport, authentication, routing, handler execution, and task persistence separate. A task record needs `task_id`, requester, method/name, state, timestamps, result reference, error, and expiry. Use idempotency keys for side-effecting methods. Emit structured audit events for authorization, dispatch, task transitions, and UI capability negotiation.

## Common Mistakes

- Reintroducing sticky in-memory sessions behind a stateless label.
- Routing from a user-controlled tool description instead of the allowlist.
- Treating MCP Apps UI as trusted server-side HTML.
- Leaving Tasks without expiry, ownership checks, or cancellation.
- Returning HTTP success for a protocol-level error.

## Verification

Exercise compliant and malformed requests, restart the gateway between task polls, verify authorization and idempotency, and test capability downgrade when MCP Apps is unavailable.
