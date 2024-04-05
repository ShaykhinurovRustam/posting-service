from app.user.adapter.output.persistence.repository_adapter import UserRepositoryAdapter
from app.user.application.dto import LoginResponseDTO
from app.user.application.exception import DuplicateEmailOrNicknameException, UserNotFoundException, \
    PasswordDoesNotMatchException
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import UserRead, User
from app.user.domain.usecase.user import UserUseCase
from core.db import Transactional
from core.helpers.password import PasswordHelper
from core.helpers.token import TokenHelper


class UserService(UserUseCase):
    def __init__(self, *, repository: UserRepositoryAdapter):
        self.repository = repository

    async def get_user_list(
        self,
        *,
        limit: int = 10,
    ) -> list[UserRead]:
        return await self.repository.get_users(limit=limit)

    async def get_user_by_id(self, *, user_id: int) -> UserRead:
        user = await self.repository.get_user_by_id(user_id=user_id)
        return UserRead.model_validate(user)

    @Transactional()
    async def create(self, *, command: CreateUserCommand):
        is_exists = await self.repository.get_user_by_email_or_nickname(
            email=command.email,
            nickname=command.nickname
        )
        if is_exists:
            raise DuplicateEmailOrNicknameException

        user = User.create(
            email=command.email,
            password=PasswordHelper.hash_password(command.password),
            nickname=command.nickname,
        )
        await self.repository.save(user=user)

    async def is_admin(self, *, user_id: int) -> bool:
        user = await self.repository.get_user_by_id(user_id=user_id)
        if not user:
            return False

        return user.is_admin

    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        user = await self.repository.get_user_by_email_or_nickname(
            email=email,
            nickname=None,
        )
        if not user:
            raise UserNotFoundException
        if not PasswordHelper.verify_password(password, user.password):
            raise PasswordDoesNotMatchException

        return LoginResponseDTO(
            token=TokenHelper.encode(payload={"user_id": user.id}),
            refresh_token=TokenHelper.encode(payload={"sub": "refresh"})
        )
