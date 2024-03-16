from datetime import datetime
from enum import Enum, IntEnum
from typing import Any, List

from beanie import PydanticObjectId
from pydantic import BaseModel


class DefaultModel(BaseModel):
    createTime: datetime = datetime.utcnow()
    creatorId: PydanticObjectId = None

    updateTime: datetime = None
    updaterId: PydanticObjectId = None

    deleteTime: datetime = None
    deleterId: PydanticObjectId = None
    isDelete: bool = False


class DefaultPage(BaseModel):
    # status: int = 200
    size: int = 0
    page: int = 0
    totalElements: int = 0
    totalPages: int = 0
    sortBy: str
    sortDir: int
    content: List[Any] = []


class PaginationDir(IntEnum, Enum):
    ASC = 1
    DESC = -1


class OutputListPagination(BaseModel):
    content: List[Any] = []
    totalElements: int
    totalPages: int
