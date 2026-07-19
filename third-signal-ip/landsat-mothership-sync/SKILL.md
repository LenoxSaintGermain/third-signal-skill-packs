---
name: landsat-mothership-sync
description: Pull and apply approved Third Signal mother-ship updates on the LANDSAT/Hermes Mac Mini, including Orbital repo updates, Hermes prompt/config handoffs, local skill sync, Ollama/Gemini route posture, and health reporting. Use when updating LANDSAT from GitHub, refreshing Hermes instructions, checking the Sovereign Bridge, or coordinating with the local-ollama-switch skill.
---

# LANDSAT Mother-Ship Sync

Use this on the Mac Mini or from an agent controlling the Mini. The pattern is pull-based: the mother ship publishes desired state to GitHub/DB; LANDSAT pulls and applies approved updates. Do not expose Ollama or Hermes publicly.

## Source Order

1. GitHub `LenoxSaintGermain/orbital-system`, branch `codex/thi-91-orbital-key-hardening` unless Linear says otherwise.
2. `docs/specs/LANDSAT_HERMES_MAC_MINI_SETUP.md` for Hermes prompt, provider posture, and UAT missions.
3. `.agent/skills/landsat-mothership-sync/SKILL.md` for this sync workflow.
4. External Mini skill `~/.agents/skills/local-ollama-switch/SKILL.md`, if present, for Ollama/Gemini activation toggles.
5. Future DB control plane: Firestore `orbital` database collections `runtime_nodes`, `agent_update_directives`, and `agent_skill_inventory`.

## Safe Sync Workflow

1. Fetch the remote refs without changing the worktree:
   ```bash
   git -C ~/conductor/repos/orbital-system fetch origin --prune
   ```
2. Check local repo cleanliness:
   ```bash
   git -C ~/conductor/repos/orbital-system status --short --branch
   ```
3. If dirty, do not overwrite. Write a truthful `blocked_dirty_worktree` status packet containing the observed remote commit, ahead/behind counts, and changed files; then ask for operator approval.
4. Fast-forward only:
   ```bash
   git -C ~/conductor/repos/orbital-system pull --ff-only origin codex/thi-91-orbital-key-hardening
   ```
5. Refresh ecosystem repos:
   ```bash
   ~/conductor/repos/orbital-system/scripts/sync_third_signal_repos.sh
   ```
6. Sync local skills without deleting operator-authored skills:
   ```bash
   mkdir -p ~/.agents/skills
   rsync -a --exclude 'local-ollama-switch/' ~/conductor/repos/orbital-system/.agent/skills/ ~/.agents/skills/
   ```
7. Load `third-signal-operator-divisions` after sync for ALFRED-Air/LANDSAT department goals, content flywheel, and handoff authority boundaries.
8. If `~/.agents/skills/local-ollama-switch/SKILL.md` exists, read it before starting, stopping, or switching Ollama. Treat it as the canonical local activation control.
9. Verify LANDSAT health:
   ```bash
   tailscale status | grep mac-mini || true
   curl -fsS http://127.0.0.1:11434/api/version || true
   curl -fsS http://127.0.0.1:11434/api/tags || true
   ```
10. Report an artifact with: `node_id`, `git_commit`, `remote_commit`, `remote_observed`, `worktree_updated`, `skills_synced`, `third_signal_operator_divisions_present`, `local_ollama_switch_present`, `active_brain_provider`, `local_fallback_status`, `sync_status`, `health`, `errors`. The latest packet is mirrored to `~/.landsat/status/mothership-sync-latest.json`.

The background Librarian must not write Git-tracked Manifest Markdown. Firestore is automatic; a Markdown export requires a one-shot `--write-manifest-file` run and is refused in Librarian watch mode.

## Provider Posture

- Gemini API is the current primary Hermes/LANDSAT brain for speed-sensitive work.
- Ollama `gemma4:e4b` is the sovereign/private fallback and bridge-health target.
- `/api/tags` proves local fallback inventory only; it does not prove active Hermes brain.
- Never report `gemma4:e4b` as active unless Hermes is actually switched to Ollama.

## Update Boundaries

- Allowed: pull docs, prompts, skills, scripts, and non-secret config templates from GitHub.
- Allowed with explicit approval: update Hermes provider config, launchd plists, cron entries, or env contract values.
- Not allowed: public Ollama exposure, committed secrets, destructive git reset, direct Agent Wiki commits, or production DB writes.
- If the DB desired state conflicts with GitHub docs, stop and escalate to ALFRED/Librarian review.

## Local Ollama Switch Awareness

If the operator says any of these, delegate to `local-ollama-switch` if installed:

- "switch LANDSAT to local Ollama"
- "switch Hermes back to Gemini"
- "free RAM Ollama is using"
- "stop local Ollama"
- "turn LANDSAT back on"

If that skill is missing, do not improvise daemon changes beyond read-only checks unless the operator explicitly approves.
