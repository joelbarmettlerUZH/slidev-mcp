from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.builder import BuildOrchestrator, BuildResult
from slidev_mcp.config import Settings
from slidev_mcp.errors import (
    BuildFailed,
    InvalidUuid,
    ThemeNotAllowed,
)
from slidev_mcp.models import Slide, SlideVersion
from slidev_mcp.server import SlideInfo
from slidev_mcp.tools import list_session_slides, render_slides


@pytest.fixture
def settings() -> Settings:
    return Settings(domain="test.example.com")


@pytest.fixture
def mock_builder() -> MagicMock:
    builder = MagicMock(spec=BuildOrchestrator)

    async def fake_build(
        markdown: str, theme: str, uuid: str, color_schema: str = "light"
    ) -> BuildResult:
        return BuildResult(
            uuid=uuid,
            url=f"https://test.example.com/slides/{uuid}/",
            build_time_seconds=2.5,
        )

    builder.build = AsyncMock(side_effect=fake_build)
    return builder


class TestRenderSlides:
    async def test_new_slide(
        self,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        result = await render_slides(
            markdown="# Test",
            theme="default",
            session_id="session-1",
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        assert "url" in result
        assert "uuid" in result
        assert "build_time_seconds" in result
        mock_builder.build.assert_called_once()

        # Verify DB row created
        async with db_session_factory() as session:
            slide = await session.get(Slide, result["uuid"])
        assert slide is not None
        assert slide.session_id == "session-1"
        assert slide.theme == "default"

        # Verify version row created
        async with db_session_factory() as session:
            ver_result = await session.execute(
                select(SlideVersion).where(SlideVersion.slide_uuid == result["uuid"])
            )
            versions = ver_result.scalars().all()
        assert len(versions) == 1
        assert versions[0].version == 1
        assert versions[0].markdown == "# Test"
        assert versions[0].theme == "default"

        # Verify session map registration

    async def test_update_owned_slide(
        self,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        # First create
        result1 = await render_slides(
            markdown="# V1",
            theme="default",
            session_id="session-1",
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        # Update with same UUID
        result2 = await render_slides(
            markdown="# V2",
            theme="seriph",
            uuid=result1["uuid"],
            session_id="session-1",
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        assert result2["uuid"] == result1["uuid"]

        # Verify DB row updated
        async with db_session_factory() as session:
            slide = await session.get(Slide, result1["uuid"])
        assert slide.theme == "seriph"

        # Verify both versions exist
        async with db_session_factory() as session:
            ver_result = await session.execute(
                select(SlideVersion)
                .where(SlideVersion.slide_uuid == result1["uuid"])
                .order_by(SlideVersion.version)
            )
            versions = ver_result.scalars().all()
        assert len(versions) == 2
        assert versions[0].version == 1
        assert versions[0].markdown == "# V1"
        assert versions[0].theme == "default"
        assert versions[1].version == 2
        assert versions[1].markdown == "# V2"
        assert versions[1].theme == "seriph"

    async def test_any_session_can_update_existing_uuid(
        self,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        """The UUID is the capability: a different (or new) session may update it."""
        existing_uuid = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
        async with db_session_factory() as session:
            session.add(Slide(uuid=existing_uuid, session_id="old-session", theme="default"))
            session.add(
                SlideVersion(slide_uuid=existing_uuid, version=1, markdown="# V1", theme="default")
            )
            await session.commit()

        result = await render_slides(
            markdown="# V2",
            theme="seriph",
            uuid=existing_uuid,
            session_id="new-session",
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        assert result["uuid"] == existing_uuid
        async with db_session_factory() as session:
            slide = await session.get(Slide, existing_uuid)
            max_ver = await session.scalar(
                select(func.max(SlideVersion.version)).where(
                    SlideVersion.slide_uuid == existing_uuid
                )
            )
        assert slide.theme == "seriph"
        assert slide.session_id == "old-session"  # informational, not rewritten
        assert max_ver == 2

    @pytest.mark.parametrize(
        "bad_uuid",
        [
            "../../etc/passwd",
            "not-a-uuid",
            "12345678-1234-1234-1234-123456789abc",  # not v4 (wrong version nibble)
            "",
            "../../../tmp/evil",
        ],
    )
    async def test_invalid_uuid_rejected(
        self,
        bad_uuid: str,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        with pytest.raises(InvalidUuid):
            await render_slides(
                markdown="# Test",
                theme="default",
                uuid=bad_uuid,
                session_id="my-session",
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_build_error_propagated(
        self,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        mock_builder.build = AsyncMock(side_effect=BuildFailed("build error"))

        with pytest.raises(BuildFailed):
            await render_slides(
                markdown="# Test",
                theme="default",
                session_id="session-1",
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_theme_validation_propagated(
        self,
        mock_builder: MagicMock,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        mock_builder.build = AsyncMock(side_effect=ThemeNotAllowed("bad-theme"))

        with pytest.raises(ThemeNotAllowed):
            await render_slides(
                markdown="# Test",
                theme="bad-theme",
                session_id="session-1",
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )


class TestListSessionSlides:
    async def test_empty_lookup(
        self,
        settings: Settings,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        result = await list_session_slides(
            uuids=[],
            db_session_factory=db_session_factory,
            settings=settings,
        )

        assert result["slides"] == []

    async def test_returns_only_requested_uuids(
        self,
        settings: Settings,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        uuid_1 = "11111111-1111-4111-8111-111111111111"
        uuid_2 = "22222222-2222-4222-8222-222222222222"
        uuid_3 = "33333333-3333-4333-8333-333333333333"
        missing = "44444444-4444-4444-8444-444444444444"
        async with db_session_factory() as session:
            session.add(Slide(uuid=uuid_1, session_id="session-a", theme="default"))
            session.add(Slide(uuid=uuid_2, session_id="session-b", theme="seriph"))
            session.add(Slide(uuid=uuid_3, session_id="session-a", theme="dracula"))
            session.add(SlideVersion(slide_uuid=uuid_1, version=1, markdown="# A", theme="default"))
            await session.commit()

        result = await list_session_slides(
            uuids=[uuid_1, uuid_2, missing, uuid_1],  # duplicate + unknown
            db_session_factory=db_session_factory,
            settings=settings,
        )

        assert [s["uuid"] for s in result["slides"]] == [uuid_1, uuid_2]
        # The server wraps each row in SlideInfo; its fields must match the tool output
        assert [SlideInfo(**s).uuid for s in result["slides"]] == [uuid_1, uuid_2]
        assert result["slides"][0]["version_count"] == 1
        assert result["slides"][1]["version_count"] == 0
        for slide in result["slides"]:
            assert "test.example.com" in slide["url"]

    async def test_invalid_uuid_rejected(
        self,
        settings: Settings,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        with pytest.raises(InvalidUuid):
            await list_session_slides(
                uuids=["../../etc/passwd"],
                db_session_factory=db_session_factory,
                settings=settings,
            )
