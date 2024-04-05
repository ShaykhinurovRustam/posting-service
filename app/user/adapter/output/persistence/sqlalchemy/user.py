from typing import Union

from sqlalchemy import and_, or_, select

from app.user.domain.entity.user import User
from app.user.domain.repository.user import UserRepo
from core.db.session import session, session_factory


class UserSQLAlchemyRepo(UserRepo):
    async def get_users(
        self,
        *,
        limit: int = 10,
    ) -> list[User]:
        query = select(User).limit(limit)

        async with session_factory() as read_session:
            result = await read_session.execute(query)

        return result.scalars().all()

    async def get_user_by_email_or_nickname(
        self,
        *,
        email: str,
        nickname: str,
    ) -> Union[User, None]:
        async with session_factory() as read_session:
            query = (
                select(User)
                .filter(
                    or_(
                        User.email == email,
                        User.nickname == nickname
                    )
                )
            )
            result = await read_session.execute(query)

            return result.scalar()

    async def get_user_by_id(self, *, user_id: int) -> Union[User, None]:
        async with session_factory() as read_session:
            query = (
                select(User)
                .filter_by(
                    id=user_id
                )
            )
            result = await read_session.execute(query)

            return result.scalar()

    async def get_user_by_email_and_password(
        self,
        *,
        email: str,
        password: str,
    ) -> Union[User, None]:
        async with session_factory() as read_session:
            query = (
                select(User)
                .filter(
                    and_(
                        User.email == email,
                        User.password == password
                    )
                )
            )
            result = await read_session.execute(query)

            return result.scalar()

    async def save(self, *, user: User) -> None:
        session.add(user)
