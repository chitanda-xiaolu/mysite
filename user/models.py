# encoding: utf-8
'''
Created Time:2019/9/26 16:34
Author  :xiaolu
Software: PyCharm
'''
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20, default='昵称', verbose_name='昵称')
    user_head = models.ImageField(default='user/bg_ftrr.png', upload_to='user')

    def __str__(self):
        return self.nickname

# def get_nickname(self):
#     if Profile.objects.filter(user=self).exists():
#         profile = Profile.objects.get(user=self)
#         return profile
#     else:
#         return ''
#
# def has_nickname(self):
#     return Profile.objects.filter(user=self).exists()


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username




# User.get_nickname = get_nickname
# User.has_nickname = has_nickname
User.get_nickname_or_username = get_nickname_or_username