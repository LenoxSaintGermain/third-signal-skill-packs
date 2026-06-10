# Cron Environment Context Pitfalls

When scheduling Hermes cron jobs that execute existing shell scripts on the host machine, you must account for the isolated runtime environment of the cron daemon.

## The `$HOME` Directory Trap

A Hermes cron job runs scoped to its active profile (e.g., `~/.hermes/profiles/donna`). If you schedule a cron job to execute an operator's existing shell script, and that script relies on `$HOME` (or implicitly expects `$HOME` to be `/Users/username`), the script will fail or look in the wrong directory. 

For example, a script trying to access `~/conductor/repos/...` will actually look in `~/.hermes/profiles/donna/home/conductor/repos/...` and throw a "Directory not found" error.

## The Solution: Explicit Wrapper Scripts

Do not run the target script directly in the cron definition. Instead, write a wrapper script that explicitly exports the necessary environment variables to simulate the operator's expected environment, then calls the target script.

**Example `wrapper.sh`:**
```bash
#!/usr/bin/env bash
# Wrapper to enforce correct paths for cron execution

# Hardcode the operator's actual home directory and expected env vars
export HOME="/Users/username"
export LANDSAT_REPO_DIR="/Users/username/conductor/repos/orbital-system"
export LANDSAT_SKILLS_DIR="/Users/username/.agents/skills"

# Execute the actual target script
/Users/username/conductor/repos/orbital-system/scripts/target_script.sh
```

Schedule the cron job to run this wrapper script to ensure perfect path resolution.