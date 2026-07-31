---
name: manus-integration
description: "Programmatic task creation, tracking, and asset recovery via the Manus Developer API v2."
version: 1.0.0
author: Donna
platforms: [macos, linux]
metadata:
  hermes:
    tags: [manus, task-automation, api-integration, swarm-orchestration]
    related_skills: [codex, alfred-air-local-ops]
---

# Manus Integration Skill

Manus is an end-to-end autonomous task agent capable of building complete applications, writing books, or rendering movie sequences. This skill provides the definitive operational blueprint on how the Sovereign Swarm integrates with the **Manus Developer API v2** to trigger and manage high-value production workloads safely and cost-effectively.

## Strategy: The Swarm Delegation Pipeline

**Never use Manus for raw brainstorming or basic prompt editing.** Manus token execution in cloud sandboxes is expensive. 

Instead, follow this two-stage delegation pipeline:
1. **The Spec Generator (Omi-Dev / Donna):** Use cheap, fast models (like `gpt-5.4-mini` or `gemini-3.5-flash`) to brainstorm, outline, edit, and compile the *exact requirements, design spec, file layout, or storyboard*.
2. **The Executioner (Manus Profile):** Send that compiled, rock-solid prompt to the Manus API to execute the heavy-lifting, multi-step cloud-sandboxed construction.

---

## The Manus Client CLI Help

We have installed a native wrapper client on the Mac Mini at:
`~/.hermes/profiles/manus/scripts/manus_client.py`

### 1. Launch a New Task (Asynchronous)
Pass your compiled spec directly:
```bash
python3 ~/.hermes/profiles/manus/scripts/manus_client.py create --prompt "Build a dark-themed Next.js calendar widget matching this spec: <spec>"
```
*Returns the task ID (e.g., `task_f58a3621`).*

### 2. Poll Task Progress & Status
```bash
python3 ~/.hermes/profiles/manus/scripts/manus_client.py status --task-id <task_id>
```
*Status values include: `pending`, `running`, `completed`, `failed`.*

### 3. Send Follow-up Input / Feedback
If Manus asks for feedback or gets stuck, continue the thread:
```bash
python3 ~/.hermes/profiles/manus/scripts/manus_client.py send --task-id <task_id> --message "Great work, now add a clear-all events button."
```

---

## Direct REST API Reference (v2)

All API calls require the header: `x-manus-api-key: $MANUS_API_KEY`.

### Create Task
* **URL:** `POST https://api.manus.ai/v2/task.create`
* **Body:**
  ```json
  {
    "message": {
      "content": "Description of your task here",
      "connectors": []
    }
  }
  ```

### Get Task Detail
* **URL:** `GET https://api.manus.ai/v2/task.detail?task_id=<task_id>`

### Send Message
* **URL:** `POST https://api.manus.ai/v2/task.sendMessage`
* **Body:**
  ```json
  {
    "task_id": "YOUR_TASK_ID",
    "message": {
      "content": "Follow-up message"
    }
  }
  ```

---

## Pitfalls & Best Practices

* **The Local Desktop Sandbox:** The Mac Mini has `Manus.app` installed at `/Applications/Manus.app`. In local runs, Manus can interact directly with your system using the "My Computer" connector (`~/.manuspre.computer`). Protect your directories and ensure clean git statuses before starting local tasks.
* **Keep Track of Task IDs:** Every created task must be logged into our `#admin` review queue or local logs folder so that we do not lose track of running cloud tasks (which can take 5-15 minutes).
* **Verify Outputs:** Once Manus completes a task, pull the output branch or retrieve files, and run tests locally before merging.
