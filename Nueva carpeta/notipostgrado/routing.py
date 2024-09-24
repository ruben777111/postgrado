from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from notipostgrado import consumers  # Reemplaza 'myapp' con el nombre de tu aplicación

application = ProtocolTypeRouter({
    "websocket": URLRouter([
        path("ws/some_path/", consumers.MyConsumer.as_asgi()),  # Define la URL de tu WebSocket
    ]),
})