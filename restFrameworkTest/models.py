from django.db import models

# Create your models here.

class UserInfo(models.Model):
    user_type_choices = (
        (1, "普通用户"),
        (2, "VIP"),
        (3, "SVIP")
    )
    user_type = models.IntegerField(choices=user_type_choices)
    username = models.CharField(max_length=32)
    pwd = models.CharField(max_length=64)
