from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.src.emoji.models import UserEmoji, GeneralEmoji, User
from app.src.emoji.service import EmojiService

from app.core.db.session import db  as get_db
router = APIRouter()


@router.get("/useremoji", response_model=List[UserEmoji])
def get_user_emojis(user_id: int, db: Session = Depends(get_db)):
    user_emojis = UserEmoji.get_all(where=UserEmoji.user_id == user_id)
    return user_emojis


@router.get("/generalemoji", response_model=List[GeneralEmoji])
def get_general_emojis(user_id: int, db: Session = Depends(get_db)):
    # Assuming you have a way to get the user from the user_id
    user = User.get_one(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    available_emojis = EmojiService.get_available_emojis(user)
    return available_emojis


@router.post("/useremoji", response_model=UserEmoji)
def create_user_emoji(user_id: int, emoji_data: dict, db: Session = Depends(get_db)):
    try:
        created_emoji = EmojiService.create_emoji(data=emoji_data, user_id=user_id, db=db)
        return created_emoji
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
