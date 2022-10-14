import datetime
from app.db.models import SystemItem


async def get_all_children_list(item: SystemItem) -> dict:
    item.date = item.date.astimezone().replace(tzinfo=datetime.timezone.utc)

    result = item.to_dict()

    items = await SystemItem.query.where(SystemItem.parentId == item.id).gino.all()

    if items:
        result["children"] = [await get_all_children_list(item) for item in items]

    return result
