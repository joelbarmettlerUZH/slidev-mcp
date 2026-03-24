from slidev_mcp.sessions import SessionMap


class TestSessionMap:
    def test_register_and_owns(self, session_map: SessionMap):
        session_map.register("uuid-1", "session-a")
        assert session_map.owns("uuid-1", "session-a")
        assert not session_map.owns("uuid-1", "session-b")

    def test_is_active(self, session_map: SessionMap):
        assert not session_map.is_active("uuid-1")
        session_map.register("uuid-1", "session-a")
        assert session_map.is_active("uuid-1")

    def test_remove_session(self, session_map: SessionMap):
        session_map.register("uuid-1", "session-a")
        session_map.register("uuid-2", "session-a")
        session_map.register("uuid-3", "session-b")

        removed = session_map.remove_session("session-a")
        assert sorted(removed) == ["uuid-1", "uuid-2"]
        assert not session_map.is_active("uuid-1")
        assert not session_map.is_active("uuid-2")
        assert session_map.is_active("uuid-3")

    def test_remove_session_empty(self, session_map: SessionMap):
        removed = session_map.remove_session("nonexistent")
        assert removed == []

    def test_owns_unknown_uuid(self, session_map: SessionMap):
        assert not session_map.owns("unknown", "session-a")
