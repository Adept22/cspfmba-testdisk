import datetime
from fastapi import APIRouter, Query

from app.db.validation_models import SystemItemBase
from app.utils.updates_list import get_updates_list

router = APIRouter(prefix="/updates")


@router.get("", response_model=list[SystemItemBase])
async def view_updates(
    date: datetime.datetime = Query(..., description="Request date")
):
    return await get_updates_list(date)
