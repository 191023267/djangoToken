from rest_framework.permissions import BasePermission


# 权限验证
class SVIPPermission(BasePermission):
    message = '必须是SVIP才能访问'

    def has_permission(self, request, view):
        if request.user and request.user.user_type != 3:
            return False
        else:
            return True
