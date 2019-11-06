from django.contrib import admin
from .models import Blogtype, Blog, Banner, PhotographyShow

# Register your models here.


@admin.register(Blogtype)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'get_visits', 'blog_type', 'author', 'created_time', 'last_updated_time', )

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'banner_url')

admin.site.register(PhotographyShow)
