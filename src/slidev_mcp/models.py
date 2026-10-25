from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Slide(Base):
    __tablename__ = "slides"

    uuid: Mapped[str] = mapped_column(String, primary_key=True)
    session_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    versions: Mapped[list["SlideVersion"]] = relationship(
        "SlideVersion",
        back_populates="slide",
        order_by="SlideVersion.version",
        cascade="all, delete-orphan",
    )


class SlideVersion(Base):
    __tablename__ = "slide_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    slide_uuid: Mapped[str] = mapped_column(
        String, ForeignKey("slides.uuid", ondelete="CASCADE"), nullable=False, index=True
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    markdown: Mapped[str] = mapped_column(Text, nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    slide: Mapped["Slide"] = relationship("Slide", back_populates="versions")

    __table_args__ = (UniqueConstraint("slide_uuid", "version", name="uq_slide_version"),)


class UsageEvent(Base):
    """One tool call or resource read, for the usage dashboard.

    Holds no user content: no markdown, no slide UUIDs, no IP addresses.
    """

    __tablename__ = "usage_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False, index=True
    )
    event_type: Mapped[str] = mapped_column(String, nullable=False)  # tool_call, resource_read
    name: Mapped[str] = mapped_column(String, nullable=False)  # tool name or normalized URI
    theme: Mapped[str | None] = mapped_column(String, nullable=True)  # allowlisted themes only
    client: Mapped[str | None] = mapped_column(String, nullable=True)  # MCP client name
    latency_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_chars: Mapped[int | None] = mapped_column(Integer, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)  # error code, not message
