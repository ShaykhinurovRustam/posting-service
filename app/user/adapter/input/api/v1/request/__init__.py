from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")


class CreateUserRequest(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    nickname: str = Field(..., description="Nickname")