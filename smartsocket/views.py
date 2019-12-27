from django.shortcuts import render

# Create your views here.
def smartsocket(request):
    return render(request, 'smartsocket/smartsocket.html')
