from fastapi import APIRouter, Depends, Body
from fastapi.responses import Response

from app.db.models import SystemItem
from app.db.validation_models import SystemItemImportRequest
from app.exceptions import ValidationException
from app.utils.validators import parent_is_folder

router = APIRouter(prefix="/imports")


async def parent_check(imports: SystemItemImportRequest = Body()):
    if not await parent_is_folder(imports.items):
        raise ValidationException(message="ParentId is not FOLDER")

    return imports


@router.post("")
async def post_imports(imports: SystemItemImportRequest = Depends(parent_check)):
    for item in imports.items:
        new_item = await SystemItem.get(item.id)

        if new_item:
            await new_item.update(date=imports.updateDate, **item.dict()).apply()
        else:
            new_item = await SystemItem.create(date=imports.updateDate, **item.dict())

        # TODO: По хорошему обернуть бы в BackgroudTask
        await SystemItem.update_folder_meta(new_item)

    return Response()
