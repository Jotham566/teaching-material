#!/bin/sh
# Local-only inference, started explicitly when grading is needed.
set -eu
course_model_root="$HOME/.local/share/iuea-ollama"
course_ollama="$course_model_root/ollama/0.34.0/libexec/ollama"
if [ ! -x "$course_ollama" ]; then
  course_ollama=$(command -v ollama || true)
fi
if [ -z "$course_ollama" ] || [ ! -x "$course_ollama" ]; then
  echo 'Install Ollama before starting local grading.'
  exit 1
fi
if command -v curl >/dev/null 2>&1 && curl --noproxy '*' -fsS --max-time 2 http://127.0.0.1:11434/api/version >/dev/null 2>&1; then
  echo 'Local Ollama is already running on 127.0.0.1:11434.'
  exit 0
fi
export OLLAMA_NO_CLOUD=1
export OLLAMA_HOST=127.0.0.1:11434
export OLLAMA_MODELS="$course_model_root/models"
exec "$course_ollama" serve
