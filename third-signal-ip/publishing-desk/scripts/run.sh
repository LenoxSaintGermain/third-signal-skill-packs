#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

candidates=()
if [[ -n "${PUBLISHING_DESK_PYTHON:-}" ]]; then
  candidates+=("$PUBLISHING_DESK_PYTHON")
fi
candidates+=(
  "$REPO_ROOT/.venv-harvest/bin/python"
  "/usr/bin/python3"
)
if command -v python3 >/dev/null 2>&1; then
  candidates+=("$(command -v python3)")
fi

for candidate in "${candidates[@]}"; do
  [[ -x "$candidate" ]] || continue
  identity="$($candidate -c 'import sys; print(sys.executable)' 2>/dev/null || true)"
  [[ -n "$identity" ]] || continue
  exec "$candidate" "$SCRIPT_DIR/publishing_desk.py" "$@"
done

echo "error: no working Python interpreter found; set PUBLISHING_DESK_PYTHON" >&2
exit 3
