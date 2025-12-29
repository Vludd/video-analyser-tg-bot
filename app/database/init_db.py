import asyncio
from pathlib import Path

from sqlalchemy import func, select
from app.database import models_to_orm
from app.database.base import AsyncSessionLocal, init_db
from app.models import MVideo, MVideoSnapshot
from app.schemas.video import SVideo
from app.utils.data_parser import parse_json

async def main():
    await init_db()
    path = Path(__file__).parent.parent / "data" / "videos.json"
    raw_data = parse_json(path)
    videos_data = [SVideo(**v) for v in raw_data["videos"]]

    videos_orm, snapshots_orm = models_to_orm(videos_data)

    async with AsyncSessionLocal() as session:
        videos_count = await session.scalar(select(func.count()).select_from(MVideo)) or 0
        snapshots_count = await session.scalar(select(func.count()).select_from(MVideoSnapshot)) or 0

        if videos_count > 0 or snapshots_count > 0:
            print("Tables are already filled in")
            return

        session.add_all(videos_orm)
        session.add_all(snapshots_orm)
        await session.commit()
        print("Data uploaded successfully")

if __name__ == "__main__":
    asyncio.run(main())
