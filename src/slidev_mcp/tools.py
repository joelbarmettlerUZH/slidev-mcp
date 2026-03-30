import re
import uuid as uuid_mod
from typing import Annotated, Any

from pydantic import Field
from sqlalchemy import func, select

from slidev_mcp.builder import BuildOrchestrator
from slidev_mcp.errors import (
    InvalidUuid,
    UuidForeign,
    UuidSealed,
)
from slidev_mcp.models import Slide, SlideVersion
from slidev_mcp.sessions import SessionMap

_UUID4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)


async def render_slides(
    markdown: Annotated[str, Field(description="Full Slidev markdown including frontmatter")],
    theme: Annotated[str, Field(description="Theme name (e.g. 'seriph', 'default')")],
    uuid: Annotated[
        str | None,
        Field(description="UUID to update existing slides, or omit for new"),
    ] = None,
    *,
    session_id: str,
    session_map: SessionMap,
    builder: BuildOrchestrator,
    db_session_factory: Any,
) -> dict[str, Any]:
    """Render a Slidev presentation from markdown.

    Images must be remote URLs or base64-encoded inline. Local file paths are not supported.
    """
    is_new = uuid is None
    if is_new:
        uuid = str(uuid_mod.uuid4())

    # Validate UUID format (path traversal prevention)
    if not is_new and not _UUID4_PATTERN.match(uuid):
        raise InvalidUuid(uuid)

    # Check UUID ownership
    if not is_new:
        if session_map.is_active(uuid):
            if not session_map.owns(uuid, session_id):
                raise UuidForeign(uuid)
        else:
            # UUID not active — check if it exists in DB (sealed)
            async with db_session_factory() as session:
                existing = await session.get(Slide, uuid)
            if existing is not None:
                raise UuidSealed(uuid)

    result = await builder.build(markdown, theme, uuid)

    # Update DB and session map
    async with db_session_factory() as session:
        existing = await session.get(Slide, uuid)
        if existing:
            existing.theme = theme
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

    session_map.register(uuid, session_id)

    return {
        "url": result.url,
        "uuid": result.uuid,
        "build_time_seconds": result.build_time_seconds,
        "preview_base64": result.preview_base64,
    }


async def list_session_slides(
    *,
    session_id: str,
    db_session_factory: Any,
    settings: Any,
) -> dict[str, Any]:
    """List all slides created in the current session."""
    async with db_session_factory() as session:
        result = await session.execute(select(Slide).where(Slide.session_id == session_id))
        slides = result.scalars().all()

        # Get version counts in one query
        version_counts: dict[str, int] = {}
        if slides:
            uuids = [s.uuid for s in slides]
            rows = await session.execute(
                select(SlideVersion.slide_uuid, func.count())
                .where(SlideVersion.slide_uuid.in_(uuids))
                .group_by(SlideVersion.slide_uuid)
            )
            version_counts = dict(rows.all())

    return {
        "slides": [
            {
                "uuid": s.uuid,
                "url": f"https://{settings.slides_domain or settings.domain}/slides/{s.uuid}/",
                "theme": s.theme,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "updated_at": s.updated_at.isoformat() if s.updated_at else None,
                "version_count": version_counts.get(s.uuid, 0),
            }
            for s in slides
        ]
    }
