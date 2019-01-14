# -*- coding:utf-8 -*-
#!python3
'''
    auth :
    date:
    desc:  python调用R

'''
import django
import os
import rpy2.robjects as robject

# print("hello world")
#
# print(django.get_version())

robject.r('pi')
print(type(robject.r('pi')))