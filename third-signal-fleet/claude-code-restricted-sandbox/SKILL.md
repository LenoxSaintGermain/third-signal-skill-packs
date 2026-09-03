---
name: claude-code-restricted-sandbox
description: Use when running Claude Code v2.1.248+ in zero-trust audits, restricted headless execution, or enterprise MCP-governed environments.
metadata:
  requires_tools: [terminal, file]
  fallback_for_tools: [terminal, file]
  progressive_disclosure: [level-0-overview, level-1-runbook, level-2-reference]
---

# Claude Code Restricted Sandbox

## Level 0 — Overview

Use Claude Code v2.1.248+ restricted mode for audits where arbitrary shell execution and web retrieval are not trusted. Set `CLAUDE_CODE_RESTRICTED=1`, apply enterprise `managed-mcp.json`, and make headless failure explicit rather than silently falling back to unrestricted tools.

Restricted mode is a safety boundary, not a prompt instruction. Verify the effective runtime policy before processing code or secrets.

## Level 1 — Runbook

1. Pin and verify the Claude Code version is at least 2.1.248.
2. Export `CLAUDE_CODE_RESTRICTED=1` in the child process environment.
3. Load the enterprise-managed MCP policy from a controlled, read-only location.
4. Allow only approved MCP servers and operations; deny arbitrary Bash and WebFetch.
5. Run a harmless capability probe and capture the effective policy.
6. Execute the audit headlessly with bounded time, output, and workspace access.
7. If policy loading, capability probing, or the audit fails, stop with a non-zero result and an actionable error. Never retry by removing restricted mode.

```bash
CLAUDE_CODE_RESTRICTED=1 claude \
  --mcp-config /etc/claude/managed-mcp.json \
  --headless -- "Audit the supplied repository; do not modify files."
```

## Level 2 — Reference

`managed-mcp.json` is enterprise policy, not project content. Validate ownership, permissions, schema, server command paths, environment-variable references, and allowed methods before launch. Keep audit output separate from policy and credentials. In CI, enforce a timeout and treat missing binaries, denied tools, malformed policy, and unexpected network access as failure states.

## Common Mistakes

- Assuming an environment variable is effective without inspecting the child process.
- Mounting a writable managed policy into an untrusted workspace.
- Treating a denied Bash/WebFetch call as permission to switch modes.
- Allowing an MCP server broader filesystem or network scope than the audit.
- Returning exit code zero when headless startup failed.

## Verification

Prove version, restricted environment, managed policy hash, denied arbitrary tools, allowed MCP calls, bounded execution, and non-zero fail-safe behavior with a negative test.
