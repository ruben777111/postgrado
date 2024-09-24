
# ContenType
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.text import slugify
#Timezone
from django.utils import timezone


# load model
from swapper import load_model

# Signals
from notify.signals import notificar

# Models
from usuario.models import Usuario

#Django
from django.contrib.auth.models import Group
from django.db.models.query import QuerySet
from django.db import models
import uuid
import random
import string
def aleatorio(longitud):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password
class NotificationQueryset(models.QuerySet):

    def leido(self):
        """
            Retornamos las notificaciones que hayan sido leidas en el actual Queryset
        """

        return self.filter(read=True)

    def no_leido(self):
        """
            Retornamos solo los items que no hayan sido leidos en el actual Queryset
        """	
        return self.filter(read=False)

    def marcar_todo_as_leido(self, destiny=None):
        """
            Marcar todas las notify como leidas en el actual queryset
        """
        qs = self.read(False)
        if destiny:
            qs = qs.filter(destiny=destiny)

        return qs.update(read=True)

    def marcar_todo_as_no_leido(self, destiny=None):
        """
            Marcar todas las notificaciones como no leidas en el actual queryset
        """

        qs = self.read(True)
        if destiny:
            qs = qs.filter(destiny=destiny)

        return qs.update(read=False)



class AbstractNotificationManager(models.Manager):
    def get_queryset(self):
        return self.NotificationQueryset(self.Model, using=self._db)

class AbstractNotificacion(models.Model):

    class Levels(models.TextChoices):
        success = 'Success', 'success',
        info = 'Info', 'info',
        wrong = 'Wrong', 'wrong'

    level = models.CharField(choices=Levels.choices, max_length=20, default=Levels.info)
    
    destiny = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones', blank=True, null=True)

    actor_content_type = models.ForeignKey(ContentType, related_name='notificar_actor', on_delete=models.CASCADE)
    object_id_actor = models.PositiveIntegerField()
    actor = GenericForeignKey('actor_content_type', 'object_id_actor')
    maestrante = models.CharField(max_length=800)
    programa = models.CharField(max_length=800)
    verbo = models.CharField(max_length=800)
    text = models.CharField(max_length=800)
    cod_notificacion = models.IntegerField( blank = True, null = True)
    rol = models.CharField(max_length=400)
    read = models.BooleanField(default=False)
    publico = models.BooleanField(default=True)
    eliminado = models.BooleanField(default=False)

    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    objects = NotificationQueryset.as_manager()
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "Actor: {} --- Destiny: {} --- Verb: {} ".format(self.actor.username, self.destiny.username, self.verbo)

    def save(self, *args, **kwargs):
        if not self.slug:
            timestamp_str = self.timestamp.strftime('%Y%m%d%H%M%S')
            aux=aleatorio(20)
            base_slug = f"{timestamp_str}-{slugify(self.actor.username)}-{slugify(aux)}"
            slug = base_slug	
           

            self.slug = slug
        super().save(*args, **kwargs)  

def notify_signals(verb,programa,maestrante,text,rol,cod_notificacion, **kwargs):
    """
        Funcion de controlador para crear una instancia de notificacion
        tras una llamada de signal de accion
    """

    destiny = kwargs.pop('destiny')
    actor = kwargs.pop('sender')

    publico = bool(kwargs.pop('publico', True))
    timestamp = kwargs.pop('timestamp', timezone.now())

    Notify = load_model('notify', 'Notification')
    levels = kwargs.pop('level', Notify.Levels.info)


    if isinstance(destiny, Group):
        destinies = destiny.user_set.all()
    elif isinstance(destiny, (QuerySet, list)):
        destinies = destiny
    else:
        destinies = [destiny]


    new_notify = []
    for destiny in destinies:
        notification = Notify(
            destiny=destiny,
            actor_content_type = ContentType.objects.get_for_model(actor),
            object_id_actor = actor.pk,
            verbo = str(verb),
            programa=str(programa),
            maestrante=str(maestrante),
            rol=str(rol),
            cod_notificacion=str(cod_notificacion),
            publico=publico,
            text=text,
            
            timestamp=timestamp,
            level=levels	

        )

        notification.save()
        new_notify.append(notification)

    return new_notify


notificar.connect(notify_signals, dispatch_uid='notify.models.Notification')