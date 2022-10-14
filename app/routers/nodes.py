from fastapi import APIRouter, Path
from pydantic.types import UUID4

from app.db.models import SystemItem
from app.db.validation_models import SystemItemExportRequest
from app.utils.children_list import get_all_children_list

router = APIRouter(prefix="/nodes")


@router.get("/{id}", response_model=SystemItemExportRequest)
async def view_node(id: UUID4 = Path(..., description="Element UUID")):
    node = await SystemItem.get_or_404(id)

    node_dict = await get_all_children_list(node)

    return node_dict
