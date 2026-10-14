# IP Continuation Desk state schema

Use this schema when creating a durable continuation ledger or weekly report.

```yaml
ip:
  id: "stable-slug"
  name: "Human-readable IP name"
  surface: "Studio | Research OS | Orbital | Signal Card | Admin OS | proof surface"
  canonical_path: "ip/<slug>/"
  state: "not-started | in-progress | awaiting-approval | blocked | approved | finalized | published | superseded"
  phase: "intake | canon | development | visual-development | script | panel-planning | art | lettering | qa | runtime | publication | archive"
  confidence: "high | medium | low"
  last_confirmed_movement: "YYYY-MM-DD"
  source_sessions: []
  recipe:
    primary: ""
    secondary: []
    narrative_job: ""
  completed: []
  pending: []
  blocked: []
  unknown: []
  evidence: []
  assets:
    locked: []
    available_local: []
    uploaded_drive: []
    needs_export: []
    superseded: []
    rejected: []
  next_action: ""
  remaining_risk: ""
```

## Evidence entry

Each evidence entry should identify:

```yaml
- path: "relative/path/to/file"
  claim: "What this source proves"
  authority: "user-lock | canon | approved-handoff | manifest | checkpoint | draft | rejected"
  observed_on: "YYYY-MM-DD"
```

## Weekly report sections

1. Executive state
2. IP-by-IP table
3. Completed movement this week
4. Pending and blocked work
5. Asset/provenance risks
6. Proposed schedule for the next week
7. Decisions needed
8. Evidence index
