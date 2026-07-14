# Spatial OS Backend Patterns

When building a Hermes Python Plugin that powers a live React/Vite Spatial OS (like the Hermes Board or A2UI Canvas), you must stream live agent state (sessions, swarms, cron) to the frontend without crashing or blocking the main Hermes runtime.

## 1. The FastAPI WebSocket Bridge
Do not use `http.server` for live UI plugins. It lacks WebSocket support and cannot handle hot-module reloading well.
Instead, use `FastAPI` and `uvicorn` in a background daemon thread:

```python
import threading
import asyncio
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

async def data_pump():
    while True:
        await asyncio.sleep(4.0)
        state = get_live_hermes_state()
        # Broadcast state to active WebSocket connections...

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(data_pump())

def serve():
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT, log_level="warning")
    server = uvicorn.Server(config)
    server.run()

# Start background server inside the plugin's __init__.py
server_thread = threading.Thread(target=serve, daemon=True)
server_thread.start()
```

## 2. Decoupling from Singletons (Disk-First Reads)
Trying to import and instantiate Hermes core singletons (like `CronScheduler` or `SessionManager`) inside a plugin's background thread is extremely dangerous. It often leads to environmental clashes, cyclic imports, or thread-safety locks.

Instead, read the underlying state stores directly from disk using the standard library.

### Reading Sessions (`state.db`)
Read the SQLite database directly to build the "Fleshie Comms Hub":
```python
import sqlite3, os
state_db = os.path.expanduser("~/.hermes/state.db")
conn = sqlite3.connect(state_db)
conn.row_factory = sqlite3.Row
c = conn.cursor()
c.execute("SELECT id, source, title, started_at, ended_at, message_count FROM sessions ORDER BY started_at DESC LIMIT 5")
# Map 'source' to platform (Telegram, CLI, API) and 'ended_at' to Active/Idle status
```

### Reading Swarms (`kanban.db`)
Read active tasks and worker traces directly from the Kanban SQLite board:
```python
kanban_db = os.path.expanduser("~/.hermes/kanban.db")
conn = sqlite3.connect(kanban_db)
# Query for tasks WHERE status IN ('ready', 'running') to plot swarm execution nodes.
```

### Reading Cron Jobs (The Portability Trick)
Do not import `hermes.cron.scheduler`. It will fail or hang outside the main process. 
Instead, dynamically parse the raw JSON schedule files across all profiles:
```python
import glob, json
cron_files = glob.glob(os.path.expanduser("~/.hermes/profiles/*/cron/jobs.json"))
for file in cron_files:
    with open(file, "r") as f:
        jobs = json.load(f)
        # Parse active statuses, cadences, and outputs for the UI
```
This guarantees the plugin stays perfectly decoupled from the core Python runtime while still providing millisecond-accurate telemetry to the Spatial OS.