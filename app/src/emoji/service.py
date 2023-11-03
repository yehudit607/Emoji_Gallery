from typing import List, Tuple, Optional
from aioredis import Redis
from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from app.src.emoji.orm import GeneralEmoji, UserEmoji
from app.src.emoji.schema import UserEmojiCreate

MAX_EMOJIS_BY_TIER = {
    'free': 5,
    'premium': 100,
    'business': None,  # Business users have no limit
}


async def can_user_upload(redis: Redis, user_id: int, user_tier: str) -> bool:
    if user_tier not in MAX_EMOJIS_BY_TIER:
        return False

    max_emojis = MAX_EMOJIS_BY_TIER[user_tier]
    if max_emojis is None:
        return True  # Business users have no limit

    current_emoji_count = await redis.get(f"user_emoji_count:{user_id}")
    current_emoji_count = int(current_emoji_count) if current_emoji_count else 0

    return current_emoji_count < max_emojis


async def increment_user_emoji_count(redis: Redis, user_id: int):
    await redis.incr(f"user_emoji_count:{user_id}")


async def get_gallery_emojis(db: Session, user_tier: str, offset: int = 0, limit: int = 10) -> Tuple[
    List[GeneralEmoji], int]:
    query = select(GeneralEmoji).where(GeneralEmoji.is_active)

    if user_tier != 'business':  # If the user is not 'business', filter by type
        allowed_types = ['free']
        if user_tier == 'premium':
            allowed_types.append('premium')
        query = query.filter(GeneralEmoji.emoji_type.in_(allowed_types))

    results = await db.execute(query.offset(offset).limit(limit))
    total = await db.execute(select([func.count()]).select_from(query.subquery()))

    return results.scalars().all(), total.scalar()


async def upload_user_emoji(session: Session, redis: Redis, emoji_data: UserEmojiCreate) -> UserEmoji:
    new_emoji = UserEmoji(**emoji_data.dict())
    session.add(new_emoji)
    session.commit()
    session.refresh(new_emoji)
    await increment_user_emoji_count(redis, emoji_data.user_id)
    return new_emoji


def get_user_emojis(
        session: Session,
        user_id: int,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10
) -> Tuple[List[UserEmoji], int]:
    query = session.query(UserEmoji).filter(UserEmoji.user_id == user_id)
    total = query.count()

    emojis = (
        query.order_by(UserEmoji.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return emojis, total
