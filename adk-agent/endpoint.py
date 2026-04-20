import os
import json
import logging

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from ag_ui_adk import ADKAgent, add_adk_fastapi_endpoint

logging.basicConfig(level=logging.INFO)
_log = logging.getLogger("endpoint")

from copilotkit_adk_agent.agent import root_agent

agent = ADKAgent(
    adk_agent=root_agent,
    app_name=os.getenv("ADK_APP_NAME", "copilotkit_adk_agent"),
    user_id=os.getenv("ADK_DEFAULT_USER_ID", "user123"),
)

app = FastAPI()


class DebugRequestMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "POST":
            body = await request.body()
            try:
                data = json.loads(body)
                tools = data.get("tools", [])
                tool_names = [t.get("name", "?") for t in tools]
                _log.info("[DEBUG] POST %s — tools in request: %s", request.url.path, tool_names)
            except Exception:
                _log.info("[DEBUG] POST %s — could not parse body", request.url.path)
        return await call_next(request)


app.add_middleware(DebugRequestMiddleware)

add_adk_fastapi_endpoint(
    app,
    agent,
    path=os.getenv("ADK_ENDPOINT_PATH", "/chat"),
    extract_headers=["x-user-id", "x-tenant-id"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ADK_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=True)
