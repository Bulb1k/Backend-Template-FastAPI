from app.db.models import User
from starlette_admin.contrib.sqla import ModelView

from .config import setup_admin_defaults, ADMIN_ICON

setup_admin_defaults()

class UserView(ModelView):
    def __init__(self):
        super().__init__(
            model=User,
            icon=ADMIN_ICON["user"]
        )

