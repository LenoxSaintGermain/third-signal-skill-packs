---
name: librarian-sync
description: Enforces that LIBRARIAN documentation workflows (Chronicle, Manifest, Backlog) are updated after every feature run or epic completion.
---

# LIBRARIAN Sync Protocol

**Purpose:**
To prevent documentation drift and prevent recursive loops where the system loses track of what was just built. This skill enforces that the LIBRARIAN cognitive engine updates the root artifacts.

**When to Use:**
You **MUST** use this skill immediately after completing any Epic, Feature, or significant code integration phase.

## Protocol Steps

1. **Information Gathering:**
   - Review your recent tool calls and the latest code changes you just merged or successfully tested.
   - **Hybrid Drive Sync:** Explicitly read `conductor/tracks.md` or `conductor/tracks/<id>/metadata.json` to ingest completed Subagent Execution Engine results. 
   - Read the current `docs/MANIFEST_AUDIT_REPORT.md` (or `OrbitalManifest`) and any active `task.md` or End-to-End backlog.

2. **Triggering LIBRARIAN (If ADK is active):**
   - If the ADK local server is running (`npm run adk:web`), you should simulate the LIBRARIAN agent ingesting the latest diffs or summaries.
   - You can send a prompt to the `/api/adk/execute` endpoint targeting `LIBRARIAN` to ask it to summarize the changes for the chronicle.

3. **Artifact Enforcement (Mandatory):**
   - You **MUST** write or update a concise summary of the newly built feature into:
     - `EXECUTION_LEDGER.md` (chronological technical log)
     - Active Project Tracker (`walkthrough.md`, `task.md`, or Epic backlog)
     - `docs/MANIFEST_AUDIT_REPORT.md` (if manifest artifacts were affected)
   - Ensure you update the status markers (e.g., changing from `[ ]` to `[x]`).
   - If a new feature was added, ensure it is recorded so the next developer or agent does not rebuild it.

4. **Compression Check (Auto-Efficiency):**
   - After writing to `EXECUTION_LEDGER.md`, measure its current state:
     - Count total lines in the ledger
     - Calculate estimated tokens (lines × 0.31)
   - Check compression thresholds:
     - **Tier 1**: ≥ 1000 lines
     - **Tier 2**: ≥ 2000 lines
     - **Tier 3**: ≥ 5000 lines

5. **Conditional Compression (Auto-Trigger):**
   - **If Tier 1 threshold met** (≥ 1000 lines):
     - Automatically invoke the `librarian-compress` skill
     - This will perform inline batch compression transparently
     - Wait for compression to complete before proceeding

   - **If Tier 2 threshold met** (≥ 2000 lines):
     - Add warning: "⚠️ **Ledger Size Alert**: {lines} lines detected. Recommend running `librarian-compress` with tier2 to shard into domain-specific ledgers for better token efficiency."
     - Do NOT auto-execute (sharding requires user approval)

   - **If Tier 3 threshold met** (≥ 5000 lines):
     - Add warning: "⚠️ **Critical Ledger Size**: {lines} lines detected. Strongly recommend `librarian-compress tier3` for semantic compression to extract Current Truth principles."
     - Do NOT auto-execute (major structural change)

6. **Confirmation:**
   - Once the documentation is synced, explicitly state that the "LIBRARIAN Sync Protocol" was executed successfully.
   - Include compression status:
     - "Compression status: None" (if < 1000 lines)
     - "Compression status: Tier-1-Auto (ledger compressed from {before} to {after} lines)" (if Tier 1 executed)
     - "Compression status: Tier-2-Recommended" (if ≥ 2000 lines)
     - "Compression status: Tier-3-Recommended" (if ≥ 5000 lines)
   - If compression was triggered, include token reduction achieved
