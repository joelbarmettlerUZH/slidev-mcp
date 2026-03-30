import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from slidev_mcp.models import Slide, SlideVersion
from tests.conftest import make_slide, make_slide_version


class TestSlideModel:
    def test_instantiation(self):
        slide = make_slide(uuid="abc-123", session_id="sess-1", theme="seriph")
        assert slide.uuid == "abc-123"
        assert slide.session_id == "sess-1"
        assert slide.theme == "seriph"

    async def test_persist_and_query(self, db_session):
        slide = make_slide(uuid="persist-test", session_id="sess-1", theme="default")
        db_session.add(slide)
        await db_session.commit()

        result = await db_session.execute(select(Slide).where(Slide.uuid == "persist-test"))
        loaded = result.scalar_one()
        assert loaded.uuid == "persist-test"
        assert loaded.session_id == "sess-1"
        assert loaded.theme == "default"

    async def test_primary_key_uniqueness(self, db_session):
        slide1 = make_slide(uuid="dup-uuid", session_id="sess-1", theme="default")
        slide2 = make_slide(uuid="dup-uuid", session_id="sess-2", theme="seriph")
        db_session.add(slide1)
        await db_session.commit()

        db_session.add(slide2)
        with pytest.raises(IntegrityError):
            await db_session.commit()


class TestSlideVersionModel:
    def test_instantiation(self):
        v = make_slide_version(slide_uuid="abc-123", version=1, markdown="# Hello", theme="seriph")
        assert v.slide_uuid == "abc-123"
        assert v.version == 1
        assert v.markdown == "# Hello"
        assert v.theme == "seriph"

    async def test_persist_and_query(self, db_session):
        slide = make_slide(uuid="ver-test", session_id="sess-1", theme="default")
        db_session.add(slide)
        await db_session.flush()

        v = make_slide_version(slide_uuid="ver-test", version=1, markdown="# V1", theme="default")
        db_session.add(v)
        await db_session.commit()

        result = await db_session.execute(
            select(SlideVersion).where(SlideVersion.slide_uuid == "ver-test")
        )
        loaded = result.scalar_one()
        assert loaded.version == 1
        assert loaded.markdown == "# V1"

    async def test_version_uniqueness(self, db_session):
        slide = make_slide(uuid="uniq-test", session_id="sess-1", theme="default")
        db_session.add(slide)
        await db_session.flush()

        db_session.add(make_slide_version(slide_uuid="uniq-test", version=1, markdown="# V1"))
        await db_session.commit()

        db_session.add(make_slide_version(slide_uuid="uniq-test", version=1, markdown="# Dup"))
        with pytest.raises(IntegrityError):
            await db_session.commit()

    async def test_multiple_versions(self, db_session):
        slide = make_slide(uuid="multi-ver", session_id="sess-1", theme="default")
        db_session.add(slide)
        await db_session.flush()

        db_session.add(make_slide_version(slide_uuid="multi-ver", version=1, markdown="# V1"))
        db_session.add(
            make_slide_version(slide_uuid="multi-ver", version=2, markdown="# V2", theme="seriph")
        )
        await db_session.commit()

        result = await db_session.execute(
            select(SlideVersion)
            .where(SlideVersion.slide_uuid == "multi-ver")
            .order_by(SlideVersion.version)
        )
        versions = result.scalars().all()
        assert len(versions) == 2
        assert versions[0].markdown == "# V1"
        assert versions[1].markdown == "# V2"
        assert versions[1].theme == "seriph"
