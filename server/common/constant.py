class Constant(object):
    SUCCESS_CODE = 2000  # 接口响应正确
    ERROR_CODE = 9999  # 接口响应错误
    NO_LOGIN_CODE = 2001  # 未登录

    # 默认分页数
    DEFAULT_PAGE_SIZE = 9999
    # token失效时间
    TOKEN_EXPIRE = 36000

    # 系统标识
    SYSTEM_KEY = 'baibao'

    "redis key"
    # 平台热度值缓存
    CACHE_PLATFORM_HEAT = SYSTEM_KEY + ':platforms:heat:{platform_id}'
    # 平台热度值缓存
    CACHE_WEBSITE_DAY_PV = SYSTEM_KEY + ':website:pv:{day}:{website_id}'