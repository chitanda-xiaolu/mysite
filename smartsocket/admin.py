from django.contrib import admin
from .models import Socket

# Register your models here.
@admin.register(Socket)
class SocketAdmin(admin.ModelAdmin):
    list_display = ('id', 'status', 'msg', 'ele')