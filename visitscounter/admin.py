from django.contrib import admin
from .models import VisitsCounter, Visitsdetail

# Register your models here.
@admin.register(VisitsCounter)
class VisitsCounterAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'visits')

@admin.register(Visitsdetail)
class VisitsdetialAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'date', 'visits')