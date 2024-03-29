from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel

from models.default.base import DefaultPage
from models.user.user import OutputUser, User


class InputTeacher(BaseModel):
    name: str
    nip: str
    email: str


class Teacher(User):
    nip: str


class OutputTeacher(OutputUser, Teacher):
    pass


class DataGetTeachers(BaseModel):
    id: PydanticObjectId
    name: str
    nip: str
    email: str


class GetTeachers(DefaultPage):
    content: List[DataGetTeachers] = []
