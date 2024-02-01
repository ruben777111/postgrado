from django.shortcuts import render
from usuario.models import Usuario

# Create your views here.
def index(request):
    return render(request,'notification/index.html')

from django.http import HttpResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

def notificar_usuario(request, user_id):
    # Lógica para obtener el usuario con user_id
    user = Usuario.objects.get(id=user_id)

    # Crea un mensaje
    message = "Tienes una nueva notificación."

    # Envía el mensaje al consumidor WebSocket correspondiente
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_add)("notification", user.username)
    async_to_sync(channel_layer.group_send)(
        user.username,
        {
            "type": "send_notification",
            "message": message,
        },
    )

    return HttpResponse("Notificación enviada a " + user.username)
