from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.src.emoji.models import UserEmoji, GeneralEmoji, User, Tier


class EmojiService:
    @staticmethod
    def can_add_emoji(user: User) -> bool:
        if user.role == 'Business':
            return True
        if user.role == 'Premium' and user.emoji_count < 100:
            return True
        if user.role == 'Free' and user.emoji_count < 5:
            return True
        return False

    @staticmethod
    async def create_emoji(data: dict, user_id: int) -> UserEmoji:
        user = User.get_one(user_id)
        if not EmojiService.can_add_emoji(user):
            raise ValueError("Emoji limit reached for your user role.")

        emoji = UserEmoji(**data)
        emoji.save()
        return emoji

    @staticmethod
    async def get_available_emojis(tier: Tier, offset: int = 0, limit: int = 20) -> (List[GeneralEmoji], int):
        cache_key = f"emojis:{tier}:{offset}:{limit}"
        cached_emojis = await get_from_cache(redis, cache_key)

        if cached_emojis:
            # If cache hit, return the cached emojis
            emojis, total_count = json.loads(cached_emojis)
            return emojis, total_count
        else:
            # If cache miss, fetch from DB and cache the result
            where_clause = (GeneralEmoji.is_active == True)
            # Your existing where clause logic...

            emojis = GeneralEmoji.get_all(
                offset=offset,
                limit=limit,
                order_by=GeneralEmoji.order,
                where=where_clause
            )
            total_count = GeneralEmoji.count(where=where_clause)

            # Cache the fetched result
            await save_to_cache(redis, cache_key, json.dumps((emojis, total_count)))

            return emojis, total_count

    @staticmethod
    async def invalidate_general_emojis_cache():
        # You might want to invalidate all tiers and ranges
        tiers = ['Free', 'Premium', 'Business']
        for tier in tiers:
            # Assuming you have a fixed range of offsets and limits you want to invalidate
            for offset in range(0, 100, 20):  # Example range for offsets
                for limit in [20, 40, 60]:  # Example set of limits
                    cache_key = f"emojis:{tier}:{offset}:{limit}"
                    await invalidate_cache(redis, cache_key)

await redis.close()
    @staticmethod
    async def get_user_emojis(user: User, offset: int = 0, limit: int = 20) -> (List[UserEmoji], int):
        where_clause = (UserEmoji.user_id == user.id)
        emojis = UserEmoji.get_all(
            offset=offset,
            limit=limit,
            where=where_clause
        )
        total_count = UserEmoji.count(where=where_clause)

        return emojis, total_count
