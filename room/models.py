from django.contrib.auth.models import User
from django.db import models
from usuario.models import Usuario

class Room(models.Model):
    
    idmaestrante = models.IntegerField( blank = False, null = True)
    iddocente = models.IntegerField( blank = False, null = True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
 

class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(Usuario, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)