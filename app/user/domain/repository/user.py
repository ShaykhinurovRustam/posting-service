from abc import ABC, abstractmethod
from typing import Union

from app.user.domain.entity.user import User


class UserRepo(ABC):
    @abstractmethod
    async def get_users(
        self,
        *,
        limit: int = 10,
    ) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str
    ) -> Union[User, None]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, *, user_id: int) -> Union[User, None]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str
    ) -> Union[User, None]:
        raise NotImplementedError

    @abstractmethod
    async def save(self, *, user: User):
        raise NotImplementedError
