---
name: agent-wiki-librarian
description: Use when working on Third Signal Agent Wiki, Librarian, Active Cognitive Compendium, compiled_wiki, Obsidian wiki mirrors, Librarian proposals, canonical memory writes, or agent awareness of knowledge updates.
---

# Agent Wiki Librarian

Use this skill when an agent needs to understand, propose to, test, or route work through Third Signal's memory spine.

## Core Rule

There are two related lanes. Do not collapse them.

1. **Cloud Agent Wiki / Orbital canon**
   - Runtime owner: Orbital Librarian.
   - Primary implementation: `scripts/librarian.ts`.
   - Proposal collection: `librarian_wiki_proposals`.
   - Canon collections: `agent_wiki_sources`, `agent_wiki_claims`, `agent_wiki_pages`, `agent_wiki_cards`, graph nodes/edges, and `swarm_events`.
   - Status surface: `system_docs/librarian_status`, Orbital/#admin activity surfaces, and Swarm trace review.
   - This is the path cloud ALFRED, Orbital, #admin, Review Queue, LANDSAT Colab, and future UAT surfaces should treat as canonical.

2. **Local Active Cognitive Compendium / Obsidian mirror**
   - Runtime owner: local Librarian daemon, intended for the Mac Mini/LANDSAT lane.
   - Primary implementation: `lib/librarian/`.
   - Shared workspace: Google Drive `Third Signal Lab`.
   - Proposal queue: `proposals/pending/*.proposal.json`.
   - Compiled output: `compiled_wiki/`, read-only for peer agents and Obsidian.
   - This is the local-first mirror/proposal lane. Until an explicit bridge exists, it must not be treated as the same canonical source as Orbital's Firestore Agent Wiki.

## Source Truth

Load these files when relevant:

- `docs/specs/ORBITAL_KNOWLEDGE_GRAPH_SPINE_2026-05-15.md`
- `docs/specs/THIRD_SIGNAL_WIKI_ACTIVE_COGNITIVE_COMPENDIUM_2026-05-27.md`
- `docs/plans/2026-05-27-third-signal-wiki-librarian-daemon.md`
- `lib/librarian/parser.py`
- `lib/librarian/compiler.py`
- `lib/librarian/daemon.py`
- `scripts/librarian.ts`
- `lib/agentWikiCompendiumBridge.ts`
- `scripts/verify_agent_wiki_compendium_bridge.ts`
- `scripts/verify_librarian_proposal_contract.ts`
- `scripts/test_workspace_init.py`
- `tests/specs/test_proposal_parser.py`
- `tests/specs/test_page_compiler.py`
- `tests/specs/test_log_and_index.py`
- `tests/specs/test_librarian_daemon_loop.py`

## Authority Boundaries

ALFRED-Air, LANDSAT, Swarm, Research OS, Ghost, Donna, and operator-side helper agents may:

- read approved sources,
- draft proposals,
- emit status packets,
- produce evidence packets,
- write `.proposal.json` payloads to the local proposal queue when instructed,
- create cloud `librarian_wiki_proposals` only through approved Review Queue/LANDSAT Colab paths,
- cite source refs and Swarm trace IDs.

They must not:

- write directly to `compiled_wiki/`,
- write directly to `agent_wiki_*` canon collections,
- bypass #admin/operator review for public or canonical outputs,
- include raw local paths, credentials, emails, or private exports in proposals,
- claim a wiki update is canonical until the Librarian has committed it.

## Local Proposal Shape

Use this shape for local Active Cognitive Compendium proposals:

```json
{
  "proposal_id": "prop_node_yyyymmdd_topic",
  "swarm_trace_id": "trace_node_yyyymmdd_xxxx",
  "author": "alfred-air-macbook-air|landsat-mac-mini|codex",
  "submitted_at": "2026-05-28T00:00:00Z",
  "type": "new_concept|edit_page|append_log",
  "source_refs": ["repo://...", "gdrive://...", "linear://..."],
  "claims": [
    {
      "statement": "Atomic claim.",
      "evidence_label": "verified|observed|inferred"
    }
  ],
  "target_page_id": "page.system.crown",
  "proposed_markdown": "Markdown body, already redacted.",
  "meta_updates": {
    "tags": ["third-signal"],
    "visibility": "internal"
  }
}
```

Before writing or handing off a proposal, run proposed text through `lib/librarian/parser.py` redaction logic or equivalent local redaction.

## Verification Commands

Cloud canonical contract:

```bash
npm run agent-wiki:compendium-bridge:verify
npm run librarian:proposal-contract:verify
npm run agent-activity:contract:verify
```

Local Active Cognitive Compendium tests:

```bash
/Users/lenoxparis/miniconda/bin/python -m pytest tests/specs -q
```

Initialize local Google Drive workspace:

```bash
/Users/lenoxparis/miniconda/bin/python -c "from pathlib import Path; from scripts.test_workspace_init import init_workspace; init_workspace(Path('/Users/lenoxparis/Library/CloudStorage/GoogleDrive-treble.design@gmail.com/My Drive/Third Signal Lab'))"
```

Process local pending proposals:

```bash
/Users/lenoxparis/miniconda/bin/python -c "from pathlib import Path; from lib.librarian.daemon import process_pending_queue; workspace = Path('/Users/lenoxparis/Library/CloudStorage/GoogleDrive-treble.design@gmail.com/My Drive/Third Signal Lab'); print(f'Processed {process_pending_queue(workspace)} proposals.')"
```

## Agent Awareness Pattern

Git is the portable source of truth. This skill must be shipped from `.agent/skills/agent-wiki-librarian/` through mothership sync so ALFRED-Air, LANDSAT, Codex, Hermes, Warp/Oz, and future harnesses use the same memory contract.

Expected sync path:

```bash
~/conductor/repos/orbital-system/scripts/landsat_mothership_sync.sh
```

If a harness cannot see this skill, it should treat Agent Wiki/Librarian work as unsafe for autonomous canonical writes and fall back to a proposal-only packet.

## Decision Rule

If the output must appear inside Orbital/#admin/ALFRED runtime memory, use the cloud Librarian proposal path.

If the output is for local Obsidian-style reading, portable source packs, or LAN/off-cloud review, use the Active Cognitive Compendium proposal path.

If the same update belongs in both, create one source-grounded local proposal, convert it through `buildCloudLibrarianProposalFromCompendium`, route the resulting cloud proposal through the approved Librarian path, then mirror the approved summary locally.
