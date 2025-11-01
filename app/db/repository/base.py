# app/db/repository/base.py
from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any, Generic, Sequence, Type, TypeVar, Callable, Awaitable

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):

    def __init__(
            self,
            session_factory: async_sessionmaker[AsyncSession],
            model: Type[ModelT],
    ) -> None:
        self._session_factory = session_factory
        self._model = model

    @asynccontextmanager
    async def _session_scope(self) -> AsyncSession:
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            else:
                await session.commit()

    async def _run(
            self, fn: Callable[[AsyncSession], Awaitable[Any]]
    ) -> Any:
        async with self._session_scope() as session:
            return await fn(session)

    async def get(self, id_: int) -> ModelT | None:
        async def _impl(session: AsyncSession):
            res = await session.execute(
                select(self._model).where(self._model.id == id_)
            )
            return res.scalar_one_or_none()

        return await self._run(_impl)

    async def list(
            self, *, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelT]:
        async def _impl(session: AsyncSession):
            res = await session.execute(
                select(self._model).offset(skip).limit(limit)
            )
            return res.scalars().all()

        return await self._run(_impl)

    async def delete(self, id_: int) -> int:
        async def _impl(session: AsyncSession):
            res = await session.execute(
                delete(self._model)
                .where(self._model.id == id_)
                .returning(self._model.id)
            )
            deleted_id = res.scalar_one_or_none()
            return deleted_id or 0

        return await self._run(_impl)

    async def update(self, id_: int, data: dict) -> ModelT | None:
        async def _impl(session: AsyncSession):
            res = await session.execute(
                select(self._model)
                .where(self._model.id == id_)
                .values(**data)
                .returning(self._model)
            )
            return res.scalar_one_or_none()

    async def count(self) -> int:
        from sqlalchemy import func

        async def _impl(session: AsyncSession):
            res = await session.execute(select(func.count(self._model.id)))
            return res.scalar_one()

        return await self._run(_impl)
