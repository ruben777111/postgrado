from django.http import Http404

class SuperuserOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            raise Http404("No tienes permiso para acceder a esta página.")
        response = self.get_response(request)
        return response