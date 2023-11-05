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
    def create_emoji(data: dict, user_id: int, db:Session) -> UserEmoji:
        user = User.get_one(user_id)
        if not EmojiService.can_add_emoji(user):
            raise ValueError("Emoji limit reached for your user role.")

        emoji = UserEmoji(**data)
        db.add(emoji)
        user.emoji_count += 1
        db.commit()
        return emoji

    from sqlalchemy import or_

    class EmojiService:

        @staticmethod
        def get_available_emojis(user: User) -> List[GeneralEmoji]:
            if user.role == 'Business':
                # Business users get all active emojis.
                return GeneralEmoji.get_all(
                    order_by=GeneralEmoji.order,
                    where=(GeneralEmoji.is_active == True)
                )
            elif user.role == 'Premium':
                # Premium users get all active emojis except for business-only.
                return GeneralEmoji.get_all(
                    order_by=GeneralEmoji.order,
                    where=(
                            GeneralEmoji.is_active == True &
                            or_(GeneralEmoji.emoji_type == Tier.Free, GeneralEmoji.emoji_type == Tier.Premium)
                    )
                )
            else:  # Assuming this is 'Free'
                # Free users get only active free emojis.
                return GeneralEmoji.get_all(
                    order_by=GeneralEmoji.order,
                    where=(GeneralEmoji.is_active == True & GeneralEmoji.emoji_type == Tier.Free)
                )





