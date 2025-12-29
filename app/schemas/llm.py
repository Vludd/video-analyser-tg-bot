from app.schemas import BaseConfig
from typing import Literal, Optional
from uuid import UUID
from datetime import date

from pydantic import Field

class QueryFilters(BaseConfig):
    creator_id: Optional[UUID] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    min_views: Optional[int] = Field(None, ge=0)

class AnalyticsQuery(BaseConfig):
    query_type: Literal[
        "count_videos",
        "sum_views",
        "count_videos_with_views_gt",
        "sum_delta_views",
        "count_distinct_videos_with_delta",
    ]
    filters: QueryFilters
