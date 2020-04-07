from django.urls import path
from . import views, api

urlpatterns = [
    path('', views.smartsocket, name='smartsocket'),
    path('api', api.socket_data, name='socket_data'),
    path('1', api.socketSwitch1, name='socket_data'),
]