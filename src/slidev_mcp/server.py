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
from fastmcp.dependencies import CurrentContext
from fastmcp.exceptions import ToolError
from fastmcp.server.apps import AppConfig, ResourceCSP
from fastmcp.server.lifespan import lifespan
from fastmcp.server.middleware.logging import StructuredLoggingMiddleware
from fastmcp.server.middleware.timing import TimingMiddleware
from fastmcp.tools import ToolResult
from mcp import types as mcp_types
from mcp.types import Icon
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

# ---------------------------------------------------------------------------
# Icons (monochrome SVG, base64-encoded data URIs)
# ---------------------------------------------------------------------------
_SVG_MIME = "image/svg+xml"

_ICON_SERVER = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxyZWN0IHg9IjIiIHk9IjMiIHdpZHRo"
        "PSIyMCIgaGVpZ2h0PSIxNCIgcng9IjIiLz48bGluZSB4MT0iOCIgeTE9IjIxIiB4Mj0iMTYiIH"
        "kyPSIyMSIvPjxsaW5lIHgxPSIxMiIgeTE9IjE3IiB4Mj0iMTIiIHkyPSIyMSIvPjwvc3ZnPg=="
    ),
    mimeType=_SVG_MIME,
)
_ICON_RENDER = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iMTIi"
        "IHI9IjEwIi8+PHBvbHlnb24gcG9pbnRzPSIxMCA4IDE2IDEyIDEwIDE2IDEwIDgiLz48L3N2Zz4="
    ),
    mimeType=_SVG_MIME,
)
_ICON_THEME = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxjaXJjbGUgY3g9IjEzLjUiIGN5PSI2"
        "LjUiIHI9IjIuNSIvPjxjaXJjbGUgY3g9IjE3LjUiIGN5PSIxMC41IiByPSIyLjUiLz48Y2lyY2"
        "xlIGN4PSI4LjUiIGN5PSI3LjUiIHI9IjIuNSIvPjxjaXJjbGUgY3g9IjYuNSIgY3k9IjEyLjUi"
        "IHI9IjIuNSIvPjxwYXRoIGQ9Ik0xMiAyQzYuNSAyIDIgNi41IDIgMTJzNC41IDEwIDEwIDEwYy"
        "45IDAgMS43LS44IDEuNy0xLjcgMC0uNS0uMi0uOS0uNS0xLjItLjMtLjMtLjUtLjctLjUtMS4y"
        "IDAtLjkuOC0xLjcgMS43LTEuN0gxNmMzLjMgMCA2LTIuNyA2LTYgMC01LjUtNC41LTkuOC0xMC"
        "05Ljh6Ii8+PC9zdmc+"
    ),
    mimeType=_SVG_MIME,
)
_ICON_EXPORT = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0yMSAxNXY0YTIgMiAw"
        "IDAgMS0yIDJINWEyIDIgMCAwIDEtMi0ydi00Ii8+PHBvbHlsaW5lIHBvaW50cz0iNyAxMCAxMi"
        "AxNSAxNyAxMCIvPjxsaW5lIHgxPSIxMiIgeTE9IjE1IiB4Mj0iMTIiIHkyPSIzIi8+PC9zdmc+"
    ),
    mimeType=_SVG_MIME,
)
_ICON_GUIDE = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik00IDE5LjVBMi41IDIu"
        "NSAwIDAgMSA2LjUgMTdIMjAiLz48cGF0aCBkPSJNNi41IDJIMjB2MjBINi41QTIuNSAyLjUgMC"
        "AwIDEgNCAxOS41di0xNUEyLjUgMi41IDAgMCAxIDYuNSAyeiIvPjwvc3ZnPg=="
    ),
    mimeType=_SVG_MIME,
)
_ICON_SESSION = Icon(
    src=(
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdm"
        "ciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25l"
        "IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD"
        "0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxsaW5lIHgxPSI4IiB5MT0iNiIgeDI9"
        "IjIxIiB5Mj0iNiIvPjxsaW5lIHgxPSI4IiB5MT0iMTIiIHgyPSIyMSIgeTI9IjEyIi8+PGxp"
        "bmUgeDE9IjgiIHkxPSIxOCIgeDI9IjIxIiB5Mj0iMTgiLz48bGluZSB4MT0iMyIgeTE9IjYiIH"
        "gyPSIzLjAxIiB5Mj0iNiIvPjxsaW5lIHgxPSIzIiB5MT0iMTIiIHgyPSIzLjAxIiB5Mj0iMTIi"
        "Lz48bGluZSB4MT0iMyIgeTE9IjE4IiB4Mj0iMy4wMSIgeTI9IjE4Ii8+PC9zdmc+"
    ),
    mimeType=_SVG_MIME,
)


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


@dataclass
class LifespanState:
    """Typed container for lifespan-managed dependencies."""

    settings: Settings
    db_session_factory: async_sessionmaker[AsyncSession]
    session_map: SessionMap
    builder: BuildOrchestrator
    resources: dict[str, str]


# Module-level state for the health endpoint (set during lifespan)
_state: LifespanState | None = None


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

    global _state
    state = LifespanState(
        settings=settings,
        db_session_factory=db_session_factory,
        session_map=session_map,
        builder=builder,
        resources=resources,
    )
    _state = state

    try:
        yield state
    finally:
        _state = None
        gc_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await gc_task
        await builder.close()
        await engine.dispose()


mcp = FastMCP(
    name="Slidev MCP",
    version="0.1.0",
    instructions=(
        "This server generates, renders, and hosts Slidev presentations from markdown. "
        "Read the available resources to learn Slidev syntax, themes, and examples, "
        "then use render_slides to create a presentation."
    ),
    icons=[_ICON_SERVER],
    lifespan=app_lifespan,
    on_duplicate="warn",
    middleware=[
        StructuredLoggingMiddleware(),
        TimingMiddleware(),
    ],
)

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
      width: 100%; display: block; aspect-ratio: 16/9;
      object-fit: cover;
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
      display: flex; align-items: center;
      margin-top: 10px; gap: 8px;
    }
    .btn {
      display: inline-flex; align-items: center; gap: 6px;
      height: 32px; padding: 0 10px;
      background: transparent; color: inherit;
      border: 0.5px solid rgba(128,128,128,0.3);
      border-radius: 8px;
      font-size: 14px;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.15s ease-in-out;
    }
    .btn:hover {
      background: rgba(128,128,128,0.1);
      border-color: rgba(128,128,128,0.15);
    }
    .btn svg { opacity: 0.5; flex-shrink: 0; }
    .btn.loading { opacity: 0.5; pointer-events: none; }
    .spacer { flex: 1; }
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
      <button id="open-btn" class="btn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="currentColor" d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2v-7h-2zM14 3v2h3.59l-9.83 9.83l1.41 1.41L19 6.41V10h2V3z"/></svg> Open</button>
      <button id="pdf-btn" class="btn"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24"><path fill="currentColor" d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2m-8.5 7.5c0 .83-.67 1.5-1.5 1.5H9v2H7.5V7H10c.83 0 1.5.67 1.5 1.5zm5 2c0 .83-.67 1.5-1.5 1.5h-2.5V7H15c.83 0 1.5.67 1.5 1.5zm4-3H19v1h1.5V11H19v2h-1.5V7h3zM9 9.5h1v-1H9zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4zm10 5.5h1v-3h-1z"/></svg> Download PDF</button>
      <div class="spacer"></div>
      <div id="meta" class="meta"></div>
    </div>
  </div>
  <script type="module">
    import { App } from
      "https://unpkg.com/@modelcontextprotocol/ext-apps@0.4.0/app-with-deps";

    const app = new App({ name: "Slidev Viewer", version: "1.0.0" });
    let slideUrl = null;
    let slideUuid = null;

    app.ontoolresult = ({ content }) => {
      const text = content?.find(c => c.type === "text");
      const img = content?.find(c => c.type === "image");

      if (!text) return;
      let data;
      try { data = JSON.parse(text.text); } catch { return; }
      if (!data.url) return;

      slideUrl = data.url;
      slideUuid = data.uuid;
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
      if (slideUrl) app.openLink({ url: slideUrl });
    });
    document.getElementById("preview").addEventListener("click", () => {
      if (slideUrl) app.openLink({ url: slideUrl });
    });
    document.getElementById("pdf-btn").addEventListener("click", async () => {
      if (!slideUuid) return;
      const btn = document.getElementById("pdf-btn");
      btn.classList.add("loading");
      btn.lastChild.textContent = " Exporting...";
      try {
        const result = await app.callServerTool({
          name: "export_slides",
          arguments: { uuid: slideUuid },
        });
        const text = result.content?.find(c => c.type === "text");
        if (text) {
          const data = JSON.parse(text.text);
          if (data.pdf_url) app.openLink({ url: data.pdf_url });
        }
      } catch (err) {
        btn.lastChild.textContent = " Export failed";
        setTimeout(() => { btn.lastChild.textContent = " Download PDF"; }, 3000);
      } finally {
        btn.classList.remove("loading");
        btn.lastChild.textContent = " Download PDF";
      }
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
        if _state is not None:
            async with _state.db_session_factory() as session:
                await session.execute(text("SELECT 1"))
            status["checks"]["database"] = "ok"
        else:
            status["checks"]["database"] = "unavailable"
    except Exception as e:
        status["status"] = "degraded"
        status["checks"]["database"] = str(e)

    # Check builder connectivity
    try:
        if _state is not None:
            resp = await _state.builder._client.get("/health")
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
    tags={"rendering", "write"},
    icons=[_ICON_RENDER],
    timeout=130,
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
    color_schema: Annotated[
        str,
        "Color scheme: 'light' (default), 'dark', or 'auto'. "
        "Controls whether slides render in light or dark mode.",
    ] = "light",
    ctx: Context = CurrentContext(),
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
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"
    markdown_size = len(markdown.encode("utf-8"))

    try:
        await ctx.report_progress(0, 3, "Validating input")
        await ctx.info(f"Building presentation with theme '{theme}'...")

        await ctx.report_progress(1, 3, "Building presentation")
        result = await _render_slides(
            markdown=markdown,
            theme=theme,
            uuid=uuid,
            color_schema=color_schema,
            session_id=session_id,
            session_map=state.session_map,
            builder=state.builder,
            db_session_factory=state.db_session_factory,
        )

        await ctx.report_progress(2, 3, "Preparing response")
        await ctx.info(f"Built {result['uuid']} in {result['build_time_seconds']:.1f}s")
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
        await ctx.report_progress(3, 3, "Done")
        return ToolResult(content=content)
    except SlidevMcpError as e:
        await ctx.warning(f"Render failed: [{e.code}] {e.message}")
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
        raise ToolError(f"[{e.code}] {e.message}") from None


@mcp.tool(
    annotations={
        "title": "List Session Slides",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    tags={"session", "read-only"},
    icons=[_ICON_SESSION],
    timeout=10,
)
async def list_session_slides(ctx: Context = CurrentContext()) -> SessionSlides:
    """List all slide presentations created in the current MCP session.

    Returns URLs, themes, and timestamps for each presentation you've created.
    """
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    result = await _list_session_slides(
        session_id=session_id,
        db_session_factory=state.db_session_factory,
        settings=state.settings,
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
    tags={"themes", "read-only"},
    icons=[_ICON_THEME],
    timeout=5,
)
async def list_themes(ctx: Context = CurrentContext()) -> str:
    """Get a list of all available themes with style descriptions and recommendations.

    Call this to decide which theme to use. Returns a guide organized by style
    (dark, academic, modern, playful, etc.) with "best for" recommendations.

    After picking a theme, call get_theme with the theme name to read its
    full documentation (layouts, components, examples) before rendering.

    This tool does NOT display anything to the user — it is for your own
    reference when choosing a theme.
    """
    state: LifespanState = ctx.lifespan_context
    guide = state.resources.get("slidev://themes/guide", "")
    if guide:
        return guide
    return state.resources.get("slidev://themes/installed", "No theme data available.")


@mcp.tool(
    annotations={
        "title": "Browse Themes",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    tags={"themes", "read-only", "visual"},
    icons=[_ICON_THEME],
    timeout=5,
    app=AppConfig(resourceUri=_GALLERY_URI),
)
async def browse_themes(
    themes: Annotated[
        list[str] | None,
        "Optional list of theme names to show (e.g. ['dracula', 'neocarbon', 'vibe']). "
        "If omitted, all themes are shown. Use list_themes first to find matching "
        "themes, then pass the filtered names here.",
    ] = None,
    ctx: Context = CurrentContext(),
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
    tags={"themes", "read-only"},
    icons=[_ICON_THEME],
    timeout=5,
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
    ctx: Context = CurrentContext(),
) -> str:
    """Get full documentation for a specific theme: layouts, components, and examples.

    Call this BEFORE render_slides to learn the theme's unique features.
    Each theme has different layouts, components, and frontmatter options.
    Use what you learn here to produce high-quality, theme-specific slides.

    This is the primary tool for preparing to render slides. When the user
    specifies a theme, call this directly — no need to call browse_themes.
    """
    state: LifespanState = ctx.lifespan_context
    uri = f"slidev://themes/{theme}"
    content = state.resources.get(uri)
    if content:
        return content
    installed = state.resources.get("slidev://themes/installed", "")
    if f"`{theme}`" in installed:
        return f"Theme '{theme}' is installed but has no detailed documentation."
    return f"Theme '{theme}' not found. Call browse_themes to see available themes."


@mcp.tool(
    annotations={
        "title": "Get Slidev Guide",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    tags={"guide", "read-only"},
    icons=[_ICON_GUIDE],
    timeout=5,
)
async def get_slidev_guide(ctx: Context = CurrentContext()) -> str:
    """Get the Slidev syntax guide: how to write slides in markdown.

    Returns the official Slidev syntax reference (frontmatter, slide separators,
    speaker notes, layouts, code blocks) plus built-in layout documentation and
    an example deck. Call this once to learn how to write Slidev presentations.
    """
    state: LifespanState = ctx.lifespan_context

    parts = []

    syntax = state.resources.get("slidev://guide/syntax")
    if syntax:
        parts.append("# Slidev Syntax Guide\n\n" + syntax)

    layouts = state.resources.get("slidev://builtin/layouts")
    if layouts:
        parts.append("\n\n# Built-in Layouts\n\n" + layouts)

    example = state.resources.get("slidev://examples/minimal")
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
    tags={"export", "write"},
    icons=[_ICON_EXPORT],
    timeout=190,
)
async def export_slides(
    uuid: Annotated[
        str,
        "UUID of the presentation to export. Must be from the current session.",
    ],
    ctx: Context = CurrentContext(),
) -> ToolResult:
    """Export a presentation as a downloadable PDF.

    The presentation must have been created in the current session.
    Returns a URL to download the PDF.
    """
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    await ctx.report_progress(0, 3, "Verifying session ownership")

    if not state.session_map.owns(uuid, session_id):
        raise ToolError("[uuid_foreign] UUID does not belong to this session")

    async with state.db_session_factory() as session:
        slide = await session.get(Slide, uuid)
        if slide is None:
            raise ToolError("[not_found] Slide not found")

        latest_version = await session.scalar(
            select(SlideVersion.markdown)
            .where(SlideVersion.slide_uuid == uuid)
            .order_by(SlideVersion.version.desc())
            .limit(1)
        )

    if not latest_version:
        raise ToolError("[not_found] No markdown version found for slide")

    try:
        await ctx.report_progress(1, 3, "Exporting to PDF")
        await ctx.info(f"Exporting {uuid} to PDF...")
        result = await state.builder.export(latest_version, slide.theme, uuid)
        await ctx.report_progress(3, 3, "Export complete")
        await ctx.info(f"Exported {uuid} in {result.export_time_seconds:.1f}s")
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
        await ctx.warning(f"Export failed: [{e.code}] {e.message}")
        raise ToolError(f"[{e.code}] {e.message}") from None


@mcp.tool(
    annotations={
        "title": "Screenshot Slides",
        "readOnlyHint": True,
        "openWorldHint": False,
    },
    tags={"export", "read-only", "visual"},
    icons=[_ICON_EXPORT],
    timeout=190,
)
async def screenshot_slides(
    uuid: Annotated[
        str,
        "UUID of the presentation to screenshot.",
    ],
    ctx: Context = CurrentContext(),
) -> ToolResult:
    """Render all slides as PNG images and return them.

    Use this to visually review a presentation. Returns one image per
    slide so you can see exactly what each slide looks like and give
    specific feedback.
    """
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    await ctx.report_progress(0, 3, "Verifying session ownership")

    if not state.session_map.owns(uuid, session_id):
        raise ToolError("[uuid_foreign] UUID does not belong to this session")

    async with state.db_session_factory() as session:
        slide = await session.get(Slide, uuid)
        if slide is None:
            raise ToolError("[not_found] Slide not found")

        latest_version = await session.scalar(
            select(SlideVersion.markdown)
            .where(SlideVersion.slide_uuid == uuid)
            .order_by(SlideVersion.version.desc())
            .limit(1)
        )

    if not latest_version:
        raise ToolError("[not_found] No markdown version found")

    try:
        await ctx.report_progress(1, 3, "Rendering slide screenshots")
        await ctx.info(f"Screenshotting {uuid}...")
        result = await state.builder.export(latest_version, slide.theme, uuid, fmt="png")
        await ctx.report_progress(3, 3, "Screenshots complete")
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
        await ctx.warning(f"Screenshot failed: [{e.code}] {e.message}")
        raise ToolError(f"[{e.code}] {e.message}") from None


@mcp.resource("slides://session", tags={"session"}, icons=[_ICON_SESSION])
async def session_slides_resource(ctx: Context = CurrentContext()) -> str:
    """All slides created in the current MCP session with themes, URLs, and markdown."""
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    async with state.db_session_factory() as session:
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
            host = state.settings.slides_domain or state.settings.domain
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


@mcp.resource("slides://session/{uuid}", tags={"session"}, icons=[_ICON_SESSION])
async def slide_detail_resource(uuid: str, ctx: Context = CurrentContext()) -> str:
    """Details for a specific slide: theme, markdown, URL, and version history."""
    state: LifespanState = ctx.lifespan_context
    session_id = ctx.session_id or ctx.client_id or "unknown"

    async with state.db_session_factory() as session:
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

    host = state.settings.slides_domain or state.settings.domain
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


def _uri_to_tags(uri: str) -> set[str]:
    """Derive resource tags from URI prefix."""
    if uri.startswith("slidev://guide/") or uri.startswith("slidev://builtin/"):
        return {"guide"}
    if uri.startswith("slidev://themes/"):
        return {"themes"}
    if uri.startswith("slidev://examples/"):
        return {"examples"}
    return set()


def _uri_to_icons(uri: str) -> list[Icon]:
    """Derive resource icons from URI prefix."""
    if uri.startswith("slidev://guide/") or uri.startswith("slidev://builtin/"):
        return [_ICON_GUIDE]
    if uri.startswith("slidev://themes/"):
        return [_ICON_THEME]
    if uri.startswith("slidev://examples/"):
        return [_ICON_GUIDE]
    return []


def _register_resources(mcp_server: FastMCP, resources: dict[str, str]) -> None:
    """Register loaded resource content as FastMCP resources."""
    from fastmcp.resources import TextResource

    for uri, content in resources.items():
        resource = TextResource(
            uri=uri,
            name=uri,
            text=content,
            mime_type="text/markdown",
            tags=_uri_to_tags(uri),
            icons=_uri_to_icons(uri),
        )
        mcp_server.add_resource(resource)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------


@mcp.prompt(
    title="Create Presentation",
    tags={"rendering"},
    icons=[_ICON_RENDER],
)
def create_presentation(
    topic: Annotated[str, "The topic for the presentation"],
    style: Annotated[
        str, "Preferred visual style (e.g. 'professional', 'playful', 'academic')"
    ] = "professional",
    slide_count: Annotated[str, "Approximate number of slides"] = "10",
) -> str:
    """Guided workflow for creating a new Slidev presentation."""
    return (
        f'Create a Slidev presentation about "{topic}" with approximately '
        f"{slide_count} slides in a {style} style.\n\n"
        "Steps:\n"
        f'1. Call list_themes to find a theme matching the "{style}" style\n'
        "2. Call get_theme with the chosen theme name to read its full documentation\n"
        "3. Call get_slidev_guide if you need a Slidev syntax refresher\n"
        "4. Write the markdown using the theme's layouts, components, and features\n"
        "5. Call render_slides with the markdown and theme name"
    )


@mcp.prompt(
    title="Review and Improve Presentation",
    tags={"export", "visual"},
    icons=[_ICON_EXPORT],
)
def review_presentation(
    uuid: Annotated[str, "UUID of the presentation to review"],
) -> str:
    """Guided workflow for visually reviewing and improving an existing presentation."""
    return (
        f"Review the presentation {uuid}:\n\n"
        "1. Call screenshot_slides to see all slides as images\n"
        "2. Analyze each slide for design quality, content clarity, and flow\n"
        "3. Suggest specific improvements (layout choices, content edits, visual balance)\n"
        "4. Offer to re-render with the improvements applied"
    )


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
