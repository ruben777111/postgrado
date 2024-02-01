from channels.testing import ChannelsLiveServerTestCase
from channels.testing.websocket import WebsocketCommunicator
from notification.consumers import NotificationConsumer
from usuario.models import Usuario
class WebSocketTest(ChannelsLiveServerTestCase):
    async def test_enviar_alerta_de_prueba(self):
        communicator = WebsocketCommunicator(NotificationConsumer.as_asgi(), "/ws/notifications/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Simular el envío de una alerta de prueba con un user_id específico
        user_id = 2  # Reemplaza con el ID de usuario deseado
        await communicator.send_json_to({"message": "Alerta de prueba", "recipient": user_id})

        # Espera a recibir una respuesta del servidor
        response = await communicator.receive_json_from()
        self.assertEqual(response["message"], "Alerta de prueba")

        # Cierra la conexión WebSocket
        await communicator.disconnect()
from django.test import TestCase

class MiPrueba(TestCase):
    def setUp(self):
        # Configuración de prueba
        # Por ejemplo, crear objetos de prueba en la base de datos
        self.objeto_prueba = Usuario(nombre="Prueba")
        self.objeto_prueba.save()

    def test_algo(self):
        # Pruebas que utilizan el objeto de prueba configurado en setUp
        self.assertEqual(self.objeto_prueba.nombre, "Prueba")
