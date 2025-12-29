from app.models import MVideo, MVideoSnapshot
from app.schemas.video import SVideo


def models_to_orm(raw_data: list[SVideo]) -> tuple[list[MVideo], list[MVideoSnapshot]]:
    videos_orm = []
    snapshots_orm = []

    for v in raw_data:
        video = MVideo(
            id=v.id,
            creator_id=v.creator_id,
            video_created_at=v.video_created_at,
            views_count=v.views_count,
            likes_count=v.likes_count,
            comments_count=v.comments_count,
            reports_count=v.reports_count,
            created_at=v.created_at,
            updated_at=v.updated_at
        )
        videos_orm.append(video)

        for s in v.snapshots:
            snapshot = MVideoSnapshot(
                id=s.id,
                video_id=v.id,
                views_count=s.views_count,
                likes_count=s.likes_count,
                comments_count=s.comments_count,
                reports_count=s.reports_count,
                delta_views_count=s.delta_views_count,
                delta_likes_count=s.delta_likes_count,
                delta_comments_count=s.delta_comments_count,
                delta_reports_count=s.delta_reports_count,
                created_at=s.created_at,
                updated_at=s.updated_at
            )
            snapshots_orm.append(snapshot)
            
    return videos_orm, snapshots_orm

