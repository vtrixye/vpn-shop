import os
from redis.asyncio import Redis
from utils.logger import get_logger

logger = get_logger(__name__)

redis_client: Redis | None = None

def get_redis() -> Redis:
    if redis_client is None:
        raise RuntimeError("Redis client is not initialized.")
    return redis_client

async def init_redis():
    global redis_client
    try:
        redis_url = os.getenv("REDIS_URL")
        redis_client = Redis.from_url(redis_url, decode_responses=True)
        await redis_client.ping()
        logger.info("Redis connected successfully")
    except Exception as e:
        logger.error(f"Failed to connect to Redis\n{e}")
        raise

async def close_redis():
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis connection closed")