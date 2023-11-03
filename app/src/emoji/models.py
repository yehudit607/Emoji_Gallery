import enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class EmojiType(str, enum.Enum):
    Free = "free"
    Premium = "premium"
    Business = "business"


class EmojiBase(BaseModel):
    name: str
    order: int

    class Config:
        orm_mode = True


class UserEmojiBase(EmojiBase):
    user_id: int


class GeneralEmojiBase(EmojiBase):
    is_active: bool = True
    emoji_type: EmojiType




