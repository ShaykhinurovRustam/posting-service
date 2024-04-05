from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request

from app.container import Container
from app.user.adapter.input.api.v1.request import CreateUserRequest, LoginRequest
from app.user.adapter.input.api.v1.response import LoginResponse
from app.user.application.dto import GetUserResponseDTO, CreateUserResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.usecase.user import UserUseCase
from core.fastapi.dependencies import PermissionDependency, IsAdmin, IsAuthenticated

user_router = APIRouter()


@user_router.get(
    "/me",
    response_model=GetUserResponseDTO,
    dependencies=[Depends(PermissionDependency([IsAuthenticated]))]
)
@inject
async def get_user(
    request: Request,
    usecase: UserUseCase = Depends(Provide[Container.user_service])
):
    return await usecase.get_user_by_id(user_id=request.user.id)


@user_router.get(
    "",
    response_model=list[GetUserResponseDTO],
    dependencies=[Depends(PermissionDependency([IsAdmin]))]
)
@inject
async def get_user_list(
    limit: int,
    usecase: UserUseCase = Depends(Provide[Container.user_service])
):
    return await usecase.get_user_list(limit=limit)


@user_router.post(
    "",
    response_model=CreateUserResponseDTO
)
@inject
async def create_user(
    request: CreateUserRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service])
):
    command = CreateUserCommand(**request.model_dump())
    await usecase.create(command=command)
    return {
        "email": request.email,
        "nickname": request.nickname
    }


@user_router.post(
    "/login",
    response_model=LoginResponse
)
@inject
async def login(
    request: LoginRequest,
    usecase: UserUseCase = Depends(Provide[Container.user_service])
):
    token = await usecase.login(email=request.email, password=request.password)
    return {"token": token.token, "refresh_token": token.refresh_token}
