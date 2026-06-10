# Automated Git Syncs in Cron

When writing `no_agent: true` cron scripts that perform automated `git push` operations, always account for remote changes to avoid silent pipeline failures (e.g. `[rejected] main -> main (fetch first)`).

## The Safe Sync Pattern

```bash
# 1. Stage changes
git add .

# 2. Check for changes and commit locally
if git diff --cached --quiet; then
    echo "No local changes."
else
    git commit -m "chore: automated sync"
fi

# 3. Pull with rebase to integrate any remote changes
git pull --rebase origin main

# 4. Push safely
git push origin main
```

Failing to commit local changes before pulling, or failing to pull before pushing, will cause the automated script to break if the remote repository has been updated from another machine or by another agent.
