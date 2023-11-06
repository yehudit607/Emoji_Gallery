from typing import List, TypeVar, Generic
from pydantic.generics import GenericModel
from pydantic import BaseModel


# Base schemas for Emojis
class EmojiBase(BaseModel):
    id: int
    name: str
    character: str
    active: bool

    class Config:
        orm_mode = True


# Specific schema for UserEmoji - extend if there are extra fields
class UserEmojiResponse(EmojiBase):
    pass


# Specific schema for GeneralEmoji - extend if there are extra fields
class GeneralEmojiResponse(EmojiBase):
    pass


# Pagination schema
T = TypeVar('T')


class Pagination(GenericModel, Generic[T]):
    total: int
    items: List[T]
    items_per_page: int
    current_page: int


# Paginated response for emojis
class UserEmojiPaginatedResponse(Pagination[UserEmojiResponse]):
    pass


class GeneralEmojiPaginatedResponse(Pagination[GeneralEmojiResponse]):
    pass


class EmojiCreate(BaseModel):
    name: str
    user_id: int
