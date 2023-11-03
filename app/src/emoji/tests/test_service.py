import pytest
from unittest.mock import AsyncMock, MagicMock

from app.src.emoji.schema import UserEmojiCreate
from app.src.emoji.service import can_user_upload, increment_user_emoji_count, get_gallery_emojis, upload_user_emoji, get_user_emojis

@pytest.mark.asyncio
async def test_can_user_upload():
    redis = AsyncMock()
    redis.get.return_value = '3'  # Assuming the user already has 3 emojis

    # Test 'free' tier where the limit is 5
    can_upload = await can_user_upload(redis, 1, 'free')
    assert can_upload is True

    # Test limit reached
    redis.get.return_value = '5'
    can_upload = await can_user_upload(redis, 1, 'free')
    assert can_upload is False

    # Test 'business' tier which has no limit
    can_upload = await can_user_upload(redis, 2, 'business')
    assert can_upload is True

@pytest.mark.asyncio
async def test_increment_user_emoji_count():
    redis = AsyncMock()
    await increment_user_emoji_count(redis, 1)
    redis.incr.assert_called_once_with("user_emoji_count:1")

@pytest.mark.asyncio
async def test_get_gallery_emojis():
    db = AsyncMock()
    db.execute.return_value.scalars().all.return_value = ['emoji1', 'emoji2']
    db.execute.return_value.scalar.return_value = 2  # Total count

    emojis, total = await get_gallery_emojis(db, 'free')
    assert len(emojis) == 2
    assert total == 2

    # You can add more scenarios for 'premium' and 'business' tiers

@pytest.mark.asyncio
async def test_upload_user_emoji():
    session = MagicMock()
    redis = AsyncMock()
    user_emoji_data = UserEmojiCreate(user_id=1, emoji_type='free', image='image_data')

    session.commit = MagicMock()
    session.refresh = MagicMock()
    session.add = MagicMock()

    # Simulate database actions
    await upload_user_emoji(session, redis, user_emoji_data)

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()

    # Check Redis is called to increment emoji count
    redis.incr.assert_called_once_with("user_emoji_count:1")

def test_get_user_emojis():
    session = MagicMock()
    user_id = 1
    offset = 0
    limit = 10
    session.query().filter().count.return_value = 1
    session.query().filter().order_by().offset().limit().all.return_value = ['emoji']

    emojis, total = get_user_emojis(session, user_id, offset, limit)

    assert total == 1
    assert len(emojis) == 1

