import asyncio
import contextlib
import json
import logging
import shutil
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Annotated

from fastmcp import Context, FastMCP
from fastmcp.server.lifespan import lifespan
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.builder import BuildOrchestrator
from slidev_mcp.config import Settings
from slidev_mcp.db import create_engine, create_session_factory, create_tables
from slidev_mcp.errors import SlidevMcpError
from slidev_mcp.models import Slide
from slidev_mcp.resource_registry import load_resources
from slidev_mcp.sessions import SessionMap
from slidev_mcp.tools import list_session_slides as _list_session_slides
from slidev_mcp.tools import render_slides as _render_slides

logger = logging.getLogger(__name__)


class _JSONFormatter(logging.Formatter):
    """Structured JSON log formatter."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[0] is not None:
            entry["exc"] = self.formatException(record.exc_info)
        # Merge extra fields (e.g. uuid, theme, duration from builder)
        for key in ("uuid", "session_id", "theme", "duration", "markdown_size", "success"):
            val = getattr(record, key, None)
            if val is not None:
                entry[key] = val
        return json.dumps(entry)


def _configure_logging(settings: Settings) -> None:
    """Configure root logger based on settings."""
    root = logging.getLogger()
    root.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    handler = logging.StreamHandler(sys.stderr)
    if settings.log_format == "json":
        handler.setFormatter(_JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

    root.handlers.clear()
    root.addHandler(handler)


async def _gc_loop(
    interval_hours: int,
    ttl_days: int,
    session_map: SessionMap,
    db_session_factory: async_sessionmaker[AsyncSession],
    slides_dir: str,
) -> None:
    """Background task: garbage-collect expired slides."""
    while True:
        await asyncio.sleep(interval_hours * 3600)
        try:
            cutoff = datetime.now(UTC) - timedelta(days=ttl_days)
            async with db_session_factory() as session:
                result = await session.execute(select(Slide).where(Slide.created_at < cutoff))
                expired = result.scalars().all()

                deleted = 0
                for slide in expired:
                    if session_map.is_active(slide.uuid):
                        continue
                    slide_path = Path(slides_dir) / slide.uuid
                    if slide_path.exists():
                        shutil.rmtree(slide_path)
                    await session.delete(slide)
                    deleted += 1

                await session.commit()

            if deleted:
                logger.info("GC: deleted %d expired slides", deleted)
        except Exception:
            logger.exception("GC task error")


@lifespan
async def app_lifespan(server: FastMCP):
    settings = Settings()

    # Database
    engine = create_engine(settings.database_url)
    await create_tables(engine)
    db_session_factory = create_session_factory(engine)

    # Session map and build orchestrator
    session_map = SessionMap()
    builder = BuildOrchestrator(settings)

    # Resources
    vendor_dir = Path(__file__).parent.parent.parent / "vendor" / "slidev-docs" / "docs"
    package_dir = Path(__file__).parent
    resources = load_resources(vendor_dir, package_dir)

    # GC background task
    gc_task = asyncio.create_task(
        _gc_loop(
            settings.gc_interval_hours,
            settings.slide_ttl_days,
            session_map,
            db_session_factory,
            settings.slides_dir,
        )
    )

    ctx = {
        "settings": settings,
        "db_session_factory": db_session_factory,
        "session_map": session_map,
        "builder": builder,
        "resources": resources,
    }
    # Store on the mcp instance so the health endpoint can access it
    mcp._lifespan_context = ctx  # type: ignore[attr-defined]

    try:
        yield ctx
    finally:
        gc_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await gc_task
        await builder.close()
        await engine.dispose()


mcp = FastMCP(
    name="Slidev MCP",
    instructions=(
        "This server generates, renders, and hosts Slidev presentations from markdown. "
        "Read the available resources to learn Slidev syntax, themes, and examples, "
        "then use render_slides to create a presentation."
    ),
    lifespan=app_lifespan,
)
mcp._lifespan_context = None  # type: ignore[attr-defined]


@mcp.custom_route("/health", methods=["GET"])
async def health_check(request):
    """Health endpoint: checks PG connection and semaphore availability."""
    from starlette.responses import JSONResponse

    status = {"status": "ok", "checks": {}}

    # Check database
    try:
        lc = mcp._lifespan_context
        if lc and "db_session_factory" in lc:
            async with lc["db_session_factory"]() as session:
                await session.execute(text("SELECT 1"))
            status["checks"]["database"] = "ok"
        else:
            status["checks"]["database"] = "unavailable"
    except Exception as e:
        status["status"] = "degraded"
        status["checks"]["database"] = str(e)

    # Check builder connectivity
    try:
        if lc and "builder" in lc:
            resp = await lc["builder"]._client.get("/health")
            status["checks"]["builder"] = resp.json() if resp.status_code == 200 else "unhealthy"
        else:
            status["checks"]["builder"] = "unavailable"
    except Exception:
        status["checks"]["builder"] = "unreachable"

    code = 200 if status["status"] == "ok" else 503
    return JSONResponse(status, status_code=code)


@dataclass
class RenderResult:
    """Result of rendering a Slidev presentation."""

    url: str
    uuid: str
    build_time_seconds: float


@dataclass
class SlideInfo:
    """Information about a single slide deck."""

    uuid: str
    url: str
    theme: str
    created_at: str | None
    updated_at: str | None


@dataclass
class SessionSlides:
    """All slides created in the current session."""

    slides: list[SlideInfo] = field(default_factory=list)


@mcp.tool(
    annotations={
        "title": "Render Slidev Presentation",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def render_slides(
    markdown: Annotated[
        str,
        "Full Slidev markdown including frontmatter. Use layouts, components, "
        "and features specific to the chosen theme.",
    ],
    theme: Annotated[
        str,
        "Theme name (e.g. 'seriph', 'default', 'neocarbon'). "
        "Read slidev://themes/installed for the full list of available themes.",
    ],
    uuid: Annotated[
        str | None,
        "UUID of an existing presentation to update in-place (same URL). "
        "Omit to create a new presentation.",
    ] = None,
    ctx: Context = None,
) -> RenderResult:
    """Render a Slidev presentation from markdown and return its hosted URL.

    IMPORTANT: Before calling this tool, you MUST first read the resource
    `slidev://themes/{theme_name}` for the theme you plan to use. Each theme
    has unique layouts, components, and frontmatter options documented there.
    Apply the theme's specific features (layouts, components, slots) in your
    markdown to produce high-quality slides that match the theme's design.

    Also read `slidev://themes/installed` to see all available themes.

    Images must be remote URLs or base64-encoded inline. Local file paths are not supported.
    """
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    markdown_size = len(markdown.encode("utf-8"))

    try:
        result = await _render_slides(
            markdown=markdown,
            theme=theme,
            uuid=uuid,
            session_id=session_id,
            session_map=lc["session_map"],
            builder=lc["builder"],
            db_session_factory=lc["db_session_factory"],
        )
        logger.info(
            "render_slides succeeded",
            extra={
                "uuid": result["uuid"],
                "session_id": session_id,
                "theme": theme,
                "duration": result["build_time_seconds"],
                "markdown_size": markdown_size,
                "success": True,
            },
        )
        return RenderResult(**result)
    except SlidevMcpError as e:
        logger.warning(
            "render_slides failed: %s",
            e.code,
            extra={
                "session_id": session_id,
                "theme": theme,
                "markdown_size": markdown_size,
                "success": False,
            },
        )
        raise ValueError(f"[{e.code}] {e.message}") from None


@mcp.tool(
    annotations={
        "title": "List Session Slides",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
async def list_session_slides(ctx: Context) -> SessionSlides:
    """List all slide presentations created in the current MCP session.

    Returns URLs, themes, and timestamps for each presentation you've created.
    """
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    result = await _list_session_slides(
        session_id=session_id,
        db_session_factory=lc["db_session_factory"],
        settings=lc["settings"],
    )
    return SessionSlides(
        slides=[SlideInfo(**s) for s in result["slides"]],
    )


def _register_resources(mcp_server: FastMCP, resources: dict[str, str]) -> None:
    """Register loaded resource content as FastMCP resources."""
    from fastmcp.resources import TextResource

    for uri, content in resources.items():
        resource = TextResource(
            uri=uri,
            name=uri,
            text=content,
            mime_type="text/markdown",
        )
        mcp_server.add_resource(resource)


# Resources are registered at startup via lifespan.
# We use a post-lifespan hook pattern: the server registers resources
# after the lifespan context is available.
# Since FastMCP resources can be added before run, and our resources are
# loaded from files, we load them eagerly at module level for non-dynamic resources.
# For the lifespan-dependent pattern, we register them in the run() call below.


def run() -> None:
    settings = Settings()
    _configure_logging(settings)

    # Load and register resources eagerly (file-based, no DB needed)
    vendor_dir = Path(__file__).parent.parent.parent / "vendor" / "slidev-docs" / "docs"
    package_dir = Path(__file__).parent
    resources = load_resources(vendor_dir, package_dir)
    _register_resources(mcp, resources)

    transport = settings.server_transport
    if transport == "streamable-http":
        mcp.run(transport="http", host=settings.server_host, port=settings.server_port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    run()
