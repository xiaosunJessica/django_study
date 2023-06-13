from server.common.redisClient import RedisClient
from django.conf import settings


class Utils(object):
    @staticmethod
    def get_redis_client():
        """获取redis链接"""
        return RedisClient(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD
        )
