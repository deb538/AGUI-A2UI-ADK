#!/bin/bash
set -e
echo "=== CopilotKit ADK Agent ==="
cd "$(dirname "$0")"

# Install deps if needed
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate 2>/dev/null || source .venv/Scripts/activate

echo "Installing dependencies with uv..."
uv sync

echo "Starting ADK agent on port 8000..."
uv run uvicorn endpoint:app --host 0.0.0.0 --port 8000 --reload
