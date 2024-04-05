from abc import ABC, abstractmethod

from app.auth.application.dto import RefreshTokenResponseDTO


class JwtUseCase(ABC):
    @abstractmethod
    async def verify_token(self, token: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create_refresh_token(
        self,
        token: str,
        refresh_token: str,
    ) -> RefreshTokenResponseDTO:
        raise NotImplementedError
