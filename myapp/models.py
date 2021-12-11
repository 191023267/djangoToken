from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=32, verbose_name='用户名', null=False)
    password = models.CharField(max_length=64, verbose_name='密码', null=False)
    states = models.BooleanField(verbose_name='状态', default=False)

    def __str__(self):
        return self.username


