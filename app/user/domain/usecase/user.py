from abc import ABC, abstractmethod

from app.user.application.dto import LoginResponseDTO
from app.user.domain.command import CreateUserCommand
from app.user.domain.entity.user import User


class UserUseCase(ABC):
    @abstractmethod
    async def get_user_list(
        self,
        *,
        limit: int = 10,
    ) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, *, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    async def create(self, *, command: CreateUserCommand):
        raise NotImplementedError

    @abstractmethod
    async def is_admin(self, *, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def login(self, *, email: str, password: str) -> LoginResponseDTO:
        raise NotImplementedError

