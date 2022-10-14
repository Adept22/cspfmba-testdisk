import datetime
from enum import Enum

from pydantic import BaseModel, validator
from pydantic.types import UUID, PositiveInt


class SystemItemType(str, Enum):
    FOLDER = 'FOLDER'
    FILE = 'FILE'


class SystemItemBase(BaseModel):
    """Базовая модель создания элемента"""
    id: UUID
    url: str | None
    parentId: UUID | None
    type: SystemItemType
    size: PositiveInt | None


class SystemItemImport(SystemItemBase):
    """Представляет элемент импорта"""

    @validator('parentId')
    def validate_parent_id(cls, v, values):
        """Проверяет наследование"""

        if values.get('id') == v:
            raise ValueError("parentId can't equal self id")

        return v

    @validator('url')
    def validate_type_url(cls, v, values):
        """Проверяет ссылку"""

        t = values.get('type')

        if t is SystemItemType.FOLDER and v is not None:
            raise ValueError('Link of folder should be null')

        if t is SystemItemType.FILE and v is None:
            raise ValueError("Link of file shouldn't be null")

        return v

    @validator('size')
    def validate_type_size(cls, v, values):
        """Проверяет размер"""

        t = values.get('type')

        if t is SystemItemType.FOLDER and v is not None:
            raise ValueError('Size of folder should be null')

        if t is SystemItemType.FILE:
            if v is None:
                raise ValueError("Size of file shouldn't be null")

            if v <= 0:
                raise ValueError("Size of file should be above zero")

        return v


class SystemItemImportRequest(BaseModel):
    """Представляет импорт"""

    items: list[SystemItemImport]
    updateDate: datetime.datetime

    @validator('items')
    def validate_unique_id(cls, items):
        """Проверяет на уникальность идентификаторов"""

        id_set = set(item.id for item in items)

        if len(id_set) != len(items):
            raise ValueError("ID in list not unique")

        return items


class SystemItemExport(SystemItemBase):
    """Базовая модель отображения элемента"""
    date: datetime.datetime | None

    class Config:
        json_encoders = {
            datetime.datetime: lambda data: data.isoformat().replace('+00:00', 'Z'),
        }


class SystemItemExportRequest(SystemItemExport):
    """Представляет элемент со всеми потомками"""

    children: list['SystemItemExportRequest'] | None
