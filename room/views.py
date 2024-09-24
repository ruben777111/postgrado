from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect,get_object_or_404,render
import json
from .models import Room, Message
from room.consumers import ChatConsumer 

@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = Room.objects.get(slug=slug)
    messages = Message.objects.filter(room=room)
    #messages = Message.objects.filter(room=room)[0:50]

    return render(request, 'room/room.html', {'room': room, 'messages': messages})

from channels.layers import get_channel_layer
from django.http import HttpResponse
from asgiref.sync import async_to_sync
from room.consumers import ChatConsumer  # Importa tu ChatConsumer
from asgiref.sync import sync_to_async
from usuario.models import Usuario
from django.http import HttpResponse
from django.views import View
from room.consumers import ChatConsumer  # Reemplaza 'myapp' con la ubicación de tu consumidor

class SendMessageView(View):
    def get(self, request):
        room = get_object_or_404(Room, id=2)
        room_name = room.name  # Reemplaza con el nombre de la sala adecuado
        # Crea una instancia del consumidor
        consumer = ChatConsumer({'type': 'chat.join', 'room_name': room_name})

        # Envía un mensaje al consumidor
        message = "Este es un mensaje por defecto."
        consumer.send({
            'type': 'chat.message',
            'message': message,
            'username': request.user.username,  # Reemplaza con el nombre de usuario deseado
            'room': room_name,
        })

        return HttpResponse('Mensaje enviado por defecto a la sala de chat.')
from asgiref.sync import async_to_sync
def Prueba(request):

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notification_broadcast",
        {
            'type': 'send_notification',
            'message': json.dumps("Notification")
        }
    )
    return HttpResponse("Done")