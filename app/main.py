import logging
import uvicorn
from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse

from app.core.redis import get_redis
from app.src.emoji.views import router as posts_router
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_limiter import FastAPILimiter

from app.core.db.session import db_session_middleware
from app.core.middlewares.rate_limiting import rate_limit_middleware

app = FastAPI()


@app.on_event("startup")
async def startup():
    redis = await get_redis()
    FastAPILimiter.init(redis)


@app.on_event("shutdown")
async def shutdown():
    redis = await get_redis()
    redis.close()
    await redis.wait_closed()


app.add_middleware(BaseHTTPMiddleware, dispatch=db_session_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

app.include_router(
    router=posts_router,
    prefix="/api/posts",
    tags=["Posts"],
)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to the social app. To see endpoints, go to /docs"}


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
