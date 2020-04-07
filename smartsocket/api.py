from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Socket
from .serializer import SocketSerializers
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

def on_message(client, userdata, msg):
    print('初始设备信息')
    statu_dict = eval(eval(str(msg.payload)[1::]))
    socket1 = Socket.objects.get(id=1)
    socket2 = Socket.objects.get(id=2)
    socket3 = Socket.objects.get(id=3)
    socket1.status = statu_dict['statu1']
    socket2.status = statu_dict['statu2']
    socket3.status = statu_dict['statu3']

    socket1.save()
    socket2.save()
    socket3.save()
    client.disconnect()

# def on_subscribe(client, userdata):
#     print('已订阅到消息')
#

@api_view(['GET'])
def socket_data(request):
    client = mqtt.Client()
    try:
        client.connect("114.55.33.165", 1883, 60)
        connect_result = client.connect("114.55.33.165", 1883, 60)
    except OSError:
        connect_result = True
    if not bool(connect_result):
        client.subscribe("socket_status")
        client.on_message = on_message
        # client.on_subscribe = on_subscribe
        client.loop_forever()
    print('数据更新成功')
    socket = Socket.objects.all()
    socketSer = SocketSerializers(socket, many=True)
    jasonData = {'socketData': socketSer.data, 'esp8266_run': 'true'}
    return Response(jasonData)

@api_view(['POST'])
def socketSwitch1(request):
    data_dict = request.POST
    for key, val in data_dict.items():
        statu = (key + val)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("114.55.33.165", 1883, 60)
    client.publish("switch", statu)
    print(statu)
    return Response(None)
