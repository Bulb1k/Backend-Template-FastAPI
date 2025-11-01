from app.db.session import sync_engine
from fastapi import FastAPI
from starlette_admin.contrib.sqla import Admin

from app.admin import views
from app.core.config import Settings
from .auth import AdminAuthProvider
from .views import UserView
from app.db.models import User

settings = Settings()


def setup_admin(app: FastAPI) -> None:
    admin = Admin(
        engine=sync_engine,
        templates_dir=f"{settings.TEMPLATES_DIR}/admin",
        statics_dir=f"{settings.STATIC_DIR}/admin",
        auth_provider=AdminAuthProvider(),
    )

    admin.add_view(UserView())

    admin.mount_to(app)


