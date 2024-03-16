from typing import List

from beanie import PydanticObjectId
from pydantic import BaseModel, Field, validator

from models.default.base import DefaultPage
from models.user.user import OutputUser, User


class Student(User):
    nim: str
    year: int


class InputStudent(BaseModel):
    name: str
    nim: str
    email: str
    year: int

    @validator("nim")
    def nim_to_upper(cls, v):
        return v.upper()


class OutputStudent(OutputUser, Student):
    pass


class OutputStudentPage(DefaultPage):
    content: List[OutputStudent] = []


class DataGetStudents(BaseModel):
    id: PydanticObjectId = Field(alias="_id")
    name: str
    nim: str
    email: str
    year: int


class GetStudents(DefaultPage):
    content: List[DataGetStudents] = []
