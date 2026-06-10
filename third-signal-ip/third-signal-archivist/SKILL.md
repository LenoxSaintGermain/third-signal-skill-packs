---
name: third-signal-archivist
description: "Extracting, normalizing, and backing up wearable AI data (Limitless, OMI)."
version: 1.0.0
author: Archivist
license: MIT
---

# Third Signal Archivist

Operational rules for extracting and archiving data from AI wearables like the Limitless Pendant and OMI Wearable.

## Workflow

### 1. Discovery
- **Limitless:** Use `mcp_limitless_getLifelogs` for the target date.
- **OMI:** Check Google Drive backups (`treble.design`) first. If stale or missing, fallback to `mcp_omi_get_conversations`.

### 2. Extraction & Normalization
- For every entry, fetch full details (e.g., `mcp_limitless_getLifelogEntry`).
- Create dated directories: `YYYY/MM/DD/` under the source folder.
- Produce two files per entry:
  - `ID.md`: A markdown summary with topics and key events.
  - `ID.json`: A raw JSON sidecar containing metadata and IDs.

### 3. Sync Management
- Maintain `manifests/last_sync.json`.
- Track `last_sync_at` (ISO timestamp) and `last_processed_id` for each source to prevent duplicates.

## Rules & Standards

- **Read-Only Sources:** Never delete data from the APIs.
- **Absolute Paths:** Always use the full path (e.g., `/Volumes/Third Signal Lab HD/archivist/`).
- **Cron Constraints:** `execute_code` is blocked in cron jobs for security. Use `terminal` loops or sequential tool calls for processing.
- **Drive Fallback:** If the local Drive mount (CloudStorage) is stale compared to the current date, bridge the gap using direct API calls.

## Troubleshooting

| Issue | Root Cause | Fix |
|-------|------------|-----|
| `execute_code` blocked | Cron security policy | Use `terminal` or direct tools. |
| OMI status tool fails | Missing Firebase token | Fallback to `get_conversations`. |
| Drive mount stale | Sync delay | Query OMI/Limitless APIs directly for the missing window. |
| MCP JSON Syntax Errors | `gemini-3-flash-preview` parallel tool calling bug | Pin the cron job to `gemini-3.1-pro-preview` which handles complex parallel MCP tool calls reliably. |
