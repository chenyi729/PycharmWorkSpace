# -*- coding:utf-8 -*-
#!python3
'''
    auth : yi.chen
    date :
    desc : 发送html格式的邮件

'''
import os
from django.core.mail import EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE']='mysite.settings'

def sendemails(toAddress):
    subject, fromEmail = '来自myapp的测试邮件', 'hcxy0729@163.com'
    textContent='欢迎访问myapp，这是陈懿写的一个测试版的app'
    htmlContext='<p>欢迎访问myapp<a href="http://127.0.0.1:8080" target=blank></a>，这是陈懿写的一个测试版的app</p>'
    msg = EmailMultiAlternatives(subject,textContent,fromEmail,[toAddress])
    msg.attach_alternative(htmlContext,"text/html")
    msg.send()

if __name__ == '__main__':
    to="1842247881@qq.com"
    sendemails(to)