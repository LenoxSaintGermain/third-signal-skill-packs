# Hermes Pilot Architecture: "One Mind, Two Modes"

Hermes Pilot acts as the "Desktop Body" to the Hermes Agent's "Mind". They operate in a continuous loop:

## 1. The Desktop Body (Mini-Me)
- **What it is**: Electron/Svelte macOS overlay app.
- **Senses**: Real-time screen awareness (via JPEG frames), voice-native input/output (Gemini Live WebSocket).
- **Role**: Handles immediate, real-time, hands-free conversation and screen-context queries.

## 2. The Agent Mind (Donna Orchestrator)
- **What it is**: Persistent Hermes `donna` profile running locally.
- **Senses**: Text/Terminal, deep persistent memory, specialist sub-agents (archivist, librarian, etc.), cron jobs.
- **Role**: Handles depth, multi-step orchestration, research, and anything that outlives a single live conversation.

## 3. The Two-Way Handoff

### Body -> Mind (Delegation)
When the user asks the Desktop Body to do something complex (research, disk cleanup, background jobs), it uses the `delegate_to_agent` tool.
- This sends an OpenAI-compatible API request to the Agent Mind at `http://127.0.0.1:8643`.
- The Mind processes the request silently, and the Body speaks the Mind's response back to the user.

### Mind -> Body (Proactive Alerts)
When the Agent Mind finishes a background task or needs to ask the user a blocking question, it hits the local Bridge API.
- `POST http://127.0.0.1:7391/notify`: Pushes an alert to the overlay.
- `POST http://127.0.0.1:7391/ask`: Pops an overlay modal requesting input, returning it synchronously.
*(Auth token dynamically read from `~/.hermes-pilot/bridge.json`)*