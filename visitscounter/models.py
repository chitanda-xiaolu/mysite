from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


# Create your models here.
#统计浏览数的模型
class VisitsCounter(models.Model):
    visits = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


# 定义返回浏览数的类
class Counter():
    def get_visits(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            visitsobj = VisitsCounter.objects.get(content_type=ct, object_id=self.pk)
            return visitsobj.visits
        except exceptions.ObjectDoesNotExist:
            return 0

#定义具体某一天计数模型
class Visitsdetail(models.Model):
    visits = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')