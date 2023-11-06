import logging
import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.core.db.engine import get_engine
from app.core.db.session import DBSessionMiddleware
# from app.core.redis import get_redis
from app.src.emoji.views import router as gallery_router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_limiter import FastAPILimiter
from .core.middleware.nocache import NoCacheMiddleware
from .core.middleware.db_session_context import DBSessionMiddleware
from sqlalchemy.exc import OperationalError


from fastapi_redis_rate_limiter import RedisRateLimiterMiddleware, RedisClient


# Initialize the Redis client
#redis_client = RedisClient(host="localhost", port=6379, db=0)

# Apply the rate limiter middleware to the app
app = FastAPI()


@app.get("/", tags=["general"])
def read_root():
    return {"msg": "Welcome to the backend core in in FastAPI!"}


# @app.on_event("startup")
# async def startup():
#     redis = await get_redis()
#     FastAPILimiter.init(redis)
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     redis = await get_redis()
#     redis.close()
#     await redis.wait_closed()
#app.add_middleware(RedisRateLimiterMiddleware, redis_client=redis_client, limit=100, window=60)

app.add_middleware(DBSessionMiddleware, custom_engine=get_engine())
# app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

app.include_router(
    router=gallery_router,
    prefix="/api/gallery",
    tags=["Gallery"],
)


@app.get("/", tags=["general"])
def read_root():
    return {"msg": "Welcome to the backend core in in FastAPI!"}


def check_db_connection():
    try:
        with get_engine().connect():
            return True
    except OperationalError:
        return False


@app.get("/check_health", tags=["general"])
async def check_health():
    """
    Check all the services in the infrastructure are working
    """
    ok_code = "running"
    ko_code = "down"

    # DB check
    db_status = check_db_connection()
    if db_status:
        db_status = ok_code
    else:
        db_status = ko_code


    # # Redis check
    # try:
    #     redis_client = redis.StrictRedis(
    #         host=settings.redis_host, port=settings.redis_port
    #     )
    #     redis_client.ping()
    #     redis_status = ok_code
    # except Exception:
    #     redis_status = ko_code

    return {
        "db": db_status,
       # "redis": redis_status,
    }


@app.exception_handler(Exception)
def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.error(
        f"An error occurred: {exc}",
        exc_info=True,
        extra={
            "url": request.url,
            "method": request.method,
        },
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": f"{type(exc).__name__}",
            "message": f"{getattr(exc, 'message', None) or str(exc)}",
        },
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        access_log=False,
    )
