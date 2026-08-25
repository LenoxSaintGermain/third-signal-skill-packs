---
name: mcp-memory-guard
description: Guarded cleanup for leaking MCP and ChatGPT renderer processes.
version: 1.0
author: Third Signal Lab
platforms: [macos]
metadata:
  hermes:
    tags: [hermes, mcp, memory, watchdog, macos, operations]
    category: devops
---

# MCP Memory Guard Skill

This skill keeps the Mac mini from being overwhelmed by stale MCP server trees
and runaway ChatGPT/Codex renderer processes. It is conservative by design: it
never terminates the app-server itself, and it only acts on old, idle MCP roots
or very large, idle ChatGPT renderers.

## When to Use

- The Mac shows application-memory exhaustion, swap growth, or a force-quit dialog.
- ChatGPT/Codex has accumulated many renderer processes.
- MCP processes remain after a task, remote session, or app restart.
- Donna or another operator needs a safe local memory-health check.

## Prerequisites

- macOS with `/usr/bin/python3`, `ps`, and `kill`.
- Hermes installed under `~/.hermes`.
- The guard script installed at `~/.hermes/skills/mcp-memory-guard/scripts/mcp_memory_guard.sh`.
- The LaunchAgent `com.thirdsignal.mcp-memory-guard` enabled for the user session.

## How to Run

```bash
# Observe only; no process changes.
~/.hermes/skills/mcp-memory-guard/scripts/mcp_memory_guard.sh --dry-run --once

# Run the guarded cleanup once.
~/.hermes/skills/mcp-memory-guard/scripts/mcp_memory_guard.sh --once

# Review the append-only JSONL log.
tail -50 ~/.hermes/runtime/mcp-memory-guard/guard.log
```

The installed LaunchAgent runs the same guarded check at login and every five
minutes. The schedule is a host-level safety rail, not an instruction to kill
active agent work.

## Quick Reference

| Guard | Default condition | Action |
|---|---|---|
| Stale MCP | App-server descendant, at least 2 hours old, idle | Terminate its process tree |
| Large MCP | At least 768 MB RSS, at least 5 minutes old, idle | Terminate its process tree |
| Large renderer | ChatGPT renderer, at least 1 GB RSS, at least 5 minutes old, idle | Terminate only that renderer |
| App-server | Any age/state | Never terminate automatically |

## Procedure

1. Run the dry run and inspect the summary plus the guard log.
2. Confirm the candidate is a ChatGPT/Codex app-server descendant, not a Hermes
   gateway, Donna process, project dev server, Docker VM, or unrelated user job.
3. Run the non-dry guard if the candidate meets the documented thresholds.
4. If the same process family returns repeatedly, inspect MCP lifecycle cleanup
   and the owning desktop task rather than lowering thresholds.
5. Keep the incident evidence: timestamp, process category, RSS, age, and the
   guard summary. Never record command-line credentials or bearer tokens.

## Pitfalls

- Do not replace the guard with `pkill -f node`; that can terminate Hermes,
  project servers, or unrelated agent work.
- Do not kill the ChatGPT/Codex app-server as part of routine cleanup; it owns
  active conversations and should be restarted only as a separate recovery step.
- Do not treat a high virtual-memory number as proof of high physical RAM use.
  Check RSS, footprint, swap pressure, and process age together.
- Do not add the skill to a profile by copying secrets or profile `.env` files.

## Verification

```bash
plutil -lint ~/Library/LaunchAgents/com.thirdsignal.mcp-memory-guard.plist
launchctl print gui/$(id -u)/com.thirdsignal.mcp-memory-guard
~/.hermes/skills/mcp-memory-guard/scripts/mcp_memory_guard.sh --dry-run --once
```

The expected result is a JSON summary with `dry_run: true`. A clean run may
report zero candidates; that is success, not a failure.
