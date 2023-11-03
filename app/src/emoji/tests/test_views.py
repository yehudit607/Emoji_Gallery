import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from sqlalchemy.orm import Session
from aioredis import Redis
from unittest.mock import AsyncMock, MagicMock

from app.core.db.session import get_session
from app.core.redis import get_redis
from app.main import app


# Mock dependencies for dependency injection
@pytest.fixture
def mock_session():
    session = AsyncMock(spec=Session)
    yield session


@pytest.fixture
def mock_redis():
    redis = AsyncMock(spec=Redis)
    yield redis


@pytest.fixture(autouse=True)
def override_dependency():
    # Override get_session and get_redis dependencies with mocks
    app.dependency_overrides[get_session] = mock_session
    app.dependency_overrides[get_redis] = mock_redis

# Test for /gallery/ endpoint
@pytest.mark.asyncio
async def test_gallery():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/gallery/", params={'user_tier': 'basic', 'user_id': 1})
    assert response.status_code == 200
    assert 'emojis' in response.json()
    assert 'total' in response.json()


# Test for /emoji/ endpoint
@pytest.mark.asyncio
async def test_upload_emoji(mock_redis):
    # Set up mock return values
    mock_redis.can_user_upload.return_value = True

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/emoji/", json={
            "user_id": 1,
            "emoji_type": "basic",
            # Add other required fields here
        })
    assert response.status_code == 200
    assert 'message' in response.json()
    assert response.json()['message'] == 'Emoji uploaded successfully'


# Test for /user/{user_id}/emojis/ endpoint
@pytest.mark.asyncio
async def test_list_user_emojis(mock_session):
    # Assuming you have a function 'get_user_emojis' that returns a list of emojis and a total
    mock_session.get_user_emojis.return_value = (['emoji1', 'emoji2'], 2)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/user/1/emojis/")
    assert response.status_code == 200
    assert 'emojis' in response.json()
    assert 'total' in response.json()
    assert response.json()['total'] == 2
