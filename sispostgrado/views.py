from django.contrib.auth import logout

from django.shortcuts import redirect,get_object_or_404    
from usuario.models import Usuario
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
import requests
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'autenticacion/password_reset_confirm.html'
    success_url = reverse_lazy('usuario:password_reset_complete')

    def form_valid(self, form):       
        response = super().form_valid(form)
        user = form.user  
        usuario = get_object_or_404(Usuario, ci_usuario=user.ci_usuario)  
        if not usuario.cambio_password:
            usuario.cambio_password = True
            usuario.save()  
        return response
def exit(request):
    logout(request)
    return redirect("/")