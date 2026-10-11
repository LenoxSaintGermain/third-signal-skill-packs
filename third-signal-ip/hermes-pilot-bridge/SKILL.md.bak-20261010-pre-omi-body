---
name: hermes-pilot-bridge
description: Architecture and programmatic control of the Hermes Pilot desktop overlay (Donna's Desktop Body).
trigger:
  - "notify via pilot"
  - "ask via pilot"
  - "pilot_notify"
  - "pilot_ask"
  - "hermes pilot architecture"
---
# Hermes Pilot Bridge & Dual Architecture

Hermes Pilot is the "Desktop Body" to Hermes' "Agent Mind".

## The Division of Labor (One Mind, Two Modes)
1. **Desktop Body (Hermes Pilot & Operator Dashboard):** Fast, immediate, voice-native (Gemini Live), and screen-aware. Houses the A2UI Spatial Canvas (infinite void, spatial graph nodes, Ghost Caddy command module). Handles real-time conversation and immediate hands-on UI interaction.
2. **Agent Mind (Hermes Orchestrator):** Deep, persistent memory, delegation to specialists, background cron tasks, and Orbital/Third Signal orchestration.

### Operator Dashboard Backend Integration
The A2UI Spatial Canvas integrates with the Agent Mind via two distinct paths:
- **The Nervous System (Passive):** A plugin (e.g., `signal-surface-telemetry` in `~/.hermes/profiles/donna/plugins/`) exposes `/api/telemetry/*` HTTP routes. The UI reads this SSE stream to map active `run_id` events to physical X/Y coordinates on the canvas (copper execution nodes, swarm radar/constellations). Hermes is unaware of this passive observation; it just runs inside the gateway.
- **The Mind (Active):** A skill (e.g., `operator-briefing` in `~/.hermes/profiles/donna/skills/`) is autoloaded into Hermes' context. The Ghost Caddy explicitly requests Hermes to generate ranked JSON briefings, which are then actively rendered as cyan institutional node clusters. SOUL.md does not mention the dashboard; Hermes' awareness of the UI is entirely through executing this briefing skill.

## Operator Dashboard Backend Integration
The Operator Dashboard operates alongside the Hermes Pilot overlay and relies on two distinct data flows:
1. **The Nervous System (Passive Telemetry):** Provided by the `signal-surface-telemetry` plugin (in `~/.hermes/profiles/donna/plugins/`). It passively adds `/api/telemetry/*` HTTP routes, streaming real-time execution state (tool runs, statuses) so the A2UI canvas can physically spawn and move execution nodes (Copper hazard borders). Hermes is largely unaware of this passive plumbing.
2. **The Mind (Active Briefing):** Provided by the `operator-briefing` skill (in `~/.hermes/profiles/donna/skills/`). The Ghost Caddy actively invokes this autoloaded skill to compose the ranked institutional briefing JSON, which spawns the high-level decision clusters (Cyan data streams).

## The Handoff (Body → Mind)
When the user asks the Pilot overlay to perform tasks requiring memory, long-running processes, or specialized subagents, Pilot uses its internal `delegate_to_agent` tool to route the prompt to the local Hermes server at `http://127.0.0.1:8643`. Pilot then speaks the Agent Mind's response.

## Programmatic Control (Mind → Body)
When the Agent Mind needs to proactively alert the user or ask a blocking question via the desktop overlay, it hits the Pilot Bridge running at `http://127.0.0.1:7391`.

*(Note: Use native `pilot_notify`, `pilot_speak`, or `pilot_ask` tools when available in your context. Use the Python snippets below as fallbacks if the native tools haven't dynamically synced yet).*

Auth token is dynamically read from `~/.hermes-pilot/bridge.json`.

### 1. Notify
```python
import urllib.request, json
with open('/Users/lenoxparis/.hermes-pilot/bridge.json', 'r') as f:
    config = json.load(f)
req = urllib.request.Request(f"{config['url']}/notify", 
    data=json.dumps({"text": "Your message", "speak": True}).encode(),
    headers={"Authorization": f"Bearer {config['token']}", "Content-Type": "application/json"})
urllib.request.urlopen(req)
```

### 2. Ask (Blocks until user replies)
```python
import urllib.request, json
with open('/Users/lenoxparis/.hermes-pilot/bridge.json', 'r') as f:
    config = json.load(f)
req = urllib.request.Request(f"{config['url']}/ask", 
    data=json.dumps({"question": "Your question?"}).encode(),
    headers={"Authorization": f"Bearer {config['token']}", "Content-Type": "application/json"})
print(urllib.request.urlopen(req).read().decode())
```

## 3. Pitfalls & Troubleshooting: macOS Permissions
When actively developing the Hermes Pilot Electron app and re-packaging it (`npm run pack`), the cryptographic signature of the `.app` binary changes. macOS sees this as a completely new, untrusted application.
- **The Issue:** This instantly invalidates previous Accessibility and Input Monitoring permissions. If using native hooks like `uiohook-napi` (for the `++` autocomplete trigger), it can cause aggressive permission prompt loops or crash the listener.
- **The Fix in Code:** Always wrap global keyboard hook initialization in a `try/catch` and immediately unmount/disable the feature if it fails to start.
- **The Fix in macOS:** To clear the permission cache, go to **System Settings -> Privacy & Security -> Accessibility / Input Monitoring**, select "Hermes Pilot", click the minus (`-`) button to delete it completely, then re-trigger the prompt to grant fresh permissions to the new binary.

## 4. Operator Dashboard (A2UI Spatial Command Center)
The Operator Dashboard operates alongside the Hermes Pilot overlay and serves as a proactive **Spatial Command Center** (abandoning linear chat interfaces). 

**Aesthetic & Mechanics (DIRTY Protocol):**
- Dark void grid substrate, glassmorphism panels.
- Cyan for active/nominal rails.
- Copper/orange for tasks requiring human pressure or intervention.
- Infinite panning, semantic zooming, with bezier curves indicating causality.

**Node Architecture:**
- **Briefing (Anchor):** Consumes `operator-briefing` skill for big-number telemetry.
- **Needs You (Triage):** Un-ignorable queue of blocked tasks (e.g. OpenWOP Confidence Escalation < 0.5) with direct resolution buttons.
- **Handled (Audit):** Transient ticker of autonomous swarms/cron completions.
- **Sandbox (Workspace):** Pop-out context nodes for active drafting/reviewing.
- **System & Signals:** Hardware telemetry and MCP inbound pressure equalizers.

**Backend Integration & Telemetry Patterns:**
- **Passive (Nervous System):** A gateway plugin (`signal-surface-telemetry`) adds `/api/telemetry/*` HTTP routes. The UI consumes this to spatialize execution nodes.
- **Active (Mind):** An autoloaded skill (`operator-briefing`) gives Hermes the context to compose ranked JSON briefings when demanded.
- **Live Plugin Architecture:** For standalone Spatial OS plugins, avoid importing core Python singletons (like `CronScheduler`). Read directly from SQLite (`state.db`, `kanban.db`) and JSON configs (`jobs.json`) using a background FastAPI/WebSocket thread. See `references/spatial-os-backend-patterns.md` for the exact decoupling code.
*Crucial context:* Hermes' core SOUL does not explicitly mention the dashboard; awareness lives purely in the loaded briefing skill.

## 5. The "Fleshie Comms Hub" Rule (User Preference)
When building UI nodes for Sessions or Chat, **never abstract them as generic system monitors** (e.g., just showing "Telegram - Active"). Fleshie operators require context and actionability.
- **Preview:** Always show the `last_message_preview` and `last_actor`.
- **Drill-down:** Clicking the node must open an Inspector Panel with an alternating left/right chat transcript, not a JSON metadata dump.
- **Action:** Include a `[REPLY]` button that instantly intercepts the click and auto-focuses the global Command Palette with `/resume <session_id> `.

## 6. Pitfalls: Native Modules & Git Worktrees
When working on the Hermes Pilot Electron codebase, **do not use temporary `git worktree` directories** (e.g., `/tmp/pilot-review`) for `npm install` or `npm run dev`. Native C++ modules like `ffi-napi` rely on exact Node header paths and macOS environment variables. Rebuilding them in `/tmp/` will fail with `node-gyp` compilation errors. Always develop, branch, and run the dev server from the main cloned repository.

## 6. Pitfalls & Troubleshooting: A2UI Canvas / Spatial UI Plugin Development
When adapting a Vite/React frontend (like the Hermes Board or A2UI Canvas) into a Hermes Python plugin, **do not serve the compiled `dist/` directory via `http.server` in `__init__.py` during active design mode**. Serving the static bundle breaks Hot Module Replacement (HMR) and results in a dead UI that doesn't reflect your live code changes.
- **The Fix:** Run the Vite dev server natively (`npm run dev` running on port 5173) in the background. The Python plugin wrapper should only register the slash command (e.g., `/board`) and redirect the browser to `http://localhost:5173`. Only serve the static `dist/` folder via Python for the final production build.

## 7. Pitfalls & Troubleshooting: TTS Voice Fallback
- **The Issue:** If `pilot_speak` or `pilot_notify` outputs a generic/robotic macOS system voice instead of the expected custom voice (e.g., ElevenLabs), the Pilot app's custom TTS pipeline has failed or disconnected, causing it to fall back to the native OS Web Speech API (`say` command).
- **The Fix:** Re-wire or verify the ElevenLabs TTS config inside the Hermes Pilot Electron app to ensure the custom audio output routing is active.