# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        recipient_username = text_data_json['recipient']  # Reemplaza con la forma en que obtienes el destinatario
        message = "Este es un mensaje para ti."

        await self.channel_layer.group_add(recipient_username, self.channel_name)

        await self.send(text_data=json.dumps({
            'message': message,
            'recipient': recipient_username
        }))

