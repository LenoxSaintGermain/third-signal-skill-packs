---
name: orbital-ingestion
description: "Validate and prepare artifacts for Orbital OS ingestion. Use when converting normalized data from Archivist or Curator into Firestore-ready artifacts with proper LANDSAT schema compliance, Worldtree linking, and ZK Steward principles."
version: 1.0.0
author: Oz
platforms: [macos]
metadata:
  hermes:
    tags: [librarian, orbital, ingestion, artifact, worldtree, firestore, zettelkasten]
---

# Orbital Ingestion

Validate and prepare artifacts for Orbital OS Firestore ingestion.

## LANDSAT Artifact Schema (Required Fields)

Every artifact destined for Orbital must include:

```json
{
  "job_id": "landsat_YYYYMMDD_shortid",
  "swarm_trace_id": "trace_landsat_YYYYMMDD_shortid",
  "objective": "string — what this artifact represents",
  "classification": "public | internal | restricted",
  "mode": "local | cloud | hybrid",
  "model": "string — which model produced or processed this",
  "sources": [
    {
      "uri": "string",
      "title": "string",
      "retrieved_at": "ISO-8601",
      "access_type": "public | authenticated | local"
    }
  ],
  "findings": [
    {
      "statement": "string",
      "evidence_label": "verified | user_confirmed | observed | inferred | contradicted",
      "source_refs": ["uri"],
      "confidence": 0.0-1.0
    }
  ],
  "citations": ["uri"],
  "caveats": ["string"],
  "follow_up_questions": ["string"],
  "recommended_handoff": "alfred | librarian | research_os | admin_review | ghost_observation"
}
```

## Validation Checklist

Before marking an artifact as ingestion-ready:

1. ☐ All required fields present and non-empty
2. ☐ `classification` is one of: public, internal, restricted
3. ☐ `confidence` values are between 0.0 and 1.0
4. ☐ `evidence_label` uses only the approved vocabulary
5. ☐ At least one source with a valid URI
6. ☐ `recommended_handoff` is a valid target
7. ☐ No undefined fields or `undefined` values (Firestore rejects these)

## ZK Steward Compliance

For knowledge artifacts going into Agent Wiki or Worldtree:

1. **Atomicity:** Can this artifact be understood without reading anything else?
2. **Connectivity:** Does it link to at least 2 other artifacts or Worldtree nodes?
3. **Organic Growth:** Are we forcing a category or letting it emerge from content?
4. **Continued Dialogue:** Does it end with follow-up questions or open threads?

## Firestore Sanitization

Before writing to Firestore, sanitize the object:

```typescript
function sanitize(obj: Record<string, any>): Record<string, any> {
  const clean = { ...obj };
  Object.keys(clean).forEach(key => {
    if (clean[key] === undefined) delete clean[key];
  });
  return clean;
}
```

## Collection Mapping

| Artifact type | Firestore collection | Notes |
|--------------|---------------------|-------|
| Conversation transcript | `sessions` | Requires session metadata |
| Knowledge extract | `artifacts` | Type: Context Card |
| Action item | `artifacts` | Type: Keycard |
| Creative output | `artifacts` | Type: Asset Card |
| Worldtree update | `worldtree` | Must go through Merge Agent |
| Memory fact | `memories` | Titan Memory system |

## Important: Never write directly

This skill validates and prepares JSON. It does NOT write to Firestore.
Actual ingestion is a separate deploy step requiring authenticated admin access.
