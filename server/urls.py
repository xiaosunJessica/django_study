"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.http import HttpResponseNotFound
import importlib


def auto_router(request, api_path):
    # 接口映射
    path_list = api_path.split('/')
    if len(path_list) < 2:
        return HttpResponseNotFound()

    # 组装执行方法路径
    method_name = 'action_{}'.format(path_list[-1].lower())
    method_name = method_name.replace('-', '_')
    api_class_name = 'Api'
    api_file_path = 'server.module'
    for i in range(len(path_list) - 1):
        api_file_path += ".{}".format(path_list[i].lower())
    api_file_path += '.{}'.format(api_class_name)
    try:
        api_package = importlib.import_module('server.module.website.Api')
    except ModuleNotFoundError:
        return HttpResponseNotFound()
    api_class = getattr(api_package, api_class_name)
    if not api_class:
        return HttpResponseNotFound()
    api_object = api_class(request)
    if not hasattr(api_object, method_name):
        return HttpResponseNotFound()
    return getattr(api_object, 'response')(method_name)


urlpatterns = [
    path('api2/<path:api_path>', auto_router)
]
