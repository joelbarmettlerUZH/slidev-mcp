"""End-to-end tests that start the real MCP server in-memory and test tools via the MCP protocol."""

import json
from pathlib import Path

import httpx
import pytest
from fastmcp import Context, FastMCP
from fastmcp.client import Client
from fastmcp.server.lifespan import lifespan

from slidev_mcp.builder import BuildOrchestrator
from slidev_mcp.config import Settings
from slidev_mcp.db import create_engine, create_session_factory, create_tables
from slidev_mcp.errors import SlidevMcpError
from slidev_mcp.resource_registry import load_resources
from slidev_mcp.server import _register_resources
from slidev_mcp.sessions import SessionMap
from slidev_mcp.tools import list_session_slides as _list_session_slides
from slidev_mcp.tools import render_slides as _render_slides


def _mock_builder_http() -> httpx.AsyncClient:
    """Returns an httpx.AsyncClient with a mock transport that simulates successful builds."""

    def handler(req: httpx.Request) -> httpx.Response:
        data = json.loads(req.content)
        return httpx.Response(
            200,
            json={"uuid": data["uuid"], "build_time_seconds": 2.5},
        )

    return httpx.AsyncClient(transport=httpx.MockTransport(handler), base_url="http://builder")


def _create_test_server(settings: Settings) -> FastMCP:
    """Create a real FastMCP server wired to the given settings."""

    @lifespan
    async def test_lifespan(server: FastMCP):
        engine = create_engine(settings.database_url)
        await create_tables(engine)
        db_session_factory = create_session_factory(engine)

        session_map = SessionMap()
        builder = BuildOrchestrator(settings)
        builder._client = _mock_builder_http()

        try:
            yield {
                "settings": settings,
                "db_session_factory": db_session_factory,
                "session_map": session_map,
                "builder": builder,
            }
        finally:
            await builder.close()
            await engine.dispose()

    server = FastMCP(
        name="Slidev MCP Test",
        lifespan=test_lifespan,
    )

    # Register the real tools — same as server.py
    @server.tool
    async def render_slides(
        markdown: str,
        theme: str,
        uuid: str | None = None,
        ctx: Context = None,
    ) -> dict:
        """Render a Slidev presentation from markdown and return its hosted URL."""
        lc = ctx.lifespan_context
        session_id = ctx.session_id or ctx.client_id or "unknown"
        try:
            return await _render_slides(
                markdown=markdown,
                theme=theme,
                uuid=uuid,
                session_id=session_id,
                session_map=lc["session_map"],
                builder=lc["builder"],
                db_session_factory=lc["db_session_factory"],
            )
        except SlidevMcpError as e:
            raise ValueError(f"[{e.code}] {e.message}") from None

    @server.tool
    async def list_session_slides(ctx: Context) -> dict:
        """List all slides created in the current MCP session."""
        lc = ctx.lifespan_context
        session_id = ctx.session_id or ctx.client_id or "unknown"
        return await _list_session_slides(
            session_id=session_id,
            db_session_factory=lc["db_session_factory"],
            settings=lc["settings"],
        )

    # Register resources
    package_dir = Path(__file__).parent.parent / "src" / "slidev_mcp"
    vendor_dir = Path(__file__).parent.parent / "vendor" / "slidev-docs" / "docs"
    resources = load_resources(vendor_dir, package_dir)
    _register_resources(server, resources)

    return server


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    db_path = tmp_path / "test.db"
    return Settings(
        database_url=f"sqlite+aiosqlite:///{db_path}",
        slides_dir=str(tmp_path / "slides"),
        domain="test.example.com",
        build_timeout=30,
    )


@pytest.fixture
def test_server(settings: Settings) -> FastMCP:
    return _create_test_server(settings)


def _tool_text(result) -> str:
    """Extract text from a CallToolResult."""
    return result.content[0].text


class TestE2ERenderSlides:
    async def test_render_new_slides(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            result = await client.call_tool(
                "render_slides",
                {"markdown": "# Hello\n\n---\n\n## World", "theme": "default"},
            )

        data = json.loads(_tool_text(result))
        assert "url" in data
        assert "uuid" in data
        assert "build_time_seconds" in data
        assert "test.example.com" in data["url"]

    async def test_render_and_update_slides(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            # Create
            result1 = await client.call_tool(
                "render_slides",
                {"markdown": "# Version 1", "theme": "default"},
            )
            data1 = json.loads(_tool_text(result1))
            slide_uuid = data1["uuid"]

            # Update with same UUID
            result2 = await client.call_tool(
                "render_slides",
                {
                    "markdown": "# Version 2",
                    "theme": "seriph",
                    "uuid": slide_uuid,
                },
            )
            data2 = json.loads(_tool_text(result2))

        assert data2["uuid"] == slide_uuid

    async def test_invalid_theme_returns_error(self, test_server: FastMCP) -> None:
        from fastmcp.exceptions import ToolError

        async with Client(transport=test_server) as client:
            with pytest.raises(ToolError, match="theme_not_allowed"):
                await client.call_tool(
                    "render_slides",
                    {"markdown": "# Test", "theme": "nonexistent-theme"},
                )

    async def test_render_then_list(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            # Render two slides
            await client.call_tool(
                "render_slides",
                {"markdown": "# Deck 1", "theme": "default"},
            )
            await client.call_tool(
                "render_slides",
                {"markdown": "# Deck 2", "theme": "seriph"},
            )

            # List session slides
            result = await client.call_tool("list_session_slides", {})

        data = json.loads(_tool_text(result))
        assert len(data["slides"]) == 2
        themes = {s["theme"] for s in data["slides"]}
        assert themes == {"default", "seriph"}


class TestE2EListSessionSlides:
    async def test_empty_session(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            result = await client.call_tool("list_session_slides", {})

        data = json.loads(_tool_text(result))
        assert data["slides"] == []


class TestE2EResources:
    async def test_list_resources(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            resources = await client.list_resources()

        uris = {str(r.uri) for r in resources}
        assert "slidev://themes/installed" in uris
        assert "slidev://examples/minimal" in uris
        assert "slidev://examples/full_demo" in uris

    async def test_read_installed_themes(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            content = await client.read_resource("slidev://themes/installed")

        text = content[0].content if hasattr(content[0], "content") else str(content[0])
        assert "default" in text
        assert "seriph" in text

    async def test_read_example_deck(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            content = await client.read_resource("slidev://examples/minimal")

        text = content[0].content if hasattr(content[0], "content") else str(content[0])
        assert "# Welcome" in text


class TestE2EToolDiscovery:
    async def test_list_tools(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            tools = await client.list_tools()

        tool_names = {t.name for t in tools}
        assert tool_names == {"render_slides", "list_session_slides"}

    async def test_render_slides_schema(self, test_server: FastMCP) -> None:
        async with Client(transport=test_server) as client:
            tools = await client.list_tools()

        render_tool = next(t for t in tools if t.name == "render_slides")
        props = render_tool.inputSchema["properties"]
        assert "markdown" in props
        assert "theme" in props
        assert "uuid" in props
