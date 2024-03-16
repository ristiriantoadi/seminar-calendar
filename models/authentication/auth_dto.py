from pydantic import BaseModel


class InputRegistration(BaseModel):
    username: str
    password: str
    name: str


class OutputCheckToken(BaseModel):
    name: str
    isFirstLogin: bool


class OutputLogin(BaseModel):
    access_token: str
    token_type: str = "bearer"
