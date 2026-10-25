---
description: How to connect Claude Desktop to a Slidev MCP server.
---

# Claude Desktop

[Claude Desktop](https://claude.ai/download) is Anthropic's desktop application for Claude.

## Setup

Remote servers are added as **custom connectors** in the app, not in `claude_desktop_config.json` (that file is for local servers that run on your machine).

**Free, Pro and Max plans**

1. Open **Customize > Connectors**
2. Click **+ Add**, then **Add custom connector**
3. Enter a name (for example `Slidev MCP`) and the server URL:

```
https://mcp.slidev-mcp.org/mcp
```

4. Click **Add**

Free plans are limited to one custom connector.

**Team and Enterprise plans**

An Owner adds the connector under **Organization settings > Connectors** (**Add**, then **Custom**, then **Web**). Members then enable it under **Customize > Connectors** by clicking **Connect**.

No sign-in is needed. Slidev MCP doesn't use authentication, so the connector connects straight away.

For details, see Anthropic's guide to [custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp). Connectors added this way are also available in claude.ai on the web.

## Verify

Open a new conversation and ask:

> What MCP tools do you have access to?

You should see `render_slides` and `list_session_slides`.

## Usage

Ask Claude to create a presentation:

> Create a 10-slide presentation about our product roadmap using the apple-basic theme
