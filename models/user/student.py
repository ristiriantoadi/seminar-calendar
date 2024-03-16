from pydantic import BaseModel

from models.user.user import OutputUser, User


class Student(User):
    nim: str
    year: int


class InputStudent(BaseModel):
    name: str
    nim: str
    email: str
    year: int


class OutputStudent(OutputUser, Student):
    pass
