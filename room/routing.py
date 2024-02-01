from django.urls import path
from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notificaciones/$', consumers.NotificacionConsumer.as_asgi()),
]