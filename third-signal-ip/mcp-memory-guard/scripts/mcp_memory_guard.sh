#!/bin/zsh

# Guarded cleanup for MCP process leaks created by the ChatGPT/Codex app-server.
# It is intentionally conservative: only old, idle MCP roots and very large,
# idle ChatGPT renderers are eligible. It never kills the app-server itself.

set -u

STATE_DIR="${HERMES_HOME:-$HOME/.hermes}/runtime/mcp-memory-guard"
LOG_FILE="${MCP_MEMORY_GUARD_LOG:-$STATE_DIR/guard.log}"
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    --once) ;;
    --help|-h)
      print "Usage: mcp_memory_guard.sh [--dry-run] [--once]"
      exit 0
      ;;
    *) print -u2 "Unknown option: $arg"; exit 2 ;;
  esac
done

mkdir -p "$STATE_DIR"
if ! mkdir "$STATE_DIR/.lock" 2>/dev/null; then
  exit 0
fi
trap 'rmdir "$STATE_DIR/.lock" 2>/dev/null || true' EXIT

PYTHON="/usr/bin/python3"
[[ -x "$PYTHON" ]] || PYTHON="/opt/homebrew/bin/python3"
[[ -x "$PYTHON" ]] || { print -u2 "mcp-memory-guard: python3 not found"; exit 1; }

export STATE_DIR LOG_FILE DRY_RUN
# Do not use exec here: the parent shell owns the lock-directory cleanup trap.
"$PYTHON" - <<'PY'
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

STATE_DIR = Path(os.environ["STATE_DIR"])
LOG_FILE = Path(os.environ["LOG_FILE"])
DRY_RUN = os.environ.get("DRY_RUN") == "1"

# Safety thresholds. These are deliberately conservative for a 16 GB Mac.
STALE_MCP_SECONDS = 2 * 60 * 60
LARGE_MCP_KB = 768 * 1024
LARGE_RENDERER_KB = 1024 * 1024
RENDERER_MIN_AGE = 5 * 60
IDLE_CPU = 1.0
LARGE_IDLE_CPU = 2.0


def log(event, **fields):
    row = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "event": event, **fields}
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def elapsed_seconds(value):
    # ps etime: [[dd-]hh:]mm:ss
    try:
        days = 0
        if "-" in value:
            day_part, value = value.split("-", 1)
            days = int(day_part)
        parts = [int(x) for x in value.split(":")]
        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            hours, minutes, seconds = 0, *parts
        else:
            return 0
        return days * 86400 + hours * 3600 + minutes * 60 + seconds
    except (ValueError, TypeError):
        return 0


def snapshot():
    cmd = ["ps", "-axo", "pid=,ppid=,rss=,%cpu=,etime=,args="]
    out = subprocess.check_output(cmd, text=True, errors="replace")
    processes = {}
    for line in out.splitlines():
        fields = line.strip().split(None, 5)
        if len(fields) != 6:
            continue
        try:
            pid, ppid, rss = int(fields[0]), int(fields[1]), int(fields[2])
            cpu = float(fields[3].replace(",", "."))
        except ValueError:
            continue
        processes[pid] = {
            "pid": pid,
            "ppid": ppid,
            "rss_kb": rss,
            "cpu": cpu,
            "age": elapsed_seconds(fields[4]),
            "args": fields[5],
        }
    return processes


def descendants(processes, roots):
    children = {}
    for proc in processes.values():
        children.setdefault(proc["ppid"], []).append(proc["pid"])
    found = set()
    stack = list(roots)
    while stack:
        pid = stack.pop()
        for child in children.get(pid, []):
            if child not in found:
                found.add(child)
                stack.append(child)
    return found


def label(args):
    if "chrome-devtools-mcp" in args:
        return "chrome-devtools-mcp"
    if "mcp-remote" in args:
        return "mcp-remote"
    if "server.bundle.mjs" in args:
        return "mcp-server-bundle"
    if "server.mjs" in args:
        return "mcp-server"
    if "server.cjs" in args:
        return "mcp-server-cjs"
    if "--type=renderer" in args:
        return "chatgpt-renderer"
    return "other"


def is_mcp(args):
    return any(token in args for token in (
        "chrome-devtools-mcp", "mcp-remote", "server.bundle.mjs",
        "server.mjs", "server.cjs",
    ))


def is_app_server(args):
    return "app-server" in args and ("ChatGPT.app" in args or "Codex.app" in args)


def is_renderer(args):
    return "--type=renderer" in args and "ChatGPT.app" in args


def sample_cpu(pid):
    try:
        current = snapshot().get(pid)
        return None if current is None else current["cpu"]
    except (subprocess.SubprocessError, OSError):
        return None


def terminate_tree(processes, root, reason):
    targets = sorted(descendants(processes, [root]) | {root}, reverse=True)
    log("terminate", root_pid=root, process_count=len(targets), reason=reason,
        process_type=label(processes.get(root, {}).get("args", "")), dry_run=DRY_RUN)
    if DRY_RUN:
        return len(targets)
    for pid in targets:
        try:
            os.kill(pid, signal.SIGTERM)
        except (ProcessLookupError, PermissionError):
            pass
    time.sleep(2)
    for pid in targets:
        try:
            os.kill(pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
    return len(targets)


def main():
    processes = snapshot()
    app_roots = [p["pid"] for p in processes.values() if is_app_server(p["args"])]
    app_descendants = descendants(processes, app_roots)
    mcp_roots = [
        pid for pid in app_descendants
        if pid in processes and is_mcp(processes[pid]["args"])
        and processes[pid]["ppid"] in processes
    ]

    # Only evaluate MCP roots, not their helper children, to avoid duplicate kills.
    nested = set()
    for pid in mcp_roots:
        nested |= descendants(processes, [pid])
    mcp_roots = [pid for pid in mcp_roots if pid not in nested]

    candidates = []
    for pid in mcp_roots:
        p = processes[pid]
        idle_age = p["age"] >= STALE_MCP_SECONDS and p["cpu"] <= IDLE_CPU
        large_idle = p["rss_kb"] >= LARGE_MCP_KB and p["age"] >= 300 and p["cpu"] <= LARGE_IDLE_CPU
        if idle_age or large_idle:
            candidates.append((pid, "stale-idle" if idle_age else "large-idle"))

    # A process must remain idle across a second observation before termination.
    confirmed = []
    for pid, reason in candidates:
        cpu = sample_cpu(pid)
        if cpu is not None and cpu <= (IDLE_CPU if reason == "stale-idle" else LARGE_IDLE_CPU):
            confirmed.append((pid, reason))

    killed = 0
    for pid, reason in confirmed:
        if pid in processes:
            killed += terminate_tree(processes, pid, reason)

    # Protect against a single renderer accounting for most of the machine's RAM.
    # Renderer kills are only allowed when the process is both old and very large.
    processes = snapshot()
    renderer_kills = 0
    for pid, p in list(processes.items()):
        if not is_renderer(p["args"]):
            continue
        if p["age"] < RENDERER_MIN_AGE or p["rss_kb"] < LARGE_RENDERER_KB or p["cpu"] > LARGE_IDLE_CPU:
            continue
        cpu = sample_cpu(pid)
        if cpu is not None and cpu <= LARGE_IDLE_CPU:
            renderer_kills += terminate_tree(processes, pid, "large-idle-renderer")

    summary = {
        "app_server_roots": len(app_roots),
        "mcp_roots": len(mcp_roots),
        "mcp_candidates": len(confirmed),
        "terminated_processes": killed + renderer_kills,
        "dry_run": DRY_RUN,
    }
    log("run", **summary)
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log("error", error=type(exc).__name__, message=str(exc))
        print(f"mcp-memory-guard: {type(exc).__name__}: {exc}", file=sys.stderr)
        sys.exit(1)
PY
