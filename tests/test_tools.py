import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from slidev_mcp.builder import BuildOrchestrator, BuildResult
from slidev_mcp.config import Settings
from slidev_mcp.errors import (
    BuildFailed,
    ConcurrentLimitReached,
    InvalidUuid,
    ThemeNotAllowed,
    UuidForeign,
    UuidSealed,
)
from slidev_mcp.models import Slide
from slidev_mcp.sessions import SessionMap
from slidev_mcp.tools import list_session_slides, render_slides


@pytest.fixture
def settings() -> Settings:
    return Settings(domain="test.example.com")


@pytest.fixture
def session_map() -> SessionMap:
    return SessionMap()


@pytest.fixture
def mock_builder() -> MagicMock:
    builder = MagicMock(spec=BuildOrchestrator)
    builder._semaphore = asyncio.Semaphore(3)

    async def fake_build(markdown: str, theme: str, uuid: str) -> BuildResult:
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
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        result = await render_slides(
            markdown="# Test",
            theme="default",
            session_id="session-1",
            session_map=session_map,
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

        # Verify session map registration
        assert session_map.owns(result["uuid"], "session-1")

    async def test_update_owned_slide(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        # First create
        result1 = await render_slides(
            markdown="# V1",
            theme="default",
            session_id="session-1",
            session_map=session_map,
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        # Update with same UUID
        result2 = await render_slides(
            markdown="# V2",
            theme="seriph",
            uuid=result1["uuid"],
            session_id="session-1",
            session_map=session_map,
            builder=mock_builder,
            db_session_factory=db_session_factory,
        )

        assert result2["uuid"] == result1["uuid"]

        # Verify DB row updated
        async with db_session_factory() as session:
            slide = await session.get(Slide, result1["uuid"])
        assert slide.theme == "seriph"

    async def test_uuid_foreign_rejected(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        foreign_uuid = "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"
        session_map.register(foreign_uuid, "other-session")

        with pytest.raises(UuidForeign):
            await render_slides(
                markdown="# Test",
                theme="default",
                uuid=foreign_uuid,
                session_id="my-session",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_uuid_sealed_rejected(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        # Insert a slide in DB (simulating a previously created slide)
        sealed_uuid = "b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e"
        async with db_session_factory() as session:
            session.add(Slide(uuid=sealed_uuid, session_id="old-session", theme="default"))
            await session.commit()

        # UUID is not in session_map (sealed)
        with pytest.raises(UuidSealed):
            await render_slides(
                markdown="# Test",
                theme="default",
                uuid=sealed_uuid,
                session_id="new-session",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

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
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        with pytest.raises(InvalidUuid):
            await render_slides(
                markdown="# Test",
                theme="default",
                uuid=bad_uuid,
                session_id="my-session",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_concurrent_limit(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        # Exhaust the semaphore
        mock_builder._semaphore = asyncio.Semaphore(0)

        with pytest.raises(ConcurrentLimitReached):
            await render_slides(
                markdown="# Test",
                theme="default",
                session_id="session-1",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_build_error_propagated(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        mock_builder.build = AsyncMock(side_effect=BuildFailed("build error"))

        with pytest.raises(BuildFailed):
            await render_slides(
                markdown="# Test",
                theme="default",
                session_id="session-1",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )

    async def test_theme_validation_propagated(
        self,
        mock_builder: MagicMock,
        session_map: SessionMap,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        mock_builder.build = AsyncMock(side_effect=ThemeNotAllowed("bad-theme"))

        with pytest.raises(ThemeNotAllowed):
            await render_slides(
                markdown="# Test",
                theme="bad-theme",
                session_id="session-1",
                session_map=session_map,
                builder=mock_builder,
                db_session_factory=db_session_factory,
            )


class TestListSessionSlides:
    async def test_empty_session(
        self,
        settings: Settings,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        result = await list_session_slides(
            session_id="empty-session",
            db_session_factory=db_session_factory,
            settings=settings,
        )

        assert result["slides"] == []

    async def test_returns_session_slides(
        self,
        settings: Settings,
        db_session_factory: async_sessionmaker[AsyncSession],
    ) -> None:
        # Insert slides for different sessions
        async with db_session_factory() as session:
            session.add(Slide(uuid="uuid-1", session_id="my-session", theme="default"))
            session.add(Slide(uuid="uuid-2", session_id="my-session", theme="seriph"))
            session.add(Slide(uuid="uuid-3", session_id="other-session", theme="dracula"))
            await session.commit()

        result = await list_session_slides(
            session_id="my-session",
            db_session_factory=db_session_factory,
            settings=settings,
        )

        assert len(result["slides"]) == 2
        uuids = {s["uuid"] for s in result["slides"]}
        assert uuids == {"uuid-1", "uuid-2"}

        for slide in result["slides"]:
            assert "url" in slide
            assert "theme" in slide
            assert "test.example.com" in slide["url"]
