import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext


# Create your views here.

# 登录页面
def my_login(request):
    return render(request, 'index.html')

# 注册页面
def my_regist(request):
    return render(request, 'register.html')

# 点击注册事件
def do_regist(request):

    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['passWord']
        print(username)
        print(password)

        # 判断用户名唯一, 保证不能注册重复的账号
        same_name_user=User.objects.filter(username=username)
        if same_name_user:
            return HttpResponse(json.dumps({'msg':'用户名已存在, 请重新选择用户名!'}),content_type='application/json')
        new_user = User.objects.create_user(username=username,password=password)

        if new_user is not None:
            return HttpResponse(json.dumps({'msg':'注册成功'}),content_type='application/json')
        else:
            return render(request,'accounts/register',{'error':'注册失败!'})
    return redirect('/accounts/register/')

#  登录验证(点击登录事件
def login_auth(request):
    """
    :return:
    成功：重定向到首页
    失败：返回login页面，并提示错误
    """
    if request.method == 'POST':
        username = request.POST['userName']
        password = request.POST['passWord']
    print(username)
    print(password)
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)  # 保存登录会话,将登陆的信息封装到request.user,包括session
        return redirect("../../")
    else:
        return render(request, 'index.html', {'error': '用户名或者密码错误！'})
    return redirect("/login/")

# 登出
@login_required()
def my_logout(request):
    """
    :param request
    :return: 退出并重定向到登录页面
    """
    logout(request)
    return redirect("/accounts/login/")

@login_required()
def change_password(request):
    return render(request, 'changePWD.html')

# 修改密码
@login_required()
def do_change_password(request):
    if request.method == "POST":
        # username = request.POST.get("username")
        password = request.POST.get("oldPassword")
        new_password = request.POST.get("newPassword")
        username = request.user.username       # 获取当前登录用户的用户名
        user = authenticate(username=username,
                            password=password)

        print("当前用户登录名是：{}".format(username))
        if not user:
            #  如果用户没在user中，证明登录失败，修改密码先判断登录成功，再去修改密码
            return HttpResponse(json.dumps({'msg':'修改失败,原密码错误, 请重新输入'}),content_type='application/json')
        else:
            user.set_password(new_password)  # 重置密码
            user.save()  #  一定要保存才会生效
            return HttpResponse(json.dumps({'msg':'修改成功'}),content_type='application/json')
