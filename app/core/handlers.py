from datetime import timedelta
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
        date_to_inclusive = f.date_to + timedelta(days=1)
        q = q.where(MVideo.video_created_at < date_to_inclusive)

    result = await session.scalar(q)
    return result or 0

async def count_videos(session, f) -> int:
    q = select(func.count()).select_from(MVideo)

    if f.creator_id:
        q = q.where(MVideo.creator_id == f.creator_id)

    if f.date_from:
        q = q.where(MVideo.video_created_at >= f.date_from)

    if f.date_to:
        date_to_inclusive = f.date_to + timedelta(days=1)
        q = q.where(MVideo.video_created_at < date_to_inclusive)

    result = await session.scalar(q)
    return result or 0


async def count_videos_with_views_gt(session, f) -> int:
    if f.min_views is None:
        return 0

    conditions = [MVideo.views_count > f.min_views]

    if getattr(f, "creator_id", None):
        conditions.append(MVideo.creator_id == f.creator_id)

    if getattr(f, "date_from", None):
        conditions.append(MVideo.video_created_at >= f.date_from)

    if getattr(f, "date_to", None):
        date_to_inclusive = f.date_to + timedelta(days=1)
        conditions.append(MVideo.video_created_at < date_to_inclusive)

    q = select(func.count()).select_from(MVideo).where(*conditions)
    result = await session.scalar(q)
    return result or 0


async def sum_delta_views(session, f) -> int:
    start, end = normalize_date_range(
        f.date_from, f.date_to, getattr(f, "time_from", None), getattr(f, "time_to", None)
    )

    q = select(func.coalesce(func.sum(MVideoSnapshot.delta_views_count), 0))

    if start:
        q = q.where(MVideoSnapshot.created_at >= start)
    if end:
        q = q.where(MVideoSnapshot.created_at <= end)

    if getattr(f, "creator_id", None):
        from app.models import MVideo
        q = q.join(MVideo, MVideo.id == MVideoSnapshot.video_id)
        q = q.where(MVideo.creator_id == f.creator_id)

    result = await session.scalar(q)
    return result or 0


async def count_negative_delta_views(session, f) -> int:
    conditions = [MVideoSnapshot.delta_views_count < 0]

    if getattr(f, "date_from", None):
        conditions.append(MVideoSnapshot.created_at >= f.date_from)

    if getattr(f, "date_to", None):
        date_to_inclusive = f.date_to + timedelta(days=1)
        conditions.append(MVideoSnapshot.created_at < date_to_inclusive)

    q = select(func.count()).select_from(MVideoSnapshot).where(*conditions)
    result = await session.scalar(q)
    return result or 0

async def count_creators_with_views_gt(session, f) -> int:
    if getattr(f, "min_views", None) is None:
        return 0

    q = select(func.count(func.distinct(MVideo.creator_id))).where(
        MVideo.views_count > f.min_views
    )

    if getattr(f, "creator_id", None):
        q = q.where(MVideo.creator_id == f.creator_id)

    if getattr(f, "date_from", None):
        q = q.where(MVideo.video_created_at >= f.date_from)
    if getattr(f, "date_to", None):
        q = q.where(MVideo.video_created_at <= f.date_to)

    result = await session.scalar(q)
    return result or 0
