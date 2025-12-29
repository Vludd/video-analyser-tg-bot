from app.schemas import BaseConfig
from datetime import datetime
from uuid import UUID


class SVideoSnapshot(BaseConfig):
    id: UUID
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    delta_views_count: int
    delta_likes_count: int
    delta_comments_count: int
    delta_reports_count: int
    created_at: datetime
    updated_at: datetime
