from pydantic import BaseModel

from models.user.user import OutputUser, User


class Admin(User):
    nip: str


class OutputAdmin(OutputUser, Admin):
    pass


class InputAdmin(BaseModel):
    name: str
    nip: str
    email: str
