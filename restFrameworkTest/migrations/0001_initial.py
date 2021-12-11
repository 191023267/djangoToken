# Generated by Django 3.2.5 on 2021-12-09 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.IntegerField(choices=[(1, '普通用户'), (2, 'VIP'), (3, 'SVIP')])),
                ('username', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=64)),
            ],
        ),
    ]
