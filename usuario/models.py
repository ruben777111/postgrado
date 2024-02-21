
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.signals import post_save,pre_save
from django.shortcuts import get_object_or_404
from django.core.validators import FileExtensionValidator
import uuid
# signals
from notify.signals import notificar
#Utils
from django.utils import timezone

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
ext_validator=FileExtensionValidator(['pdf'])         
usuario_tipo=[
    
    (1,'Maestrante'),
    (2,'Docente'),    
    (3,'Tecnico de Postgrado/Coordinación de investigación'),
    
    (5,'Coordinación de Postgrado'),
    
 
]
departamentos=(
    
    ('La Paz','La Paz'),
    ('Cochabamba','Cochabamba'),
    ('Santa Cruz','Santa Cruz'),
    ('Potosi','Potosi'),
    ('Oruro','Oruro'),
    ('Chuquisaca','Chuquisaca'),
    ('Pando','Pando'),
    ('Beni','Beni'),
    ('Tarija','Tarija')
)
sede=(
    
    ('La Paz','La Paz'),
    ('Cochabamba','Cochabamba'),
    ('Santa Cruz','Santa Cruz'),
    ('Potosi','Potosi'),
    ('Oruro','Oruro'),
    ('Chuquisaca','Chuquisaca'),
    ('Pando','Pando'),
    ('Beni','Beni'),
    ('Tarija','Tarija')
)

class Programa(models.Model):
    id_programa = models.AutoField(primary_key = True)             	
    nombre_programa = models.TextField('Programa ',max_length=200,blank=True,null=True)
    version = models.TextField('Versión programa ',max_length=200,blank=True,null=True)
    class Meta:
        verbose_name='Programa'
        verbose_name_plural='Programas'

    def __str__(self):
        return "%s "% (self.nombre_programa)



class UsuarioManager(BaseUserManager):
    def create_user(self, username, nombre_usuario, password=None, **extra_fields):
        user = self.model(
            username=username,
            nombre_usuario=nombre_usuario,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, nombre_usuario, password=None, correo_inst=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, nombre_usuario, password, correo_inst=correo_inst, **extra_fields)
class Usuario(AbstractBaseUser):
    
    username = models.CharField('Usuario', unique=True,max_length=100)
    ci_usuario = models.BigIntegerField( blank = False, null = True)
    departamento = models.CharField('Departamento',max_length=200,blank=True,null=True,choices=departamentos)
    nombre_usuario = models.CharField('Nombre',max_length=200,blank=True,null=True)    
    paterno = models.CharField('Apellido Paterno',max_length=200,blank=True,null=True)
    materno = models.CharField('Apellido Materno',max_length=200,blank=True,null=True)    
    cel_usuario = models.IntegerField( blank = False, null = True)
    cel_usuario2 = models.IntegerField( blank = False, null = True)
    correo = models.CharField('Correo personal',max_length=240,blank=True,null=True)
    correo_inst = models.CharField('Correo institucional',max_length=240,blank=True,null=True)    
    notificacion = models.BooleanField(default = False)
    usuario_administrador = models.BooleanField(default = False)
    fecha_registro = models.DateField('Fecha de registro', auto_now = False, auto_now_add = True)       
    cambio_password = models.BooleanField(default = False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default = True)
    tipo_usuario = models.IntegerField(blank = True, null = True,choices=usuario_tipo)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'  # Utiliza 'username' o el campo que desees como identificador de inicio de sesión
    EMAIL_FIELD = 'correo_inst'  # Utiliza 'correo_inst' como el campo de dirección de correo electrónico
    REQUIRED_FIELDS = ['nombre_usuario', 'correo_inst']  # Ajusta esto según tus requerimientos

    def has_perm(self,perm,ob=None):
        return True
    def has_module_perms(self,app_label):
        return True
    def __str__(self):
        return "%s "% (self.nombre_usuario)+ "%s "% (self.paterno)+ "%s "% (self.materno)

class Docente(Usuario):
    id_docente = models.AutoField(primary_key=True)
    especialidad_docente = models.CharField(max_length=130, blank=True, null=True)
    docente_interno = models.BooleanField(default=False)
    docente_externo = models.BooleanField(default=False)
    docente_activo = models.BooleanField(default=True)
    mostrar_numero = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'


    def __str__(self):
        return "%s "% (self.nombre_usuario)+ "%s "% (self.paterno)+ "%s "% (self.materno)

class Docente_Revisor(models.Model):
    id_revisor = models.AutoField(primary_key = True)
    especialidad_docente = models.CharField(max_length = 220, blank = True, null = True)    
    user = models.OneToOneField(Usuario,on_delete=models.CASCADE,blank = True, null = True)
    docente_activo = models.BooleanField(default = True)
    class Meta:
        verbose_name='Docente Revisor'
        verbose_name_plural='Docentes Revisores'

    def __str__(self):
        return "%s "% (self.user.nombre_usuario)+ "%s "% (self.user.paterno)+ "%s "% (self.user.materno)

class DocenteProvisional(models.Model):
    id_provisional = models.AutoField(primary_key = True)    
    user = models.OneToOneField(Usuario,on_delete=models.CASCADE,blank = True, null = True)
    docente_activo = models.BooleanField(default = True)
    class Meta:
        verbose_name='Docente Provisional'
        verbose_name_plural='Docentes Provisionales'

    def __str__(self):
        return "%s "% (self.user.nombre_usuario)+ "%s "% (self.user.paterno)+ "%s "% (self.user.materno)


class Maestrante(Usuario):
    id_maestrante = models.AutoField(primary_key = True)    
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE,blank = True, null = True)
    ru = models.IntegerField( blank = False, null = True)
    sede = models.CharField('Sede',max_length=100,blank=True,null=True,choices=sede)
    gestion = models.IntegerField( blank = False, null = True)
    
    perfil_tesis = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/borrador/', max_length=254,blank = True, null = True)     
    perfil_tesis_mejorado = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    borrador_tesis = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    tesis_mejorado = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    tesis_mejorado_aprobacion = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    tesis_optimizado = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    nombramiento_revisor = models.FileField(validators=[ext_validator],upload_to='tesis/nombramiento_revisor/', max_length=254,blank = True, null = True)     
    fecha_nombramiento = models.DateField(null=True, blank=True)
    guia = models.ForeignKey(Docente, on_delete=models.CASCADE,blank = True, null = True)
    provisional = models.ForeignKey(DocenteProvisional, on_delete=models.CASCADE,blank = True, null = True)
    revisor = models.ForeignKey(Docente_Revisor, on_delete=models.CASCADE,blank = True, null = True)
    tema_tesis_perfil = models.CharField('Tema de perfil de Tesis',max_length=200,blank=True,null=True)
    tema_tesis = models.CharField('Tema de Tesis',max_length=200,blank=True,null=True)
    instancia = models.IntegerField( default=1)
    instancia_defensa = models.IntegerField( default=1)
    procedencia_tema = models.BooleanField(null=True, blank=True)
    procedencia_tesis = models.BooleanField(default = False)
    listacomunicacion = models.BooleanField(default = False)
    tiempo = models.DateField(null=True, blank=True)
    avance_tesis = models.IntegerField( blank = False, null = True)
    dictamen_nota = models.IntegerField( blank = False, null = True)
    dictamen_escala  = models.CharField(max_length=200,blank=True,null=True)
    aprobacion_empaste = models.BooleanField(default = False)   
    tesis_recomendada = models.BooleanField(default = False)   
    observacion_empaste = models.TextField(max_length=1000,blank=True,null=True)
    codigo_empaste= models.TextField(max_length=100,blank=True,null=True)
    maestrante_activo = models.BooleanField(default = True)
    maestrante_habilitado = models.BooleanField(default = False)
    fecha_derivacion  = models.DateField(blank = True, null = True)  
    tesis_segunda_instancia = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    hoja_de_evaluacion = models.FileField(validators=[ext_validator],upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     

    recepcion_solicitud = models.DateField(blank = True, null = True) 
    solicitud_area_finaciera = models.DateField(blank = True, null = True) 
    observacion_pago = models.TextField(max_length=1000,blank=True,null=True)  
    observacion_segunda_instancia = models.TextField(max_length=1000,blank=True,null=True)
    tipo_m = [
        ('1', 'Programa regular'),
        ('2', 'Reincorporación'),
        ('3', 'Con vigencia de matricula'),
       
    ]  
    tipo_maestrante = models.CharField(max_length=20, choices=tipo_m)

    programa_regular  = models.BooleanField(default = False)    
    version = models.CharField('Versión',max_length = 220, blank = True, null = True) 

    reincorporacion = models.BooleanField(default = False)
    nueva_version = models.CharField('Nueva versión',max_length = 220, blank = True, null = True)    

    vigencia_matricula = models.BooleanField(default = False) 
    version_cursada = models.CharField('Versión cursada',max_length = 220, blank = True, null = True)    
    vigencia_inicio = models.DateField(null=True, blank=True)
    vigencia_final = models.DateField(null=True, blank=True)
    empaste_cd = models.BooleanField(default = False) 
    gestion_empastado = models.IntegerField( blank = False, null = True) 
    tesis_terminado = models.BooleanField(default = False) 
    articulos_revision = models.BooleanField(default = False) 
    articulos_original= models.BooleanField(default = False) 
    articulos_revision_original= models.BooleanField(default = False)

    class Meta:
        verbose_name='Maestrante'
        verbose_name_plural='Maestrantes'

    def __str__(self):
        return "%s "% (self.nombre_usuario)+ "%s "% (self.paterno)+ "%s "% (self.materno)

    def nombre_completo(self):
        return f"{self.nombre_usuario} {self.paterno} {self.materno} {self.programa}"




class SustentacionPerfil(models.Model):
    id_sustentacion = models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante, on_delete=models.CASCADE,blank = True, null = True)
    tema_perfil = models.TextField(max_length = 500, blank = True, null = True)
    fecha_sustentacion = models.DateField(null=True, blank=True)
    hora_sustentacion = models.TimeField(null=True, blank=True)
    docente_guia = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_perfil_1 = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_perfil_2 = models.TextField(max_length = 500, blank = True, null = True)
    resultado =  models.BooleanField(default = False)
    acta = models.FileField(validators=[ext_validator],upload_to='tesis/actas/', max_length=254,blank = True, null = True)     


    class Meta:
        verbose_name='Sustentacion de perfil'
        verbose_name_plural='Sustentacion de perfiles'

    def __str__(self):

        return "%s "% (self.user) 

class SustentacionPerfilHistorial(models.Model):
    id_sustentacion = models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante, on_delete=models.CASCADE,blank = True, null = True)
    tema_perfil = models.TextField(max_length = 500, blank = True, null = True)
    fecha_sustentacion = models.DateField(null=True, blank=True)
    hora_sustentacion = models.TimeField(null=True, blank=True)
    docente_guia = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_perfil_1 = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_perfil_2 = models.TextField(max_length = 500, blank = True, null = True)
    resultado =  models.BooleanField(default = False)
    instancia = models.IntegerField( blank = False, null = True)
    acta = models.FileField(validators=[ext_validator],upload_to='tesis/actas/', max_length=254,blank = True, null = True)     
    hoja_evaluacion = models.FileField(validators=[ext_validator],upload_to='tesis/hoja_evaluacion/', max_length=254,blank = True, null = True)     
    carta_externa = models.FileField(validators=[ext_validator],upload_to='tesis/carta_externa/', max_length=254,blank = True, null = True)     
    carta_externa_designacion = models.FileField(validators=[ext_validator],upload_to='tesis/carta_externa/', max_length=254,blank = True, null = True)     
    documento_respaldo = models.FileField(validators=[ext_validator],upload_to='tesis/documento_respaldo/', max_length=254,blank = True, null = True)     
    fecha_recibido_perfil = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name='Sustentacion de perfil historial'
        verbose_name_plural='Sustentacion de perfiles historial'

    def __str__(self):

        return "%s "% (self.user) 


class SustentacionTesisHistorial(models.Model):
    id_sustentacion = models.AutoField(primary_key = True)
    fecha = models.DateField(null=True, blank=True)
    user = models.ForeignKey(Maestrante, on_delete=models.CASCADE,blank = True, null = True)
    tema_tesis = models.TextField(max_length = 500, blank = True, null = True)
    fecha_sustentacion = models.DateField(null=True, blank=True)
    hora_sustentacion = models.TimeField(null=True, blank=True)
    docente_guia = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_1 = models.TextField(max_length = 500, blank = True, null = True)
    tribunal_2 = models.TextField(max_length = 500, blank = True, null = True)
    resultado =  models.BooleanField(default = False)
    dictamen_nota = models.IntegerField( blank = False, null = True)
    dictamen_escala  = models.CharField(max_length=200,blank=True,null=True)    
    acta = models.FileField(validators=[ext_validator],upload_to='tesis/actas/', max_length=254,blank = True, null = True)     
    hoja_evaluacion = models.FileField(validators=[ext_validator],upload_to='tesis/hoja_evaluacion/', max_length=254,blank = True, null = True)         
    designacion = models.FileField(validators=[ext_validator],upload_to='tesis/carta_externa/', max_length=254,blank = True, null = True)     

    class Meta:
        verbose_name='Sustentacion de tesis historial'
        verbose_name_plural='Sustentacion de tesis historial'

    def __str__(self):

        return "%s "% (self.user) 

    
class TribunalPerfil(models.Model):
    id_tribunal = models.AutoField(primary_key = True)        
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)    
    tribunal_perfil_1 = models.ForeignKey(Docente, on_delete=models.CASCADE,blank = True, null = True)
    tribunal_perfil_2 = models.ForeignKey(Docente_Revisor, on_delete=models.CASCADE,blank = True, null = True)
    tribunal_perfil_3 = models.CharField('Tribunal perfil 3',max_length=200,blank=True,null=True)    
    class Meta:
        verbose_name='Tribunal de perfil'
        verbose_name_plural='Tribunales de perfil'

    def __str__(self):
        return "%s "% (self.user)


class TribunalTesis(models.Model):
    id_tribunal = models.AutoField(primary_key = True)        
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)    
    tribunal_tesis_1 = models.ForeignKey(Docente, on_delete=models.CASCADE,blank = True, null = True)
    tribunal_tesis_2 = models.ForeignKey(Docente_Revisor, on_delete=models.CASCADE,blank = True, null = True)
    tribunal_tesis_3 = models.CharField('Tribunal Tesis 3',max_length=200,blank=True,null=True)    
    class Meta:
        verbose_name='Tribunal de tesis'
        verbose_name_plural='Tribunales de tesis'

    def __str__(self):
        return "%s "% (self.user)


class BancoNotificacion(models.Model):
    id_notificacion = models.AutoField(primary_key = True) 
    numero_notificacion = models.IntegerField( blank = False, null = True) 
    titulo = models.CharField(max_length=400,blank=True,null=True)
    contenido = models.CharField(max_length=400,blank=True,null=True)
    descripcion = models.CharField(max_length=400,blank=True,null=True)
    class Meta:
        verbose_name='Banco de notificacion'
        verbose_name_plural='Banco de notificaciones'

    def __str__(self):
       return "%s "% (self.numero_notificacion)+ "%s "% (self.titulo)
class Requisitos(models.Model):
    id_requisito = models.AutoField(primary_key = True)             	
    nro_requisito = models.IntegerField( blank = False, null = True) 
    actividad = models.TextField('Actividad ',max_length=1000,blank=True,null=True)
    requisito = models.TextField('Evidencia ',max_length=1000,blank=True,null=True)
    tiempo = models.IntegerField('Dias ', blank = False, null = True)
    rol1 =  models.BooleanField('Tecnico de Postgrado ',default = False)
    rol2 =  models.BooleanField('Coordinación de investigación ',default = False)
    rol3 =  models.BooleanField('Coordinación de Postgrado ',default = False)
    requisito_habilitado =  models.BooleanField(default = False)   
    
    class Meta:
        verbose_name='Requisito'
        verbose_name_plural='Requisitos'

    def __str__(self):
       return "%s "% (self.nro_requisito)


class Requisitos1(models.Model):
    id_requisito = models.AutoField(primary_key = True)             	
    requisito = models.TextField('Evidencia ',max_length=1000,blank=True,null=True)



class Administracion(models.Model):
    id_administracion = models.AutoField(primary_key = True)    
    user = models.OneToOneField(Usuario,on_delete=models.CASCADE,blank = True, null = True)
    
    class Meta:
        verbose_name='Administrador'
        verbose_name_plural='Administradores'

    def __str__(self):
       return "%s "% (self.user.nombre_usuario)+ "%s "% (self.user.paterno)+ "%s "% (self.user.materno)





class ActividadesMaestrante(models.Model):
    id_actividad = models.AutoField(primary_key = True)    
    idmaestrante = models.IntegerField( blank = False, null = True)
    descripcion = models.CharField(max_length = 220, blank = True, null = True)    
    archivo_documento = models.FileField(upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    fecha_publicacion = models.DateField('Fecha de publicación', auto_now = False, auto_now_add = True)       

           
    class Meta:
        verbose_name='Actividad'
        verbose_name_plural='Actividades'

    def __str__(self):

        return "%s "% (self.idmaestrante) 

 
class CentroActividades(models.Model):
    maestrante = models.ForeignKey(Maestrante, on_delete=models.CASCADE, blank=True, null=True, related_name='actividades_maestrante')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, blank=True, null=True)
    numero_actividad = models.IntegerField(blank = True, null = True)
    id_actividad = models.AutoField(primary_key = True)  
    observacion = models.TextField(max_length=1000,blank=True,null=True)
    fecha_programada = models.DateField(null=True, blank=True)
    fecha = models.DateField('Fecha de registro', auto_now = False, auto_now_add = True)       
    evidencia = models.TextField(max_length = 220, blank = True, null = True)
    archivo_documento = models.FileField(upload_to='tesis/actividades/', max_length=254,blank = True, null = True)     
    class Meta:
        verbose_name='Centro actividad'
        verbose_name_plural='Centro actividades'

    def __str__(self):

        return "%s "% (self.maestrante) 

class Cronograma(models.Model):
    id_cronograma = models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    fecha_induccion  = models.DateField(blank = True, null = True)    
    hora_induccion = models.TimeField(null=True, blank=True)
    reunion_realizada = models.BooleanField(default = False)
    fecha_1  = models.DateField(blank = True, null = True)    
    fecha_2  = models.DateField(blank = True, null = True)
    fecha_3  = models.DateField(blank = True, null = True)
    hora_sustentacion = models.TimeField(null=True, blank=True)
    fecha_4  = models.DateField(blank = True, null = True)
    

    class Meta:
        verbose_name='Cronograma1'
        verbose_name_plural='Cronogramas1'

    def __str__(self):

        return "%s "% (self.user)  
class Cronograma2(models.Model):
    id_cronograma = models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    fecha_avance1  = models.DateField(blank = True, null = True)    
    fecha_avance2  = models.DateField(blank = True, null = True)
    fecha_borrador  = models.DateField(blank = True, null = True)
    fecha_borrador_prorroga  = models.DateField(blank = True, null = True)    
    fecha_recepcion_borrador  = models.DateField(blank = True, null = True)
    
    borrador_tesis  =  models.BooleanField('Borrador de tesis con aval de docente guia',default = False)
    fecha_formulario_revisor  = models.DateField(blank = True, null = True)    
    fecha_formulario_guia  = models.DateField(blank = True, null = True)    
    fecha_tesis_habilitada  = models.DateField(blank = True, null = True)
    fecha_reporte_general  = models.DateField(blank = True, null = True)
    fecha_reporte_general2  = models.DateField(blank = True, null = True)
    fecha_sustentacion  = models.DateField(blank = True, null = True)
    hora_sustentacion = models.TimeField(null=True, blank=True)
    fecha_tesis_mejorada  = models.DateField(blank = True, null = True)
    fecha_reporte_general_tribunal_interno  = models.DateField(blank = True, null = True)
    class Meta:
        verbose_name='Cronograma2'
        verbose_name_plural='Cronogramas2'

    def __str__(self):

        return "%s "% (self.user) 

class ReporteGeneral(models.Model):
    id_reportegeneral =  models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    fecha_registro = models.DateField(auto_now = True, auto_now_add = False)     
    reporte = models.TextField('Reporte ',max_length=1000,blank=True,null=True)

    aceptar_revisor = models.BooleanField(default = False)
 
    OPCIONES = [
        ('si', 'Aprobado'),
        ('no', 'No aprobado'),
       
    ]
    aprobacion = models.CharField(max_length=20, choices=OPCIONES)
    activar_reporte2 = models.BooleanField(default = False)

    fecha_registro2 = models.DateTimeField(auto_now=True)
    reporte2 = models.TextField('Reporte ',max_length=1000,blank=True,null=True)

    aceptar_revisor2 = models.BooleanField(default = False)

    fecha_registro2 = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        # Actualiza la fecha de modificación antes de guardar el registro
        self.fecha_registro2 = timezone.now()
        super().save(*args, **kwargs)


    class Meta:
        verbose_name='Reporte General'
        verbose_name_plural='Reportes Generales'

    def __str__(self):

        return "%s "% (self.user) 

class ReporteGeneralTribunalInterno(models.Model):
    id_reportegeneral =  models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    fecha_registro = models.DateField(auto_now = True, auto_now_add = False)       
    reporte = models.TextField('Reporte 2',max_length=1000,blank=True,null=True)
    aceptar_revisor = models.BooleanField(default = False)



    class Meta:
        verbose_name='Reporte General Tribunal Interno'
        verbose_name_plural='Reporte General Tribunal Interno'

    def __str__(self):

        return "%s "% (self.user) 


class Informe(models.Model):
    id_informe =  models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    otras_obs = models.TextField(max_length=1000,blank=True,null=True)
    fecha_registro  = models.DateField(blank = True, null = True)      
    aceptar_revisor = models.BooleanField(default = False)
    class Meta:
        verbose_name='Informe reviso'
        verbose_name_plural='Informes revisores'

    def __str__(self):

        return "%s "% (self.user) 
class InformeGuia(models.Model):
    id_informe =  models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    otras_obs = models.TextField(max_length=1000,blank=True,null=True)
    fecha_registro  = models.DateField(blank = True, null = True)      
    aceptar_guia = models.BooleanField(default = False)
    class Meta:
        verbose_name='Informe guia'
        verbose_name_plural='Informes guias'

    def __str__(self):

        return "%s "% (self.user) 
class InformeRevisor(models.Model):
    id_informe_revisor =  models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    capitulo = models.TextField(max_length=500,blank=True,null=True)    
    descripcion = models.TextField(max_length=500,blank=True,null=True)    
    sugerencia = models.TextField(max_length=500,blank=True,null=True)
    

    class Meta:
        verbose_name='Informe revisor formulario'
        verbose_name_plural='Informes revisores formularios'

    def __str__(self):

        return "%s "% (self.user) 


class InformeGuiaFormulario(models.Model):
    id_informe_guia =  models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    
    capitulo = models.TextField(max_length=500,blank=True,null=True)    
    obs = models.TextField(max_length=500,blank=True,null=True)
    opcion= models.TextField(max_length=10,blank=True,null=True)
    pagina = models.TextField(max_length=300,blank=True,null=True)
    fundamentacion = models.TextField(max_length=500,blank=True,null=True)
    

    class Meta:
        verbose_name='Informe guia formulario'
        verbose_name_plural='Informes guias formularios'

    def __str__(self):

        return "%s "% (self.user) 
class AsistenciaInduccion(models.Model):
    id_asistencia = models.AutoField(primary_key = True)
    maestrante = models.ForeignKey(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    fecha_asesoramiento = models.DateField(null=True, blank=True)
    hora_asesoramiento = models.TimeField(null=True, blank=True)
    fecha_realizada = models.DateField(null=True, blank=True) 
    hora_realizada = models.TimeField(null=True, blank=True)
    enlace_reunion = models.URLField(null=True, blank=True,max_length=1000)
    obs  = models.TextField('Observaciones',max_length=700,blank=True,null=True)
    hoja_reunion = models.FileField(validators=[ext_validator],upload_to='tesis/', max_length=254,blank = True, null = True)         
    class Meta:
        verbose_name='Registro de asistencia'
        verbose_name_plural='Registros de asistencias'

    def __str__(self):
        return "%s "% (self.maestrante)
class Avance(models.Model):
    id_avance = models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    cap1 = models.IntegerField( 'Capitulo I', blank = True, null = True)
    cap2 = models.IntegerField( 'Capitulo II', blank = True, null = True)
    cap3 = models.IntegerField( 'Capitulo III', blank = True, null = True)

    cap1_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap2_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap3_cualitativo = models.TextField(max_length=1000,blank=True,null=True)

    OPCIONES = [
        ('si', 'Aprobado'),
        ('no', 'No aprobado'),
       
    ]
    aprobacion = models.CharField(max_length=20, choices=OPCIONES)
    fecha_registro = models.DateField('Fecha de registro', auto_now = True, auto_now_add = False)       
    aceptar_avance = models.BooleanField(default = False)
   
 

    class Meta:
        verbose_name='Avance 1 '
        verbose_name_plural='Avances 1'

    def __str__(self):
        return "%s "% (self.user)


class AvanceHistorial(models.Model):
    id_avance = models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    cap1 = models.IntegerField( 'Capitulo I', blank = True, null = True)
    cap2 = models.IntegerField( 'Capitulo II', blank = True, null = True)
    cap3 = models.IntegerField( 'Capitulo III', blank = True, null = True)

    cap1_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap2_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap3_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    OPCIONES = [
        ('si', 'Aprobado'),
        ('no', 'No aprobado'),
       
    ]
    aprobacion = models.CharField(max_length=20, choices=OPCIONES)
    fecha_registro = models.DateField('Fecha de registro', auto_now = True, auto_now_add = False)       
    fecha_programada =  models.DateField(null=True, blank=True)      
    aceptar_avance = models.BooleanField(default = False)
    docete_guia = models.TextField(max_length=300,blank=True,null=True)
 

    class Meta:
        verbose_name='Avance 1 historial'
        verbose_name_plural='Avances 1 historial'

    def __str__(self):
        return "%s "% (self.user)
    
class Avance_2(models.Model):
    id_avance = models.AutoField(primary_key = True)
    user = models.OneToOneField(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    cap4 = models.IntegerField( 'Capitulo IV', blank = True, null = True)
    cap5 = models.IntegerField( 'Capitulo V', blank = True, null = True)
    cap6 = models.IntegerField( 'Capitulo VI', blank = True, null = True)
    cap7 = models.IntegerField( 'REFERENCIAS', blank = True, null = True)

    cap4_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap5_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap6_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap7_cualitativo = models.TextField(max_length=1000,blank=True,null=True)

    fecha = models.DateField('Fecha de registro',  auto_now = False, auto_now_add = True) 
    aceptar_avance = models.BooleanField(default = False)
  
    OPCIONES = [
        ('si', 'Aprobado'),
        ('no', 'No aprobado'),
       
    ]
    aprobacion = models.CharField(max_length=20, choices=OPCIONES)

    class Meta:
        verbose_name='Avance 2'
        verbose_name_plural='Avances 2'

    def __str__(self):
        return "%s "% (self.user)
class Avance_2_Histoiral(models.Model):
    id_avance = models.AutoField(primary_key = True)
    user = models.ForeignKey(Maestrante,on_delete=models.CASCADE,blank = True, null = True)
    cap4 = models.IntegerField( 'Capitulo IV', blank = True, null = True)
    cap5 = models.IntegerField( 'Capitulo V', blank = True, null = True)
    cap6 = models.IntegerField( 'Capitulo VI', blank = True, null = True)
    cap7 = models.IntegerField( 'REFERENCIAS', blank = True, null = True)

    cap4_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap5_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap6_cualitativo = models.TextField(max_length=1000,blank=True,null=True)
    cap7_cualitativo = models.TextField(max_length=1000,blank=True,null=True)

    fecha = models.DateField('Fecha de registro',  auto_now = False, auto_now_add = True) 
    aceptar_avance = models.BooleanField(default = False)
    fecha_programada =  models.DateField(null=True, blank=True)      
    
    docete_guia = models.TextField(max_length=300,blank=True,null=True)
 

    OPCIONES = [
        ('si', 'Aprobado'),
        ('no', 'No aprobado'),
       
    ]
    aprobacion = models.CharField(max_length=20, choices=OPCIONES)

    class Meta:
        verbose_name='Avance 2 historial'
        verbose_name_plural='Avances 2 historial'

    def __str__(self):
        return "%s "% (self.id_avance)
class Post(models.Model):
	user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
	title = models.CharField(max_length=400)
	tipo_noti = models.IntegerField( blank = False, null = True)
	text = models.TextField()    
	timestamp = models.DateTimeField(default=timezone.now, db_index=True)

	def __str__(self):
		return self.title


def notify_post(sender, instance, created, **kwargs):
  
	notificar.send(instance.user, destiny=instance.user,  verb=instance.title, level='success',tipo_notificacion=instance.tipo_noti,text=instance.text)

post_save.connect(notify_post, sender=Post)








