from datetime import datetime
from server.common.utils import Utils
from server.common.constant import Constant
from .models import Website, WebsiteStatistics
from django.db.models import Sum
import logging

logger = logging.getLogger('django')


class Service(object):
    @staticmethod
    def iter_day_pv(website_id: int) -> None:
        today = datetime.now().strftime('%Y-%m-%d')
        redis = Utils.get_redis_client()
        conn = redis.connect()
        key = Constant.CACHE_WEBSITE_DAY_PV.format(website_id=website_id, day=today)
        has_cache = conn.exists(key)
        logger.info('-has_cache:{}:{}'.format(has_cache, today))
        if not has_cache:
            Website.objects.get(id=website_id)
            pv = conn.incr(key)
            conn.expire(key, 86400)
            WebsiteStatistics.objects.create(
                website_id=website_id,
                day=today,
                pv=pv
            )
        else:
            pv = conn.incr(key)
            conn.expire(key, 86400)
            WebsiteStatistics.objects.filter(website_id=website_id, day=today).update(pv=pv)

    @staticmethod
    def search_pv_per_day(start_day: str, end_day: str) -> list:
        """根据日期分组统计pv数据"""
        days = Utils.calc_date_diff(start_day, end_day)
        if days <= 0:
            return AssertionError('日期筛选错误')
        result = []
        query = WebsiteStatistics.objects.filter(day__gte=start_day, day__lte=end_day).values('day')
        query = query.annotate(num=Sum('pv'))
        day_map = {row['day']: row['num'] for row in query}
        for i in range(days):
            day = Utils.calc_date(start_day, i)
            pv = day_map.get(day)
            result.append({
                'day': day,
                'pv': pv if pv else 0
            })
        return result
