import threading
from django.conf import settings
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render


class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )

# Create your models here.

#定义评论模块的模型
class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    root = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='root_comment')
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE, related_name='comments')
    reply_to = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='replies')

    def send_mail(self):
        if self.parent is None:
            # 评论我的博客
            subject = '有人评论你的博客'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复你的评论'
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_text'] = self.comment_text
            context['url'] = self.content_object.get_url()
            text = render(None, 'comment/send_mail.html', context).content.decode('utf-8')
            send_mail = SendMail(subject, text, email)
            send_mail.start()

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ['comment_time']

