from typing import Union

from app.user.domain.entity.user import User, UserRead
from app.user.domain.repository.user import UserRepo


class UserRepositoryAdapter:
    def __init__(self, *, user_repo: UserRepo):
        self.user_repo = user_repo

    async def get_users(
        self,
        *,
        limit: int = 10,
    ) -> list[UserRead]:
        users = await self.user_repo.get_users(limit=limit)
        return [UserRead.model_validate(user) for user in users]

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> Union[User, None]:
        return await self.user_repo.get_user_by_email_or_nickname(
            email=email,
            nickname=nickname,
        )

    async def get_user_by_id(self, *, user_id: int) -> Union[User, None]:
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        return user

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> Union[User, None]:
        return await self.user_repo.get_user_by_email_and_password(
            email=email,
            password=password,
        )

    async def save(self, *, user: User):
        await self.user_repo.save(user=user)
