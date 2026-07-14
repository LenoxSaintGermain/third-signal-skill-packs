# Wearable Data Export Standards (v1.0)

## Directory Structure
`[Source]/[YYYY]/[MM]/[DD]/`

## Markdown Summary (.md)
- **Header:** `# [Title or Summary Line]`
- **Metadata Block:** 
  - `**ID:** [Original UUID]`
  - `**Time:** [Local Time Range]`
- **Summary Section:** 2-3 sentence overview of the recording.
- **Topics Section:** Bulleted list of themes.
- **Key Events:** Notable quotes or transitions.

## JSON Sidecar (.json)
Should include at minimum:
- `id`
- `time` (human-readable)
- `duration`
- `topics` (array)
- `raw_data_link` (optional)

## Manifest Schema
Stored at `manifests/last_sync.json`:
```json
{
  "last_sync": "ISO8601",
  "sources": {
    "source_name": {
      "last_processed_id": "string",
      "last_sync_at": "ISO8601"
    }
  }
}
```
