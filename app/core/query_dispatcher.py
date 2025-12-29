from app.schemas.llm import AnalyticsQuery

import logging

from app.core.handlers import (
    count_distinct_videos_with_delta, 
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
        "count_distinct_videos_with_delta": count_distinct_videos_with_delta,
    }

    handler = handlers.get(query.query_type)
    if not handler:
        raise ValueError("Unknown query type")

    logging.info(f"Query type: {query.query_type}")
    
    return await handler(session, query.filters)
