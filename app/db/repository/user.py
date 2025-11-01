from app.db.models import User
from app.db.repository.base import BaseRepository
from app.schemas import UserCreate, UserUpdate
from sqlalchemy import select, update


class UserRepository(BaseRepository[User]):
    def __init__(self, session_factory):
        super().__init__(session_factory, User)

    async def get(self, id: int) -> User | None:
        async def _impl(session):
            res = await session.execute(
                select(User).where(User.id == id)
            )
            return res.scalars().first()

        return await self._run(_impl)


    async def create(self, data: UserCreate) -> User:
        async def _impl(session):
            user = User(**data.model_dump())
            session.add(user)
            return user

        return await self._run(_impl)


    async def update(self, id: int, data: UserUpdate) -> User | None:
        async def _impl(session):
            res = await session.execute(
                update(User)
                .where(User.id == id)
                .values(**data.model_dump(exclude_unset=True))
                .returning(User)
            )
            return res.scalars().first()

        return await self._run(_impl)
