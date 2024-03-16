from pydantic import BaseModel

from models.user.user import OutputUser


class Admin(OutputUser):
    nip: str


class OutputAdmin(OutputUser):
    pass


class InputAdmin(BaseModel):
    name: str
    nip: str
    email: str
