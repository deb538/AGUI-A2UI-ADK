# Environment and Runbook

## Root `.env` (example)

```env
AGENT_URL=http://localhost:8123
OPENAI_API_KEY=...
USE_ADK_AGENT=true
ADK_AGENT_URL=http://127.0.0.1:8000/chat
```

## ADK `.env` (optional)

`adk-agent/.env` or `adk-agent/.env.local`:

```env
AI_CREDIT_API_KEY=...
AI_CREDIT_BASE_URL=https://api.aicredits.in/v1
ADK_MODEL=openai/gpt-5-mini
ADK_ENDPOINT_PATH=/chat
```

## Start (ADK mode)

1. Start ADK endpoint (`adk-agent/run.bat`)
2. Start UI (`npm run dev:ui`)
3. Verify health (`/health` on ADK port)

## Start (LangGraph mode)

1. Set `USE_ADK_AGENT=false`
2. Start agent (`npm run dev:agent`)
3. Start UI (`npm run dev:ui`)

## Useful Checks

- Confirm `OPENAI_API_KEY` set
- Confirm selected mode env vars
- Confirm target backend port is reachable
