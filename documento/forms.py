#importamos form
from django.forms import ValidationError
from django import forms
from .models import Documento

class DocumentoForm(forms.ModelForm):
    #referencia a los metadatos del formulario
    
    titulo_documento = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),min_length=3, max_length=120)
    archivo_documento = forms.FileField(required=True) 

    class Meta:
        model = Documento
        
        #fields = ['id_guia','nombre_guia','apellidos_guia','especialidad_guia','estado_guia']
        fields = ['titulo_documento','archivo_documento']
        labels = {

            'titulo_documento' : 'Titulo del documento',
            'archivo_documento' : 'Documento',
   
        }
  