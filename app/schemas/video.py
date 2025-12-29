from app.schemas import BaseConfig
from typing import List
from datetime import datetime
from uuid import UUID

from app.schemas.snapshot import SVideoSnapshot

class SVideo(BaseConfig):
    id: UUID
    creator_id: UUID
    video_created_at: datetime
    views_count: int
    likes_count: int
    comments_count: int
    reports_count: int
    created_at: datetime
    updated_at: datetime
    snapshots: List[SVideoSnapshot]
