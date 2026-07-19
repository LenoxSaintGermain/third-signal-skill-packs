---
name: mac-mini-daemon-registry
description: "CRITICAL registry of all persistent daemons, LaunchAgents, cron jobs, and background services running on the Mac Mini Sovereign Bridge. Use when setting up a new machine, auditing running services, troubleshooting missing automation, or verifying infrastructure after an OS update or hardware migration."
version: 1.0.0
author: Oz
platforms: [macos]
metadata:
  hermes:
    tags: [mac-mini, daemon, launchagent, cron, migration, infrastructure, sovereign-bridge]
---

# Mac Mini Daemon Registry

**This is the canonical list of every persistent service on the Mac Mini.**
Check this document when setting up a new machine, after an OS update, or when automation stops working.

## LaunchAgents (~\/Library/LaunchAgents/)

### com.landsat.ollama
- **Purpose:** Ollama model server bound to `0.0.0.0:11434`
- **Binary:** `/usr/local/bin/ollama serve`
- **Env:** `OLLAMA_HOST=0.0.0.0:11434`, `OLLAMA_MODELS=/Volumes/Third Signal Lab HD/ollama/models`, `OLLAMA_KEEP_ALIVE=24h`, `OLLAMA_LOAD_TIMEOUT=600`, `OLLAMA_MAX_LOADED_MODELS=1`, `OLLAMA_NUM_PARALLEL=2`
- **KeepAlive:** true (auto-restarts on crash)
- **Logs:** `/tmp/ollama.out.log`, `/tmp/ollama.err.log`
- **Status:** Currently stopped (Gemini is active provider). Activate via `local-ollama-switch` skill.

### com.landsat.ollama-warmup
- **Purpose:** Pre-loads Ollama model into VRAM at boot
- **Behavior:** Polls `/api/tags` until daemon responds, then sends one prompt to force model load
- **KeepAlive:** false (runs once per boot)
- **Logs:** `/tmp/ollama-warmup.out`, `/tmp/ollama-warmup.err`, `/tmp/ollama-warmup.log`
- **Depends on:** com.landsat.ollama

### com.thirdsignal.librarian-watcher
- **Purpose:** Filesystem watcher for Librarian proposal intake pipeline
- **Binary:** `/opt/homebrew/bin/npx tsx scripts/librarian.ts --watch`
- **WorkingDirectory:** `~/conductor/repos/orbital-system`
- **KeepAlive:** true (auto-restarts)
- **Logs:** `~/conductor/repos/orbital-system/logs/librarian-watcher.out.log`, `~/conductor/repos/orbital-system/logs/librarian-watcher.err.log`
- **ThrottleInterval:** 30 seconds between restarts

### com.thirdsignal.donna-gateway
- **Purpose:** Donna's always-on gateway — Jarvis-like orchestrator interface
- **Binary:** `/Users/lenoxparis/.local/bin/donna gateway run`
- **KeepAlive:** true (auto-restarts)
- **Logs:** `/Volumes/Third Signal Lab HD/hermes/data/profiles/donna/logs/gateway.out.log`
- **Model:** GPT-5.4 via OpenAI
- **Delegation:** max 5 concurrent children, depth 2, 60 iterations

### com.thirdsignal.mirror (if installed)
- **Purpose:** Nightly off-cloud bare-clone mirror of GitHub repos
- **Schedule:** 2:00 AM daily
- **Script:** `~/conductor/repos/orbital-system/scripts/mirror_repos.sh`
- **Logs:** `/Volumes/Third Signal Lab HD/hermes/archives/mirror.log`

## Cron Jobs (crontab -l)

| Schedule | Command | Purpose |
|----------|---------|---------|
| `*/30 * * * *` | `landsat_mothership_sync.sh` | Pull latest from Air's pushes, sync skills |
| `0 */4 * * *` | `run_librarian.sh` | Periodic librarian run (non-watch mode) |
| `0 3 * * *` | Ollama keep-alive ping | Refresh 24h VRAM hold (when Ollama is active) |
| `0 */6 * * *` | `thermal_decay.ts` | Thermal decay scoring (old orbital path) |
| `0 6 * * *` | `archivist --oneshot` | Daily Limitless + OMI data pull |
| `0 2 * * 0` | `curator --oneshot` | Weekly scan for new AI conversation exports |
| `0 3 * * 1` | `janitor --oneshot` | Weekly disk usage report |

## Tailscale Services

### tailscale serve
- **Port 8642** → `http://127.0.0.1:8642` (Hermes API server)
- **URL:** `http://mac-mini.tail4608aa.ts.net:8642/`
- **Persistent:** Yes (survives reboots)
- **Disable:** `tailscale serve --http=8642 off`

### tailscale up
- **Flags:** `--accept-routes`
- **IP:** `100.71.149.80`

## Hermes Profiles (symlinked from 8TB drive)

All profile data lives on `/Volumes/Third Signal Lab HD/hermes/data/profiles/`.
Symlinks in `~/.hermes/profiles/` point there.

| Profile | Model | Provider | Gateway |
|---------|-------|----------|---------|
| default | gemini-3.5-flash | google | Desktop-managed |
| archivist | gemini-3-flash-preview | gemini | on-demand |
| curator | gpt-5.4 | auto (OpenAI) | on-demand |
| omi-dev | gpt-5.4 | auto (OpenAI) | on-demand |
| librarian | gemini-3-pro-preview | gemini | on-demand |
| janitor | gemini-3-flash-preview | gemini | on-demand |
| poe-hub | Claude-Sonnet-4.8 | custom (Poe) | on-demand |
| donna | gpt-5.4 | auto (OpenAI) | **always-on** (LaunchAgent) |

## Verification Commands

Run these after a machine setup or OS update to confirm everything is in place:

```bash
# 1. All LaunchAgents loaded
launchctl list | grep -E 'landsat|thirdsignal'

# 2. All cron jobs
crontab -l

# 3. Tailscale up and serving
tailscale status
tailscale serve status

# 4. Hermes gateway responding
curl -fsS http://127.0.0.1:8642/health

# 5. Ollama (if active)
curl -fsS http://127.0.0.1:11434/api/tags

# 6. Profile symlinks intact
ls -la ~/.hermes/profiles/

# 7. External drive mounted
ls "/Volumes/Third Signal Lab HD/" > /dev/null && echo "drive OK"

# 8. Librarian watcher running
ps aux | grep librarian | grep -v grep

# 9. Mothership sync log
tail -5 /tmp/landsat-mothership-sync.log
```

## Migration Checklist

When moving to a new Mac Mini:

1. ☐ Mount external drive at `/Volumes/Third Signal Lab HD/`
2. ☐ Install Homebrew, Tailscale, Ollama, Node, pnpm, jq, git
3. ☐ Run `bootstrap_mac_mini.sh` (handles steps 3-8 below)
4. ☐ Clone repos to `~/conductor/repos/`
5. ☐ Symlink `~/.ollama/models` → external drive
6. ☐ Symlink `~/.hermes/profiles/*` → external drive profiles
7. ☐ Copy API keys into all profile `.env` files
8. ☐ Install all LaunchAgents from this registry
9. ☐ Set up cron jobs from this registry
10. ☐ Configure Tailscale serve for port 8642
11. ☐ Apply no-sleep policy (`pmset`)
12. ☐ Run verification commands above
13. ☐ Test from MacBook Air: `curl http://mac-mini.tail4608aa.ts.net:8642/health`
