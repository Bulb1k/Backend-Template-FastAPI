from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class AdminBase(BaseModel):
    chat_id: int
    user_name: str = Field(min_length=3, max_length=50)
    is_active: bool = True


class AdminCreate(AdminBase):
    password: str = Field(min_length=8)


class AdminUpdate(BaseModel):
    chat_id: Optional[int] = None
    user_name: Optional[str] = Field(default=None, min_length=3, max_length=50)
    password: Optional[str] = Field(default=None, min_length=8)
    is_active: Optional[bool] = None


class Admin(AdminBase):
    id: int
    created_at: datetime
    type: str

    model_config = ConfigDict(from_attributes=True)
