# Tooling and File Map

## Runtime Route

- `src/app/api/copilotkit/[[...slug]]/route.ts`
  - Chooses default agent (ADK vs LangGraph)

## LangGraph Agent

- `agent/main.py`
- `agent/src/query.py`
- `agent/src/todos.py`
- `agent/src/a2ui_fixed_schema.py`
- `agent/src/a2ui_dynamic_schema.py`

## ADK Agent

- `adk-agent/endpoint.py`
- `adk-agent/copilotkit_adk_agent/agent.py`
- `adk-agent/copilotkit_adk_agent/tools.py`
- `adk-agent/pyproject.toml`

## Frontend A2UI

- `src/app/layout.tsx`
- `src/app/declarative-generative-ui/definitions.ts`
- `src/app/declarative-generative-ui/renderers.tsx`

## Data/Schema Assets

- `agent/src/db.csv`
- `agent/src/a2ui/schemas/flight_schema.json`
