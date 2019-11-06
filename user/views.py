# encoding: utf-8
'''
Created Time:2019/9/26 15:08
Author  :xiaolu
Software: PyCharm
'''
import string
import random
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import RegisterForm, ChangeNicknameForm, BindEmailForm, ChangePasswordForm, ForgotPasswordForm
from django.urls import reverse
from .models import Profile

def userlogin(request):
    if request.method == 'GET':
        frompage = request.GET.get('from')
        context = {'frompage': frompage}
        return render(request, 'user/sign_In.html', context)
    if request.method == 'POST':
        username_or_email = request.POST.get('username_or_emial', '')
        if '@' in username_or_email:
            username = User.objects.get(email=username_or_email).username
        else:
            username = username_or_email
        password = request.POST.get('password', '')
        # referer = request.META.get('HTTP_REFERER', reverse('homepage'))
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST.get('from', reverse('homepage')))
        else:
            frompage = request.POST.get('frompage')
            return render(request, 'user/sign_In.html', {'loginfailed': True, 'frompage': frompage})

def user_register(request):
    if request.method == 'POST':
        reg_form = RegisterForm(request.POST, request=request)
        if reg_form.is_valid():#判断数据是否验证通过
            #用户注册实例化方法1
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            #创建用户
            user = User.objects.create_user(username, email, password)
            profile, created = Profile.objects.get_or_create(user=user)
            profile.nickname = username
            user.save()
            profile.save()
            # 清除session
            del request.session['register_code']
            #用户实例化方法2
            # user = User()
            # user.username = username
            # user.email = email
            # user.set_password(password)
            # user.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('homepage')))


        #页面跳转为处理
    else:
        reg_form = RegisterForm()

    context = {'reg_form': reg_form}
    return render(request, 'user/register.html', context)

def log_out(request):
    logout(request)
    return redirect(request.GET.get('from', reverse('homepage')))

def user_info(request):
    return render(request, 'user/userinfo.html')

def about_me(request):
    return render(request, 'user/about_me.html')

def change_nickname(request):
    redirect_to = redirect(request.GET.get('from', reverse('homepage')))
    if request.method == 'POST':
        form = ChangeNicknameForm(request.POST, user=request.user)
        if form.is_valid():
            nickname_new = form.cleaned_data['nickname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = nickname_new
            profile.save()
            return redirect('userinfo')

    else:
        form = ChangeNicknameForm()

    context = {}
    context['page_title'] = '修改昵称'
    context['form_title'] = '修改昵称'
    context['submit_text'] = '修改'
    context['return_back'] = redirect_to
    context['form'] = form
    return render(request, 'user/change_nickname.html', context)


def bind_email(request):
    print('开始绑定邮箱')
    if request.method == 'POST':
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect('userinfo')
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = '绑定邮箱'
    context['form_title'] = '绑定邮箱'
    context['submit_text'] = '绑定'
    context['form'] = form
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    print('send code')
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}

    if email != '':
        # 生成验证码
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            print('send code by email')
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_mail(
                '绑定邮箱',
                '验证码：%s' % code,
                '183138896@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)

def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect('homepage')
    else:
        form = ChangePasswordForm()

    context = {}
    context['page_title'] = '修改密码'
    context['form_title'] = '修改密码'
    context['submit_text'] = '修改'
    context['form'] = form
    return render(request, 'user/change_password.html', context)

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect('homepage')
    else:
        form = ForgotPasswordForm()

    context = {}
    context['page_title'] = '重置密码'
    context['form_title'] = '重置密码'
    context['submit_text'] = '重置'
    context['form'] = form
    return render(request, 'user/reset_password.html', context)