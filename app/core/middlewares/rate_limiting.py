from fastapi import Request

from fastapi_limiter import FastAPILimiter


async def rate_limit_middleware(request: Request, call_next):
    identifier = f"{request.client.host}"
    await FastAPILimiter.check(identifier)
    response = await call_next(request)
    return response
