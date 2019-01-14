# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.sessions import base_session
from django.contrib import auth
from . import models
from . import forms
import hashlib
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

user_list = []

def apage(request):
    return render(request, 'myapp/test.html')

def home(request):
    pass
    return render(request,'myapp/home.html')

def index(request):
    pass
    return render(request,'myapp/index.html')


def login(request):

    if request.method == "POST":
        login_form = forms.loginForm(request.POST)

        #重复登陆检查
        if request.session.get('is_login',None):
            return redirect("/index/")
        #重复登陆检查 end

        message="所有字段都必须填写"
        # print(username,passowrd)
        # if userName and passWord :

        if login_form.is_valid(): #表单自带方法，数据验证
            userName = login_form.cleaned_data['username']
            passWord = login_form.cleaned_data['password']


            user = models.userinfo.objects.get(uName=userName)


            if user == None:
                message = "用户不存在"
                return render('/login/')

            if not user.uhasConfirmed:
                message = "该用户还未邮件确认"
                return render(request, 'myapp/login.html', locals())

            if user.uPassword == hashCode(passWord):  # 判断密码，加密
                # seesion
                request.session['is_login'] = True
                request.session['username'] = user.uName
                # seesion end


                return redirect('/index/')
            else:
                message = "密码不正确"




        return render(request,'myapp/login.html',locals())
    else:
        login_form = forms.loginForm()

    return render(request, "myapp/login.html",locals())


def register(request):
    if request.session.get('is_login',None):
        #登陆状态不允许注册
        return redirect('/index/')
    if request.method == "POST":
        register_form = forms.registerForm(request.POST)
        message = "请检查填写内容"
        if register_form.is_valid():
            username  = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']

            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request,'login/register.html',locals())
            else:
                #检查用户名是否唯一
                same_name_user = models.userinfo.objects.filter(uName=username)
                if same_name_user:
                    message = "用户名已经存在，请重新选择"
                    return render(request,"login/register.html",locals())

                same_email_user=models.userinfo.objects.filter(uEamil=email)
                if same_email_user:
                    message="该邮箱已被注册，请使用别的邮箱"
                    return  render(request,"login/register.html",locals())
            #检查通过
            newUser = models.userinfo()
            newUser.uName=username
            newUser.uPassword=hashCode(password1) #加密
            newUser.uEamil=email
            newUser.uSex=sex
            newUser.save()

            #发送邮件确认
            code = makeConfirmString(newUser)
            sendConfirmEmial(email,code)
            return redirect('/login/')
    else:
        register_form =forms.registerForm()

    return render(request,'myapp/register.html',locals())


def logout(request):

    if not request.session.get('is_login',None):
        return redirect('/login/')

    request.session.flush() # 删除当前的会话数据和会话cookie。经常用在用户退出后，删除会话。
    '''
        del request.session['is_login']
        del request.session['user_id']
        del request.session['user_name']
    '''
    return redirect('/index/')




def userConfirm(request):
    code = request.GET.get('code',None)
    message=''
    try:
        confirm = models.confirmString.objects.get(code=code)
    except:
        message='无效的确认请求！'
        return render(request,'myapp/confirm.html',locals())

    c_time = confirm.confirmDate
    now = datetime.datetime.now()
    if now > c_time+datetime.timedelta(settings.CONFIRM_DAYS):
        confirm.user.delete()
        message='您的邮件已过期，请重新注册'
        return render(request,'myapp/confirm.html',locals())
    else:
        confirm.user.uhasConfirmed = True
        confirm.user.save()
        confirm.delete()
        message = '感谢确认，请使用账户登录'
        return render(request,'myapp/confirm.html',locals())


#密码加密
def hashCode(s,salt='mysite'):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()

def dehashCode(s,salt='mysite'):
    h=hashlib.sha256()
    s=s-salt
    h.update(s.encode())
    return h.hexdigest()

#注册确认 码
def makeConfirmString(user):
    #生成一个独一无二的code
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = hashCode(user.uName,now)
    models.confirmString.objects.create(code=code,user=user)
    return code


def sendConfirmEmial(email,confirmCode):

    subject, fromEmail = '来自myapp的注册确认邮件', 'hcxy0729@163.com'

    textContent = '感谢注册，这是cy编写的一个测试版的app。如果你看到这条信息，说明你的邮箱服务器不提供HTML连接功能，请联系管理员'
    htmlContext = '''<p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.liujiangblog.com</a>，这里是陈懿的Django App</p> , \
                     <p>请点击站点链接完成注册确认！</p> \
                     <p>此链接有效期为{}天！</p> \
                  '''
    htmlContext = htmlContext.format('127.0.0.1:8080',confirmCode,settings.CONFIRM_DAYS)
    msg = EmailMultiAlternatives(subject, textContent, settings.EMAIL_HOST_USER, [email])
    msg.attach_alternative(htmlContext, "text/html")
    msg.send()