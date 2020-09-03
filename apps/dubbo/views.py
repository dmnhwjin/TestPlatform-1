import json

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from dubbo.dubbo_client import GetDubboService, InvokeDubboApi


class DubboApi(APIView):

    def get(self, request):
        '''
        获取服务的ip和端口
        :param request:
        :return:
        '''
        service_name = request.GET.get('service_name')
        dubbo_info = GetDubboService().get_dubbo_info(service_name)
        return Response(dubbo_info)

    def post(self, request, *args):
        """
        请求Dubbo接口
        :param request:
        :return:
        """
        service_name = request.data.get('service_name')
        dubbo_method = request.data.get('dubbo_method')
        # 多参数类型，多参数
        params_type = request.data.get('params_type')
        params = request.data.get('params')
        dubbo_info = GetDubboService().get_dubbo_info(service_name)
        server_host = dubbo_info.get("server_host")
        server_port = dubbo_info.get("server_port")
        # 判断参数类型 ,
        if params_type == "class":
            result = InvokeDubboApi(server_host, server_port).invoke_dubbo_api(service_name, dubbo_method, params)
        else:
            args = params
            result = InvokeDubboApi(server_host, server_port).invoke_dubbo_api(service_name, dubbo_method, *args)
        return Response(json.loads(result))