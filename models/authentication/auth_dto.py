from pydantic import BaseModel


class InputRegistration(BaseModel):
    username: str
    password: str
    name: str


class OutputCheckToken(BaseModel):
    username: str
    name: str


class OutputLogin(BaseModel):
    access_token: str
    token_type: str = "bearer"
