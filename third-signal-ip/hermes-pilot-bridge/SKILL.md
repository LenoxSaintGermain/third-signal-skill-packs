---
name: hermes-pilot-bridge
description: Programmatic control of the macOS Hermes Pilot desktop overlay via local REST API.
tags: [hermes, desktop, pilot, integration, api]
---
# Hermes Pilot Bridge API

When native tools (`pilot_notify`, `pilot_ask`, `pilot_speak`) are unavailable or fail, you can control the Hermes Pilot desktop overlay directly via its local REST API using Python (`execute_code`).

## Credentials & Endpoint
- **Bridge File:** `~/.hermes-pilot/bridge.json`
- **Format:** `{"url": "http://127.0.0.1:7391", "token": "..."}`
- **Auth Header:** `Authorization: Bearer <token>`

## REST Endpoints & Payloads

### POST /notify
Displays a one-way message or spoken notification in the desktop overlay.
- **Payload:** `{"text": "Message content here", "speak": true}`
- **Pitfall:** The text field MUST be named `text`. Sending `{"message": "..."}` results in `400 Bad Request: text required`.

### POST /ask
Prompts the user for a response in the overlay. Blocks until they reply.
- **Payload:** `{"question": "Your question here?"}`
- **Pitfall:** The prompt field MUST be named `question`. Sending `{"text": "..."}` results in `400 Bad Request: question required`.
- **Response:** `{"ok": true, "answer": "<user input>"}`

## Architecture Reference
See `references/architecture.md` for the "One Mind, Two Modes" design pattern governing the Desktop Body and Agent Mind, and how they hand off tasks.

## Code Example (Python)
```python
import urllib.request, json

# 1. Read configuration
with open('/Users/lenoxparis/.hermes-pilot/bridge.json') as f:
    bridge = json.load(f)

# 2. Make request
req = urllib.request.Request(
    f"{bridge['url']}/notify", 
    data=json.dumps({"text": "Hello overlay!", "speak": False}).encode(),
    headers={"Authorization": f"Bearer {bridge['token']}", "Content-Type": "application/json"}
)

try:
    with urllib.request.urlopen(req) as response:
        print("SUCCESS:", response.read().decode())
except urllib.error.HTTPError as e:
    print("ERROR:", e.code, e.read().decode())
```

## Architecture & Mental Model
For a deep dive into the separation of concerns between the "Desktop Body" (Gemini Live) and the "Agent Mind" (Hermes Orchestrator), as well as why pushed notifications use local TTS instead of the premium model voice, see `references/architecture.md`.