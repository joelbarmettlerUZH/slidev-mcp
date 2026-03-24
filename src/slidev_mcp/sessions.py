class SessionMap:
    """In-memory mapping of slide UUIDs to their owning session IDs."""

    def __init__(self) -> None:
        self._active: dict[str, str] = {}

    def register(self, uuid: str, session_id: str) -> None:
        """Register a UUID as owned by a session."""
        self._active[uuid] = session_id

    def owns(self, uuid: str, session_id: str) -> bool:
        """Check if a session owns a UUID."""
        return self._active.get(uuid) == session_id

    def is_active(self, uuid: str) -> bool:
        """Check if a UUID is currently active (owned by any session)."""
        return uuid in self._active

    def remove_session(self, session_id: str) -> list[str]:
        """Remove all UUIDs owned by a session. Returns the removed UUIDs."""
        removed = [uuid for uuid, sid in self._active.items() if sid == session_id]
        for uuid in removed:
            del self._active[uuid]
        return removed
