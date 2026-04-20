# A2UI: How It Works

## Core Concepts

- Catalog: definitions + renderers registered once in frontend
- Surface: per-response UI instance
- Operations: agent-returned commands (create surface, update components, bind data)

## Frontend Registration

Catalog is wired in `src/app/layout.tsx` via CopilotKit `a2ui` configuration.

## Catalog Sources

- Definitions: `src/app/declarative-generative-ui/definitions.ts`
- React renderers: `src/app/declarative-generative-ui/renderers.tsx`

## Agent Patterns

### Fixed Schema

- Tool: `search_flights`
- Uses JSON schema from `agent/src/a2ui/schemas/flight_schema.json`
- Updates data model with flights payload

### Dynamic Schema

- Tool: `generate_a2ui`
- Secondary model generates `components` + `data`
- Tool wraps result as A2UI operations and returns render payload

## End-to-End Render

1. Tool returns `a2ui.render(operations=[...])`
2. Runtime streams payload
3. A2UI renderer resolves component tree using catalog
4. Data bindings (`{ path: ... }`) populate UI props
