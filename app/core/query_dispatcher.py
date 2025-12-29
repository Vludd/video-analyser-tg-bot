from app.schemas.llm import AnalyticsQuery

import logging

from app.core.handlers import (
    count_creators_with_views_gt,
    count_negative_delta_views, 
    count_videos, 
    count_videos_with_views_gt, 
    sum_delta_views,
    sum_views
)


async def execute_analytics_query(session, query: AnalyticsQuery) -> int:
    handlers = {
        "count_videos": count_videos,
        "sum_views": sum_views,
        "count_videos_with_views_gt": count_videos_with_views_gt,
        "sum_delta_views": sum_delta_views,
        "count_negative_delta_views": count_negative_delta_views,
        "count_creators_with_views_gt": count_creators_with_views_gt,
    }

    handler = handlers.get(query.query_type)
    if not handler:
        raise ValueError("Unknown query type")

    logging.info(f"Query type: {query.query_type}")
    
    return await handler(session, query.filters)
