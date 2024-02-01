from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse

def send_notification(request):
    message = "Nueva notificación"
    
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "my_group_name",  # Reemplaza 'my_group_name' con el nombre de tu grupo
        {
            "type": "notification.message",
            "message": message,
        },
    )
    #return JsonResponse(request, 'notipostgrado/notificaciones.html', { 'messages': 'messages'})
    return JsonResponse({"message": "Notificación enviada"})

from django.shortcuts import render

def VerNotificaciones(request):
    return render(request, 'notipostgrado/notificaciones.html')