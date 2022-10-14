from fastapi import APIRouter, Path
from pydantic.types import UUID4
from starlette.responses import Response

from app.db.models import SystemItem

router = APIRouter(prefix="/delete")


@router.delete("/{id}")
async def delete_node(id: UUID4 = Path(..., description="Element UUID")):
    node = await SystemItem.get_or_404(id)

    await node.delete()

    # TODO: Лучше обернуть бы в BackgroudTask
    await SystemItem.update_folder_meta(node)

    return Response()
