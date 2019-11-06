# encoding: utf-8
'''
Created Time:2019/11/4 0:35
Author  :xiaolu
Software: PyCharm
'''

from django.urls import path
from .views import comment_update

urlpatterns = [
    path('comment_update', comment_update, name='comment_update')
]