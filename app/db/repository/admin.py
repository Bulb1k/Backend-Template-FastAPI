from __future__ import annotations

from passlib.hash import bcrypt
from sqlalchemy import func, select, update

from app.db.models.admin import Admin
from app.db.repository.base import BaseRepository
from app.schemas.admins import AdminCreate, AdminUpdate


class AdminRepository(BaseRepository[Admin]):

    def __init__(self, session_factory):
        super().__init__(session_factory, Admin)

    async def has_any(self) -> bool:
        async def _impl(session):
            res = await session.execute(
                select(func.count()).select_from(Admin)
            )
            return res.scalar_one() > 0
        return await self._run(_impl)

    async def get_by_username(self, user_name: str) -> Admin | None:
        async def _impl(session):
            res = await session.execute(
                select(Admin).where(Admin.user_name == user_name)
            )
            return res.scalar_one_or_none()
        return await self._run(_impl)


    async def create(self, data: AdminCreate) -> Admin:
        async def _impl(session):
            admin = Admin(
                chat_id=data.chat_id,
                user_name=data.user_name,
                hashed_password=bcrypt.hash(data.password),
                is_active=True,
                type="admin",
            )
            session.add(admin)
            return admin
        return await self._run(_impl)

    async def update(self, id_: int, data: AdminUpdate) -> Admin | None:
        values = data.model_dump(exclude_unset=True)
        if "password" in values:
            values["hashed_password"] = bcrypt.hash(values.pop("password"))

        async def _impl(session):
            res = await session.execute(
                update(Admin)
                .where(Admin.id == id_)
                .values(**values)
                .returning(Admin)
            )
            return res.scalars().first()
        return await self._run(_impl)

    async def authenticate(self, user_name: str, password: str) -> Admin | None:
        admin = await self.get_by_username(user_name)
        if admin and bcrypt.verify(password, admin.hashed_password):
            return admin
        return None
