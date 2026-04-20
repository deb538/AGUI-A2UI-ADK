"""
Google ADK agent that mirrors the LangGraph agent functionality.

Supports:
- query_data: query the CSV database
- manage_todos / get_todos: todo management
- search_flights: A2UI fixed-schema flight cards
- generate_a2ui: A2UI dynamic-schema UI generation

Uses AI Credits or OpenAI via LiteLLM routing.
"""

import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from ag_ui_adk import AGUIToolset

# ---------------------------------------------------------------------------
# Environment setup (mirrors sibling project pattern)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent  # my-app root

# Load .env.local (preferred), then .env from adk-agent dir, then project root
for env_path in [
    ROOT / ".env.local",
    ROOT / ".env",
    PROJECT_ROOT / ".env.local",
    PROJECT_ROOT / ".env",
]:
    if env_path.exists():
        try:
            load_dotenv(env_path)
        except Exception:
            pass

# Map AI Credits key → OPENAI_API_KEY / OPENAI_API_BASE for LiteLLM
_ai_key = os.getenv("AI_CREDIT_API_KEY") or ""
_openai_key = os.getenv("OPENAI_API_KEY") or ""

# Detect sk-live- keys that belong to AI Credits
if _openai_key.startswith("sk-live-") and not _ai_key:
    _ai_key = _openai_key

if _ai_key:
    os.environ.setdefault("OPENAI_API_KEY", _ai_key)
    os.environ.setdefault(
        "OPENAI_API_BASE",
        os.getenv("AI_CREDIT_BASE_URL") or "https://api.aicredits.in/v1",
    )
elif _openai_key:
    os.environ.setdefault("OPENAI_API_KEY", _openai_key)

# Startup logging
logging.basicConfig(level=logging.INFO)
_log = logging.getLogger(__name__)
_has_key = bool(os.getenv("OPENAI_API_KEY"))
_masked = None
if _has_key:
    _k = os.environ["OPENAI_API_KEY"]
    _masked = (_k[:4] + "..." + _k[-4:]) if len(_k) > 12 else "(set)"
_log.info("OPENAI_API_KEY present=%s masked=%s", _has_key, _masked)
_log.info("OPENAI_API_BASE present=%s value=%s", bool(os.getenv("OPENAI_API_BASE")), os.getenv("OPENAI_API_BASE", ""))

# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------
from google.adk.agents.llm_agent import Agent
from google.genai.types import GenerateContentConfig

from .tools import query_data, manage_todos, get_todos, search_flights, generate_a2ui

MODEL = os.getenv("ADK_MODEL", "openai/gpt-5-mini")


SYSTEM_PROMPT = """You are a polished, professional demo assistant. Keep responses to 1-2 sentences.

Tool guidance:
- Flights: call search_flights to show flight cards with a pre-built schema.
- Dashboards & rich UI: call generate_a2ui to create dashboard UIs with metrics,
  charts, tables, and cards. It handles rendering automatically.
- Charts: call query_data first, then render with the chart component.
- Todos: use manage_todos to update todos, get_todos to retrieve current list.
- A2UI actions: when you see a log_a2ui_event result (e.g. "view_details"),
  respond with a brief confirmation. The UI already updated on the frontend.
"""

root_agent = Agent(
    model=MODEL,
    name="copilotkit_adk_agent",
    description="Demo assistant with todos, data queries, flight search, and A2UI.",
    instruction=SYSTEM_PROMPT,
    tools=[AGUIToolset(), query_data, manage_todos, get_todos, search_flights, generate_a2ui],
    generate_content_config=GenerateContentConfig(
        max_output_tokens=8192,
    ),
)
