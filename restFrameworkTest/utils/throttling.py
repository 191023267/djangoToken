from rest_framework.throttling import SimpleRateThrottle


# 访客用户
class VisitThrottle(SimpleRateThrottle):
    scope = 'thro'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# 登录账户
class UserThrottle(SimpleRateThrottle):
    scope = 'userthro'

    def get_cache_key(self, request, view):
        # 返回用户的唯一认证信息
        return request.user.id
