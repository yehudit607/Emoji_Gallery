from fastapi import APIRouter
from app.src.emoji.models import UserEmoji, GeneralEmoji, User

from app.core.db.session import db as get_db

router = APIRouter()

from fastapi import APIRouter
from typing import List

router = APIRouter()

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.src.emoji.models import User
from app.src.emoji.schema import UserEmojiResponse, EmojiCreate
from app.src.emoji.service import EmojiService

router = APIRouter()


@router.post("/user-emojis/", response_model=UserEmoji)
def create_user_emoji(
        user_id: int,
        tier: str,
        emoji_data: EmojiCreate,
):
    # Fetch the user based on user_id (You need to have a method for that)
    user = User.filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    try:
        return EmojiService.create_emoji(data=emoji_data.dict(), user_id=user.id, tier=tier, db=db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user-emojis/", response_model=List[UserEmoji])
def list_user_emojis(
        user_id: int,
        tier: str,
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    emojis = EmojiService.get_user_emojis(user_id=user.id, tier=tier, db=db)
    return emojis


@router.get("/general-emojis/", response_model=List[GeneralEmoji])
def list_general_emojis(tier: str):
    emojis = EmojiService.get_available_emojis(tier=tier)
    return emojis
