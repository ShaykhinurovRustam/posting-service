from pydantic import BaseModel, Field


class GetUserResponseDTO(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class CreateUserRequestDTO(BaseModel):
    email: str = Field(..., description="Email")
    password: str = Field(..., description="Password")
    nickname: str = Field(..., description="Nickname")


class CreateUserResponseDTO(BaseModel):
    email: str = Field(..., description="Email")
    nickname: str = Field(..., description="Nickname")


class LoginResponseDTO(BaseModel):
    token: str = Field(..., description="Token")
    refresh_token: str = Field(..., description="Refresh token")

