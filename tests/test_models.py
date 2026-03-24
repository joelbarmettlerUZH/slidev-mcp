from sqlalchemy import select

from slidev_mcp.models import Slide
from tests.conftest import make_slide


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
        import pytest
        from sqlalchemy.exc import IntegrityError

        slide1 = make_slide(uuid="dup-uuid", session_id="sess-1", theme="default")
        slide2 = make_slide(uuid="dup-uuid", session_id="sess-2", theme="seriph")
        db_session.add(slide1)
        await db_session.commit()

        db_session.add(slide2)
        with pytest.raises(IntegrityError):
            await db_session.commit()
