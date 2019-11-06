# encoding: utf-8
'''
Created Time:2019/11/4 13:55
Author  :xiaolu
Software: PyCharm
'''

from django.urls import path
from .views import like_change

urlpatterns = [
    path('likechange', like_change, name='likechange'),
]