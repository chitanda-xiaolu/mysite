"""chitanda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from blog import views
from user.views import about_me
# from .views import page_error, page_not_found


urlpatterns = [
    path('', views.blog_list, name='homepage'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('comment/', include('comment.urls')),
    path('likes/', include('like.urls')),
    path('user/', include('user.urls')),
    path('smartsocket/', include('smartsocket.urls')),
    path('aboutme/', about_me, name='aboutme'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# handler404 = page_not_found
# handler500 = page_error
