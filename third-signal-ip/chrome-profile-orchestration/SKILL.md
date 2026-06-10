---
name: chrome-profile-orchestration
description: Allows Hermes to programmatically identify, launch, and manage specific Google Chrome profiles on macOS based on active tasks.
---

# Chrome Profile Orchestration

This skill defines the interface and methods for solving the "Multi-Profile Problem." It allows the agent to intelligently launch separate Chrome environments (with their own cookies, logins, and GWS permissions) depending on whether the Operator is working on Third Signal, Career Concierge, or client deployments.

## The Profile Mapping on LANDSAT
We have mapped the physical Chrome folders on the Mac Mini to their respective identities:

*   **`Default` ("Person 1"):** The primary `lenoxparis` / Third Signal account.
*   **`Profile 2` ("conciergecareerservices.com"):** The corporate/GWS profile for **Career Concierge**.
*   **`Profile 3` ("Jimmy"):** The **Jim Butler** developer/deployment profile (GCP, Cloud, GWS).
*   **`Profile 1` ("Style"):** Branding & Design.
*   **`Profile 5` ("elbert"):** Specialized work.

## Commands and Execution

Use the `/Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py` Python utility to execute commands.

### 1. Identify Running Context
Check which Chrome profiles are active or open.

### 2. Launch Workspace on Demand
When the Operator asks to shift tasks:
1. Capture/Save the current workspace in Open Notebook.
2. Force-launch the target Chrome Profile with the exact project URLs.

**Examples:**
- Launch Career Concierge GCP Console:
  `python3 /Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py --launch "Profile 3" "https://console.cloud.google.com/?project=career-concierge"`
- Launch Third Signal Admin Dashboard:
  `python3 /Users/lenoxparis/Third_Signal_Command_Cockpit/chrome_profile_manager.py --launch "Default" "https://thirdsignal.ai/#admin"`

## Safety & Boundaries
- Never attempt to cross-pollinate cookies, history, or credentials between these profiles.
- Keep data isolation strict. If the Operator is in "Jimmy" profile, focus all research and code-deployments on Career Concierge. If in "Default", focus on Third Signal.