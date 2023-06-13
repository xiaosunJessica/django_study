import datetime
import inspect
import json
from functools import wraps
import pydantic.error_wrappers
from django.http import JsonResponse
from server.common.constant import Constant
from json.encoder import JSONEncoder
from django.db.models.base import ModelBase
from django.db.models.query import QuerySet
from django.core.paginator import Page
from server.common.myExcept import NoLoginExcept
from pydantic.main import ModelMetaclass
import logging

logger = logging.getLogger('django')


class BaseApi(object):
    def __init__(self, request):
        self.request = request
        self.user_info = dict()
        self.token = None

    def response(self, action_name: str):
        try:
            resp = getattr(self, action_name)()
        except NoLoginExcept:
            resp = self.response_json(code=Constant.NO_LOGIN_CODE, msg='登录已失效')
        except AssertionError as e:
            logger.info('request请求非法', exc_info=True)
            resp = self.response_error("{}".format(e))
        except Exception as e:
            logger.error('request请求异常', exc_info=True)
            resp = self.response_error("服务器error, 请查看日志{}".format(e))
        return resp

    def response_json(self, msg: str = '', code: int = None, data=None) -> JsonResponse:
        """
        :param msg: 接口返回msg
        :param code: 接口返回code
        :param data: 接口返回的data
        :return:
        """
        return JsonResponse({
            "code": code if code else Constant.SUCCESS_CODE,
            "msg": msg if msg else '',
            "data": data if data else dict()
        }, encoder=JsonDjangoEncoder)

    def response_error(self, msg: str) -> JsonResponse:
        return self.response_json(msg=msg, code=Constant.ERROR_CODE)


class ArgsFormat(object):
    """校验接口参数"""

    def __init__(self, method='GET', login=True):
        self.method = method  # 接口请求类型
        self.login = login  # 是否校验登陆

    def __call__(self, f):
        @wraps(f)
        def inner(*args, **kwargs):
            apiObject = args[0]
            request = apiObject.request
            # 请求校验
            if request.method != self.method:
                raise AssertionError('不支持的请求类型')
            # 权限校验
            if self.login:
                token = request.headers.get(Constant.SYSTEM_KEY + '-token')
                if token != 'qa':
                    raise NoLoginExcept()
            # 参数类型校验
            request_kwargs = dict()
            if request.GET:
                request_kwargs.update(request.GET.dict())
            if self.method == 'POST':
                if request.content_type == 'application/json':
                    if request.body:
                        request_kwargs.update(json.loads(request.body))
                elif request.content_type == 'multipart/form-data':
                    for k, v in request.POST.items():
                        request_kwargs[k] = v
            f_signature = inspect.signature(f)
            # 记录接口调用
            logger.info('({}) PATH={},PARAMS={}'.format(
                apiObject.user_info.get('name'),
                request.path,
                json.dumps(request_kwargs, ensure_ascii=False)
            ))
            param_kwargs = dict()
            for k, v in f_signature.parameters.items():
                if k == 'self':
                    continue
                param_type = v.annotation
                if isinstance(param_type, ModelMetaclass):
                    try:
                        formObject = param_type(**request_kwargs)
                    except pydantic.error_wrappers.ValidationError as e:
                        raise AssertionError('接口参数校验不通过：' + str(e))
                    param_kwargs[k] = formObject
                    continue
                has_default = False  # 是否设置默认值
                default = None  # 默认值
                if v.default != inspect._empty:
                    has_default = True
                    default = v.default

                if k not in request_kwargs.keys():
                    if not has_default:
                        raise AssertionError('{}参数缺失'.format(k))
                    param_kwargs[k] = default
                    continue
                if isinstance(request_kwargs[k], str):
                    api_v = request_kwargs[k].strip()
                else:
                    api_v = request_kwargs[k]
                if api_v is None or api_v == '':
                    if not has_default:
                        raise AssertionError('{}参数不能为空'.format(k))
                    param_kwargs[k] = default
                    continue
                param_kwargs[k] = api_v
                if v.annotation != inspect._empty:
                    # 兼容前端字符类型错误
                    if v.annotation == str and isinstance(api_v, int):
                        param_kwargs[k] = str(api_v)
                    elif v.annotation == int and isinstance(api_v, str) and api_v.isdigit():
                        param_kwargs[k] = int(api_v)
                    if not isinstance(param_kwargs[k], v.annotation):
                        raise AssertionError('{}参数必须是{}类型'.format(k, v.annotation))
            return f(*args, **param_kwargs)

        return inner


class JsonDjangoEncoder(JSONEncoder):
    """序列化接口返回"""

    def default(self, o):
        if isinstance(type(o), ModelBase):  # 数据库model对象
            o = o.__dict__
            if o.get('_state'):
                del o['_state']
            new_o = {}
            for k, v in o.items():
                if k.endswith('_id_id'):
                    new_o[k.replace('_id_id', '_id')] = v
                    continue
                new_o[k] = v
            return new_o
        elif isinstance(o, QuerySet) or isinstance(o, Page):  # orm查询结果对象或分页数据对象
            result = []
            for model_object in o:
                model_map = self.default(model_object)
                if model_map.get('_state'):
                    del model_map['_state']
                result.append(model_map)
            return result
        elif isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return JsonDjangoEncoder.default(self, o)
