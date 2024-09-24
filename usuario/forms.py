from django import forms
from .models import SustentacionTesisHistorial,SustentacionPerfilHistorial,CentroActividades,BancoNotificacion,Programa,Avance_2,DocenteProvisional,TribunalPerfil,TribunalTesis,Avance,Requisitos,Usuario,Maestrante,Docente,Cronograma,Cronograma2,ReporteGeneral,Docente_Revisor


import random
import string
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class BackupForm(forms.Form):
    output_directory = forms.CharField(label='Directorio de salida', required=False)
    output_filename = forms.CharField(label='Nombre del archivo de salida', required=False)

def generar_password(longitud):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password


class CustomPasswordResetForm(PasswordResetForm):
    correo_inst = forms.EmailField(
        label=_("Correo Institucional"),
        widget=forms.EmailInput(attrs={'placeholder': 'Correo Institucional', "class": "form-control", 'required': 'true', 'id': 'correo_inst'})
    )
    email = forms.EmailField(widget=forms.HiddenInput(attrs={'id': 'correo'}))

    username = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'required': 'true', 'id': 'usuario', "class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super(CustomPasswordResetForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('correo_inst')
        username = cleaned_data.get('username')

        if not email and not username:
            raise forms.ValidationError("Debes proporcionar un correo electrónico o un nombre de usuario.")

        return cleaned_data

    def clean_correo_inst(self):
        correo_inst = self.cleaned_data.get('correo_inst')
        if not correo_inst or not get_user_model().objects.filter(correo_inst__iexact=correo_inst).exists():
            raise forms.ValidationError(
                "No existe una cuenta con ese correo institucional.",
                code='correo_inst_does_not_exist',
            )
        return correo_inst
    
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        username = self.cleaned_data.get('username')
        correo_inst = self.cleaned_data.get('correo_inst')
        
        
        # Valida que al menos se proporcione un username o un correo_inst
        if not username and not correo_inst:
            return

        user = None

        if correo_inst:
            users_by_correo_inst = get_user_model()._default_manager.filter(
                correo_inst__iexact=correo_inst,
                is_active=True
            )

            if users_by_correo_inst.count() > 0:
                user = users_by_correo_inst[0]

        if username and not user:
            user_by_username = get_user_model()._default_manager.filter(
                username=username,
                is_active=True
            )

            if user_by_username.count() > 0:
                user = user_by_username[0]

        if user is not None:
            context['user'] = user
            super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)
    def get_users(self, email=None, username=None):
        if not email and not username:
            raise ValueError("Debes proporcionar un correo electrónico o un nombre de usuario.")

        users = get_user_model()._default_manager.filter(is_active=True)

        if email:
            users = users.filter(correo_inst__iexact=email)

        if username:
            users = users.filter(username=username)

        return users



class FormularioPrograma(forms.ModelForm):
    nombre_programa= forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Programa"}),min_length=3, max_length=150, label="PROGRAMA :")
    class Meta:
            
        model=Programa        
        fields=('nombre_programa',)
    def clean_nombre_programa(self):
        nombre_programa = self.cleaned_data['nombre_programa']
        if nombre_programa:
            return nombre_programa.upper()
        return nombre_programa  

class FormularioUsuario(forms.ModelForm):     
    
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad","id":"ci"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre","id":"nom"}),min_length=3, max_length=120, label="NOMBRE :") 
    ru = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"RU","id":"ru"}),required=False, max_value=100000000000000, label="R.U. :")  
    cel_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular","id":"celular"}),required=True,min_value=1, max_value=100000000000000, label="Nº CELULAR :")  
    cel_usuario2 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular de referencia","id":"celular2"}),required=False,min_value=1, max_value=100000000000000, label="Nº CELULAR DE REFERENCIA:") 
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional", "id": "correoinst"}), label="CORREO INSTITUCIONAL", required=True)
    correo = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico personal", "id": "correo"}), label="CORREO PERSONAL", required=False)
  
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    class Meta:
        model=Usuario
        fields=('ci_usuario','nombre_usuario','paterno','materno','ru','cel_usuario','cel_usuario2','correo_inst','correo')
        widgets={
            
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
          
            'correo_inst': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo electronico institucionalsss','required':'required'}),
            
        }      
      
        labels = {
            
           
            'correo_inst': ('CORREO INSTITUCIONAL :'),
            'ci_usuario': ('CEDULA DE IDENTIDAD  :'),
        }


    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno    

class FormularioAdministradores(forms.ModelForm):     
    
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :") 
    cel_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=True,min_value=1, max_value=100000000000000, label="Nº CELULAR :")  
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    class Meta:
        model=Usuario
        fields=('ci_usuario','nombre_usuario','paterno','materno','cel_usuario','correo_inst')
        widgets={
            
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),

        }      
      
        labels = {
            
           
            'correo_inst': ('CORREO INSTITUCIONAL :'),
            'ci_usuario': ('CEDULA DE IDENTIDAD  :'),
        }

    tipo_usuario = forms.ChoiceField(
        choices=[('', 'Seleccione tipo de administrador'), ('1', 'Tecnico de Postgrado/Coordinación de investigación'), ('2', 'Coordinación de Postgrado')],
        required=True,
        label="TIPO DE ADMINISTRADOR",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno     
class FormularioAdministradoresNuevo(forms.ModelForm):     
    
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :") 
    cel_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=True,min_value=1, max_value=100000000000000, label="Nº CELULAR :")  
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    class Meta:
        model=Usuario
        fields=('ci_usuario','nombre_usuario','paterno','materno','cel_usuario','correo_inst')
        widgets={
            
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),

        }      
      
        labels = {
            
           
            'correo_inst': ('CORREO INSTITUCIONAL :'),
            'ci_usuario': ('CEDULA DE IDENTIDAD  :'),
        }

    tipo_usuario = forms.ChoiceField(
        choices=[('', 'Seleccione tipo de administrador'), ('1', 'Tecnico de Postgrado/Coordinación de investigación'), ('2', 'Coordinación de Postgrado')],
        required=True,
        label="TIPO DE ADMINISTRADOR",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno 
class FormularioAdministradoresEditar(forms.ModelForm):     
    
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :") 
    cel_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=True,min_value=1, max_value=100000000000000, label="Nº CELULAR :")  
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    class Meta:
        model=Usuario
        fields=('ci_usuario','nombre_usuario','paterno','materno','cel_usuario','correo_inst','rol_postgrado','rol_tecnico_investigacion')
        widgets={
            
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),

        }      
      
        labels = {
            
           
            'correo_inst': ('CORREO INSTITUCIONAL :'),
            'ci_usuario': ('CEDULA DE IDENTIDAD  :'),
        }


    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno     


class FormularioUsuarioMaestrante(forms.ModelForm):
    
   
    version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa","id":"tipo1"}),min_length=1, max_length=120, label="VERSIÓN DEL PROGRAMA :",required=False) 
   
    gestion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Gestión"}),required=True,min_value=1, max_value=999999999999, label="GESTIÓN :")    
 
    class Meta:
        model=Maestrante
        fields=('programa','version','gestion','tipo_maestrante')
        widgets={
            'programa': forms.Select(attrs={'class':'form-control','placeholder':'Seleccione programa','required':'required',}),

           'tipo_maestrante': forms.Select(attrs={'class':'form-control','placeholder':'Seleccione programa','required':'required',}),
        } 
        labels = {
            'programa': ('PROGRAMA :'),    

        }
        placeholder = {
            'programa': ('Seleccione programa'),

        }

class FormularioUsuarioMaestranteDictamen(forms.ModelForm):
   

    class Meta:
        model=Maestrante
        fields=('procedencia_tema','procedencia_tesis')
   
       
 

class RegistroMaestranteForm(forms.ModelForm):
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    ru = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"R.U."}),required=False,min_value=1, max_value=10000000000, label="R.U. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :")
    cel_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=True,min_value=1, max_value=100000000000000, label="Nº CELULAR :")    
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    

    tipo_maestrante = forms.ChoiceField(
        choices=[('', 'Seleccione un tipo de maestrante'), ('1', 'Programa regular'), ('2', 'Programa Antiguo')],
        required=True,
        label="TIPO DE MAESTRANTE",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = ['ci_usuario', 'nombre_usuario','paterno','materno', 'correo_inst','ru','cel_usuario']
    
    tipo_usuario = forms.IntegerField(initial=1, widget=forms.HiddenInput())  # Por defecto debe ser 1

    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(), 
        required=True, 
        label="SELECCIONE PROGRAMA",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione programa"
    )
   
    version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa"}),min_length=1, max_length=120, label="VERSIÓN DEL PROGRAMA :",required=True) 
    gestion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Gestión"}),required=True,min_value=1, max_value=999999999999, label="GESTIÓN :")    
    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
   
    def clean_version(self):
        version = self.cleaned_data['version']
        if version:
            return version.upper()
        return version 
    
class RegistroNuevoMaestranteForm(forms.ModelForm):
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    ru = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"R.U."}),required=False,min_value=1, max_value=10000000000, label="R.U. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :")
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    cel_usuario= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=False,min_value=999999, max_value=100000000000000, label="Nº CELULAR :")
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    tipo_maestrante = forms.ChoiceField(
        choices=[('', 'Seleccione un tipo de maestrante'), ('1', 'Programa regular'), ('2', 'Programa antiguo')],
        required=True,
        label="TIPO DE MAESTRANTE",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'paterno', 'materno', 'ci_usuario', 'ru', 'correo_inst','cel_usuario', 'tipo_maestrante', 'programa', 'version', 'gestion', 'tipo_usuario']
    
    tipo_usuario = forms.IntegerField(initial=1, widget=forms.HiddenInput())  # Por defecto debe ser 1

    programa = forms.ModelChoiceField(
        queryset=Programa.objects.all(), 
        required=True, 
        label="SELECCIONE UN PROGRAMA",
        widget=forms.Select(attrs={'class': 'form-control'}),
        empty_label="Seleccione un programa"
    )
   
    version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa"}),min_length=1, max_length=120, label="VERSIÓN DEL PROGRAMA :",required=True) 
    gestion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Gestión"}),required=True,min_value=1, max_value=999999999999, label="GESTIÓN :")    


    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno     
    def clean_version(self):
        version = self.cleaned_data['version']
        if version:
            return version.upper()
        return version 

class RegistroDocenteForm(forms.ModelForm):
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :")
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    cel_usuario= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=False,min_value=999999, max_value=100000000000000, label="Nº CELULAR :")
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    

    class Meta:
        model = Usuario
        fields = ['ci_usuario', 'nombre_usuario', 'paterno', 'materno', 'correo_inst','cel_usuario']
    
    tipo_usuario = forms.IntegerField(initial=2, widget=forms.HiddenInput()) 
    especialidad_docente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Especialidad del docente"}),min_length=1, max_length=120, label="ESPECIALIDAD DEL DOCENTE :",required=True) 
    docente_interno = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), label="DOCENTE INTERNO", required=False)
    docente_externo = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), label="DOCENTE EXTERNO", required=False)
    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
   
    def clean_especialidad_docente(self):
        especialidad_docente = self.cleaned_data['especialidad_docente']
        if especialidad_docente:
            return especialidad_docente.upper()
        return especialidad_docente 
class RegistroNuevoDocenteForm(forms.ModelForm):
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :")
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),required=False,min_length=3, max_length=120, label="APELLIDO MATERNO :")    
    correo_inst = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control no-uppercase", "placeholder": "Correo electronico institucional"}), label="CORREO INSTITUCIONAL", required=True)
    cel_usuario= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular"}),required=False,min_value=999999, max_value=100000000000000, label="Nº CELULAR :")

    class Meta:
        model = Usuario
        fields = ['ci_usuario', 'nombre_usuario', 'paterno', 'materno', 'correo_inst','cel_usuario']
    
    tipo_usuario = forms.IntegerField(initial=2, widget=forms.HiddenInput()) 
    especialidad_docente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa"}),min_length=1, max_length=120, label="ESPECIALIDAD DEL DOCENTE :",required=True) 
    docente_interno = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), label="DOCENTE INTERNO", required=False)
    docente_externo = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-check-input"}), label="DOCENTE EXTERNO", required=False)
    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if nombre_usuario:
            return nombre_usuario.upper()
        return nombre_usuario 
    def clean_paterno(self):
        paterno = self.cleaned_data['paterno']
        if paterno:
            return paterno.upper()
        return paterno     
    def clean_materno(self):
        materno = self.cleaned_data['materno']
        if materno:
            return materno.upper()
        return materno  
    def clean_especialidad_docente(self):
        especialidad_docente = self.cleaned_data['especialidad_docente']
        if especialidad_docente:
            return especialidad_docente.upper()
        return especialidad_docente 
class FormularioUsuarioMaestranteComplemento(forms.ModelForm):
    cel_usuario= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular de referencia"}),required=False,min_value=999999, max_value=100000000000000, label="NÚMERO DE CELULAR:") 
    cel_usuario2= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Número de celular de referencia"}),required=False,min_value=999999, max_value=100000000000000, label="Nº CEL REFERENCIA :") 

    class Meta:
        model=Usuario
        fields=('cel_usuario','cel_usuario2','correo')
        widgets={
        
            'correo': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo personal'}),
            

        } 
        labels = {
     
            'correo': ('CORREO PERSONAL :'),
           
        }
      


class FormularioUsuarioDocente(forms.ModelForm):
  
    especialidad_docente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Especialidad del docente"}),min_length=1, max_length=120, label="ESPECIALIDAD DEL DOCENTE :") 
    docente_interno = forms.BooleanField(  widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}),required=False)
    docente_externo = forms.BooleanField(  widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}),required=False)
    class Meta:
        model=Docente
        fields=('especialidad_docente','docente_interno','docente_externo')
      
        labels = {

            'docente_interno': ('DOCENTE INTERNO  :'),
            'docente_interno': ('DOCENTE EXTERNO  :'),

        }
    def clean_especialidad_docente(self):
        especialidad_docente = self.cleaned_data['especialidad_docente']
        if especialidad_docente:
            return especialidad_docente.upper()
        return especialidad_docente       




class FormularioDocenteProvisional(forms.ModelForm):
    avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
    class Meta:
        model = Maestrante
        fields = ('provisional',"avance_tesis")
        
        widgets={
            'provisional': forms.Select(attrs={'class':'form-control','required':'required'}),
            
        }     
        labels = {
            'provisional': ('DOCENTE PROVISIONAL:'),
            
            
        }  

class FormularioMatricula(forms.ModelForm):
    vigencia_matricula_regular_total = forms.DateField(label='ACTUALIZAR VIGENCIA DEL PROGRAMA - PROGRAMA REGULAR', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    vigencia_matricula_antiguo_total = forms.DateField(label='ACTUALIZAR VIGENCIA DEL PROGRAMA - PROGRAMA ANTIGUO', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    vigencia_matricula_antiguo = forms.DateField(label='ACTUALIZAR VIGENCIA DE MATRICULA DEL PROGRAMA - PROGRAMA ANTIGUO', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)



    version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa","id":"tipo1"}),min_length=1, max_length=120, label="VERSIÓN DEL PROGRAMA :",required=False) 
   
    gestion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Gestión"}),required=True,min_value=1, max_value=999999999999, label="GESTIÓN :")    
 
    
    class Meta:
        model = Maestrante
        fields = ('version',"gestion","vigencia_matricula_antiguo","vigencia_matricula_antiguo_total","vigencia_matricula_regular_total")
        
          
        labels = {
            'version': ('VERSIÓN DEL PROGRAMA:'),
            'gestion': ('GESTIÓN:')
            
            
        }  

class FormularioActividad2(forms.ModelForm):
    
    avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
  
    class Meta:
        model=Maestrante
        fields=("avance_tesis",)

class FormularioReporteGeneral(forms.ModelForm):
    reporte = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"8"}),min_length=3, max_length=1000,required=True)
    aceptar_revisor = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    aprobacion = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('si', 'Doy procedencia para la Defensa de tesis'), ('no', 'No doy procedencia para la Defensa de tesis')],required=True
    )
    class Meta:
        model=ReporteGeneral
        fields=('reporte','aceptar_revisor','aprobacion')

class FormularioReporteGeneral2(forms.ModelForm):
    reporte2 = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"8"}),min_length=3, max_length=1000,required=True)
    aceptar_revisor2 = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))

    class Meta:
        model=ReporteGeneral
        fields=('reporte2','aceptar_revisor2')



class FormularioMaestranteGuia(forms.ModelForm):
   
    class Meta:
        model=Maestrante
        fields=("provisional","guia","revisor")
        widgets={
            'provisional': forms.Select(attrs={'class':'form-control'}),
            'guia': forms.Select(attrs={'class':'form-control'}),
            'revisor': forms.Select(attrs={'class':'form-control'}),
            
        }     
        labels = {
            'provisional': ('DOCENTE PROVISIONAL:'),
            'revisor': ('DOCENTE REVISOR:'),
            'guia': ('DOCENTE GUÍA:'),
            
            
        }      
       

class FormularioTemaTesis(forms.ModelForm):
 
    tema_perfil_postulado = forms.CharField(label='Tema del perfil postulado',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),required=False,min_length=1, max_length=240)
    tema_tesis_perfil = forms.CharField(label='Tema del perfil de Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),required=False,min_length=1, max_length=240)
    tema_borrador_tesis = forms.CharField(label='Tema del borrador Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),required=False,min_length=1, max_length=240)
    tema_tesis = forms.CharField(label='Tema de Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),required=False,min_length=1, max_length=240)
    titulo_de_tesis = forms.CharField(label='Título de la Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),required=False,min_length=1, max_length=240)

    
    class Meta:
        model=Maestrante
        fields=("tema_perfil_postulado","tema_tesis_perfil","tema_borrador_tesis","tema_tesis","titulo_de_tesis")






class FormularioTribunalPerfil(forms.ModelForm):
     
    
    class Meta:
        model = TribunalPerfil
        fields = ('tribunal_perfil_1','tribunal_perfil_2')
     
        widgets={
            'tribunal_perfil_1': forms.Select(attrs={'class':'form-control','required':'required'}),
            'tribunal_perfil_2': forms.Select(attrs={'class':'form-control','required':'required'}),            
            
        }       
        labels = {
            'tribunal_perfil_1': ('TRIBUNAL 1 :'),
            'tribunal_perfil_2': ('TRIBUNAL 2 :'),
            
        }       
   
class FormularioTribunalTesis(forms.ModelForm):
     
    
    class Meta:
        model = TribunalTesis
        fields = ('tribunal_tesis_1','tribunal_tesis_2')
     
        widgets={
            'tribunal_tesis_1': forms.Select(attrs={'class':'form-control','required':'required'}),
            'tribunal_tesis_2': forms.Select(attrs={'class':'form-control','required':'required'}),            
            
        }       
        labels = {
            'tribunal_tesis_1': ('Tribunal interno 1 designado (Presidente de Tribunal)'),
            'tribunal_tesis_2': ('Tribunal interno 2 designado (Docente de Área - Revisor)'),
            
        }       
   
class FormularioFechaSustentacion(forms.ModelForm):
    fecha_3 = forms.DateField(label='Fecha del acto de sustentación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=True)
    hora_sustentacion = forms.TimeField(label='Hora del acto de sustentación', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  '}), required=True)
    class Meta:
        model = Cronograma
        fields = ('fecha_3','hora_sustentacion')
     
class FormularioFechaSustentacionTesis(forms.ModelForm):
    fecha_sustentacion = forms.DateField(label='Fecha del acto de sustentación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=True)
    hora_sustentacion = forms.TimeField(label='Hora del acto de sustentación', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  '}), required=True)
    class Meta:
        model = Cronograma2
        fields = ('fecha_sustentacion','hora_sustentacion')   

class FormularioCronograma(forms.ModelForm):
    #fecha_1 = forms.DateField(label='Fecha de entrega de formulario de habilitación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=True)
    fecha_1 = forms.DateField(label='Fecha límite de presentación del formulario de habilitación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_2 = forms.DateField(label='Fecha límite de presentación del perfil de Tesis', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_3 = forms.DateField(label='Fecha de sustentación del tema de Tesis', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    hora_sustentacion = forms.TimeField(label='Hora de sustentación del tema de Tesis', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  datetimepicker'}), required=False)
    fecha_4 = forms.DateField(label='Fecha límite de presentación del Perfil de Tesis Mejorado', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)

    class Meta:
        model = Cronograma
        fields = ('fecha_1','fecha_2','fecha_3','hora_sustentacion','fecha_4')
class FormularioCronograma2(forms.ModelForm):

    fecha_avance1 = forms.DateField(label='Primer avance', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_avance2 = forms.DateField(label='Segundo avance', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_borrador = forms.DateField(label='Presentación de borrador', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_borrador_prorroga = forms.DateField(label='Presentación de borrador prorroga', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)

    fecha_recepcion_borrador = forms.DateField(label='Recepción del Borrador', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_formulario_revisor = forms.DateField(label='Formulario del docente Revisor', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_formulario_guia = forms.DateField(label='Formulario del docente Gúia', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_tesis_habilitada = forms.DateField(label='Tesis habilitada', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_reporte_general = forms.DateField(label='Reporte General', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_reporte_general2 = forms.DateField(label='Segundo Reporte General', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_sustentacion = forms.DateField(label='Sustentación de Tesis', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    hora_sustentacion = forms.TimeField(label='Hora de sustentación de Tesis', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  datetimepicker'}), required=False)
    
    fecha_tesis_mejorada = forms.DateField(label='Tesis mejorada', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_reporte_general_tribunal_interno = forms.DateField(label='Reporte General Tribunal Intermo', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
        

    class Meta:
        model = Cronograma
        fields = ('fecha_avance1','fecha_avance2','fecha_borrador','fecha_borrador_prorroga','fecha_recepcion_borrador','fecha_formulario_revisor','fecha_formulario_guia','fecha_tesis_habilitada','fecha_reporte_general','fecha_reporte_general2','fecha_sustentacion','hora_sustentacion','fecha_tesis_mejorada','fecha_reporte_general_tribunal_interno')

class FormularioEvidencia(forms.ModelForm):
    nro_requisito = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),disabled=True,required=False,min_value=-1, label="Código de actividad")
    actividad = forms.CharField(label='Actividad',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),required=True,min_length=1, max_length=600)
    requisito = forms.CharField(label='Requisito',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),required=True,min_length=1, max_length=600)
    tiempo = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False, max_value=1000, label="Días (ingresar el número de días)")
    
    class Meta:
        model = Requisitos
        fields = ('nro_requisito','actividad','requisito','tiempo')

class FormularioBancoNotificacion(forms.ModelForm):
    numero_notificacion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),disabled=True,required=False,min_value=-1)
    enviar = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "form-control"}), label="Activar o desactivar ésta notificación a los usuarios", required=False)
    titulo = forms.CharField(
        label='Título de la notificación', 
        widget=forms.Textarea(attrs={"class": "form-control no-uppercase", "rows": 2}), 
        max_length=300
    )
    contenido = forms.CharField(
        label='Contenido de la notificación', 
        widget=forms.Textarea(attrs={"class": "form-control no-uppercase", "rows": 4}), 
        max_length=300
    )
    descripcion = forms.CharField(
        label='Descripcion de la notificación', 
        widget=forms.Textarea(attrs={"class": "form-control no-uppercase", "rows": 4}), 
        required=False, 
        max_length=300
    )   
  
    class Meta:
        model = BancoNotificacion
        fields = ('numero_notificacion','titulo','contenido','descripcion','enviar')


class FormularioAvance(forms.ModelForm):
    cap1 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap2 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap3 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)

    cap1_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)
    cap2_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)
    cap3_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)

    aceptar_avance = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    aprobacion = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('si', 'Doy mi aprobación para programar segundo avance (solo en caso de contar con un primer avance satisfactorio)'), ('no', 'No doy aprobación para programar segundo avance (falta consolidar el primer avance)')],required=True
    )
    class Meta:
        model = Avance
        fields = ('cap1','cap2','cap3','cap1_cualitativo','cap2_cualitativo','cap3_cualitativo','aceptar_avance','aprobacion')


class FormularioAvance2(forms.ModelForm):
    cap4 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap5 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap6 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap7 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)

    cap4_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)
    cap5_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)
    cap6_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)
    cap7_cualitativo = forms.CharField(label='Observaciones relevantes por capítulo',widget=forms.Textarea(attrs={"class":"form-control no-uppercase","type":"search",'rows': '4', 'cols': '20'}), max_length=800,required=False)


    
    aceptar_avance = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    aprobacion = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('si', 'Doy mi aprobación del segundo avance (solo en caso de contar con un segundo avance satisfactorio)'), ('no', 'No doy aprobación del segundo avance (falta consolidar el segundo avance)')],required=True
    )
    class Meta:
        model = Avance_2
        fields = ('cap4','cap5','cap6','cap7','cap4_cualitativo','cap5_cualitativo','cap6_cualitativo','cap7_cualitativo','aceptar_avance','aprobacion')
               
class FormularioDocenteGuia(forms.ModelForm):
        avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
        class Meta:
            model = Maestrante
            fields = ('guia',"avance_tesis")
            widgets={
                'guia': forms.Select(attrs={'class':'form-control','required':'required'}),
                
                
            }       
            labels = {
                'guia': ('Seleccionar docente guía:'),
                
                
            }  

class FormularioArchivoEvidencia(forms.ModelForm):
        archivo_documento = forms.FileField(required=True)

        class Meta:
            model = CentroActividades
            fields = ('archivo_documento',)
  
class FormularioDocenteRevisor(forms.ModelForm):
      
        class Meta:
            model = Maestrante
            fields = ('revisor',)
            widgets={
                'revisor': forms.Select(attrs={'class':'form-control','required':'required'}),
              
            }     
            labels = {
                'revisor': ('DOCENTE REVISOR:'),
                
                
            }  

class FormularioDocenteRevisorCompartido(forms.ModelForm):
        avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
        fecha_nombramiento = forms.DateField(label='Fecha de notificación del nombramiento y entrega de borrador:', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=True)
        nombramiento_revisor = forms.FileField(required=True, widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}))

        class Meta:
            model = Maestrante
            fields = ('avance_tesis','nombramiento_revisor','fecha_nombramiento')

class FormularioHistorialArchivosPerfil(forms.ModelForm):
    
        class Meta:
            model =SustentacionPerfilHistorial
            fields = ('acta','hoja_evaluacion','carta_externa','carta_externa_designacion','documento_respaldo')

class FormularioHistorialArchivosTesis(forms.ModelForm):
    
        class Meta:
            model =SustentacionTesisHistorial
            fields = ('acta','hoja_evaluacion','designacion')


 


#        def __init__(self, *args, **kwargs):
#            super().__init__(*args, **kwargs)
#            self.fields['fecha_sustentacion'].widget.format = '%d/%m/%Y %H:%M'
#widgets = {
#            
#            'fecha_sustentacion': DateTimeInput(attrs={'class': 'form-control'}),
#            
#        }


