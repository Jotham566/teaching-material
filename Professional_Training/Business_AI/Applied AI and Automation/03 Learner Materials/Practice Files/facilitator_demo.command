#!/bin/zsh
set -eu
KLAI_SCRIPT_DIR="$(cd -- "$(dirname -- "$0")" && pwd)"
KLAI_PYTHON="$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3"
if [[ ! -x "$KLAI_PYTHON" ]]; then
  print -u2 "Teaching runtime missing. Use the guide's saved-output route; prepare the runtime before class."
  exit 1
fi
exec "$KLAI_PYTHON" "$KLAI_SCRIPT_DIR/facilitator_demo.py" "$@"
