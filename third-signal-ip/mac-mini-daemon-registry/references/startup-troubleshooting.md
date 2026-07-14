# Startup Troubleshooting Notes

Use this file for recurring Mac Mini startup failures that are worth remembering but too session-specific for the main SKILL.md.

## LANDSAT sync resolves the wrong repo path from Donna/Hermes

Symptom:
- `landsat_mothership_sync.sh` reports `Repo not found: /Users/lenoxparis/.hermes/profiles/donna/home/conductor/repos/orbital-system`

Cause:
- Hermes profile sessions can run with a profile-scoped `HOME`, so scripts that derive repo paths from `$HOME` look under the profile home instead of the macOS account home.

Fix:
- Run with an explicit home:
  - `HOME=/Users/lenoxparis ./scripts/landsat_mothership_sync.sh`
- Or bypass `HOME` entirely:
  - `LANDSAT_REPO_DIR=/Users/lenoxparis/conductor/repos/orbital-system ./scripts/landsat_mothership_sync.sh`

Preferred hardening:
- For automation that may run from Hermes profiles, prefer explicit absolute env vars over `$HOME`-derived defaults.

## Librarian watcher exits with missing dotenv

Symptom:
- `launchctl print gui/$(id -u)/com.thirdsignal.librarian-watcher` shows repeated exits
- Watcher stderr includes `Error [ERR_MODULE_NOT_FOUND]: Cannot find package 'dotenv' imported from .../scripts/librarian.ts`

Fix:
1. `cd ~/conductor/repos/orbital-system`
2. `npm install`
3. `npm ls dotenv --depth=0`
4. If still absent, add or restore `dotenv` in the repo dependencies, then reinstall
5. Restart the agent:
   - `launchctl kickstart -k gui/$(id -u)/com.thirdsignal.librarian-watcher`

Verification:
- `launchctl print gui/$(id -u)/com.thirdsignal.librarian-watcher | egrep 'state =|last exit code =|pid ='`
- Confirm the watcher no longer reports `job state = exited`
- Check logs:
  - `~/conductor/repos/orbital-system/logs/librarian-watcher.err.log`
  - `~/conductor/repos/orbital-system/logs/librarian-watcher.out.log`

## Mac Mini M4 Hardware Power Reset (Undervoltage)

Symptom:
- The Mac Mini reboots unexpectedly overnight or mid-session.
- Diagnostic logs in `/Library/Logs/DiagnosticReports/ResetCounter-*.diag` contain the following boot failure details:
  ```
  Boot failure count: 1
  Boot faults: uv,vdd_boost_uvlo rst sgio
  ```
  (`uv` = undervoltage event; `vdd_boost_uvlo` = VDD Boost Under-Voltage Lock Out).

Cause:
- Sudden power fluctuation, dip, or brownout on the shared electrical circuit supplying the Mac Mini. The M4 power management detects insufficient voltage and triggers a hardware shutdown to prevent corruption.

Fix / Hardening:
- **Hardware UPS:** Install an **APC Back-UPS 600VA (Model BE600M1)** or a CyberPower 625VA/650VA flat desktop UPS. These are widely available on Facebook Marketplace in Pembroke Pines, FL, used for **$20 – $40** (or $90 brand new).
- **Graceful Shutdown:** Connect the UPS to the Mac Mini via USB and make sure PowerChute or macOS native energy settings are configured for graceful shutdown during extended blackouts.

## Port 9120-9129 Blocked / Desktop App Boot-Loops

Symptom:
- Desktop app launch fails with `ECONNREFUSED 127.0.0.1:9121` or `[Errno 48] address already in use` error and boot-loops endlessly.

Cause:
- Sudden hardware reset or crash left orphaned CLI/dashboard Python processes squatting on ports `9120-9129`. Because these are independent processes, macOS doesn't kill them when the Desktop app exits.

Fix:
- Trigger the boot cleanup LaunchAgent or run the script manually:
  ```bash
  /Users/lenoxparis/.hermes/scripts/hermes_boot_cleanup.sh
  ```
- Or manually kill the processes:
  ```bash
  kill -9 $(lsof -t -i :9120-9129 2>/dev/null)
  ```

Preventive Hardening:
- The `com.hermes.cleanup` LaunchAgent runs `/Users/lenoxparis/.hermes/scripts/hermes_boot_cleanup.sh` at user login. This script clears stale ports, kills orphaned processes, cleans up old lock files, and force-kills orphaned MCP servers (like `hermes-pilot-mcp` and `mcp-limitless`).
- The `hermes-pilot-mcp.mjs` has been updated with stdin EOF and close event handlers to ensure it naturally shuts down when its parent exits:
  ```javascript
  process.stdin.on('end', () => process.exit(0));
  process.stdin.on('close', () => process.exit(0));
  ```

## Profile Boots into First-Run Setup Screen (BWS Transition)

Symptom:
- Desktop app opens but displays the first-run configuration screen instead of loading the intended profile (e.g. `donna`), reporting credential or resolution failures.

Cause:
- The active profile's local `.env` is missing critical API keys (e.g., `GOOGLE_API_KEY`), which does not automatically inherit from the master `~/.hermes/.env`.

Fix / Modern BWS Setup:
- We have transitioned secret management to **Bitwarden Secrets Manager (BWS)**! All 23 master credentials have been synced into BWS Project ID `6de3305b-6f29-46b4-bc7a-b46501030712`.
- Enable BWS in each profile's `config.yaml` to auto-inject credentials from the cloud vault on boot, eliminating manual `.env` synchronization completely:
  ```yaml
  secrets:
    bitwarden:
      enabled: true
      project_id: "6de3305b-6f29-46b4-bc7a-b46501030712"
      access_token_env: BWS_ACCESS_TOKEN
      auto_install: true
      override_existing: true
  ```

## Model Strategy & Deprecated 404 Errors

Symptom:
- API calls fail with `HTTP 404: Gemini HTTP 404 (NOT_FOUND)` specifying that the model string is no longer available.

Cause:
- Deprecated Google preview model strings (e.g., `gemini-3-pro-preview`) have been turned off in the upstream API.

Fix:
- We have deployed our canonical **Multi-Agent Model Strategy** to align profiles based on capability vs. grunt-work requirements:
  * **Bleeding Edge / Reasoning (`donna`):** Configure with the absolute latest reasoning preview model: **`gemini-3.1-pro-preview`** (or newer).
  * **Knowledge Workers (`librarian`, `archivist`, `curator`):** Configure with **`gemini-3.5-flash`** (or newer).
  * **Workhorses / Grunts (`janitor`, `omi-dev`):** Configure with **`gemini-2.5-pro`** (highly stable, extremely capable previous-gen Pro model).
- Verify the model swap by querying the profile directly:
  ```bash
  /Users/lenoxparis/.local/bin/hermes -p <profile> chat -q "hello" --quiet
  ```

## WebUI Dashboard HTTP 429 Quota Exhausted

Symptom:
- The WebUI dashboard (port 9120 or 9121) loads with a blank screen, an infinite spinner, or throws an "Unauthorized/Connection Refused" crash overlay on first boot.

Cause:
- The React frontend fires an immediate configuration handshake (`/api/config`, `/api/models/status`) to populate available models. If your Google Gemini or OpenAI API keys are locked behind a billing/quota block (`RESOURCE_EXHAUSTED` / HTTP 429), the backend handshake fails, halting the frontend's render loop and crashing the UI before it draws.

Fix:
- Check Google AI Studio (or GCP Console) billing settings to ensure your credit card is active and you haven't exceeded your monthly paid-tier limit. Once the Google balance is topped up, the 429 blocks will clear, and the WebUI dashboard will load cleanly.


