from app.db.models.user import User
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column


class Admin(User):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "admin",
    }
