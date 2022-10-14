from sqlalchemy import Column, String, BigInteger, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db import db


class SystemItem(db.Model):
    __tablename__ = 'system_item'

    id = Column(UUID, primary_key=True)
    url = Column(String(255), nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    parentId = Column('parent_id', UUID, ForeignKey('system_item.id', ondelete='CASCADE'), index=True)
    type = Column(String(6), nullable=False)
    size = Column(BigInteger, nullable=True)

    @staticmethod
    async def update_folder_meta(node: 'SystemItem') -> None:
        if not node.parentId:
            return

        parent = await SystemItem.get(node.parentId)

        await SystemItem.__set_date(parent)
        await SystemItem.__set_size(parent)

        await SystemItem.update_folder_meta(parent)

    # ---------------
    # Private section
    # ---------------

    @staticmethod
    async def __set_date(node: 'SystemItem') -> None:
        result = await db.select((db.func.max(SystemItem.date),)).where(SystemItem.parentId == node.id).gino.first()

        await node.update(date=(result[0])).apply()

    @staticmethod
    async def __set_size(node: 'SystemItem') -> None:
        result = await db.select((db.func.sum(SystemItem.size),)).where(SystemItem.parentId == node.id).gino.first()

        await node.update(size=(result[0])).apply()
