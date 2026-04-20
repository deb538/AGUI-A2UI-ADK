# Architecture and Network Flow

## System Components

1. Frontend UI (Next.js + Copilot UI)
2. BFF runtime endpoint (`/api/copilotkit`)
3. Agent backend (LangGraph or ADK)
4. A2UI catalog + renderers

## Runtime Endpoint

`src/app/api/copilotkit/[[...slug]]/route.ts` selects the default agent:

- ADK mode (`USE_ADK_AGENT=true`): `HttpAgent` -> `ADK_AGENT_URL`
- LangGraph mode (default): `LangGraphAgent` -> `AGENT_URL` / `LANGGRAPH_DEPLOYMENT_URL`

## Request Flow (ADK Mode)

1. Browser sends chat request to `/api/copilotkit`
2. Runtime forwards to ADK `HttpAgent`
3. ADK FastAPI endpoint receives `/chat`
4. `ADKAgent` executes `root_agent`
5. Model/tool calls run in ADK agent
6. Streamed events/response return to runtime and UI

## Request Flow (LangGraph Mode)

1. Browser -> `/api/copilotkit`
2. Runtime forwards to LangGraph deployment URL
3. Graph executes in `agent/main.py`
4. Tool outputs and model output stream to UI

## Ports (Typical Local)

- UI/BFF: `http://localhost:3000`
- LangGraph: `http://localhost:8123`
- ADK endpoint: `http://127.0.0.1:8000/chat`
