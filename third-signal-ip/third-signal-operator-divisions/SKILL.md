---
name: third-signal-operator-divisions
description: Use when working on Third Signal, Orbital OS, ALFRED-Air, LANDSAT, Agent Wiki, Signal Spark, content publishing, NotebookLM source packs, YouTube/video workflows, or any cross-harness agent work that needs the Third Signal north star, department goals, safe authority boundaries, and handoff rules.
---

# Third Signal Operator Divisions

Use this skill when navigating the organizational boundaries, goals, and communication styles of the Third Signal Lab divisions.

*See `references/agent-readable-exports.md` for the standard on how to format exports with embedded system directives for autonomous consumption.*

## North Star

Third Signal is an agent-first single-operator lab.

The operator should increasingly work inside Orbital instead of juggling ChatGPT, Claude, Gemini, wrappers, and scattered tools. Agents should help synthesize research, harden the operating harness, preserve context, package ideas, produce media, distribute content, and route work through reviewable pipelines.

Core principle: agents may propose, prepare, draft, route, and explain. Canonical writes, production deploys, secret changes, and public publishing stay behind explicit authority gates.

## Source Truth

Load in this order when relevant:

1. Root `AGENTS.md` in the active repo.
2. `docs/ORBITAL_MANIFEST_2026.md`.
3. `docs/specs/ALFRED_AIR_HERMES_LOCAL_OPERATOR_2026-05-17.md`.
4. `docs/specs/LANDSAT_HERMES_MAC_MINI_SETUP.md`.
5. `docs/specs/LANDSAT_MODEL_BROKER_V0_2_HANDOFF_2026-05-15.md`.
6. `docs/specs/ORBITAL_KNOWLEDGE_GRAPH_SPINE_2026-05-15.md`.
7. `docs/specs/THIRD_SIGNAL_WIKI_ACTIVE_COGNITIVE_COMPENDIUM_2026-05-27.md` when working on the local Agent Wiki v2 / Obsidian / Google Drive compiled wiki lane.
8. `.agent/skills/agent-wiki-librarian/SKILL.md` when an agent needs executable rules for cloud Librarian canon versus local Active Cognitive Compendium proposals.
9. `docs/specs/RESEARCH_OS_LANDSAT_LANE_CONSOLIDATION_2026-05-22.md` when working on Research OS, `/research-push`, NotebookLM/source packs, LANDSAT evidence packets, #admin research review, or Research OS v2 migration.
10. `.agent/skills/landsat-research-os/SKILL.md` when an agent needs the executable Research OS lane contract.
11. `docs/goals/THIRD_SIGNAL_BACKLOG_UAT_GOAL_2026-05-17.md` when working on backlog completion, UAT readiness, or long-horizon Codex `/goal` runs.
12. `docs/goals/THIRD_SIGNAL_REVENUE_TRACTION_GOAL_2026-05-20.md` when working on traffic, revenue, offers, clients, launch campaigns, or content-to-sales operations.
13. `docs/specs/THIRD_SIGNAL_AGENTIC_BUSINESS_OS_1M_PLAN_2026-05-20.md` when designing the $1M single-operator agency system, Hermes identities, sales operating cadence, local-market research, or service packaging.
14. `docs/specs/THIRD_SIGNAL_INDUSTRIAL_ONSHORING_ACQUISITION_THESIS_2026-05-20.md` when working on industrial SMB acquisition, onshoring, automation integrators, MRO, specialized logistics, or macro-to-dealflow Signal Spark theses.
15. `docs/goals/THIRD_SIGNAL_PRE_UAT_PLUMBING_CLOSEOUT_GOAL_2026-05-21.md` when closing pre-UAT plumbing, agent activity visibility, local-agent reporting, cloud ALFRED status reads, or Orbital/#admin cockpit readiness.
16. `docs/goals/THIRD_SIGNAL_PERSONAL_CONTEXT_INGESTION_GOAL_2026-05-29.md` when organizing Obsidian, Google Drive, Google Workspace, ChatGPT, Claude, Gemini, Poe, Manus, Limitless, Omi, or other historical operator context.
17. `docs/goals/THIRD_SIGNAL_ORBITAL_DOCS_TO_OBSIDIAN_SYNC_GOAL_2026-05-30.md` when staging Orbital Librarian-known docs into the local Active Cognitive Compendium / Obsidian graph proposal lane.
18. `docs/specs/THIRD_SIGNAL_A2UI_NATIVE_AGENT_OS_RESET_2026-05-30.md` when working on Orbital/#admin UI overhaul, A2UI-native surfaces, Mission Canvas, trusted catalogs, ALFRED screen direction, or agent OS navigation consolidation.
19. `docs/goals/ALFRED_AIR_MACBOOK_AUTONOMY_GOAL_2026-05-31.md` and `.agent/skills/alfred-air-local-ops/SKILL.md` when working on MacBook Air local autonomy, Hermes skill visibility, Kanban, cleanup inventories, Obsidian/Compendium upkeep, ALFRED-Air schedules, or MacBook/LANDSAT divergence.
20. Linear issue context, if provided.
21. Live status packets:
   - `~/.agents/status/alfred-air/status-latest.json`
   - `~/.agents/status/alfred-air/codex-bridge-latest.json`

Environment posture:

- Production: `third-signal-v2`.
- Original `third-signal`: deferred recovery/archive only. Do not gate v2 UAT on it, and do not attempt migration unless the operator explicitly reopens recovery after Google restores data-plane access.
- Git is the portable source of truth between MacBook Air, Mac Mini LANDSAT, Codex, Hermes, Warp/Oz, and future harnesses.

## Divisions

### Portfolio Architecture (The Venture Studio)
**CRITICAL:** When discussing or presenting the Third Signal IP portfolio, you must maintain strict structural separation between back-office infra, front-office distribution, and physical IP. For example, "The Line" (back-office agent gateway) is distinct from "The Showcase" (presentation UI). "Orbital OS" (software) is distinct from "Orbital Climate Systems" (physical apparel).
See `references/venture-studio-portfolio-architecture.md` for the exact 8-part taxonomy and positioning of the studio's assets.

### ALFRED-Air Department

Mission: mobile/off-cloud operator companion on the MacBook Air.

ALFRED-Air should excel at:

- Keeping the operator productive while mobile.
- Running read-only repo/docs audits.
- Drafting specs, runbooks, content briefs, and proposed patches.
- Using `scripts/alfred_air_codex_bridge.sh` as a local Codex CLI tool lane when no provider keys are configured.
- Creating status packets and LANDSAT task packets.
- Preparing NotebookLM source packs from reviewed docs.
- Turning Signal Spark backlog items into research briefs, outlines, scripts, and campaign plans.
- Building read-only personal-context source inventories before any ingestion into the Active Cognitive Compendium.

Default authority: `proposal_only`.

Success metric: the operator can say an objective once and receive a traceable packet that Codex, LANDSAT, Librarian, or #admin can act on safely.

### LANDSAT Department

Mission: Mac Mini sovereign operations node and long-running local/private lane.

**Telegram Command Center (Group Chat Integration):** 
LANDSAT is designed to operate seamlessly via a unified Telegram Group (acting as a multi-agent cockpit) rather than 1-on-1 DMs. To configure a new group for LANDSAT:
1. **Disable Group Privacy:** Telegram blocks bots from reading group messages by default. Use `@BotFather` -> `/mybots` -> Bot Settings -> Group Privacy -> **Turn Off**.
2. **Disable Mention Requirement:** Hermes ignores untagged messages in groups by default. Run `hermes config set telegram.require_mention false` locally on LANDSAT and restart the gateway.
3. **Set Home:** Run `/sethome` in the group so background cron jobs route to the group chat instead of direct messages.

LANDSAT should excel at:

- Pulling mothership updates safely with fast-forward sync.
- Running local/private research and reconnaissance tasks.
- Preparing heavy or long-running jobs for Colab Lab Lane when approved.
- Maintaining local model/provider posture and reporting the active route truthfully.
- Producing evidence packs for Agent Wiki, NotebookLM, and content production.
- Supporting publishing work with source-grounded research, clips/assets inventories, and campaign scaffolds.
- Processing approved Omi, Limitless, Drive, Obsidian, and AI-app export batches into reviewable source packs.

Default authority: local specialist, proposal-only for canonical memory.

Success metric: LANDSAT turns scattered sources and local files into structured, cited, reviewable packages without exposing private files or bypassing authority gates.

Research OS posture: Research OS is a governed LANDSAT-backed capability lane by default, not a separate operator app. Use `landsat-research-os` for `/research-push`, cited evidence packets, NotebookLM source packs, #admin research review, and Librarian research proposals. Keep separate Research OS runtime boundaries only for private MCP/OIDC, Colab/Raziel notebooks, or future public research-library publishing.

### Librarian / Agent Wiki Department

Mission: institutional memory and canonical narrative.

Librarian owns canonical writes for Agent Wiki, Armory, Manifest, Chronicle, and Field Guide. Other agents propose. Librarian commits after review.

Librarian has two lanes: the cloud Agent Wiki canon that Orbital/#admin reads, and the local Active Cognitive Compendium that compiles Google Drive proposals into an Obsidian-ready `compiled_wiki/`. Use `agent-wiki-librarian` to decide which lane applies. Non-Librarian agents remain proposal-only in both lanes.

Success metric: the system can explain what changed, why it changed, where the proof is, and which agent/action produced it.

### Publishing / Signal Spark Department

Mission: convert Third Signal ideas into public-safe artifacts and distribution.

Content flywheel:

1. Select idea from Signal Spark backlog or operator brief.
2. Build source pack from repo docs, Agent Wiki claims, research notes, and approved artifacts.
3. Produce NotebookLM-ready notebook packet when useful.
4. Draft narrative: thesis, proof, storyboard, script, social cuts.
5. Route through review: accuracy, public-safety, brand voice, rights/privacy.
6. Publish only after explicit approval.
7. Feed results back into Agent Wiki/Armory/Manifest through Librarian proposals.
8. **Investor Pitch Validation:** For high-value MVP assets, use the NotebookLM validation pattern (see `references/notebooklm_analyst_validation.md`) to embed third-party audio analyst reviews into the data room.

Success metric: Third Signal can regularly publish grounded demos, essays, video scripts, shorts, and YouTube concepts from the operating memory without leaking private/internal material.

## Required Handoff Shapes

Status packet minimum:

```json
{
  "node_id": "alfred-air-macbook-air",
  "provider": "codex-cli|poe|openrouter|gemini|ollama|unknown",
  "model": "model-id-or-unknown",
  "sync_sha": "git-sha",
  "last_contact": "iso-8601",
  "mode": "proposal_only"
}
```

Task packet minimum:

```json
{
  "queued_by": "alfred-air-macbook-air",
  "target_node_id": "landsat-mac-mini",
  "objective": "clear objective",
  "classification": "public|internal|restricted",
  "requested_action": "read_only_audit|research_brief|docs_draft|proposed_patch|safe_local_skill|content_packet",
  "requires_operator_approval": true,
  "expected_output": "markdown plus compact json"
}
```

Content packet minimum:

```json
{
  "content_id": "signal_spark_or_generated_id",
  "source_refs": ["repo://...", "linear://...", "notebooklm://..."],
  "audience": "operator|public|investor|creator|operator-training",
  "format": "notebook|script|short|youtube_episode|blog|thread|demo_scene",
  "public_safety": "internal_only|public_safe_pending_review|approved",
  "next_review_surface": "#admin|operator|librarian"
}
```

Research evidence packet minimum:

```json
{
  "packet_id": "research_packet_...",
  "node_id": "landsat-mac-mini",
  "classification": "public|internal|operator-only|restricted|secret-ref-only|redacted",
  "public_safety": "internal_only|public_safe_pending_review|approved",
  "claims": [],
  "citations": [],
  "gaps": [],
  "recommended_handoff": "#admin|librarian|operator|ghost_observation|signal-card-review",
  "no_canonical_writes": true,
  "no_public_publish": true,
  "swarm_trace_id": "trace_landsat_yyyymmdd_xxxx"
}
```

## Platform & Gateway Quirks

- **Telegram Group Privacy:** Telegram bots cannot read group messages by default. When setting up a multi-agent or Sovereign Command Center in a private Telegram Group, the Operator MUST disable "Group Privacy" via @BotFather. Otherwise, the local gateway will only see explicit `@mentions` and will fail to register ambient commands or general chat.

## Safety Rules

- Do not deploy production, rotate/delete secrets, force-push, rewrite shared history, or publish public content without explicit approval.
- Do not move secrets into Git, prompts, screenshots, status packets, or notebooks.
- Do not claim a model/provider route unless the live response actually used it.
- Do not write canonical Agent Wiki, Armory, Manifest, or Field Guide records directly unless acting as the approved Librarian path.
- For public content, never surface raw internal claims. Use public-safe cards or approved source packs.
- If a request touches private exports from ChatGPT, Claude, Gemini, Limitless, Omi, email, or local files, classify it at least `internal` until reviewed.

## Useful Commands

Codex bridge smoke test:

```bash
~/conductor/repos/orbital-system/scripts/alfred_air_codex_bridge.sh "Return compact JSON confirming ALFRED-Air can call Codex safely."
```

ALFRED-Air interactive CLI:

```bash
~/conductor/repos/orbital-system/scripts/alfred_air_start.sh
```

Backlog/UAT goal packet:

```bash
~/conductor/repos/orbital-system/docs/goals/THIRD_SIGNAL_BACKLOG_UAT_GOAL_2026-05-17.md
```

Install this skill locally from the repo:

```bash
~/conductor/repos/orbital-system/scripts/install_third_signal_operator_skill.sh
```

LANDSAT sync:

```bash
~/conductor/repos/orbital-system/scripts/landsat_mothership_sync.sh
```

## Agent Behavior

When an agent using this skill receives a Third Signal task:

1. Identify which division owns the work.
2. Classify sensitivity: `public`, `internal`, or `restricted`.
3. Pick the safest lane: Codex, ALFRED-Air, LANDSAT, Librarian, #admin, or operator review.
4. Produce a packet, proposal, patch, or plan with source references.
5. Stop at authority boundaries instead of silently escalating.

## Additional Third Signal Operations
- **Archivist:** Extracting, normalizing, and backing up wearable AI data (Limitless, OMI) using extraction loops and cron jobs.
- **Vision OS UI:** Guidelines and code patterns for achieving Apple Vision OS-level fidelity in Third Signal web applications (see `references/third-signal-spatial-ui.md`).
- **Virtual Data Room:** Pattern for building an interactive Virtual Data Room (Agentic Pitch Deck) for investors.
