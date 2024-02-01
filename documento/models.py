from datetime import timedelta
from django.db import models

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save,pre_save
from django.core.validators import FileExtensionValidator
#from guia.models import Guia

# Create your models here.
ext_validator=FileExtensionValidator(['pdf']) 
class Documento(models.Model):
    id_documento = models.AutoField(primary_key = True)
    titulo_documento = models.CharField(max_length=200, verbose_name="Título")
    archivo_documento = models.FileField(validators=[ext_validator],upload_to='tesis/', max_length=254,blank = True, null = True)
     
    created = models.DateTimeField(auto_now_add=True,verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True,verbose_name="Fecha de edición")
    estado_documento = models.BooleanField('Estado', default = True)
    class Meta:
        verbose_name = "Documento"
        verbose_name_plural = "Documentos"
        ordering = ["-created"]

    def __str__(self):
        return self.titulo_documento

