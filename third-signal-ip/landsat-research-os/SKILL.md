---
name: landsat-research-os
description: Use when routing research work through LANDSAT, Research OS, /research-push, NotebookLM source packs, cited evidence packets, #admin review, or Librarian research proposals.
---

# LANDSAT Research OS Lane

Research OS is a governed capability lane, not a separate operator-facing app by default.

The operator should invoke research from Orbital, review and approve it in #admin, and preserve approved memory through Librarian. LANDSAT is the primary worker for source collection, synthesis, evidence packets, and NotebookLM-ready packs.

## Operating Decision

Do not create a separate Research OS cockpit unless the work is specifically about:

- private MCP/OIDC runtime isolation,
- Colab/Raziel notebook execution,
- public `research.thirdsignal.ai` publishing,
- or a dedicated public research library.

For normal operator work, use this shape:

```text
Orbital request -> LANDSAT research work -> Swarm trace -> #admin review -> Librarian proposal or public-safe publishing
```

## Roles

| Surface | Responsibility | Authority |
| --- | --- | --- |
| Orbital | Invoke, steer, attach artifacts, run `/research-push`, ask ALFRED for research handoffs | operator cockpit |
| LANDSAT | Collect sources, analyze, cite, summarize, produce evidence/source packs | proposal-only worker |
| Swarm | Emit trace events and preserve lineage | trace owner |
| #admin | Review citations, claims, confidence, redaction, publish-safety, routing decisions | approval surface |
| Librarian | Convert approved evidence into Agent Wiki, Manifest, Armory, Field Guide proposals/commits | canonical writer |
| Signal Card / Donna | Surface public-safe outputs only | public-safe only |

## Input Contract

Every LANDSAT Research OS job should start from a compact packet:

```json
{
  "packet_id": "research_packet_...",
  "queued_by": "orbital|alfred|alfred-air|admin|operator",
  "target_node_id": "landsat-mac-mini",
  "objective": "clear research objective",
  "classification": "public|internal|operator-only|restricted|secret-ref-only|redacted",
  "requested_action": "research_brief|evidence_pack|notebook_source_pack|research_polish|citation_audit",
  "source_refs": ["repo://...", "artifact://...", "linear://...", "url://..."],
  "source_payload_refs": ["internal ref only, no raw secrets"],
  "evidence_requirements": ["verified", "user_confirmed", "observed"],
  "requires_operator_approval": true,
  "swarm_trace_id": "trace_landsat_yyyymmdd_xxxx",
  "destination": "#admin|librarian|notebooklm|orbital|signal-card-review"
}
```

## Output Contract

LANDSAT returns a Research Evidence Packet. It must be reviewable without exposing raw sensitive material.

```json
{
  "packet_id": "research_packet_...",
  "node_id": "landsat-mac-mini",
  "provider": "gemini|ollama|poe|orbital_model_broker|unknown",
  "model": "actual-model-used-or-unknown",
  "sync_sha": "git-sha-or-unknown",
  "classification": "public|internal|operator-only|restricted|secret-ref-only|redacted",
  "public_safety": "internal_only|public_safe_pending_review|approved",
  "summary": "operator-grade synthesis",
  "claims": [
    {
      "statement": "single claim",
      "evidence_label": "verified|user_confirmed|observed|inferred|contradicted",
      "source_refs": ["url://...", "repo://..."],
      "freshness_state": "fresh|stale|unknown"
    }
  ],
  "citations": [
    {
      "source_ref": "url://...",
      "title": "source title",
      "retrieved_at": "iso-8601",
      "evidence_label": "verified|observed"
    }
  ],
  "gaps": ["missing proof, stale source, unresolved contradiction"],
  "notebooklm_markdown": "optional source-pack markdown path or summary",
  "recommended_handoff": "#admin|librarian|operator|ghost_observation|signal-card-review",
  "no_canonical_writes": true,
  "no_public_publish": true,
  "swarm_trace_id": "trace_landsat_yyyymmdd_xxxx"
}
```

## Workflow

1. Classify the request before collecting sources.
2. Refuse or route to operator review if the packet asks for raw secret handling, public publishing, direct canonical writes, production mutation, or broad local filesystem exposure.
3. Collect only approved sources and source refs.
4. Emit or preserve a Swarm trace ID before work starts.
5. Produce a cited Research Evidence Packet.
6. Route to #admin for review unless the operator explicitly requested a local-only draft.
7. Route approved knowledge to Librarian as a proposal, never as a direct commit.
8. Route public outputs only through public-safe review.

## Routing Matrix

| Request | Default lane |
| --- | --- |
| “Research this artifact / idea / thesis” | Orbital `/research-push` -> LANDSAT -> #admin |
| “Make a NotebookLM packet” | LANDSAT -> #admin review -> operator exports/imports to NotebookLM |
| “Update Agent Wiki with this” | LANDSAT evidence packet -> #admin -> Librarian proposal |
| “Publish this research” | LANDSAT evidence packet -> #admin public-safe review -> Signal Card/Donna |
| “Run heavy notebook analysis” | LANDSAT -> supervised Colab Lab Lane -> #admin |
| “Private/local-only research” | LANDSAT local/Hermes/Ollama when available -> internal-only packet |

## Boundaries

LANDSAT may:

- draft research briefs,
- produce source inventories,
- generate NotebookLM-ready Markdown,
- prepare citation audits,
- propose Librarian updates,
- and identify evidence gaps or contradictions.

LANDSAT must not:

- commit Agent Wiki, Manifest, Armory, or Field Guide records directly,
- publish to public channels,
- expose local filesystems publicly,
- store raw secrets in packets,
- mutate production resources,
- or claim a provider/model that was not actually used.

## Existing Integration Points

- Orbital slash command: `/research-push`
- Orbital artifact/context handoff: `lib/researchPipeline.ts`
- Context packet target: `research` in `lib/contextPackets.ts`
- #admin review target: CaptureCard `research_os` handoff
- Activity visibility: Research OS lane in Agent Activity Cockpit
- Canonical memory: Librarian proposal flow

## Verification

From `orbital-system`:

```bash
npm run landsat:research-os:verify
```

Expected result:

```json
{
  "ok": true,
  "verifier": "landsat_research_os_lane",
  "writes_performed": false
}
```
