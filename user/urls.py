# encoding: utf-8
'''
Created Time:2019/9/26 15:19
Author  :xiaolu
Software: PyCharm
'''
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.userlogin, name='userlogin'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.log_out, name='logout'),
    path('userinfo/', views.user_info, name='userinfo'),
    path('change_nickname/', views.change_nickname, name='change_nickname'),
    path('bind_email/', views.bind_email, name='bind_email'),
    path('bind_code/', views.send_verification_code, name='send_verification_code'),
    path('change_password/', views.change_password, name='change_password'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
]