from sqlalchemy import func, select
from app.models import MVideo, MVideoSnapshot
from app.utils import normalize_date_range


async def sum_views(session, f) -> int:
    q = select(func.coalesce(func.sum(MVideo.views_count), 0))

    if f.creator_id:
        q = q.where(MVideo.creator_id == f.creator_id)
    
    if f.date_from:
        q = q.where(MVideo.video_created_at >= f.date_from)
    
    if f.date_to:
        q = q.where(MVideo.video_created_at <= f.date_to)

    result = await session.scalar(q)
    return result or 0

async def count_videos(session, f) -> int:
    q = select(func.count()).select_from(MVideo)

    if f.creator_id:
        q = q.where(MVideo.creator_id == f.creator_id)

    if f.date_from:
        q = q.where(MVideo.video_created_at >= f.date_from)

    if f.date_to:
        q = q.where(MVideo.video_created_at <= f.date_to)

    result = await session.scalar(q)
    return result or 0


async def count_videos_with_views_gt(session, f) -> int:
    if f.min_views is None:
        return 0

    q = select(func.count()).select_from(MVideo).where(MVideo.views_count > f.min_views)
    result = await session.scalar(q)
    return result or 0


async def sum_delta_views(session, f) -> int:
    start, end = normalize_date_range(f.date_from, f.date_to)

    q = select(func.coalesce(func.sum(MVideoSnapshot.delta_views_count), 0))

    if start:
        q = q.where(MVideoSnapshot.created_at >= start)
    if end:
        q = q.where(MVideoSnapshot.created_at <= end)

    result = await session.scalar(q)
    return result or 0


async def count_distinct_videos_with_delta(session, f) -> int:
    q = select(func.count(func.distinct(MVideoSnapshot.video_id))).where(
        MVideoSnapshot.delta_views_count > 0
    )

    if f.date_from:
        q = q.where(MVideoSnapshot.created_at >= f.date_from)
    if f.date_to:
        q = q.where(MVideoSnapshot.created_at <= f.date_to)

    result = await session.scalar(q)
    return result or 0
