from sqlalchemy import (
    Integer, BigInteger, DateTime, ForeignKey, UUID as PGUUID
)

from uuid import UUID as PyUUID

from sqlalchemy.orm import Mapped, declarative_base, relationship, mapped_column
from datetime import datetime, timezone

Base = declarative_base()


class MVideo(Base):
    __tablename__ = "videos"

    id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True), 
        primary_key=True
    )
    
    creator_id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True),
        nullable=False
    )
    
    video_created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False
    )

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    snapshots = relationship(
        "VideoSnapshot",
        back_populates="video",
        lazy="selectin"
    )

class MVideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[PyUUID] = mapped_column(
        PGUUID(as_uuid=True), 
        primary_key=True
    )
    
    video_id = mapped_column(
        PGUUID(as_uuid=True), 
        ForeignKey("videos.id"),
        nullable=False
    )

    views_count: Mapped[int] = mapped_column(BigInteger, default=0)
    likes_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comments_count: Mapped[int] = mapped_column(BigInteger, default=0)
    reports_count: Mapped[int] = mapped_column(BigInteger, default=0)

    delta_views_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_likes_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_comments_count: Mapped[int] = mapped_column(Integer, default=0)
    delta_reports_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    video = relationship("Video", back_populates="snapshots")
