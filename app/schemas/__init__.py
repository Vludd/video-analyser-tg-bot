from pydantic import BaseModel
from typing import List
from datetime import datetime
from uuid import UUID

class SVideoSnapshot(BaseModel):
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

class SVideo(BaseModel):
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
