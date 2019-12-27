from rest_framework import serializers
from .models import Socket

class SocketSerializers(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Socket
        fields = '__all__'