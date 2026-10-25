import re
import uuid as uuid_mod
from typing import Annotated, Any

from pydantic import Field
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.builder import BuildOrchestrator
from slidev_mcp.config import Settings
from slidev_mcp.errors import InvalidUuid
from slidev_mcp.models import Slide, SlideVersion

_UUID4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)

MAX_LOOKUP_UUIDS = 50


def validate_uuid(uuid: str) -> str:
    """Return the UUID if it is a well-formed v4, else raise InvalidUuid.

    Must run before a user-supplied UUID reaches any filesystem path.
    """
    if not _UUID4_PATTERN.match(uuid):
        raise InvalidUuid(uuid)
    return uuid


async def render_slides(
    markdown: Annotated[str, Field(description="Full Slidev markdown including frontmatter")],
    theme: Annotated[str, Field(description="Theme name (e.g. 'seriph', 'default')")],
    uuid: Annotated[
        str | None,
        Field(description="UUID to update existing slides, or omit for new"),
    ] = None,
    color_schema: Annotated[
        str,
        Field(description="Color scheme: 'light', 'dark', or 'auto'"),
    ] = "light",
    *,
    session_id: str,
    builder: BuildOrchestrator,
    db_session_factory: async_sessionmaker[AsyncSession],
) -> dict[str, Any]:
    """Render a Slidev presentation from markdown.

    Images must be remote URLs or base64-encoded inline. Local file paths are not supported.

    The UUID is the only capability needed to update a presentation: there is no
    per-session ownership, because the stateless MCP protocol has no stable session.
    `session_id` is recorded for diagnostics only and is never used for access control.
    """
    is_new = uuid is None
    if is_new:
        uuid = str(uuid_mod.uuid4())

    # Validate UUID format (path traversal prevention)
    if not is_new:
        validate_uuid(uuid)

    result = await builder.build(markdown, theme, uuid, color_schema=color_schema)

    # Update DB
    async with db_session_factory() as session:
        existing = await session.get(Slide, uuid)
        if existing:
            existing.theme = theme
            existing.updated_at = func.now()
        else:
            session.add(Slide(uuid=uuid, session_id=session_id, theme=theme))

        # Append versioned markdown snapshot
        max_ver = await session.scalar(
            select(func.max(SlideVersion.version)).where(SlideVersion.slide_uuid == uuid)
        )
        session.add(
            SlideVersion(
                slide_uuid=uuid,
                version=(max_ver or 0) + 1,
                markdown=markdown,
                theme=theme,
            )
        )
        await session.commit()

    return {
        "url": result.url,
        "uuid": result.uuid,
        "build_time_seconds": result.build_time_seconds,
        "preview_base64": result.preview_base64,
    }


async def list_session_slides(
    uuids: Annotated[
        list[str],
        Field(description="UUIDs of presentations to look up", max_length=MAX_LOOKUP_UUIDS),
    ],
    *,
    db_session_factory: async_sessionmaker[AsyncSession],
    settings: Settings,
) -> dict[str, Any]:
    """Look up presentations by UUID. Unknown UUIDs are omitted from the result."""
    unique = list(dict.fromkeys(validate_uuid(u) for u in uuids))
    if not unique:
        return {"slides": []}

    async with db_session_factory() as session:
        result = await session.execute(select(Slide).where(Slide.uuid.in_(unique)))
        by_uuid = {s.uuid: s for s in result.scalars().all()}

        rows = await session.execute(
            select(SlideVersion.slide_uuid, func.count())
            .where(SlideVersion.slide_uuid.in_(list(by_uuid)))
            .group_by(SlideVersion.slide_uuid)
        )
        version_counts: dict[str, int] = dict(rows.all())

    host = settings.slides_domain or settings.domain
    return {
        "slides": [
            {
                "uuid": s.uuid,
                "url": f"https://{host}/slides/{s.uuid}/",
                "theme": s.theme,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "updated_at": s.updated_at.isoformat() if s.updated_at else None,
                "version_count": version_counts.get(s.uuid, 0),
            }
            for u in unique
            if (s := by_uuid.get(u))
        ]
    }
