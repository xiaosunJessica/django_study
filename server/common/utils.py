from server.common.redisClient import RedisClient
from django.conf import settings
from datetime import date, timedelta


class Utils(object):
    @staticmethod
    def get_redis_client():
        """获取redis链接"""
        return RedisClient(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD
        )

    @staticmethod
    def calc_date(current_day:str, num:int) -> str:
        """
        计算日期
        :param current_day: 被计算的日期，2021-12-10
        :param num: 加减的天数
        :return: 计算后的日期
        """
        date_obj = date.fromisoformat(current_day)
        new_date_obj = date_obj + timedelta(days=num)
        new_date_str = new_date_obj.isoformat()
        return new_date_str


    @staticmethod
    def calc_date_diff(start_day: str, end_day: str) -> int:
        """
         计算日期差值
         :param start_day: 开始日期，2021-12-10
         :param end_day: 结束日期
         :return: 天数，相同日期=1
         """
        start_date = date.fromisoformat(start_day)
        end_day = date.fromisoformat(end_day)
        days = (end_day - start_date).days
        return days + 1
