import redis
from app.utils.config import CELERY_BROKER_URL


def get_redis_client():
    """Get Redis client instance"""
    return redis.Redis.from_url(CELERY_BROKER_URL, decode_responses=True)
