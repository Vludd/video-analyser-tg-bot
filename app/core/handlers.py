from sqlalchemy import func
from app.models import MVideo, MVideoSnapshot
from app.utils import normalize_date_range


def sum_views(session, f) -> int:
    q = session.query(
        func.coalesce(func.sum(MVideo.views_count), 0)
    )
    
    if f.creator_id:
        q = q.filter(MVideo.creator_id == f.creator_id)
        
    if f.date_from:
        q = q.filter(MVideo.video_created_at >= f.date_from)
        
    if f.date_to:
        q = q.filter(MVideo.video_created_at <= f.date_to)

    return q.scalar() or 0

def count_videos(session, f) -> int:
    q = session.query(MVideo)

    if f.creator_id:
        q = q.filter(MVideo.creator_id == f.creator_id)

    if f.date_from:
        q = q.filter(MVideo.video_created_at >= f.date_from)

    if f.date_to:
        q = q.filter(MVideo.video_created_at <= f.date_to)

    return q.count()

def count_videos_with_views_gt(session, f) -> int:
    if f.min_views is None:
        return 0

    return session.query(MVideo).filter(
        MVideo.views_count > f.min_views
    ).count()

def sum_delta_views(session, f) -> int:
    start, end = normalize_date_range(f.date_from, f.date_to)

    q = session.query(
        func.coalesce(func.sum(MVideoSnapshot.delta_views_count), 0)
    )

    if start:
        q = q.filter(MVideoSnapshot.created_at >= start)

    if end:
        q = q.filter(MVideoSnapshot.created_at <= end)

    return q.scalar() or 0


def count_distinct_videos_with_delta(session, f) -> int:
    q = session.query(
        func.count(func.distinct(MVideoSnapshot.video_id))
    ).filter(MVideoSnapshot.delta_views_count > 0)

    if f.date_from:
        q = q.filter(MVideoSnapshot.created_at >= f.date_from)

    if f.date_to:
        q = q.filter(MVideoSnapshot.created_at <= f.date_to)

    return q.scalar()
