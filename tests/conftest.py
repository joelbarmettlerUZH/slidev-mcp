import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from slidev_mcp.models import Base, Slide, SlideVersion
from slidev_mcp.sessions import SessionMap


@pytest.fixture
def session_map() -> SessionMap:
    return SessionMap()


@pytest.fixture
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite://", echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session_factory(db_engine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(db_engine, expire_on_commit=False)


@pytest.fixture
async def db_session(db_session_factory) -> AsyncSession:
    async with db_session_factory() as session:
        yield session


def make_slide(
    uuid: str = "test-uuid",
    session_id: str = "test-session",
    theme: str = "default",
) -> Slide:
    return Slide(uuid=uuid, session_id=session_id, theme=theme)


def make_slide_version(
    slide_uuid: str = "test-uuid",
    version: int = 1,
    markdown: str = "# Test",
    theme: str = "default",
) -> SlideVersion:
    return SlideVersion(slide_uuid=slide_uuid, version=version, markdown=markdown, theme=theme)
