from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .form import UserLoginForm,UserRegisterForm,User
# Create your views here.

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.is_staff=1
            new_user.is_superuser=1
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("index")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'blog/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")