from server.common.baseModel import BaseModel, models


class Website(BaseModel):
    """页面配置"""
    is_out = models.BooleanField(verbose_name='是否外部页面', default=True)
    name = models.CharField(max_length=128, verbose_name='名称')
    url = models.CharField(max_length=1024, verbose_name='地址', null=True)
    sort = models.IntegerField(verbose_name='从大到小排序', default=0)


class WebsiteStatistics(BaseModel):
    """工具数据统计表"""
    website_id = models.IntegerField(verbose_name='Website表主键')
    day = models.CharField(max_length=128, verbose_name='日期')
    pv = models.IntegerField(verbose_name='pv值')
