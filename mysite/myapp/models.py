# -*- coding:utf-8 -*-
#!python3

# Create your models here.

#创建模型 , 会自动映射的数据库里面（自动创建）
from django.db import models
from django.contrib import admin




# user
class userinfo(models.Model):
    gender = (
        ('male','男'),
        ('female','女'),
    )

    uName = models.CharField(max_length=128,primary_key=True,unique=True,blank=True)
    uPassword=models.CharField(max_length=256)
    uEamil = models.CharField(max_length=128)
    uSex = models.CharField(max_length=32,choices=gender,default="男")
    uRegisterDate = models.DateTimeField(auto_now_add=True)
    uhasConfirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.uName

    class Mata:
        ordering = ["-uRegisterDate"]
        verbose_name="用户"
        verbose_name_plural = "用户"


class confirmString(models.Model):
    code=models.CharField(max_length=256)
    user=models.OneToOneField('userinfo',on_delete=None)
    confirmDate=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.uName+":"+self.code

    class Mate:
        ordering = ["-uRegisterDate"]
        verbose_name = "确认码"
        verbose_name_plural = "确认码"