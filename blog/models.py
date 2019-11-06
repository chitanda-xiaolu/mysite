from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from visitscounter.models import Counter, Visitsdetail


# Create your models here.
class Blogtype(models.Model):
    type_name = models.CharField(max_length=15)
    def __str__(self):
        return self.type_name


class Blog(models.Model, Counter):
    title = models.CharField(default='标题', max_length=100)
    blog_type = models.ForeignKey(Blogtype, on_delete=models.CASCADE)
    thumbnail = models.ImageField(blank=True, upload_to='thumbnail')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    visits_details = GenericRelation(Visitsdetail)

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-created_time',)

class Banner(models.Model):
    banner_title = models.CharField(default='幻灯片标题', max_length=30)
    banner_img = models.ImageField(default='幻灯片图片', upload_to='banner')
    banner_url = models.CharField(default='链接', max_length=100)

    def __str__(self):
        return self.banner_title

class PhotographyShow(models.Model):
    photo_name = models.CharField(default='照片名', max_length=30)
    photo = models.ImageField(default='展示照片', upload_to='photographyshow')
    photo_url = models.CharField(default='照片大图链接', max_length=100)
    blog_url = models.CharField(default='照片大图链接', max_length=100)

    def __str__(self):
        return self.photo_name

