from typing import Optional

from app.db.repository.admin import AdminRepository
from app.db.session import async_session_maker
from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AuthProvider, AdminUser
from starlette_admin.exceptions import FormValidationError, LoginFailed


class AdminAuthProvider(AuthProvider):
    def __init__(self, *, session_factory=async_session_maker, **kwargs):
        super().__init__(**kwargs)
        self._repo = AdminRepository(session_factory)

    async def is_authenticated(self, request: Request) -> bool:
        admin_id: int | None = request.session.get("admin_id")
        if admin_id is None:
            return False

        admin = await self._repo.get(admin_id)
        if admin is None or not admin.is_active:
            request.session.clear()
            return False

        request.state.admin = admin
        return True

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username or "") < 3:
            raise FormValidationError({"username": "Ім’я мінімум 3 символи"})

        admin = await self._repo.authenticate(username, password)
        if admin is None or not admin.is_active:
            raise LoginFailed("Неправильний логін або пароль")

        request.session.update({"admin_id": admin.id})

        if remember_me:
            response.set_cookie(
                "session",
                request.cookies.get("session"),
                max_age=60 * 60 * 24 * 30,
                httponly=True,
            )
        return response


    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response

    def get_admin_user(self, request: Request) -> Optional[AdminUser]:
        admin = getattr(request.state, "admin", None)
        if admin is None:
            return None
        return AdminUser(username=admin.user_name, photo_url=None)
