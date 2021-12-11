from django.shortcuts import render, HttpResponse, get_object_or_404

import jwt
from . import models
import datetime
from django.http import JsonResponse

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage


# 获全部用户信息
def getUsers(request, user_id=None):
    if request.method == 'GET':
        # 如果user_id 为None的说明是全部查找
        if user_id == None:
            users = models.Users.objects.all()

            """ 分页 """
            # 获取 url 后面的 page 参数的值, 首页不显示 page 参数, 默认值是 1
            page = request.GET.get('page', 1)
            page_size = request.GET.get('page_size', None)  # 一页显示几条数据
            if page_size is None:
                page_size = 5  # 如果没有传过来默认一页显示5条数据

            # 将数据按照规定每页显示 10 条, 进行分割
            paginator = Paginator(users, page_size)
            try:
                users = paginator.page(page)
                # todo: 注意捕获异常
            except PageNotAnInteger:
                # 如果请求的页数不是整数, 返回第一页。
                users = paginator.page(1)
            except InvalidPage:
                # 如果请求的页数不存在, 重定向页面
                return HttpResponse('找不到页面的内容')
            except EmptyPage:
                # 如果请求的页数不在合法的页数范围内，返回结果的最后一页。
                users = paginator.page(paginator.num_pages)

            # 将限制的数据进行显示
            users = users.object_list.values()
            """  """

        # 如果user_id 有值就是按条件查询
        else:
            users = models.Users.objects.filter(id=user_id).values_list()

        # 将用户数据的QuerySet转换成列表
        users = list(users)
        data = {
            "count": len(users),
            "next": None,
            "previous": None,
            "data": {'data': users, 'meta': {'status': 200, 'msg': '获取用户成功'}}
        }
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii':False})

    # 不是get请求
    else:
        return JsonResponse({"status": 400, "msg": "不是GET请求"})


# 删除单个用户
def delUser(request, user_id):
    # 定义返回的信息
    data = {
        "next": None,
        "previous": None,
        "data": {
            "data": None,
            "meta": {'status': 200, 'msg': '删除成功'}
        }
    }
    if request.method == 'DELETE':
        try:
            userInfo = get_object_or_404(models.Users, id=user_id)
        except:
            data.get('data')['meta'] = {'status': 400, 'msg': '查无此用户'}
            return JsonResponse(data)
        if userInfo:
            # 执行删除操作
            delUser = userInfo.delete()
            return JsonResponse(data)

    # 如果不是DELETE请求
    else:
        data.get('data')['meta'] = {'status': 400, 'msg': '不是DELETE请求'}
        return JsonResponse(data)


# 添加用户
def addUser(request):
    data = {
        "next": None,
        "previous": None,
        "data": {
            "data": None,
            "meta": {'status': 200, 'msg': '添加用户成功'}
        }
    }
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return JsonResponse({"status": 401, "msg": "用户名或密码不能为空"})

        try:  # 尝试查询该用户名是否存在
            user = models.Users.objects.filter(username=username)
            # a = get_object_or_404(models.Users, username=username)

            data.get('data')['data'] = user.values()
            data.get('data')['meta'] = {"status": 401, "msg": "该用户已经存在"}
            return JsonResponse(data)
        except:  # 如果报错说明不存在啊然后在创建
            user = models.Users.objects.create(username=username, password=password)

            user = models.Users.objects.filter(id=user.id).values()
            data.get('data')['data'] = list(user)[0]
            return JsonResponse(data, safe=False)

    # 如果不是POST请求
    else:
        data.get('data')['meta'] = {'status': 400, 'msg': '不是POST请求'}
        return JsonResponse(data, safe=False)


# 修改用户
def modUser(request, user_id):
    data = {
        "next": None,
        "previous": None,
        "data": {
            "data": None,
            "meta": {'status': 200, 'msg': '修改用户成功'}
        }
    }
    if request.method == 'PUT':
        username = request.POST.get('username')
        password = request.POST.get('password')
        status = request.POST.get('status')
        if username == '' or password == '':
            return JsonResponse({"status": 401, "msg": "用户名或密码不能为空"})
        # 尝试获取用户信息
        try:
            get_object_or_404(models.Users, id=user_id)
        except:
            data.get('data')['meta'] = {"status": 401, "msg": "没有此用户"}
            # 如果查询不到直接返回
            return JsonResponse(data)
        # 如果获取到信息
        else:
            models.Users.objects.filter(id=user_id).update(
                username=username, password=password, states=status
            )
            userInfo = models.Users.objects.filter(id=user_id).values_list()
            data.get('data')['data'] = list(userInfo)
            return JsonResponse(data)
    else:
        data.get('data')['meta'] = {"status": 402, "msg": "不是PUT请求"}
        return JsonResponse(data)


# 登录给出token
def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return JsonResponse({"status": 401, "msg": "用户名或密码不能为空"})
        user = models.Users.objects.filter(username=username, password=password)
        # 如果查询到用户后
        if user:
            user = user[0]  # 永远登录第一个
            dic = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 开始时间
                'data': {'id': user.id, 'username': user.username},
            }
            # 生成token
            encoded_jwt = jwt.encode(dic, 'secret_key', algorithm='HS256')
            print(encoded_jwt)

            # 调用验证token函数
            from middleware.LearnMiddle import token_verify
            userDict = token_verify(encoded_jwt)

            userDict['token'] = encoded_jwt  # 将token带过去

            return JsonResponse(userDict, safe=False)
        # 如果没有查询到
        else:
            return JsonResponse({"status": 401, "msg": "用户名或密码错误"})
    # 如果不是POST提交
    else:
        return JsonResponse({"status": 400, "msg": "不是POST提交"})


# 用户注册
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '' or password == '':
            return JsonResponse({"status": 401, "msg": "用户名或密码不能为空"})
        # 创建用户
        models.Users.objects.create(username=username, password=password, states=False)

        return JsonResponse({"status": 200, "msg": "创建用户成功"})

    # 如果直接访问路径
    return JsonResponse({"status": 402, "msg": "未使用POST请求"})


# k = base64.b64decode(
#     'eyJ1c2VybmFtZSI6Ilx1OGZkMFx1N2VmNFx1NTQ5Nlx1NTU2MVx1NTQyNyIsInNpdGUiOiJodHRwczovL29wcy1jb2ZmZWUuY24ifQ==')
# print(k.decode(), '*--------*')
#
# toke = jwt.decode(encoded_jwt, 'secret_key', algorithms=['HS256'])
# print(toke)
# n = jwt.decode(encoded_jwt, verify=False)
# print(n)

# import base64
# encoded_jwt = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MjQ2MDc5OTEsImlhdCI6MTYyNDUyMTU5MSwiZGF0YSI6eyJ1c2VybmFtZSI6ImFkbWluIiwicGFzc3dvcmQiOiJhZG1pbiJ9fQ.lKjAg0UXykP28OnrCm2L2OU6CbLU9_B0kAG2WgL1sd0"
#
# print(base64.b64decode(encoded_jwt))
