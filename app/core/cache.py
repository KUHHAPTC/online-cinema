from typing import Callable, ParamSpec

from redis.asyncio import ConnectionPool, Redis

from app.core.config import get_cache_settings
from app.schemas import Schema

redis_settings = get_cache_settings()

P = ParamSpec("P")
connection_pool = ConnectionPool.from_url(redis_settings.REDIS_DSN)


async def get_redis_connect() -> Redis:

    return Redis(connection_pool=connection_pool, encoding="utf-8", decode_responses=True)


def cache(model: Schema, expire: int = 120) -> Callable[[Callable[P, Schema]], Callable[P, Schema]]:
    def decorator(func: Callable[P, Schema]) -> Callable[P, Schema]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Schema:
            _redis = await get_redis_connect()
            cache_key = f"{func.__name__}_{kwargs}"

            cached_result: Schema | None = await _redis.get(cache_key)
            if cached_result:
                return model.model_validate_json(cached_result)

            result: Schema = await func(*args, **kwargs)
            await _redis.set(cache_key, result.model_dump_json(), ex=expire)
            return result

        return wrapper

    return decorator
