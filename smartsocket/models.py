from django.db import models

# Create your models here.
class Socket(models.Model):
    status = models.CharField(max_length=15)
    msg = models.CharField(max_length=15)
    ele = models.CharField(max_length=15)
