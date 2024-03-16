from pydantic import BaseModel

from models.user.user import OutputUser, User


class InputTeacher(BaseModel):
    name: str
    nip: str
    email: str


class Teacher(User):
    nip: str


class OutputTeacher(OutputUser, Teacher):
    pass
