from pathlib import Path

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client

from slidev_mcp.server import _register_resources


@pytest.fixture
def test_mcp() -> FastMCP:
    """Create a clean FastMCP instance without the DB lifespan for registration tests."""
    server = FastMCP(name="Slidev MCP Test")

    # Re-register the tools using the same function signatures
    @server.tool
    async def render_slides(
        markdown: str,
        theme: str,
        uuid: str | None = None,
    ) -> dict:
        """Render a Slidev presentation from markdown and return its hosted URL."""
        return {}

    @server.tool
    async def list_session_slides() -> dict:
        """List all slides created in the current MCP session."""
        return {}

    return server


@pytest.fixture
def test_mcp_with_resources(test_mcp: FastMCP) -> FastMCP:
    """Test MCP server with resources loaded."""
    vendor_dir = Path(__file__).parent.parent / "vendor" / "slidev-docs" / "docs"
    package_dir = Path(__file__).parent.parent / "src" / "slidev_mcp"
    from slidev_mcp.resource_registry import load_resources

    resources = load_resources(vendor_dir, package_dir)
    _register_resources(test_mcp, resources)
    return test_mcp


class TestServerRegistration:
    async def test_tools_registered(self, test_mcp: FastMCP) -> None:
        async with Client(transport=test_mcp) as client:
            tools = await client.list_tools()
        tool_names = {t.name for t in tools}
        assert "render_slides" in tool_names
        assert "list_session_slides" in tool_names

    async def test_render_slides_tool_has_parameters(self, test_mcp: FastMCP) -> None:
        async with Client(transport=test_mcp) as client:
            tools = await client.list_tools()
        render_tool = next(t for t in tools if t.name == "render_slides")
        param_names = set(render_tool.inputSchema.get("properties", {}).keys())
        assert "markdown" in param_names
        assert "theme" in param_names
        assert "uuid" in param_names

    async def test_resources_registered(self, test_mcp_with_resources: FastMCP) -> None:
        async with Client(transport=test_mcp_with_resources) as client:
            resources = await client.list_resources()
        resource_uris = {str(r.uri) for r in resources}
        # Our hand-authored resources should always be present
        assert "slidev://themes/installed" in resource_uris
        assert "slidev://examples/minimal" in resource_uris
        assert "slidev://examples/full_demo" in resource_uris

    async def test_resource_content_readable(self, test_mcp_with_resources: FastMCP) -> None:
        async with Client(transport=test_mcp_with_resources) as client:
            content = await client.read_resource("slidev://themes/installed")
        assert len(content) > 0
        text = content[0].content if hasattr(content[0], "content") else str(content[0])
        assert "default" in text
