from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from models.default.base import DefaultModel


class Credential(BaseModel):
    password: str
    isFirstLogin: bool = True


class User(DefaultModel):
    name: str
    email: str
    credential: Credential


class OutputUser(User):
    id: PydanticObjectId = Field(alias="_id")
