from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

import jwt


# 验证token
def token_verify(encoded_jwt):
    try:
        data = {'data': jwt.decode(encoded_jwt, 'secret_key', algorithms=['HS256']),
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


class getToken(MiddlewareMixin):

    def process_request(self, request):
        # request.META 包含了本次HTTP请求的Header信息
        # 调用获取请求头函数
        token = request.META.get('HTTP_TOKEN', -1)  # 获取客户端的token

        # 如果路径是用户登录的话直接结束
        path = request.META.get('PATH_INFO')
        # 判断字符串是否以指定字符开头
        # print(path.startswith('/api/v1/'))
        if (path == '/users/login/') or (path == '/users/register/') or (path.startswith('/api/v1/')):
            return

        # 如果客户端没有携带请求头过来返回值是 -1
        if token == -1:
            return JsonResponse({'meta': {'status': 403, 'msg': '您没有权限'}}, safe=False)

        # 调用验证token的函数
        msg = token_verify(token)

        status = msg.get('meta').get('status', -1)

        # token验证成功情况
        if status == 200:
            # 通过
            return

        # token验证失败情况
        else:
            data = {
                "next": None,
                "previous": None,
                "data": {
                    "data": None,
                    "meta": {'status': 200, 'msg': '删除成功'}
                }
            }
            data.get('data')['meta'] = msg
            return JsonResponse(data, safe=False)
