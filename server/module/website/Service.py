from datetime import datetime
from server.common.utils import Utils
from server.common.constant import Constant
from .models import Website


class Service():
    @staticmethod
    def iter_day_pv(website_id: int) -> None:
        today = datetime.now().strftime('%Y-%m-%d')
        redis = Utils.get_redis_client()
        conn = redis.connect()
        key = Constant.CACHE_WEBSITE_DAY_PV.format(website_id=website_id, day=today)
        has_cache = conn.exists(key)
        if not has_cache:
            Website.objects.get(id=website_id)
            pv = conn.incr(key)
            conn.expire(key, 86400)
        else:
            pv = conn.incr(key)
            conn.expire(key, 86400)
