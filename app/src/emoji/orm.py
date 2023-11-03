# models.py
import uuid
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
import enum

from app.core.db.session import BaseORM


class EmojiType(enum.Enum):
    Free = "free"
    Premium = "premium"
    Business = "business"

class GeneralEmoji(BaseORM):  # Assuming BaseORM is your declarative base with timestamps
    __tablename__ = 'general_emojis'

    id = Column(String(250), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), nullable=True)
    emoji_type = Column(Enum(EmojiType))
    is_active = Column(Boolean, default=True)

class UserEmoji(BaseORM):
    __tablename__ = 'user_emojis'

    id = Column(String(250), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(250), nullable=True)
    emoji_type = Column(Enum(EmojiType))
    is_active = Column(Boolean, default=True)
    user_id = Column(String(250), nullable=False)

