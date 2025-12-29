from app.schemas import BaseConfig
from typing import Literal, Optional
from uuid import UUID
from datetime import date, time

from pydantic import Field

class QueryFilters(BaseConfig):
    creator_id: Optional[UUID] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    time_from: Optional[time] = None
    time_to: Optional[time] = None
    min_views: Optional[int] = Field(None, ge=0)

class AnalyticsQuery(BaseConfig):
    query_type: Literal[
        "count_videos",
        "sum_views",
        "count_videos_with_views_gt",
        "sum_delta_views",
        "count_negative_delta_views",
        "count_creators_with_views_gt",
    ]
    filters: QueryFilters
