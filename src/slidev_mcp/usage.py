"""Usage analytics: record every tool call and resource read in PostgreSQL.

One middleware covers all tools and resources, so new ones are counted
automatically. Nothing user-supplied is stored verbatim: themes must be on the
allowlist, resource URIs are normalized (slide UUIDs are capabilities), the
client name is length-limited, and errors are reduced to their code.
"""

import logging
import re
import time
from collections.abc import Mapping
from typing import Any

from fastmcp.server.middleware import Middleware, MiddlewareContext
from mcp.types import ImageContent, TextContent
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.config import ALLOWED_THEMES
from slidev_mcp.models import UsageEvent

logger = logging.getLogger(__name__)

_CLIENT_INFO_KEY = "io.modelcontextprotocol/clientInfo"
# FastMCP prefixes tool errors with "Error calling tool 'name': "
_ERROR_CODE = re.compile(r"^(?:Error calling tool '[^']*': )?\[([a-z0-9_]{1,40})\]")
_CLIENT_CLEAN = re.compile(r"[^A-Za-z0-9 ._-]")
_MAX_CLIENT_LEN = 64
_SESSION_URI_PREFIX = "slides://session/"

# Tool argument that carries a theme name, per tool
_THEME_ARG = {"render_slides": "theme", "get_theme": "name"}


def client_name(info: Mapping[str, Any] | Any | None) -> str | None:
    """Sanitized MCP client name, or None. The value is client-controlled."""
    if info is None:
        return None
    raw = info.get("name") if isinstance(info, Mapping) else getattr(info, "name", None)
    if not isinstance(raw, str):
        return None
    cleaned = _CLIENT_CLEAN.sub("", raw).strip()[:_MAX_CLIENT_LEN]
    return cleaned or None


def normalize_uri(uri: str, known: set[str]) -> str:
    """Resource name safe to store: slide UUIDs are replaced, unknown URIs collapsed."""
    if uri.startswith(_SESSION_URI_PREFIX):
        return _SESSION_URI_PREFIX + "{uuid}"
    return uri if uri in known else "(other)"


def error_code(exc: BaseException) -> str:
    """Error code from a "[code] message" tool error, else the underlying exception class."""
    match = _ERROR_CODE.match(str(exc))
    if match:
        return match.group(1)
    root = exc.__cause__ or exc
    return type(root).__name__[:40]


def response_size(result: Any) -> int | None:
    """Characters of text (plus image payload) in a tool or resource result."""
    total = 0
    for block in getattr(result, "content", None) or []:
        if isinstance(block, TextContent):
            total += len(block.text)
        elif isinstance(block, ImageContent):
            total += len(block.data)
    return total


class UsageMiddleware(Middleware):
    """Record tool calls and resource reads. Never fails or delays a request on error."""

    def __init__(self, extra_known_uris: frozenset[str] = frozenset()) -> None:
        # Resource URIs served by handlers rather than the loaded resource files
        self._extra_known = extra_known_uris

    def _known_uris(self, context: MiddlewareContext) -> set[str]:
        fc = context.fastmcp_context
        state = getattr(fc, "lifespan_context", None) if fc else None
        loaded = getattr(state, "resources", None) or {}
        return set(loaded) | set(self._extra_known)

    @staticmethod
    def _session_factory(context: MiddlewareContext) -> async_sessionmaker[AsyncSession] | None:
        fc = context.fastmcp_context
        state = getattr(fc, "lifespan_context", None) if fc else None
        return getattr(state, "db_session_factory", None)

    @staticmethod
    def _client(context: MiddlewareContext) -> str | None:
        fc = context.fastmcp_context
        if fc is None:
            return None
        try:
            meta = fc.request_context.meta
            if isinstance(meta, Mapping) and _CLIENT_INFO_KEY in meta:
                return client_name(meta[_CLIENT_INFO_KEY])
            params = fc.session.client_params  # initialize-based protocol revisions
            info = getattr(params, "clientInfo", None) or getattr(params, "client_info", None)
            return client_name(info)
        except Exception:
            return None

    async def _record(self, context: MiddlewareContext, event: dict[str, Any]) -> None:
        factory = self._session_factory(context)
        if factory is None:
            return
        try:
            async with factory() as session:
                session.add(UsageEvent(client=self._client(context), **event))
                await session.commit()
        except Exception:
            logger.debug("Failed to record usage event", exc_info=True)

    async def on_call_tool(self, context, call_next):  # type: ignore[no-untyped-def]
        name = context.message.name
        args = context.message.arguments or {}
        theme_arg = _THEME_ARG.get(name)
        theme = args.get(theme_arg) if theme_arg else None
        theme = theme if isinstance(theme, str) and theme in ALLOWED_THEMES else None

        start = time.monotonic()
        error: str | None = None
        result: Any = None
        try:
            result = await call_next(context)
            return result
        except Exception as exc:
            error = error_code(exc)
            raise
        finally:
            await self._record(
                context,
                {
                    "event_type": "tool_call",
                    "name": name,
                    "theme": theme,
                    "latency_ms": int((time.monotonic() - start) * 1000),
                    "response_chars": response_size(result) if result is not None else None,
                    "error": error,
                },
            )

    async def on_read_resource(self, context, call_next):  # type: ignore[no-untyped-def]
        uri = str(context.message.uri)
        start = time.monotonic()
        error: str | None = None
        result = None
        try:
            result = await call_next(context)
            return result
        except Exception as exc:
            error = error_code(exc)
            raise
        finally:
            size = None
            if result is not None:
                size = sum(len(getattr(c, "content", "") or "") for c in result.contents)
            await self._record(
                context,
                {
                    "event_type": "resource_read",
                    "name": normalize_uri(uri, self._known_uris(context)),
                    "latency_ms": int((time.monotonic() - start) * 1000),
                    "response_chars": size,
                    "error": error,
                },
            )
