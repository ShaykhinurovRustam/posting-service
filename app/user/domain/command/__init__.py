from pydantic import BaseModel


class CreateUserCommand(BaseModel):
    email: str
    password: str
    nickname: str