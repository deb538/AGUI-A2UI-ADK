@echo off
echo === CopilotKit ADK Agent ===
cd /d "%~dp0"

REM Install deps if needed
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Installing dependencies with uv...
uv sync

echo Starting ADK agent on port 8000...
uv run uvicorn endpoint:app --host 0.0.0.0 --port 8000 --reload
