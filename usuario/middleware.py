from django.http import HttpResponseRedirect
from django.urls import reverse

class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http' and scope['path'].startswith(reverse('admin:index')):
            user = scope.get('user')
            if not user or not user.is_superuser:
                response = HttpResponseRedirect(reverse('admin:login'))
                await response(scope, receive, send)  # Enviar la respuesta correctamente
                return

        # Llamar al siguiente middleware o aplicación en la cadena.
        return await self.get_response(scope, receive, send)
