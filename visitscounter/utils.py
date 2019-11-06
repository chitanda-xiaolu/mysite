# encoding: utf-8
'''
Created Time:2019/9/9 21:49
Author  :xiaolu
Software: PyCharm
'''
import datetime
from django.db.models import Sum
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import VisitsCounter, Visitsdetail
from blog.models import Blog


def counterMethod(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    if not request.COOKIES.get('blog_{}_readed'.format(obj.pk)):
        # if VisitsCounter.objects.filter(content_type=ct, object_id=obj.pk).count():  # 在判断blog是否已经应有计数模型
        #     visitsobj = VisitsCounter.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     visitsobj = VisitsCounter(content_type=ct, object_id=obj.pk)
        visitsobj, created = VisitsCounter.objects.get_or_create(content_type=ct, object_id=obj.pk)
        visitsobj.visits += 1
        visitsobj.save()
        date = timezone.now().date()
        visitsdetail, created = Visitsdetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        visitsdetail.visits += 1
        visitsdetail.save()
        print(ct.model)
    key = '{}_{}_readed'.format(ct.model, obj.pk)
    return key

#统计近七天的浏览数
def visits_of_recent(content_type):
    result_list = []
    today = timezone.now().date()
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=1)
        visits_details = Visitsdetail.objects.filter(content_type=content_type, date=date)
        result = visits_details.aggregate(visits_sum=Sum('visits'))#result是一个字典
        result_list.append(result['visits_sum'] or 0)
    return result_list

#获取今天的热门阅读
def get_popular_blog_of_today(content_type):
    today  = timezone.now().date()
    visits_today = Visitsdetail.objects.filter(content_type=content_type, date=today).order_by('-visits')
    return visits_today#返回的是一个content_type的查询对象

#获取昨天的热门阅读
def get_popular_blog_of_yesterday(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(1)
    visits_details = Visitsdetail.objects.filter(content_type=content_type, date=yesterday).order_by('-visits')
    return visits_details

#统计近七天的热门阅读
def get_popular_blog_of_sevenday():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blog_visits = Blog.objects.filter(visits_details__date__lt=today, visits_details__date__gte=date).\
        values('id', 'title').annotate(visits_sum=Sum('visits_details__visits')).order_by('-visits_sum')

    return blog_visits[:7]