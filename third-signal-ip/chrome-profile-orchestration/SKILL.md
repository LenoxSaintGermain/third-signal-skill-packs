---
name: chrome-profile-orchestration
description: Allows Hermes to programmatically identify, launch, and manage specific Google Chrome profiles on macOS based on active tasks.
---

# Chrome Profile Orchestration

This skill defines the interface and methods for solving the "Multi-Profile Problem." It allows the agent to intelligently launch separate Chrome environments (with their own cookies, logins, and GWS permissions) depending on whether the Operator is working on Third Signal, Career Concierge, or client deployments.

## The Profile Mapping on LANDSAT
We have mapped the physical Chrome folders on the Mac Mini to their respective identities and primary Google accounts:

*   **`Default` ("Person 1"):** The primary `lenoxparis` / Third Signal / **Treble Design** account (`treble.design@gmail.com`).
*   **`Profile 1` ("Style"):** Branding & Design (`stylebrewery@gmail.com`).
*   **`Profile 2` ("conciergecareerservices.com"):** The corporate/GWS profile for **Career Concierge** (`gws@conciergecareerservices.com`).
*   **`Profile 3` ("Jimmy"):** The **Jim Butler** developer/deployment profile (`lifecalendarai@gmail.com`).
*   **`Profile 4` ("Your Chrome"):** LSGP Consulting (`lsgp@foundrpack.com`).
*   **`Profile 5` ("elbert"):** Specialized work (`malefic.treble@gmail.com`).

## Commands and Execution

Use the `/Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py` Python utility to execute commands.

### 1. Identify Running Context
Check which Chrome profiles are active or open.

### 2. Launch Workspace on Demand (Context Switch)
When the Operator asks to shift tasks (e.g., "switch auth and chrome over to X"):
1. Capture/Save the current workspace in Open Notebook.
2. **Switch CLI Auth:** Run `gcloud config set account <profile_email>` to align terminal authentication with the target workspace.
3. **Launch Chrome:** Force-launch the target Chrome Profile with the exact project URLs (e.g., GCP console, GWS admin) using the `--launch` command.

**Examples:**
- Launch Career Concierge GCP Console:
  `python3 /Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py --launch "Profile 3" "https://console.cloud.google.com/?project=career-concierge"`
- Launch Third Signal Admin Dashboard:
  `python3 /Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py --launch "Default" "https://thirdsignal.ai/#admin"`

## Passive Scraper Workflow (The "Grab This" / "Ingest Active Tab" Protocol)

When the user asks you to "grab this," "ingest active tab," or extract raw context from Claude, ChatGPT, or Poe, **never attempt to force-navigate or hijack their active browser tab** by setting its URL. Instead, passively extract the focused screen content in-place.

### Pitfall: Claude Desktop vs. Chrome History
The Chrome History SQLite database **only** tracks pages visited *inside* the Chrome browser. 
Because the Operator primarily uses the native **Claude Desktop App** for day-to-day chat threads, standard conversational logs (`claude.ai/chat/*`) do **not** write to Chrome's history. 
- Only **Claude Design/Artifacts** links (`claude.ai/design/p/*`) land in Chrome's history because clicking those interactive previews automatically triggers Chrome to launch and show the full-screen view.
- To scrape conversational logs, you must either:
  1. Ask the Operator to open the chat inside Chrome Web (where the session is synchronized).
  2. Access the native Claude Desktop App's local databases on disk located under `~/Library/Application Support/Claude/IndexedDB`.

### In-Place Scrape Script (Python + AppleScript)
Use this pattern to copy the active tab's DOM content to the clipboard and save it without shifting the user's cursor or window state:

```python
import subprocess
import os
import re

# Simulate Cmd+A, Cmd+C on active window passively
applescript = """
tell application "Google Chrome"
    activate
end tell
tell application "System Events"
    tell process "Google Chrome"
        set frontmost to true
        key code 48 -- Tab to focus web body
        delay 0.2
        key code 48 -- Tab
        delay 0.2
        keystroke "a" using command down
        delay 0.5
        keystroke "c" using command down
        delay 0.5
    end tell
end tell
"""
subprocess.run(["osascript", "-e", applescript])
content = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout

# Get active tab metadata for clean routing
get_meta = """
tell application "Google Chrome"
    set activeTab to active tab of front window
    return (title of activeTab) & "|||" & (URL of activeTab)
end tell
"""
meta = subprocess.run(["osascript", "-e", get_meta], capture_output=True, text=True).stdout.strip()
title, url = meta.split("|||", 1) if "|||" in meta else ("Active_Tab", "")

# Save directly to Curator paths based on the domain (e.g. curator/claude, curator/chatgpt)
```

## Cookie & Profile Auditing
To discover which profile has an active, authenticated session for a specific domain (such as `claude.ai` or `chatgpt.com`), copy and query the Chrome Cookies SQLite databases on disk rather than guessing:

```bash
# Example query to check active cookies per profile
sqlite3 "/Users/lenoxparis/Library/Application Support/Google/Chrome/<Profile Name>/Network/Cookies" "SELECT host_key FROM cookies WHERE host_key LIKE '%claude.ai%';"
```

## Safety & Boundaries
- Never attempt to cross-pollinate cookies, history, or credentials between these profiles.
- Keep data isolation strict. If the Operator is in "Jimmy" profile, focus all research and code-deployments on Career Concierge. If in "Default", focus on Third Signal.