# Usage dashboard

Small read-only dashboard over the server's `usage_events` table: requests per day, tools (calls, p50/p95, errors),
themes rendered, MCP clients, most-read resources and error codes. Bun API (`server/`, no dependencies, Bun's built-in
Postgres client) plus a Vue 3 + Vite page (`web/`).

"Requests" means logged events: tool calls and resource reads. Protocol traffic such as `initialize` and `tools/list` is
not logged by the server.

What is stored (see `src/slidev_mcp/usage.py`): tool or resource name, theme (allowlisted names only), the MCP client
name (sanitized, 64 characters at most), latency, response size and an error *code*. Never slide markdown, slide UUIDs
(resource URIs are normalized to `slides://session/{uuid}`), IP addresses or session identifiers. There is no retention
window: events are kept indefinitely.

## Run locally

```bash
make docker-dev-up                       # from the repo root: local Postgres on :5432
cd dashboard && bun install
bun run seed                             # synthetic traffic, LOCAL ONLY (truncates usage_events)
bun run dev                              # API on :3100, Vite on :5173 (proxies /api)
```

Or `bun run build && bun run start` and open http://127.0.0.1:3100.

Environment: `DATABASE_URL` (default `postgres://slidev:slidev@localhost:5432/slidev`), `PORT` (3100),
`HOST` (127.0.0.1), `DASHBOARD_USER` (admin) and `DASHBOARD_PASSWORD`. Every query runs in a `READ ONLY` transaction;
in production it also connects as a role that can only `SELECT` from `usage_events`. With `HOST` beyond loopback the
server refuses to start without a password of at least 12 characters.
