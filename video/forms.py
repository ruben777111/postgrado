#importamos form
from django.forms import ValidationError
from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    #referencia a los metadatos del formulario
    
    titulo_video = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),min_length=3, max_length=120)
    enlace_video = forms.URLField(widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),min_length=3, max_length=100)

    class Meta:
        model = Video
        
        #fields = ['id_guia','nombre_guia','apellidos_guia','especialidad_guia','estado_guia']
        fields = ['titulo_video','enlace_video']
        labels = {

            'titulo_video' : 'Titulo del video',
            'enlace_video' : 'Enlace del video',
   
        }
