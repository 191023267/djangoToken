from django.urls import path, re_path
from . import views

urlpatterns = [
    # 用户登录
    path('', views.login_action),
    path('login/', views.login_action),
    # 用户注册
    path('register/', views.register),
    # 删除用户
    path('delUser/<int:user_id>/', views.delUser),
    # 修改用户
    path('modUser/<int:user_id>/', views.modUser),
    # 添加用户
    path('addUser/', views.addUser),
    # 查询用户
    re_path(r'^getUsers/((?P<user_id>\d)?/)?$', views.getUsers),
]
