---
name: third-signal-utilities
description: Use when deploying, building, syncing, or fixing Third Signal custom desktop tools on any of Lenox's Macs — Hermes Pilot (macOS AI overlay, Cmd+J chat, Donna voice, agent bridge on 127.0.0.1:7391), permission/TCC/codesign issues with these tools, or when deciding where a new custom agentic utility should live.
---

# Third Signal Agentic Utilities

## Overview

All Third Signal custom tools live in one monorepo. Each tool ships with an agentic README that is the **deployment contract** — follow it top to bottom; every step encodes a failure that already happened.

**Repo:** `https://github.com/LenoxSaintGermain/third-signal-agentic-utilities` (private)
**Canonical local clone (Mac mini):** `/Volumes/Mini_2T/lenoxparis data/Dev/third-signal-agentic-utilities`

## Workflow

1. Clone or `git pull` the repo (it is private — `gh auth status` / SSH key must work on the machine first).
2. Read root `AGENTS.md` (operating contract), then `tools/<tool>/README.md`.
3. Follow the tool README exactly. Deploy scripts are in `tools/<tool>/scripts/` and are idempotent.

## Tools

| Tool | What | Deploy |
|---|---|---|
| `tools/hermes-pilot` | macOS AI overlay + agent→user bridge | `scripts/make-signing-cert.sh` (once per machine) → build per README → `scripts/install-app.sh` |
| `tools/omi-ocr-repair` | Local Omi DB OCR Indexing Daemon + Compiled Swift OCR Engine | See `references/omi-ocr-repair.md` for compilation & database patching scripts |

## Critical rules (full detail in repo)

- TCC permission loops on these tools = signing identity problem. Never sign ad-hoc; use the per-machine stable cert (`make-signing-cert.sh`).
- Never SIGKILL Hermes Pilot (CGEventTap can freeze the Mac's keyboard) — quit via `osascript -e 'quit app "Hermes Pilot"'`.
- No secrets in the repo; keys go in `~/.hermes/.env` on each machine (Hermes Pilot needs `GOOGLE_API_KEY` with Gemini access — ask the user for it if absent).
- New tools: one self-contained folder under `tools/`, agentic README, idempotent scripts, update this skill's table + reinstall to `~/.agents/skills/`.
