# CopilotKit <> LangGraph Starter

This is a starter template for building AI agents using [LangGraph](https://www.langchain.com/langgraph) and [CopilotKit](https://copilotkit.ai). It provides a modern Next.js application with an integrated LangGraph agent to be built on top of.

https://github.com/user-attachments/assets/47761912-d46a-4fb3-b9bd-cb41ddd02e34

## Prerequisites

- Node.js 18+
- Python 3.8+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- Any of the following package managers:
  - npm (default)
  - [pnpm](https://pnpm.io/installation)
  - [yarn](https://classic.yarnpkg.com/lang/en/docs/install/)
  - [bun](https://bun.sh/)
- OpenAI API Key (for the LangGraph agent)

## Getting Started

1. Install dependencies using your preferred package manager:

```bash
# Using npm (default)
npm install

# Using pnpm
pnpm install

# Using yarn
yarn install

# Using bun
bun install
```

This will also install the Python agent dependencies via `uv sync`.

2. Set up your environment variables:

```bash
cp .env.example .env
```

Then edit the `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

3. Start the development server:

```bash
# Using npm (default)
npm run dev

# Using pnpm
pnpm dev

# Using yarn
yarn dev

# Using bun
bun run dev
```

This will start both the UI and agent servers concurrently.

## Available Scripts

The following scripts can also be run using your preferred package manager:

- `dev` - Starts both UI and agent servers in development mode
- `dev:debug` - Starts development servers with debug logging enabled
- `dev:ui` - Starts only the Next.js UI server
- `dev:agent` - Starts only the LangGraph agent server
- `build` - Builds the Next.js application for production
- `start` - Starts the production server
- `install:agent` - Installs Python dependencies for the agent

## Project Structure

```
├── src/                         # Next.js frontend source
│   ├── app/
│   │   ├── page.tsx             # Main page
│   │   └── api/copilotkit/      # CopilotKit API route
│   ├── components/
│   │   ├── example-canvas/      # Todo list UI
│   │   ├── example-layout/      # Layout: chat + canvas side-by-side
│   │   └── generative-ui/       # Example generative UI components
│   └── hooks/
├── agent/                       # LangGraph Python agent
│   ├── main.py                  # Agent entry point
│   └── src/
│       ├── todos.py             # Todo tools and state schema
│       └── query.py             # Example data query tool
├── scripts/                     # Agent setup and run scripts
│   ├── setup-agent.sh / .bat
│   └── run-agent.sh / .bat
├── public/                      # Static assets
├── next.config.ts
├── tsconfig.json
└── package.json
```

## A2UI — Agent-to-User Interface

This starter includes [A2UI](https://a2ui.org/specification/) support, allowing the agent to generate rich, interactive UI surfaces declaratively. Instead of returning plain text, the agent sends a JSON description of the UI it wants to render, and the frontend turns it into real components.

### How it works

A2UI uses three concepts:

1. **Catalog** — a set of component definitions (schema) paired with React renderers. Registered once in `layout.tsx` via `<CopilotKitProvider a2ui={{ catalog: demonstrationCatalog }}>`.
2. **Surface** — a rendered UI instance. The agent creates a surface, sets its components, and binds data to it.
3. **Operations** — the agent returns `a2ui.render(operations=[...])` from a tool, which the middleware streams to the frontend.

### Two patterns

| Pattern            | Description                                                                   | Agent tool       | Frontend                                    |
| ------------------ | ----------------------------------------------------------------------------- | ---------------- | ------------------------------------------- |
| **Fixed schema**   | Pre-defined component layout. Only the data changes per invocation.           | `search_flights` | Schema in `a2ui/schemas/flight_schema.json` |
| **Dynamic schema** | A secondary LLM generates both components and data based on the conversation. | `generate_a2ui`  | Components decided at runtime               |

Both patterns use the same catalog on the frontend — the difference is where the component tree comes from.

### Key files

| Purpose                              | Path                                               |
| ------------------------------------ | -------------------------------------------------- |
| Catalog definitions (Zod schemas)    | `src/app/declarative-generative-ui/definitions.ts` |
| Catalog renderers (React components) | `src/app/declarative-generative-ui/renderers.tsx`  |
| Catalog registration                 | `src/app/layout.tsx`                               |
| Fixed-schema agent tool              | `agent/src/a2ui_fixed_schema.py`                   |
| Dynamic-schema agent tool            | `agent/src/a2ui_dynamic_schema.py`                 |
| Flight schema JSON                   | `agent/src/a2ui/schemas/flight_schema.json`        |
| Showcase config                      | `showcase.json`                                    |

### Adding a custom component

1. **Define** the component schema in `definitions.ts`:

   ```typescript
   MyWidget: {
     description: "A brief description for the agent.",
     props: z.object({ title: z.string(), value: z.number() }),
   },
   ```

2. **Render** it in `renderers.tsx`:

   ```typescript
   MyWidget: ({ props }) => (
     <div>{props.title}: {props.value}</div>
   ),
   ```

   Renderers are type-checked against the definitions — TypeScript will error if props don't match.

3. **Use it** from the agent. The component is automatically available to both fixed-schema templates and the dynamic-schema LLM.

### Adding a new fixed-schema tool

1. Create a JSON schema file in `agent/src/a2ui/schemas/` describing the component tree.
2. Create a Python tool that loads the schema with `a2ui.load_schema()` and returns `a2ui.render(operations=[...])` with your data. See `a2ui_fixed_schema.py` for the pattern.

### Showcase mode

`showcase.json` controls which suggestion pills are visually highlighted. Set `"showcase": "a2ui"` to highlight the A2UI demos, or `"showcase": "default"` for no highlights. This is configured automatically when scaffolding via `npx copilotkit create --framework a2ui`.

### Further reading

- [A2UI Specification](https://a2ui.org/specification/)
- [CopilotKit A2UI Documentation](https://docs.copilotkit.ai)

## Documentation

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/) - Learn more about LangGraph and its features
- [CopilotKit Documentation](https://docs.copilotkit.ai) - Explore CopilotKit's capabilities

## Contributing

Feel free to submit issues and enhancement requests! This starter is designed to be easily extensible.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Agent Connection Issues

If you see "I'm having trouble connecting to my tools", make sure:

1. The LangGraph agent is running on port 8123
2. Your OpenAI API key is set correctly
3. Both servers started successfully

### Python Dependencies

If you encounter Python import errors:

```bash
npm run install:agent
```

## Optional: Google ADK Agent Mode

This repo can run with either:

1. **LangGraph agent** (default), or
2. **Google ADK agent** (external HTTP agent endpoint)

### ADK files added

- `adk-agent/endpoint.py` — FastAPI endpoint exposing AG-UI at `/chat`
- `adk-agent/copilotkit_adk_agent/agent.py` — root ADK agent configuration
- `adk-agent/copilotkit_adk_agent/tools.py` — ported tools (`query_data`, todos, `search_flights`, `generate_a2ui`)
- `adk-agent/pyproject.toml` — ADK runtime dependencies
- `adk-agent/run.bat` / `adk-agent/run.sh` — local ADK run scripts

### Runtime switching

`src/app/api/copilotkit/[[...slug]]/route.ts` chooses the backend agent:

- `USE_ADK_AGENT=true` → use `HttpAgent` (`ADK_AGENT_URL`, default `http://127.0.0.1:8000/chat`)
- otherwise → use `LangGraphAgent` (`AGENT_URL`, default `http://localhost:8123`)

### ADK environment example

In `.env` (project root):

```bash
USE_ADK_AGENT=true
ADK_AGENT_URL=http://127.0.0.1:8000/chat
OPENAI_API_KEY=...
```

In `adk-agent/.env` or `adk-agent/.env.local` (optional overrides):

```bash
AI_CREDIT_API_KEY=...
AI_CREDIT_BASE_URL=https://api.aicredits.in/v1
ADK_MODEL=openai/gpt-5-mini
ADK_ENDPOINT_PATH=/chat
```

`agent.py` maps AI Credits env vars to OpenAI-compatible vars for LiteLLM:

- `AI_CREDIT_API_KEY` → `OPENAI_API_KEY`
- `AI_CREDIT_BASE_URL` → `OPENAI_API_BASE`

## Architecture & Network Flow

### Components

1. **Frontend (Next.js + CopilotKit UI)**
  - `src/app/layout.tsx`
  - `src/app/page.tsx`
2. **BFF runtime endpoint**
  - `src/app/api/copilotkit/[[...slug]]/route.ts`
3. **Agent backend**
  - LangGraph: `agent/main.py`
  - ADK: `adk-agent/endpoint.py` + `adk-agent/copilotkit_adk_agent/agent.py`
4. **A2UI catalog**
  - Definitions: `src/app/declarative-generative-ui/definitions.ts`
  - Renderers: `src/app/declarative-generative-ui/renderers.tsx`

### Request path (ADK mode)

1. Browser sends request to `POST /api/copilotkit`
2. Route runtime forwards to `HttpAgent` (`ADK_AGENT_URL`)
3. FastAPI `adk-agent/endpoint.py` receives request at `/chat`
4. `ADKAgent` executes `root_agent`
5. ADK model calls tools in `copilotkit_adk_agent/tools.py`
6. AG-UI events + content stream back through BFF to frontend

### Request path (LangGraph mode)

1. Browser sends request to `POST /api/copilotkit`
2. Route runtime forwards to `LangGraphAgent`
3. LangGraph executes `graph` in `agent/main.py`
4. Tool responses and/or A2UI payload stream back to frontend

## How A2UI Works End-to-End

1. Frontend registers catalog once in `layout.tsx` using `a2ui={{ catalog: demonstrationCatalog }}`.
2. Agent tool returns A2UI operations via `a2ui.render(operations=[...])`.
3. Copilot runtime streams operations to client.
4. A2UI renderer binds data to catalog definitions and renders React components.

### Fixed-schema path

- Tool: `search_flights`
- Schema source: `agent/src/a2ui/schemas/flight_schema.json`
- Data model update: `{"flights": [...]}`

### Dynamic-schema path

- Tool: `generate_a2ui`
- Secondary LLM outputs `components` + `data`
- Tool wraps into A2UI operations and returns render payload

## Known Issue: Calculator/Complex Tool Calls

If pie chart works but calculator (or another complex tool call) fails with JSON parse errors such as:

- `JSONDecodeError: Unterminated string ...`

that typically means the model emitted a truncated tool-arguments payload while streaming.

Current mitigation in ADK agent:

- `GenerateContentConfig(max_output_tokens=8192)` in `adk-agent/copilotkit_adk_agent/agent.py`

If this still happens intermittently:

1. Reduce tool argument size / schema complexity
2. Keep model at `openai/gpt-5-mini` for stability
3. Add retry/repair logic around tool argument JSON parsing in tool-generation paths
