# encoding: utf-8
'''
Created Time:2019/11/4 0:04
Author  :xiaolu
Software: PyCharm
'''
from django.urls import path
from .views import blog_detail, blog_with_type, blog_classify_by_date



urlpatterns = [
    #http://localhost:8000/blog/1
    path('<int:blog_pk>', blog_detail, name='blog_detail'),
    path('type/<int:id>', blog_with_type, name='blog_with_type'),
    path('date/<int:year>/<int:month>', blog_classify_by_date, name='blog_classify_by_date'),
]