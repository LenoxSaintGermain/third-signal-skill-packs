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
