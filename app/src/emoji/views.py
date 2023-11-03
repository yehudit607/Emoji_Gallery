import logging
from typing import List

from aioredis import Redis
from fastapi import status, Depends, HTTPException, Query, APIRouter

from app.core.db.session import get_session
from app.core.redis import get_redis
from service import can_user_upload, get_gallery_emojis, upload_user_emoji
from schema import CreatedSuccessfullyResponse, PagedEmojisResponse, UserEmojiCreate
from sqlalchemy.orm import Session

from app.src.emoji.service import get_user_emojis

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/gallery/emojis", response_model=PagedEmojisResponse)
async def gallery(
        user_tier: str, user_id: int,
        offset: int = 0, limit: int = 10,
        session: Session = Depends(get_session),
):
    emojis, total = await get_gallery_emojis(session, user_tier, offset, limit)
    return PagedEmojisResponse(emojis=emojis, total=total, offset=offset, limit=limit)


@router.post("/emoji/", response_model=CreatedSuccessfullyResponse)
async def upload_emoji(
        emoji_data: UserEmojiCreate,
        session: Session = Depends(get_session),
        redis: Redis = Depends(get_redis)
):
    if not await can_user_upload(redis, emoji_data.user_id, emoji_data.emoji_type):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Upload limit reached for user tier.")

    return await upload_user_emoji(session, redis, emoji_data)


@router.get("/user/emojis/{user_id}/", response_model=List[PagedEmojisResponse])
async def list_user_emojis(
    user_id: int,
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session),
):
    try:
        emojis, total = get_user_emojis(session, user_id, offset, limit)
        return {
            "emojis": emojis,
            "total": total,
            "offset": offset,
            "limit": limit
        }
    except Exception as e:
        logger.exception(f"Failed to list emojis for user {user_id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to list emojis for user {user_id}") from e

