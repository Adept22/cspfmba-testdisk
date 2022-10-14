from datetime import timedelta

from app.db.models import SystemItem


async def get_updates_list(date: SystemItem) -> list[dict]:
    items = (
        await SystemItem.query.where(SystemItem.date >= date - timedelta(hours=24))
        .where(SystemItem.date <= date)
        .gino.all()
    )

    return [item.to_dict() for item in items]
