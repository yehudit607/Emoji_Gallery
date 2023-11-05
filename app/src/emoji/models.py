from enum import Enum

from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional

from app.core.models.base import ModelCore


class Tier(str, Enum):
    Free = "Free"
    Premium = "Premium"
    Business = "Business"


class User(ModelCore, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    user_tier: Tier = Field(sa_column_kwargs={"index": True})  # Role of the user
    emoji_count: int = Field(default=0)  # Number of emojis added by the user
    user_emojis: List["UserEmoji"] = Relationship(back_populates="user")

    class Config:
        orm_mode = True


class UserEmoji(ModelCore, table=True):
    __tablename__ = 'user_emojis'

    id: Optional[int] = Field(default=None, primary_key=True)
    emoji_id: int = Field(foreign_key="general_emojis.id")
    user_id: int = Field(foreign_key="users.id")
    user: User = Relationship(back_populates="user_emojis")

    class Config:
        orm_mode = True


class GeneralEmoji(ModelCore, table=True):
    __tablename__ = 'general_emojis'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    order: int = Field(default=0)
    emoji_type: Tier = Field(sa_column_kwargs={"index": True})
    is_active: bool = Field(default=True)
    user_emojis: List["UserEmoji"] = Relationship(back_populates="emoji")

    class Config:
        orm_mode = True
