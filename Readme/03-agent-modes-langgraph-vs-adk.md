# Agent Modes: LangGraph vs ADK

## LangGraph Mode

- Entry: `agent/main.py`
- Runtime adapter: `LangGraphAgent`
- Uses LangGraph graph + tools
- Good parity with original starter behavior

## ADK Mode

- Endpoint: `adk-agent/endpoint.py`
- Agent: `adk-agent/copilotkit_adk_agent/agent.py`
- Tools: `adk-agent/copilotkit_adk_agent/tools.py`
- Runtime adapter: `HttpAgent`

## ADK-Specific Notes

- `AGUIToolset()` is required in ADK mode for AG-UI protocol features.
- Env mapping is applied for AI Credits/OpenAI-compatible calls:
  - `AI_CREDIT_API_KEY` -> `OPENAI_API_KEY`
  - `AI_CREDIT_BASE_URL` -> `OPENAI_API_BASE`

## Switching Logic

Controlled by env:

- `USE_ADK_AGENT=true` -> ADK
- `USE_ADK_AGENT=false` (or unset) -> LangGraph
