import datetime as dt

from app.db.base import Base
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(nullable=False, unique=True)
    chat_id: Mapped[int] = mapped_column(nullable=False, unique=True)
    credits: Mapped[int] = mapped_column(default=0)

    created_at: Mapped[dt.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        default=dt.datetime.utcnow,
        nullable=False,
    )

    type: Mapped[str] = mapped_column(default="user", nullable=False)
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "user",
    }

