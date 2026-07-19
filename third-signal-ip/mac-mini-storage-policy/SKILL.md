---
name: mac-mini-storage-policy
description: "MANDATORY storage rules for the Mac Mini Sovereign Bridge. Use whenever writing files, creating directories, storing exports, or managing data on this machine. The internal SSD is small — bulk data goes to the 8TB external drive with symlinks for integration."
version: 1.0.0
author: Oz
platforms: [macos]
metadata:
  hermes:
    tags: [storage, mac-mini, external-drive, symlink, disk, sovereign-bridge]
---

# Mac Mini Storage Policy

**This machine has limited internal SSD. The 8TB external drive is the canonical bulk storage location.**

## The Rule

All bulk data — exports, archives, model weights, backups, media, logs — goes on the external drive. The internal SSD is reserved for:
- Git repo working copies (`~/conductor/repos/`)
- Application binaries and configs (`~/.hermes/`, `~/.agents/`)
- Transient build artifacts

Everything else → `/Volumes/Third Signal Lab HD/`

## Drive Layout

```
/Volumes/Third Signal Lab HD/
├── ollama/models/              # Ollama model weights (symlinked from ~/.ollama/models)
├── hermes/
│   ├── data/                   # HERMES_HOME for profiles on external drive
│   ├── workspaces/
│   └── archives/
├── archivist/                  # Wearable data exports (Limitless, OMI)
│   ├── limitless/
│   ├── omi/
│   └── manifests/
├── curator/                    # AI conversation exports (Gemini, ChatGPT, Claude, Manus)
│   ├── gemini/
│   ├── chatgpt/
│   ├── claude/
│   ├── manus/
│   ├── classified/
│   └── archive/
├── third-signal-mirror/        # Off-cloud DR bare clones
├── snapshots/                  # Nightly snapshots
└── hermes/data/profiles/       # Profile data (symlinked into ~/.hermes/profiles/)
```

## Symlink Convention

When an app expects data at a path on the internal SSD, create a symlink:

```bash
# Pattern: internal path → external drive
ln -sfn "/Volumes/Third Signal Lab HD/<target>" "<internal path>"
```

**Active symlinks on this machine:**
- `~/.ollama/models` → `/Volumes/Third Signal Lab HD/ollama/models`
- `~/.hermes/profiles/archivist` → `/Volumes/Third Signal Lab HD/hermes/data/profiles/archivist`
- `~/.hermes/profiles/curator` → `/Volumes/Third Signal Lab HD/hermes/data/profiles/curator`
- `~/.hermes/profiles/omi-dev` → `/Volumes/Third Signal Lab HD/hermes/data/profiles/omi-dev`
- `~/.hermes/profiles/librarian` → `/Volumes/Third Signal Lab HD/hermes/data/profiles/librarian`
- `~/.hermes/profiles/janitor` → `/Volumes/Third Signal Lab HD/hermes/data/profiles/janitor`

## Rules for All Agents

1. **Never write bulk data to the internal SSD.** If your output is >10MB or will grow over time, put it on the external drive.
2. **Check free space before large writes:** `df -h "/Volumes/Third Signal Lab HD/"` and `df -h /`
3. **Use dated subdirectories** for exports: `YYYY/MM/DD/` under the appropriate top-level folder.
4. **If the external drive is not mounted**, stop and alert the operator. Do NOT fall back to writing to the internal SSD.
5. **Verify symlinks before writing:** if you're writing to a path that should be symlinked, confirm the symlink is intact first.

## Drive Health Check

```bash
# Quick health check
df -h "/Volumes/Third Signal Lab HD/" /
ls -la ~/.ollama/models  # should be a symlink
ls -la ~/.hermes/profiles/archivist  # should be a symlink
```

If the drive disconnects, Ollama returns "model not found" and profile chats will fail. Reattach the drive and verify symlinks.
