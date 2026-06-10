---
name: hermes-dream
description: Autonomously consolidates, cleans, and optimizes Hermes persistent memory during sleep cycles, replicating the 'dream-skill' pattern.
version: 1.0.0
metadata:
  hermes:
    requires_toolsets: [terminal, file]
---

# The Hermes Dream Protocol

This skill codifies the memory consolidation workflow for local Hermes agents on LANDSAT, heavily inspired by the open-source `dream-skill` repo for Claude Code. It prevents memory rot, resolves contradictions, normalizes dates, and prunes verbose facts to stay strictly within our 2,200-character cognitive memory limit.

## Trigger
Use this skill when running the automated nightly `/dream` cron job, or when the memory tool returns an "out of space" / "limit exceeded" error.

## The 4-Phase Consolidation Process

### Phase 1: Orient
- Read all active entries in the `memory` tool (both `memory` and `user` targets).
- Count current character usage and identify remaining memory runway.

### Phase 2: Gather Signal
- Read the recent transcripts of our conversations (you can use `session_search` with no query or temporal sorting to find recent topics, or read the local execution logs).
- Look for:
  - Direct corrections from the Operator ("Don't do that again", "Prefer X over Y").
  - Preferences or tools that have changed (e.g., we upgraded the Chrome extension to port `4114` today).
  - Outdated environment facts (e.g., old versions of tools or obsolete paths).

### Phase 3: Consolidate
- Synthesize the gathered signals with the existing memory bank.
- **Normalize Dates:** Convert relative dates (e.g., "yesterday" or "last week") to absolute calendar dates (e.g., "2026-06-08") so they preserve meaning.
- **Resolve Contradictions:** If an old memory says "using n8n for workflows" but a new one says "using python + cron on LANDSAT," delete the old one.
- **Merge Duplicates:** Consolidate redundant facts into tight, single-sentence declarative statements.

### Phase 4: Prune & Index
- Rewrite the memory bank using the `memory(action='replace')` or `remove` tools.
- Keep every entry highly condensed and focused *only* on high-value facts that will reduce future steering or prevent mistakes.
- Ensure the total memory footprint drops below 1,500 characters, leaving a healthy safety margin for active sessions.

## The Nightly Command
Running `/dream` executes this 4-phase process, allowing the agent to "sleep" and reorganize its mind.
