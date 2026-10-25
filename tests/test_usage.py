"""Usage analytics: what gets recorded, and what must never be."""

from dataclasses import dataclass

import pytest
from fastmcp import FastMCP
from fastmcp.client import Client
from fastmcp.exceptions import ToolError
from fastmcp.server.lifespan import lifespan
from mcp.types import Implementation
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.models import UsageEvent
from slidev_mcp.usage import (
    UsageMiddleware,
    client_name,
    error_code,
    normalize_uri,
)

SLIDE_UUID = "11111111-1111-4111-8111-111111111111"


@dataclass
class _State:
    db_session_factory: async_sessionmaker[AsyncSession]
    resources: dict[str, str]


def _server(factory: async_sessionmaker[AsyncSession]) -> FastMCP:
    @lifespan
    async def state(server: FastMCP):
        yield _State(db_session_factory=factory, resources={"slidev://themes/guide": "guide"})

    mcp = FastMCP(
        "usage-test",
        lifespan=state,
        middleware=[UsageMiddleware(extra_known_uris=frozenset({"ui://slidev-mcp/viewer.html"}))],
    )

    @mcp.tool
    def render_slides(markdown: str, theme: str) -> str:
        if theme == "boom":
            raise ValueError("[build_timeout] Build exceeded timeout of 180s")
        return "built " + markdown

    @mcp.tool
    def get_theme(name: str) -> str:
        return f"theme {name}"

    @mcp.tool
    def crash() -> str:
        raise RuntimeError("secret internal detail")

    @mcp.resource("slidev://themes/guide")
    def guide() -> str:
        return "guide"

    @mcp.resource("slides://session/{uuid}")
    def detail(uuid: str) -> str:
        return f"slide {uuid}"

    return mcp


async def _events(factory: async_sessionmaker[AsyncSession]) -> list[UsageEvent]:
    async with factory() as session:
        return list((await session.execute(select(UsageEvent).order_by(UsageEvent.id))).scalars())


class TestHelpers:
    def test_client_name_is_sanitized_and_bounded(self) -> None:
        assert client_name({"name": "claude-ai"}) == "claude-ai"
        assert client_name({"name": "<script>alert(1)</script>"}) == "scriptalert1script"
        assert len(client_name({"name": "x" * 500}) or "") == 64
        assert client_name({"name": "   "}) is None
        assert client_name({"name": 42}) is None
        assert client_name(None) is None

    def test_uris_never_store_slide_uuids(self) -> None:
        known = {"slidev://themes/guide"}
        assert normalize_uri(f"slides://session/{SLIDE_UUID}", known) == "slides://session/{uuid}"
        assert normalize_uri("slidev://themes/guide", known) == "slidev://themes/guide"
        assert normalize_uri("slidev://made/up", known) == "(other)"

    def test_error_code(self) -> None:
        assert error_code(ValueError("[build_timeout] too slow")) == "build_timeout"
        assert error_code(ToolError("Error calling tool 'x': [not_found] gone")) == "not_found"
        assert error_code(RuntimeError("no code here")) == "RuntimeError"


class TestMiddleware:
    async def test_records_tool_call_with_theme_client_and_size(
        self, db_session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        client_info = Implementation(name="claude-desktop-test", version="1")
        async with Client(_server(db_session_factory), client_info=client_info) as c:
            await c.call_tool("render_slides", {"markdown": "# Secret deck", "theme": "dracula"})

        (event,) = await _events(db_session_factory)
        assert event.event_type == "tool_call"
        assert event.name == "render_slides"
        assert event.theme == "dracula"
        assert event.client == "claude-desktop-test"
        assert event.error is None
        assert event.latency_ms is not None and event.latency_ms >= 0
        assert event.response_chars == len("built # Secret deck")

    async def test_never_stores_markdown_or_unlisted_themes(
        self, db_session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        async with Client(_server(db_session_factory)) as c:
            await c.call_tool("render_slides", {"markdown": "# Private", "theme": "evil'; --"})
            await c.call_tool("get_theme", {"name": "seriph"})

        events = await _events(db_session_factory)
        assert [e.theme for e in events] == [None, "seriph"]
        # Only the declared columns exist; no column can hold the markdown
        stored = " ".join(str(v) for e in events for v in vars(e).values())
        assert "Private" not in stored

    async def test_records_error_code_not_message(
        self, db_session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        async with Client(_server(db_session_factory)) as c:
            with pytest.raises(ToolError):
                await c.call_tool("render_slides", {"markdown": "x", "theme": "boom"})
            with pytest.raises(ToolError):
                await c.call_tool("crash", {})

        events = await _events(db_session_factory)
        assert [e.error for e in events] == ["build_timeout", "RuntimeError"]
        assert all("secret" not in (e.error or "") for e in events)
        assert all(e.response_chars is None for e in events)

    async def test_resource_reads_are_normalized(
        self, db_session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        async with Client(_server(db_session_factory)) as c:
            await c.read_resource("slidev://themes/guide")
            await c.read_resource(f"slides://session/{SLIDE_UUID}")

        events = await _events(db_session_factory)
        assert [(e.event_type, e.name) for e in events] == [
            ("resource_read", "slidev://themes/guide"),
            ("resource_read", "slides://session/{uuid}"),
        ]
        assert SLIDE_UUID not in " ".join(e.name for e in events)

    async def test_database_failure_never_breaks_a_tool(
        self, db_session_factory: async_sessionmaker[AsyncSession]
    ) -> None:
        class _Broken:
            def __call__(self):
                raise ConnectionError("database is down")

        async with Client(_server(_Broken())) as c:  # type: ignore[arg-type]
            result = await c.call_tool("render_slides", {"markdown": "ok", "theme": "default"})
        assert result.content[0].text == "built ok"
