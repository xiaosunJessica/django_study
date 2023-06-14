import time
from .models import Website
from server.common.baseApi import BaseApi, ArgsFormat
from .Service import Service


class Api(BaseApi):
    @ArgsFormat(method='POST', login=False)
    def action_click(self, website_id: int, timestamp: int):
        system_timestamp = int(time.time())
        if abs(timestamp - system_timestamp) > 3:
            return self.response_error('参数非法')

        Service.iter_day_pv(website_id)
        return self.response_json()

    @ArgsFormat(method='POST', login=False)
    def action_statistics_day_pv(self, start_day: str, end_day: str):
        result = Service.search_pv_per_day(start_day=start_day, end_day=end_day)
        return self.response_json(data={'records': result})