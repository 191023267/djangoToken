import datetime
import json
import jwt

from django.http import JsonResponse, HttpResponse


from rest_framework.views import APIView
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, versioning
from rest_framework.request import Request

from restFrameworkTest.utils.throttling import VisitThrottle
from restFrameworkTest import models

from django.views import View


# 登录
class AuthView(View):
    # 不进行用户验证
    authentication_classes = []
    # 不验证权限
    permission_classes = []
    # 访客节流
    throttle_classes = [VisitThrottle, ]

    def get(self, request, *args, **kwargs):
        return JsonResponse({})

    def post(self, request, *args, **kwargs):
        ret = {
            'code': 200,
            'msg': 'ok'
        }
        try:
            req = json.loads(request.body)
            username = req.get('username')
            password = req.get('password')
            obj = models.UserInfo.objects.filter(username=username, pwd=password).first()
        except Exception as e:
            return HttpResponse('err！')
        if not obj:
            ret['code'] = 400
            ret['msg'] = '用户名或密码错误'
            return JsonResponse(ret)
        else:
            dic = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 开始时间
                'data': {'id': obj.id, 'username': obj.username},
            }
            # 生成token
            token_encoded_jwt = jwt.encode(dic, 'secret_key', algorithm='HS256')
            ret['token'] = token_encoded_jwt
            return JsonResponse(ret)

    def put(self, request, *args, **kwargs):
        pass


# 订单
class OrderView(APIView):

    def get(self, request, *args, **kwargs):
        self.dispatch
        # print(request.POST)
        # print(request.query_params)

        # print(request.body)
        # print(request.POST)
        print(request.data.get('username'))

        # from rest_framework.versioning import URLPathVersioning
        # 获取版本
        # print(request.version)
        # 获取处理版本的对象
        # print(request.versioning_scheme)


        return HttpResponse('订单')
