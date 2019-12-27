from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Socket
from .serializer import SocketSerializers
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


@api_view(['GET', 'POST'])
def socket_data(request):
    socket = Socket.objects.all()
    socketSer = SocketSerializers(socket, many=True)
    jasonData = {'socketData': socketSer.data}
    return Response(jasonData)

@api_view(['GET', 'POST'])
def socketSwitch1(request):
    data = request.POST
    payload = str(data)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("127.0.0.1", 1883, 60)
    # 发布 test主题
    client.publish("test", payload)
    print(data)
    return Response(None)
