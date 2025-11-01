from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    user_name: str
    chat_id: int


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    credits: Optional[int] = None
    type: Optional[str] = None


class User(BaseModel):
    id: int
    type: str
    chat_id: int
    credits: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
