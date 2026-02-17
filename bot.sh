#!/usr/bin/env bash

# Adjust paths as needed
APP="$HOME/Documents/workspace/dict-bot"
VENV="$APP/dict-env"
PY="$VENV/bin/python"
SCRIPT="$APP/main.py"

# Simply pass everything to python.
"$PY" "$SCRIPT" "$@"