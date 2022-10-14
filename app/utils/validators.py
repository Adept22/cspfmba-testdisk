from app.db.models import SystemItem
from app.db.validation_models import SystemItemImport, SystemItemType


def __parent_is_folder_in_query(
    nodes: list[SystemItemImport], pending: SystemItemImport
) -> None | bool:
    for node in nodes:
        if node.id == pending.parentId:
            return node.type is SystemItemType.FOLDER


async def parent_is_folder(nodes: list[SystemItemImport]) -> bool:
    for node in nodes:
        if node.parentId is None:
            continue

        in_query = __parent_is_folder_in_query(nodes, node)

        if in_query == False:
            return False
        elif in_query:
            continue

        parent_node = await SystemItem.get_or_404(node.parentId)

        if parent_node.type != SystemItemType.FOLDER:
            return False

    return True
