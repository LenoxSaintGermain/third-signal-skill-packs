---
name: wearable-data-export
description: "Standardized export format for Limitless pendant and OMI wearable data. Use when extracting lifelogs, memories, conversations, or transcripts from wearable devices and saving them as normalized markdown + JSON archives."
version: 1.0.0
author: Oz
platforms: [macos]
metadata:
  hermes:
    tags: [limitless, omi, wearable, export, backup, archivist]
---

# Wearable Data Export

Standardized procedures for extracting and archiving data from Limitless and OMI wearables.

## Output Format

Every export produces two files per item:
1. **`{id}.md`** — Human-readable markdown summary
2. **`{id}.json`** — Raw API response with full metadata

## Limitless Export

Use the `getLifelogs` MCP tool with date filtering. For each lifelog:

```markdown
# {title}
- **Date:** {startTime} → {endTime}
- **ID:** {id}
- **Speakers:** {speaker list}

## Summary
{markdown content}

## Transcript
{full transcript if available}
```

Store under: `limitless/YYYY/MM/DD/{id}.md` and `limitless/YYYY/MM/DD/{id}.json`

## OMI Export

### Memories
Use `get_memories` tool. Store under: `omi/memories/YYYY/MM/DD/{id}.md`

### Conversations
Use `get_conversations` tool. Store under: `omi/conversations/YYYY/MM/DD/{id}.md`

### Action Items
Use `get_action_items` tool. Store under: `omi/action-items/YYYY/MM/DD/{id}.md`

## Sync State

Maintain `manifests/last_sync.json`:

```json
{
  "limitless": {
    "last_pulled": "2026-05-26T00:00:00Z",
    "last_id": "abc123",
    "total_exported": 142
  },
  "omi": {
    "memories_last_pulled": "2026-05-26T00:00:00Z",
    "conversations_last_pulled": "2026-05-26T00:00:00Z",
    "total_exported": 89
  }
}
```

After each successful export, update the timestamp so the next run only pulls new data.

## Daily Export Procedure

1. Read `manifests/last_sync.json` for last timestamps
2. Pull Limitless lifelogs since last timestamp
3. Pull OMI memories, conversations, action items since last timestamp
4. Write markdown + JSON files to dated directories
5. Update `manifests/last_sync.json`
6. Log summary: how many items pulled, any errors
