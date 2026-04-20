# Known Issues and Fixes

## 1) 401 invalid API key

Symptom:
- OpenAI auth failure in agent logs

Checks/Fix:
- Ensure expected key is set for active mode
- If using AI Credits, ensure mapping to OpenAI-compatible env vars is active

## 2) Invalid model ID (`/gpt-5.4 is not a valid model ID`)

Symptom:
- LiteLLM/OpenAI-compatible backend rejects model

Fix:
- Use supported model for current provider (stabilized to `openai/gpt-5-mini`)

## 3) JSONDecodeError Unterminated string in tool arguments

Symptom:
- Tool call args truncated mid-stream

Mitigation:
- Increased ADK max output tokens in agent config (`max_output_tokens=8192`)
- Reduce argument/schema size for large tool payloads
- Add retry/repair strategy for malformed tool args if needed

## 4) Port already in use

Symptom:
- Agent startup fails on configured port

Fix:
- Stop existing process or run on alternate port and update env

## 5) ADK endpoint connected but feature mismatch

Note:
- LangGraph `StateStreamingMiddleware` does not map 1:1 to ADK internals
- ADK relies on AG-UI tool/event flow (`AGUIToolset`)
