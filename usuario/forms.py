from django import forms
from .models import BancoNotificacion,Programa,ReporteGeneralTribunalInterno,Avance_2,DocenteProvisional,TribunalPerfil,TribunalTesis,Avance,Requisitos,Usuario,Maestrante,Docente,Cronograma,Cronograma2,ReporteGeneral,Docente_Revisor


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
        print(username)
        print(correo_inst)
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
class FormularioAdministradores(forms.ModelForm):     
    
    ci_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Numero de cedula de identidad"}),required=True,min_value=1, max_value=100000000000000, label="C.I. :")    
    nombre_usuario = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nombre"}),min_length=3, max_length=120, label="NOMBRE :")
    paterno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido paterno"}),min_length=3, max_length=120, label="APELLIDO PATERNO :")
    materno = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Apellido materno"}),min_length=3, max_length=120, label="APELLIDO MATERNO :")    
    cel_usuario= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Numero de celular"}),required=True,min_value=1, max_value=2147483646, label="Nº CEL :")
    cel_usuario2= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Numero de celular de referencia"}),required=True,min_value=1, max_value=2147483646, label="Nº CEL REFERENCIA :") 
    departamento= forms.Select(attrs={'class':'form-control','required':'required'})

    class Meta:
        model=Usuario
        fields=('nombre_usuario','paterno','materno','ci_usuario','departamento','cel_usuario','cel_usuario2','correo','correo_inst','tipo_usuario')
        widgets={
            'departamento': forms.Select(attrs={'class':'form-control','required':'required'}),
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
            'correo': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo personal','required':'required'}),
            'correo_inst': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo electronico institucional','required':'required'}),
            
        }       
        labels = {
            'departamento': ('DEPARTAMENTO :'),
            'correo': ('CORREO PERSONAL :'),
            'correo_inst': ('CORREO INSTITUCIONAL  :'),
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

class FormularioUsuarioMaestrante(FormularioAdministradores):
    tipo_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"value":"1","type":"hidden"}),required=True)

    version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión del programa","id":"tipo1","hidden":"true"}),min_length=1, max_length=120, label="VERSIÓN DEL PROGRAMA :",required=False) 
    nueva_version = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Nueva versión del programa","id":"tipo2","hidden":"true"}),min_length=1, max_length=120, label="NUEVA VERSIÓN DEL PROGRAMA :",required=False) 
    version_cursada = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Versión cursada del programa","id":"tipo3","hidden":"true"}),min_length=1, max_length=120, label="VERSIÓN CURSADA DEL PROGRAMA :",required=False) 
    vigencia_inicio = forms.DateField(label='Fecha desde', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker',"id":"vigencia_inicio","hidden":"true"}), required=False)
    vigencia_final = forms.DateField(label='Fecha hasta', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker',"id":"vigencia_final","hidden":"true"}), required=False)
    gestion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Gestión"}),required=True,min_value=1, max_value=999999999999, label="GESTIÓN :")    
    ru = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Registro unico universitario"}),required=True,min_value=1, max_value=999999999999, label="R.U. :")
    programa_regular = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'op1',"hidden":"true"}),required=False) 
    reincorporacion = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'op2',"hidden":"true"}),required=False) 
    vigencia_matricula = forms.BooleanField(widget=forms.CheckboxInput(attrs={'id': 'op3',"hidden":"true"}),required=False) 
 
    class Meta:
        model=Maestrante
        fields=('nombre_usuario','paterno','materno','ci_usuario','departamento','cel_usuario','cel_usuario2','correo','correo_inst','tipo_usuario','ru','sede','programa','version','nueva_version','version_cursada','vigencia_inicio','vigencia_final','gestion','programa_regular','reincorporacion','vigencia_matricula')
        widgets={
            'programa': forms.Select(attrs={'class':'form-control','placeholder':'Seleccione departamento','required':'required',}),
            'sede': forms.Select(attrs={'class':'form-control','required':'required'}),
            'departamento': forms.Select(attrs={'class':'form-control','required':'required'}),
            'correo': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo personal','required':'required'}),
            'correo_inst': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo electronico institucional','required':'required'}),
            

        } 
        labels = {
            'programa': ('PROGRAMA :'),
            'sede': ('SEDE :'),
            'programa_regular': ('PROGRAMA REGULAR EN CURSO :'),
            'reincorporacion': ('REINCORPORACIÓN A NUEVA VERSIÓN DE PROGRAMA :'),
            'vigencia_matricula': ('REINCORPORACIÓN CON VIGENCIA DE MATRICULA :'),
            'departamento': ('DEPARTAMENTO :'),
            'correo': ('CORREO PERSONAL :'),
            'correo_inst': ('CORREO INSTITUCIONAL  :'),
        }
        placeholder = {
            'programa': ('Seleccione programa')
        }
 

  


class FormularioUsuarioDocente(FormularioAdministradores):
    tipo_usuario = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden","value":"2"}),required=True)
    especialidad_docente = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Especialidad del docente"}),min_length=1, max_length=120, label="ESPECIALIDAD DEL DOCENTE :") 
    docente_interno = forms.BooleanField(  widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}),required=False)
    docente_externo = forms.BooleanField(  widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}),required=False)
    class Meta:
        model=Docente
        fields=('nombre_usuario','paterno','materno','ci_usuario','departamento','cel_usuario','cel_usuario2','correo','correo_inst','tipo_usuario','especialidad_docente','docente_interno','docente_externo')
        widgets={
            'departamento': forms.Select(attrs={'class':'form-control','required':'required'}),
            'tipo_usuario': forms.Select(attrs={'class':'form-control'}),
            'correo': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo personal','required':'required'}),
            'correo_inst': forms.EmailInput(attrs={'class':'form-control no-uppercase','placeholder':'Correo electronico institucional','required':'required'}),
            
        }       
        labels = {
            'departamento': ('DEPARTAMENTO :'),
            'correo': ('CORREO PERSONAL :'),
            'correo_inst': ('CORREO INSTITUCIONAL  :'),
            'ci_usuario': ('CEDULA DE IDENTIDAD  :'),
            'docente_interno': ('DOCENTE INTERNO  :'),
            'docente_interno': ('DOCENTE EXTERNO  :'),

        }
    def clean_especialidad_docente(self):
        especialidad_docente = self.cleaned_data['especialidad_docente']
        if especialidad_docente:
            return especialidad_docente.upper()
        return especialidad_docente       




class FormularioDocenteProvisional(forms.ModelForm):
    provisional=forms.ModelChoiceField(widget=forms.Select(attrs={"class":"form-control"}),queryset= DocenteProvisional.objects.filter(docente_activo=True), label="DOCENTE PROVISIONAL :")
    avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
  
    class Meta:
        model=Maestrante
        fields=("provisional","avance_tesis")

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

class FormularioReporteGeneralTribunalInterno(forms.ModelForm):
    reporte = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"8"}),min_length=3, max_length=1000,required=True)
    aceptar_revisor = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    class Meta:
        model=ReporteGeneralTribunalInterno
        fields=('reporte','aceptar_revisor')

class FormularioMaestranteGuia(forms.ModelForm):
    provisional=forms.ModelChoiceField(widget=forms.Select(attrs={"class":"form-control"}),queryset= DocenteProvisional.objects.filter(docente_activo=True), label="DOCENTE PROVISIONAL :",required=False)
    guia=forms.ModelChoiceField(widget=forms.Select(attrs={"class":"form-control"}),queryset= Docente.objects.filter(docente_activo=True), label="DOCENTE GUíA :",required=False)
    revisor=forms.ModelChoiceField(widget=forms.Select(attrs={"class":"form-control"}),queryset= Docente_Revisor.objects.filter(docente_activo=True), label="DOCENTE REVISOR :",required=False)
    class Meta:
        model=Maestrante
        fields=("provisional","guia","revisor")
    
       

class FormularioTemaTesis(forms.ModelForm):
 
    tema_tesis = forms.CharField(label='Tema de  Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),min_length=10, max_length=240)
    tema_tesis_perfil = forms.CharField(label='Tema de perfil Tesis',widget=forms.TextInput(attrs={"class":"form-control","type":"search"}),min_length=10, max_length=240)

    
    class Meta:
        model=Maestrante
        fields=("tema_tesis_perfil","tema_tesis")




class FormularioPerfilTesis(forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("perfil_tesis",)
        widgets = {
            'perfil_tesis': forms.FileInput(
                attrs={'id':'tesis','name':'tesis','accept':'application/pdf'}
            )
            
                
        }        
class FormularioPerfilTesisMejorado(forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("perfil_tesis_mejorado",)

class FormularioBorradorTesis(forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("borrador_tesis",)

class FormularioTesisMejorado (forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("tesis_mejorado",)

class FormularioTesisMejoradoAprobacion (forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("tesis_mejorado_aprobacion",)

class FormularioTesisOptimizado (forms.ModelForm):
    

    class Meta:
        model=Maestrante
       
        fields=("tesis_optimizado",)


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
            'tribunal_tesis_2': ('Tribunal interno 2 designado (Docente de Area - Revisor)'),
            
        }       
   
class FormularioFechaSustentacion(forms.ModelForm):
    fecha_3 = forms.DateField(label='Fecha del acto de sustentación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    hora_sustentacion = forms.TimeField(label='Hora del acto de sustentación', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  '}), required=False)
    class Meta:
        model = Cronograma
        fields = ('fecha_3','hora_sustentacion')
     
class FormularioFechaSustentacionTesis(forms.ModelForm):
    fecha_sustentacion = forms.DateField(label='Fecha del acto de sustentación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    hora_sustentacion = forms.TimeField(label='Hora del acto de sustentación', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  '}), required=False)
    class Meta:
        model = Cronograma2
        fields = ('fecha_sustentacion','hora_sustentacion')   

class FormularioCronograma(forms.ModelForm):
    #fecha_1 = forms.DateField(label='Fecha de entrega de formulario de habilitación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=True)
    fecha_1 = forms.DateField(label='Fecha de entrega de formulario de habilitación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_2 = forms.DateField(label='Fecha de entrega de perfil de Tesis', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_3 = forms.DateField(label='Fecha de sustentación de tema de Tesis', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    hora_sustentacion = forms.TimeField(label='Hora de sustentación de tema de Tesis', widget=forms.TextInput(attrs={'type': 'time','class': 'form-control  datetimepicker'}), required=False)
    fecha_4 = forms.DateField(label='Desarrollo de la investigación', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)

    class Meta:
        model = Cronograma
        fields = ('fecha_1','fecha_2','fecha_3','hora_sustentacion','fecha_4')
class FormularioCronograma2(forms.ModelForm):
    
    fecha_avance1 = forms.DateField(label='Primer avance', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_avance2 = forms.DateField(label='Segundo avance', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_borrador = forms.DateField(label='Presentación de borrador', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
    fecha_borrador_prorroga = forms.DateField(label='Presentación de borrador prorroga', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)

    class Meta:
        model = Cronograma
        fields = ('fecha_avance1','fecha_avance2','fecha_borrador','fecha_borrador_prorroga')

class FormularioEvidencia(forms.ModelForm):
    nro_requisito = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=-1, max_value=100)
    actividad = forms.CharField(label='Actividad',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),min_length=10, max_length=240)
    requisito = forms.CharField(label='Requisito',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),min_length=10, max_length=240)
    tiempo = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=0, max_value=1000)
  
    class Meta:
        model = Requisitos
        fields = ('nro_requisito','actividad','requisito','tiempo','rol1','rol2','rol3')

class FormularioBancoNotificacion(forms.ModelForm):
    numero_notificacion = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=-1, max_value=100)
   
    titulo = forms.CharField(label='Titulo de la notificación',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),min_length=10, max_length=300)
    contenido = forms.CharField(label='Contenido de la notificación',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),min_length=10, max_length=300)
    descripcion = forms.CharField(label='Descripcion de la notificación',widget=forms.TextInput(attrs={"class":"form-control no-uppercase","type":"search"}),min_length=10, max_length=300)
    class Meta:
        model = BancoNotificacion
        fields = ('numero_notificacion','titulo','contenido','descripcion')


class FormularioAvance(forms.ModelForm):
    cap1 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap2 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap3 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap4 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap5 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    anexos = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    bibliografia = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    aceptar_avance = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    aprobacion = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('si', 'Doy mi aprobación para programar segundo avance (solo en caso de contar con un primer avance satisfactorio)'), ('no', 'No doy aprobación para programar segundo avance (falta consolidar el primer avance)')],required=True
    )
    class Meta:
        model = Avance
        fields = ('cap1','cap2','cap3','cap4','cap5','anexos','bibliografia','aceptar_avance','aprobacion')


class FormularioAvance2(forms.ModelForm):
    cap1 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap2 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap3 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap4 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    cap5 = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    anexos = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    bibliografia = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),required=False,min_value=1, max_value=100)
    aceptar_avance = forms.BooleanField( required = True, widget=forms.widgets.CheckboxInput( attrs={'class': 'checkbox-inline'}))
    aprobacion = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=[('si', 'Doy mi aprobación para programar segundo avance (solo en caso de contar con un primer avance satisfactorio)'), ('no', 'No doy aprobación para programar segundo avance (falta consolidar el primer avance)')],required=True
    )
    class Meta:
        model = Avance_2
        fields = ('cap1','cap2','cap3','cap4','cap5','anexos','bibliografia','aceptar_avance','aprobacion')
               
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
class FormularioDocenteRevisor(forms.ModelForm):
        avance_tesis = forms.IntegerField(widget=forms.NumberInput(attrs={"type":"hidden"}))
        fecha_nombramiento = forms.DateField(label='Fecha de notificación del nombramiento y entrega de borrador:', widget=forms.TextInput(attrs={'type': 'date','class': 'form-control  datetimepicker'}), required=False)
        class Meta:
            model = Maestrante
            fields = ('revisor','avance_tesis','nombramiento_revisor','fecha_nombramiento')
            widgets={
                'revisor': forms.Select(attrs={'class':'form-control','required':'required'}),
                'nombramiento_revisor': forms.FileInput( attrs={'class':'form-control','accept':'application/pdf'}   )
                
            }     
            labels = {
                'revisor': ('DOCENTE REVISOR:'),
                
                
            }  
#        def __init__(self, *args, **kwargs):
#            super().__init__(*args, **kwargs)
#            self.fields['fecha_sustentacion'].widget.format = '%d/%m/%Y %H:%M'
#widgets = {
#            
#            'fecha_sustentacion': DateTimeInput(attrs={'class': 'form-control'}),
#            
#        }


