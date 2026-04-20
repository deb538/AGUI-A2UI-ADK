"""
Tools for the ADK agent — ported from the LangGraph agent.

Each tool is a plain Python function decorated for google-adk.
"""

from __future__ import annotations

import csv
import json
import uuid
from pathlib import Path
from typing import Literal, TypedDict

# ---------------------------------------------------------------------------
# Data: CSV database (same file used by LangGraph agent)
# ---------------------------------------------------------------------------
_BASE_DIR = Path(__file__).resolve().parent
_CSV_PATH = _BASE_DIR / "db.csv"
if not _CSV_PATH.exists():
    # Backward-compatible fallback to shared LangGraph data file.
    _CSV_PATH = Path(__file__).resolve().parents[1].parent / "agent" / "src" / "db.csv"

with open(_CSV_PATH) as _f:
    _cached_data = list(csv.DictReader(_f))


def query_data(query: str) -> list[dict]:
    """Query the database. Takes natural language. Always call before showing a chart or graph."""
    return _cached_data


# ---------------------------------------------------------------------------
# Todos
# ---------------------------------------------------------------------------
class Todo(TypedDict):
    id: str
    title: str
    description: str
    emoji: str
    status: Literal["pending", "completed"]


# In-memory todo store (ADK agents are single-process, so module-level is fine)
_todos: list[Todo] = []


def manage_todos(todos: list[dict]) -> str:
    """Manage the current todos. Pass the full updated list of todos.

    Each todo should have: title, description, emoji, status ("pending" or "completed").
    An id will be assigned automatically if missing.
    """
    global _todos
    for todo in todos:
        if not todo.get("id"):
            todo["id"] = str(uuid.uuid4())
    _todos = todos  # type: ignore[assignment]
    return f"Successfully updated todos ({len(todos)} items)."


def get_todos() -> list[dict]:
    """Get the current todos."""
    return _todos  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# A2UI — Fixed schema: flight search
# ---------------------------------------------------------------------------
_FLIGHT_SCHEMA_PATH = (
    _BASE_DIR
    / "a2ui"
    / "schemas"
    / "flight_schema.json"
)
if not _FLIGHT_SCHEMA_PATH.exists():
    # Backward-compatible fallback to shared LangGraph schema file.
    _FLIGHT_SCHEMA_PATH = (
        Path(__file__).resolve().parents[1].parent
        / "agent"
        / "src"
        / "a2ui"
        / "schemas"
        / "flight_schema.json"
    )

try:
    from copilotkit import a2ui

    FLIGHT_SCHEMA = a2ui.load_schema(_FLIGHT_SCHEMA_PATH)
except Exception:
    FLIGHT_SCHEMA = None

CATALOG_ID = "copilotkit://app-dashboard-catalog"
SURFACE_ID = "flight-search-results"


def search_flights(flights: list[dict]) -> str:
    """Search for flights and display the results as rich cards. Return exactly 2 flights.

    Each flight must have: id, airline (e.g. "United Airlines"),
    airlineLogo (use Google favicon API: https://www.google.com/s2/favicons?domain={airline_domain}&sz=128),
    flightNumber, origin, destination,
    date (short readable format like "Tue, Mar 18"),
    departureTime, arrivalTime,
    duration (e.g. "4h 25m"), status (e.g. "On Time" or "Delayed"),
    statusIcon (colored dot placeholder URL),
    and price (e.g. "$289").
    """
    if not FLIGHT_SCHEMA:
        return json.dumps({"error": "flight schema not loaded"})

    return a2ui.render(
        operations=[
            a2ui.create_surface(SURFACE_ID, catalog_id=CATALOG_ID),
            a2ui.update_components(SURFACE_ID, FLIGHT_SCHEMA),
            a2ui.update_data_model(SURFACE_ID, {"flights": flights}),
        ],
    )


# ---------------------------------------------------------------------------
# A2UI — Dynamic schema: LLM-generated UI
# ---------------------------------------------------------------------------
CUSTOM_CATALOG_ID = "copilotkit://app-dashboard-catalog"


def generate_a2ui(user_request: str) -> str:
    """Generate dynamic A2UI components based on the user request.

    A secondary LLM designs the UI schema and data. The result is
    returned as A2UI operations for the middleware to render.
    Pass a short description of what the user wants to see.
    """
    import os
    import time
    from openai import OpenAI

    t0 = time.time()

    # Build OpenAI client pointing at AI Credits or direct OpenAI
    base_url = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL") or None
    api_key = os.getenv("OPENAI_API_KEY") or ""
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    model = os.getenv("ADK_MODEL", "openai/gpt-5.4")

    render_a2ui_tool = {
        "type": "function",
        "function": {
            "name": "render_a2ui",
            "description": "Render a dynamic A2UI v0.9 surface.",
            "parameters": {
                "type": "object",
                "properties": {
                    "surfaceId": {"type": "string", "description": "Unique surface identifier."},
                    "catalogId": {"type": "string", "description": "The catalog ID."},
                    "components": {
                        "type": "array",
                        "items": {"type": "object"},
                        "description": "A2UI v0.9 component array (flat format). Root must have id 'root'.",
                    },
                    "data": {
                        "type": "object",
                        "description": "Optional initial data model for the surface.",
                    },
                },
                "required": ["surfaceId", "catalogId", "components"],
            },
        },
    }

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Generate A2UI components for the user's request. Always call render_a2ui."},
            {"role": "user", "content": user_request},
        ],
        tools=[render_a2ui_tool],
        tool_choice={"type": "function", "function": {"name": "render_a2ui"}},
    )

    msg = response.choices[0].message
    if not msg.tool_calls:
        return json.dumps({"error": "LLM did not call render_a2ui"})

    args = json.loads(msg.tool_calls[0].function.arguments)
    surface_id = args.get("surfaceId", "dynamic-surface")
    catalog_id = args.get("catalogId", CUSTOM_CATALOG_ID)
    components = args.get("components", [])
    data = args.get("data", {})

    ops = [
        a2ui.create_surface(surface_id, catalog_id=catalog_id),
        a2ui.update_components(surface_id, components),
    ]
    if data:
        ops.append(a2ui.update_data_model(surface_id, data))

    result = a2ui.render(operations=ops)
    print(f"[ADK-A2UI] generate_a2ui done in {time.time()-t0:.1f}s, {len(components)} components")
    return result
