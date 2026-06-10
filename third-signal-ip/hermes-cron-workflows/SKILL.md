---
name: hermes-cron-workflows
description: Patterns and pitfalls for managing native Hermes cron jobs, migrating from system crontab, and handling script paths.
---

# Hermes Cron Workflows

## Linked Files
- **`references/cron_environment_pitfalls.md`**: Details the isolated `$HOME` directory trap when executing shell scripts via cron, and how to fix it using explicit wrapper scripts.

This skill covers how to properly manage, schedule, and migrate background tasks using Hermes' native `cronjob` tool.

## Migrating from System Crontab
Often, legacy automation was placed in the host OS `crontab`. When migrating these to native Hermes cron jobs so they are visible in the UI:
1. Read the existing crontab (`crontab -l`).
2. Identify jobs that belong to the agent/Hermes.
3. Recreate them using the `cronjob` tool (action: `create`).
4. Rewrite the system crontab to remove the migrated jobs while preserving the user's non-agent jobs.

## ⚠️ Pitfall: Script Paths for `no_agent: true`
When creating a cron job that runs a shell script directly (`no_agent: true`), the `cronjob` tool strictly requires the `script` parameter to be a filename relative to `~/.hermes/scripts/` (or the profile's scripts directory). It will reject absolute paths or home-relative paths (e.g., `/Users/name/repo/script.sh`).

**The Workaround:**
If the target script is managed in a git repository or elsewhere, create a symlink into the Hermes scripts directory before scheduling the job:

```bash
mkdir -p ~/.hermes/scripts
ln -sf /absolute/path/to/repo/script.sh ~/.hermes/scripts/script_name.sh
```
Then, create the cron job passing `script: "script_name.sh"`.

## Task Visibility (Kanban/Schedules)
When a user asks for a visual map or "Kanban" of scheduled jobs to understand their week, use the `todo` tool to write the scheduled cron jobs into the session's task list. This provides immediate, structured visibility that satisfies the operator's need to know "when to step in" without building external systems.

## Execute Code Restriction
`execute_code` is blocked by default in cron jobs as a security measure (it runs arbitrary Python/subprocess calls without a user present to approve). 
- **Pitfall:** Sequential logic or loops that rely on `execute_code` will fail in cron.
- **Workaround:** Use the `terminal` tool for shell-level loops (`for i in ...; do ...; done`) or perform multi-step tasks using sequential direct tool calls.
