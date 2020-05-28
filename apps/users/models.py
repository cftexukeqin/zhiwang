from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from django.utils.timezone import now as now_func
# Create your models here.


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ('male','男'),
        ('female','女')
    )
    nick_name = models.CharField(max_length=30,null=True,blank=True,verbose_name="姓名")
    birthday = models.DateField("出生日期",null=True,blank=True)
    gender = models.CharField("性别",choices=GENDER_CHOICES,default="female",max_length=10)
    mobile = models.CharField('电话',max_length=11,null=True,blank=True)
    email = models.CharField('邮箱',max_length=100,null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y%m', default='image/default.png', max_length=100)
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username