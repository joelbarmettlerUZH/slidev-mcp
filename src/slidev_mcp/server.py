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
from fastmcp.server.apps import AppConfig, ResourceCSP
from fastmcp.server.lifespan import lifespan
from fastmcp.tools import ToolResult
from mcp import types as mcp_types
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.builder import BuildOrchestrator
from slidev_mcp.config import Settings
from slidev_mcp.db import create_engine, create_session_factory, create_tables
from slidev_mcp.errors import SlidevMcpError
from slidev_mcp.gallery import build_gallery_html
from slidev_mcp.models import Slide, SlideVersion
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

# ---------------------------------------------------------------------------
# MCP App: Slide Viewer
# ---------------------------------------------------------------------------

_VIEWER_URI = "ui://slidev-mcp/viewer.html"
_GALLERY_URI = "ui://slidev-mcp/gallery.html"

_VIEWER_HTML = """\
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="color-scheme" content="light dark">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                   Helvetica, Arial, sans-serif;
      display: flex; flex-direction: column; align-items: center;
      width: 100%; background: transparent; padding: 12px;
    }
    .loading {
      display: flex; align-items: center; justify-content: center;
      min-height: 120px; opacity: 0.5; font-size: 14px;
    }
    .result { display: none; width: 100%; max-width: 640px; }
    .preview {
      width: 100%; border-radius: 8px; overflow: hidden;
      border: 1px solid rgba(128,128,128,0.2);
      cursor: pointer; position: relative;
    }
    .preview img {
      width: 100%; display: block;
    }
    .preview .overlay {
      position: absolute; inset: 0;
      display: flex; align-items: center; justify-content: center;
      background: rgba(0,0,0,0.4); opacity: 0;
      transition: opacity 0.2s; color: #fff;
      font-size: 18px; font-weight: 600;
    }
    .preview:hover .overlay { opacity: 1; }
    .bar {
      display: flex; align-items: center; justify-content: space-between;
      margin-top: 10px; gap: 12px;
    }
    .open-btn {
      padding: 10px 24px;
      background: #2563eb; color: #fff;
      border: none; border-radius: 8px;
      font-size: 14px; font-weight: 600;
      cursor: pointer; transition: background 0.2s;
    }
    .open-btn:hover { background: #1d4ed8; }
    .meta { font-size: 12px; opacity: 0.45; }
    .meta span + span::before { content: " · "; }
    .hidden { display: none; }
  </style>
</head>
<body>
  <div id="loading" class="loading">Building slides&hellip;</div>
  <div id="result" class="result">
    <div id="preview" class="preview hidden">
      <img id="preview-img" alt="Slide preview">
      <div class="overlay">Open Presentation &#x2197;</div>
    </div>
    <div class="bar">
      <button id="open-btn" class="open-btn">
        Open Presentation &#x2197;
      </button>
      <div id="meta" class="meta"></div>
    </div>
  </div>
  <script type="module">
    import { App } from
      "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const app = new App({ name: "Slidev Viewer", version: "1.0.0" });
    let slideUrl = null;

    app.ontoolresult = ({ content }) => {
      const text = content?.find(c => c.type === "text");
      const img = content?.find(c => c.type === "image");

      if (!text) return;
      let data;
      try { data = JSON.parse(text.text); } catch { return; }
      if (!data.url) return;

      slideUrl = data.url;
      document.getElementById("loading").style.display = "none";
      document.getElementById("result").style.display = "block";

      if (img) {
        const preview = document.getElementById("preview");
        preview.classList.remove("hidden");
        const imgEl = document.getElementById("preview-img");
        imgEl.src = "data:" + img.mimeType + ";base64," + img.data;
      }

      document.getElementById("meta").innerHTML =
        "<span>" + data.uuid.slice(0, 8) + "</span>"
        + "<span>Built in " + data.build_time_seconds.toFixed(1) + "s</span>";
    };

    document.getElementById("open-btn").addEventListener("click", () => {
      if (slideUrl) app.openLink({ uri: slideUrl });
    });
    document.getElementById("preview").addEventListener("click", () => {
      if (slideUrl) app.openLink({ uri: slideUrl });
    });

    await app.connect();
  </script>
</body>
</html>"""


@mcp.resource(
    _VIEWER_URI,
    app=AppConfig(
        csp=ResourceCSP(
            resource_domains=["https://unpkg.com"],
        ),
    ),
)
def slide_viewer() -> str:
    """Interactive slide deck viewer — renders the built presentation inline."""
    return _VIEWER_HTML


@mcp.resource(
    _GALLERY_URI,
    app=AppConfig(
        csp=ResourceCSP(
            resource_domains=[
                "https://unpkg.com",
                "https://cdn.jsdelivr.net",
                "https://raw.githubusercontent.com",
                "https://gureckis.github.io",
                "https://i.imgur.com",
            ],
        ),
    ),
)
def theme_gallery() -> str:
    """Visual theme gallery with preview images for all installed themes."""
    return build_gallery_html()


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
    app=AppConfig(resourceUri=_VIEWER_URI),
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
) -> ToolResult:
    """Render a Slidev presentation from markdown and return its hosted URL.

    IMPORTANT: Before calling this tool, you MUST call get_theme with the theme
    name you plan to use. Each theme has unique layouts, components, and
    frontmatter options. Apply the theme's specific features in your markdown
    to produce high-quality slides that match the theme's design.

    If the user has not specified a theme, call list_themes to pick one.
    If you are unfamiliar with Slidev markdown syntax, call get_slidev_guide.

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
        preview = result.pop("preview_base64", "")
        content: list = [
            mcp_types.TextContent(type="text", text=json.dumps(result)),
        ]
        if preview:
            content.append(mcp_types.ImageContent(type="image", data=preview, mimeType="image/png"))
        return ToolResult(content=content)
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


@mcp.tool(
    annotations={
        "title": "List Themes",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
async def list_themes(ctx: Context) -> str:
    """Get a list of all available themes with style descriptions and recommendations.

    Call this to decide which theme to use. Returns a guide organized by style
    (dark, academic, modern, playful, etc.) with "best for" recommendations.

    After picking a theme, call get_theme with the theme name to read its
    full documentation (layouts, components, examples) before rendering.

    This tool does NOT display anything to the user — it is for your own
    reference when choosing a theme.
    """
    lc = ctx.lifespan_context
    resources = lc.get("resources", {})
    guide = resources.get("slidev://themes/guide", "")
    if guide:
        return guide
    return resources.get("slidev://themes/installed", "No theme data available.")


@mcp.tool(
    annotations={
        "title": "Browse Themes",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    app=AppConfig(resourceUri=_GALLERY_URI),
)
async def browse_themes(
    themes: Annotated[
        list[str] | None,
        "Optional list of theme names to show (e.g. ['dracula', 'neocarbon', 'vibe']). "
        "If omitted, all themes are shown. Use list_themes first to find matching "
        "themes, then pass the filtered names here.",
    ] = None,
    ctx: Context = None,
) -> ToolResult:
    """Show the user a visual theme gallery with preview images.

    ONLY call this when the user explicitly asks to SEE or BROWSE themes
    visually (e.g. "show me the themes", "what do they look like", "let me
    pick a theme"). This renders an interactive gallery in the user's UI.

    To show a filtered subset (e.g. only dark themes), first call list_themes
    to identify matching themes, then pass their names here.

    Do NOT call this to decide which theme to use yourself — use list_themes
    for that instead.
    """
    return ToolResult(content=json.dumps({"themes": themes}))


@mcp.tool(
    annotations={
        "title": "Get Theme Details",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
async def get_theme(
    theme: Annotated[
        str,
        "Theme name (e.g. 'seriph', 'neocarbon', 'field-manual'). "
        "Available themes: default, seriph, apple-basic, bricks, shibainu, "
        "academic, cobalt, dracula, eloc, field-manual, frankfurt, geist, "
        "neocarbon, neversink, nord, penguin, purplin, scholarly, "
        "swiss-ai-hub, the-unnamed, unicorn, vibe, vuetiful, zhozhoba.",
    ],
    ctx: Context = None,
) -> str:
    """Get full documentation for a specific theme: layouts, components, and examples.

    Call this BEFORE render_slides to learn the theme's unique features.
    Each theme has different layouts, components, and frontmatter options.
    Use what you learn here to produce high-quality, theme-specific slides.

    This is the primary tool for preparing to render slides. When the user
    specifies a theme, call this directly — no need to call browse_themes.
    """
    lc = ctx.lifespan_context
    resources = lc.get("resources", {})
    uri = f"slidev://themes/{theme}"
    content = resources.get(uri)
    if content:
        return content
    # Check if theme exists at all
    installed = resources.get("slidev://themes/installed", "")
    if f"`{theme}`" in installed:
        return f"Theme '{theme}' is installed but has no detailed documentation."
    return f"Theme '{theme}' not found. Call browse_themes to see available themes."


@mcp.tool(
    annotations={
        "title": "Get Slidev Guide",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
async def get_slidev_guide(ctx: Context) -> str:
    """Get the Slidev syntax guide: how to write slides in markdown.

    Returns the official Slidev syntax reference (frontmatter, slide separators,
    speaker notes, layouts, code blocks) plus built-in layout documentation and
    an example deck. Call this once to learn how to write Slidev presentations.
    """
    lc = ctx.lifespan_context
    resources = lc.get("resources", {})

    parts = []

    syntax = resources.get("slidev://guide/syntax")
    if syntax:
        parts.append("# Slidev Syntax Guide\n\n" + syntax)

    layouts = resources.get("slidev://builtin/layouts")
    if layouts:
        parts.append("\n\n# Built-in Layouts\n\n" + layouts)

    example = resources.get("slidev://examples/minimal")
    if example:
        parts.append("\n\n# Example Deck\n\n" + example)

    if parts:
        return "\n".join(parts)
    return "Slidev guide not available."


@mcp.tool(
    annotations={
        "title": "Export Slides as PDF",
        "readOnlyHint": False,
        "openWorldHint": False,
    },
)
async def export_slides(
    uuid: Annotated[
        str,
        "UUID of the presentation to export. Must be from the current session.",
    ],
    ctx: Context = None,
) -> ToolResult:
    """Export a presentation as a downloadable PDF.

    The presentation must have been created in the current session.
    Returns a URL to download the PDF.
    """
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    builder = lc["builder"]
    session_map = lc["session_map"]

    # Verify UUID ownership
    if not session_map.owns(uuid, session_id):
        raise ValueError("[uuid_foreign] UUID does not belong to this session")

    # Get latest markdown and theme from DB
    async with lc["db_session_factory"]() as session:
        slide = await session.get(Slide, uuid)
        if slide is None:
            raise ValueError("[not_found] Slide not found")

        latest_version = await session.scalar(
            select(SlideVersion.markdown)
            .where(SlideVersion.slide_uuid == uuid)
            .order_by(SlideVersion.version.desc())
            .limit(1)
        )

    if not latest_version:
        raise ValueError("[not_found] No markdown version found for slide")

    try:
        result = await builder.export(latest_version, slide.theme, uuid)
        return ToolResult(
            content=json.dumps(
                {
                    "pdf_url": result.url,
                    "uuid": result.uuid,
                    "export_time_seconds": result.export_time_seconds,
                }
            )
        )
    except SlidevMcpError as e:
        raise ValueError(f"[{e.code}] {e.message}") from None


@mcp.tool(
    annotations={
        "title": "Screenshot Slides",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
)
async def screenshot_slides(
    uuid: Annotated[
        str,
        "UUID of the presentation to screenshot.",
    ],
    ctx: Context = None,
) -> ToolResult:
    """Render all slides as PNG images and return them.

    Use this to visually review a presentation. Returns one image per
    slide so you can see exactly what each slide looks like and give
    specific feedback.
    """
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    builder = lc["builder"]
    session_map = lc["session_map"]

    if not session_map.owns(uuid, session_id):
        raise ValueError("[uuid_foreign] UUID does not belong to this session")

    async with lc["db_session_factory"]() as session:
        slide = await session.get(Slide, uuid)
        if slide is None:
            raise ValueError("[not_found] Slide not found")

        latest_version = await session.scalar(
            select(SlideVersion.markdown)
            .where(SlideVersion.slide_uuid == uuid)
            .order_by(SlideVersion.version.desc())
            .limit(1)
        )

    if not latest_version:
        raise ValueError("[not_found] No markdown version found")

    try:
        result = await builder.export(latest_version, slide.theme, uuid, fmt="png")
        content: list = []
        for img_b64 in result.images_base64:
            content.append(
                mcp_types.ImageContent(
                    type="image",
                    data=img_b64,
                    mimeType="image/png",
                )
            )
        if not content:
            return ToolResult(content="No screenshots generated.")
        return ToolResult(content=content)
    except SlidevMcpError as e:
        raise ValueError(f"[{e.code}] {e.message}") from None


@mcp.resource("slides://session")
async def session_slides_resource(ctx: Context) -> str:
    """All slides created in the current MCP session with themes, URLs, and markdown."""
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    settings = lc["settings"]

    async with lc["db_session_factory"]() as session:
        result = await session.execute(select(Slide).where(Slide.session_id == session_id))
        slides = result.scalars().all()

        entries = []
        for slide in slides:
            latest = await session.scalar(
                select(SlideVersion.markdown)
                .where(SlideVersion.slide_uuid == slide.uuid)
                .order_by(SlideVersion.version.desc())
                .limit(1)
            )
            version_count = await session.scalar(
                select(func.count())
                .select_from(SlideVersion)
                .where(SlideVersion.slide_uuid == slide.uuid)
            )
            host = settings.slides_domain or settings.domain
            entries.append(
                f"## {slide.uuid}\n\n"
                f"- **Theme:** {slide.theme}\n"
                f"- **URL:** https://{host}/slides/{slide.uuid}/\n"
                f"- **Versions:** {version_count}\n\n"
                f"```markdown\n{latest or '(no markdown stored)'}\n```"
            )

    if not entries:
        return "No slides in this session yet."
    return "# Session Slides\n\n" + "\n\n---\n\n".join(entries)


@mcp.resource("slides://session/{uuid}")
async def slide_detail_resource(uuid: str, ctx: Context) -> str:
    """Details for a specific slide: theme, markdown, URL, and version history."""
    lc = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    settings = lc["settings"]

    async with lc["db_session_factory"]() as session:
        slide = await session.get(Slide, uuid)
        if slide is None:
            return f"Slide `{uuid}` not found."
        if slide.session_id != session_id:
            return f"Slide `{uuid}` belongs to a different session."

        versions_result = await session.execute(
            select(SlideVersion)
            .where(SlideVersion.slide_uuid == uuid)
            .order_by(SlideVersion.version.desc())
        )
        version_list = versions_result.scalars().all()

    host = settings.slides_domain or settings.domain
    latest = version_list[0] if version_list else None

    output = f"# Slide {uuid}\n\n"
    output += f"- **Theme:** {slide.theme}\n"
    output += f"- **URL:** https://{host}/slides/{uuid}/\n"
    output += f"- **Created:** {slide.created_at}\n"
    output += f"- **Updated:** {slide.updated_at}\n"
    output += f"- **Versions:** {len(version_list)}\n"

    if latest:
        output += f"\n## Current Markdown (v{latest.version})\n\n"
        output += f"```markdown\n{latest.markdown}\n```\n"

    if len(version_list) > 1:
        output += "\n## Version History\n\n"
        for v in version_list:
            output += f"- **v{v.version}** ({v.created_at}) — theme: {v.theme}\n"

    return output


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
