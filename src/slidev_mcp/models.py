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
