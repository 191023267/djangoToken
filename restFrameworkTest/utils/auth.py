import jwt

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from restFrameworkTest import models


# 验证token
def token_verify(encoded_jwt):
    try:
        data = {'data': jwt.decode(encoded_jwt, 'secret_key', algorithms=['HS256']).get('data'),
                'meta': {'status': 200, 'msg': '验证成功'}}
        return data

    # 验证不通过异常
    except jwt.InvalidSignatureError as error:
        return {"meta": {"status": 403, "msg": "token验证出错"}}
    # token过期异常
    except jwt.ExpiredSignatureError as error:
        return {'meta': {"status": 403, "msg": "token过期"}}
    # 验证不通过异常
    except jwt.InvalidTokenError as error:
        return {'meta': {"status": 403, "msg": "token异常出错"}}


class MyBaseAuthentication(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs):
        token = request._request.GET.get('token')
        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')
        return ("alex", None)


class Authtication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        ret = token_verify(token)
        if ret['meta']['status'] == 403:
            raise exceptions.AuthenticationFailed(ret)
        else:
            user_id = ret['data'].get('id')
            user_data = models.UserInfo.objects.get(id=user_id)

            # self.user, self.auth = user_auth_tuple
            return (user_data, token)  # 如果返回值是None表示我不管 交给下一个认证类
