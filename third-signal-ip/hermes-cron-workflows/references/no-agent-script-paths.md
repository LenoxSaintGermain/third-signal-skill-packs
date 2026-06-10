# Cronjob Script Path Resolution

When configuring `no_agent: true` cron jobs that run a bash `script`:

**The Pitfall**
The Hermes scheduler executes from the root context and looks for scripts in `~/.hermes/scripts/`. If your script lives inside a specific profile (e.g., `~/.hermes/profiles/librarian/scripts/run_librarian.sh`), the job will instantly fail with `No such file or directory`.

**The Fix**
Always symlink profile-specific cron scripts back to the root `scripts/` directory:
```bash
ln -sfn ~/.hermes/profiles/<profile>/scripts/my_script.sh ~/.hermes/scripts/my_script.sh
```
This ensures the scheduler can resolve the relative script name while keeping the actual file localized to its relevant profile.