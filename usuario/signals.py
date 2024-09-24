# usuario/signals.py

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in

from django.utils import timezone

@receiver(user_logged_in)
def verificar_vigencia_matricula(sender, user, request, **kwargs):
    from .models import Maestrante 

   # maestrantes = Maestrante.objects.filter(usuario=user)
   # if  maestrantes:
   #     fecha_actual = timezone.now().date()
   #     for maestrante in maestrantes:
   #         if maestrante.vigencia_matricula < fecha_actual:            
   #             maestrante.bloqueo_maestrante = True
   #             maestrante.save()
