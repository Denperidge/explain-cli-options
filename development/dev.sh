#!/usr/bin/env bash

# Go to development/script folder, thanks to https://stackoverflow.com/a/3355423
cd "$(dirname "$0")"

# Generate uv venv if needed
if [ ! -d .venv ]; then
    uv venv
    echo Generated venv...
fi

# Thanks to https://stackoverflow.com/a/2172367
# Show help if nothing is passed
if [ "$1" = "" ] || [[ "$1" == "-h" ]] || [[ "$1" == --h* ]] ; then
    echo "eco dev (re-run with action)"
    echo -----------
    echo "[SHOW HELP]: ./dev.sh -h/--help"
    echo "[GENERATE README]: ./dev.sh -r/--readme"
    echo "[RUN TESTS]: ./dev.sh -t/--test"
fi

if [[ "$1" == -r ]] || [[ "$1" == --r* ]]; then
    uv run mkdocs.py
fi

if [[ "$1" == -t ]] || [[ $1 == --t* ]]; then
    uv run pytest
fi
