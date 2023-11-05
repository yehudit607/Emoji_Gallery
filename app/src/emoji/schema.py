# from typing import List, Optional
#
# from pydantic import Field, ConfigDict
#
# from app.core.models.base import BaseModel
# from app.src.emoji.models import EmojiBase, EmojiType
#
#
# class UserEmojiCreate(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     is_active: Optional[bool] = True
#     emoji_type: EmojiType
#     name: str
#     order: Optional[int] = Field(None)
#
#
#
#
# class PagedEmojisResponse(BaseModel):
#     emojis: List[EmojiBase]
#     total: int
#     offset: int
#     limit: int
#
#
# class CreatedSuccessfullyResponse(BaseModel):
#     id: Optional[str] = Field(None)
#     message: str = "created successfully"
