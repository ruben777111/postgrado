from typing import Any, Dict, Optional
from django.contrib import messages
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.utils import timezone
from xhtml2pdf import pisa
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import time
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime

    
from .forms import FormularioHistorialArchivosTesis,FormularioHistorialArchivosPerfil,FormularioAdministradoresNuevo,FormularioAdministradoresEditar,FormularioArchivoEvidencia,FormularioMatricula,RegistroNuevoDocenteForm,RegistroNuevoMaestranteForm,RegistroDocenteForm,RegistroDocenteForm,RegistroMaestranteForm,FormularioAdministradores,FormularioUsuario,FormularioBancoNotificacion,FormularioPrograma,FormularioAvance2,FormularioTribunalTesis,FormularioTribunalPerfil,FormularioCronograma2,FormularioEvidencia,FormularioUsuarioDocente,FormularioUsuarioMaestranteComplemento,FormularioUsuarioMaestrante,FormularioUsuarioMaestranteDictamen,FormularioAvance,FormularioDocenteProvisional,FormularioTemaTesis,FormularioReporteGeneral2,FormularioReporteGeneral,FormularioCronograma,FormularioFechaSustentacion,FormularioAdministradores,FormularioMaestranteGuia
from usuario.models import ReporteGeneralTribunalInterno,DocenteProvisional,SustentacionTesisHistorial,BancoNotificacion,Programa,AvanceHistorial,Avance_2_Histoiral,Avance_2,Cronograma2,SustentacionPerfilHistorial,TribunalPerfil,TribunalTesis,InformeGuiaFormulario,InformeGuia,InformeRevisor,Post,Administracion,AsistenciaInduccion,Avance,Informe,ReporteGeneral,Requisitos,Cronograma,CentroActividades,Docente_Revisor,Docente,Usuario,Maestrante
from room.models import Room 
from django.views.generic import ListView,View,TemplateView,UpdateView, CreateView,DeleteView,DetailView
from django.urls import reverse_lazy

from datetime import date,datetime,timedelta

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth import get_user_model

import random
import string

from .forms import CustomPasswordResetForm

from django.conf import settings
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView

from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import JsonResponse
import requests

import time
import requests
from django.http import JsonResponse

def logout_view(request):

    return redirect("index.html")

def obtener_informacion(request, pk):
    # URL de donde obtener la información
    url = f'https://sias.usalesiana.edu.bo/usalesiana/alumnos/?dato={str(pk)}&sistema=1&tipo=CI'
  

    try:
        response = requests.get(url, timeout=10)  # Limitar el tiempo de espera a 10 segundos
    
        if response.status_code == 200:
            data = response.json()
            

            return JsonResponse(data, safe=False)
        else:
            
            return JsonResponse({'error': 'Error al obtener información del servidor externo'}, status=response.status_code)
    
    except requests.exceptions.RequestException as e:
      
        return JsonResponse({'error': 'Error de conexión con el servidor externo. Inténtalo de nuevo más tarde.'}, status=503)
    
    except Exception as e:
        # Manejo de otros errores
        
        return JsonResponse({'error': f'Error inesperado: {str(e)}'}, status=500)

@csrf_exempt
def obtener_usuario(request, usuario_id):
    try:
        usuario = Usuario.objects.get(ci_usuario=usuario_id)
        maestrantes = Maestrante.objects.filter(usuario=usuario)
        
        maestrantes_list = []  # Lista para almacenar los maestrantes
        
        for maestrante in maestrantes:
            programa_info = {
                "nombre": maestrante.programa.nombre_programa+" - "+maestrante.version,
                
             
            }
            maestrantes_list.append({                
                "programa": programa_info,               
            })
            print(maestrantes_list)
        data = {
        
            'ci_usuario': usuario.ci_usuario,
            'nombre_usuario': usuario.nombre_usuario,
            'paterno': usuario.paterno,
            'materno': usuario.materno,
            'ru': usuario.ru,
            'cel_usuario': usuario.cel_usuario,
        
            'correo_inst': usuario.correo_inst,
            'rol_maestrante': usuario.rol_maestrante,
            'rol_docente': usuario.rol_docente,
            'rol_postgrado': usuario.rol_postgrado,
            'rol_tecnico_investigacion': usuario.rol_tecnico_investigacion,

            'fecha_registro': usuario.fecha_registro.strftime("%d-%m-%Y"),
            'maestrantes': maestrantes_list,
            
           
        }
       
        return JsonResponse(data)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
@csrf_exempt
def obtener_usuario_docente(request, usuario_id):
    try:
        usuario = Usuario.objects.get(ci_usuario=usuario_id)
        
        # Buscar al usuario en el modelo Docente
        try:
            docente = Docente.objects.get(user=usuario)
            especialidad_docente = docente.especialidad_docente
        except Docente.DoesNotExist:
            especialidad_docente = None

        # Construir los datos de respuesta JSON
        data = {
            'ci_usuario': usuario.ci_usuario,
            'nombre_usuario': usuario.nombre_usuario,
            'paterno': usuario.paterno,
            'materno': usuario.materno,
            'cel_usuario': usuario.cel_usuario,
            'correo': usuario.correo,
            'correo_inst': usuario.correo_inst,
            'rol_maestrante': usuario.rol_maestrante,
            'rol_docente': usuario.rol_docente,
            'rol_postgrado': usuario.rol_postgrado,
            'rol_tecnico_investigacion': usuario.rol_tecnico_investigacion,

            'fecha_registro': usuario.fecha_registro.strftime("%d-%m-%Y"),
           
            'especialidad_docente': especialidad_docente,
        }
        return JsonResponse(data)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

@csrf_exempt
def obtener_usuario_administrador(request, usuario_id):
    try:
        usuario = Usuario.objects.get(ci_usuario=usuario_id)
        
        data = {
            'ci_usuario': usuario.ci_usuario,
            'nombre_usuario': usuario.nombre_usuario,
            'paterno': usuario.paterno,
            'materno': usuario.materno,
            'cel_usuario': usuario.cel_usuario,
            'correo': usuario.correo,
            'correo_inst': usuario.correo_inst,
            'rol_maestrante': usuario.rol_maestrante,
            'rol_docente': usuario.rol_docente,
            'rol_postgrado': usuario.rol_postgrado,
            'rol_tecnico_investigacion': usuario.rol_tecnico_investigacion,
            'usuario_administrador': usuario.usuario_administrador,
            

            'fecha_registro': usuario.fecha_registro.strftime("%d-%m-%Y"),
           
          
        }
        return JsonResponse(data)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
def vista_maestrante(request, username):
    user = Usuario.objects.get(username=username)
    user.tipo_usuario = 1
    user.save()
    return redirect('/')
def vista_docente(request, username):
    user = Usuario.objects.get(username=username)
    user.tipo_usuario = 2
    user.save()
    return redirect('/')
def vista_tecnico_investigacion(request, username):
    user = Usuario.objects.get(username=username)
    user.tipo_usuario = 3
    user.save()
    return redirect('/')
def vista_postgrado(request, username):
    user = Usuario.objects.get(username=username)
    user.tipo_usuario = 5
    user.save()
    return redirect('/')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'autenticacion/password-reset.html'
    form_class = CustomPasswordResetForm        
    success_url = reverse_lazy('usuario:password_reset_done') 

    def post(self, request, *args, **kwargs):
        form = self.get_form()  # Obtiene el formulario

        # Verifica si el formulario es válido
        if form.is_valid():
            username = self.request.POST.get('username')
            email = self.request.POST.get('correo_inst')
            
            # Verifica si el username y el email están presentes
            if username and email:
                try:
                    # Obtiene el usuario usando el email y el username
                    user = form.get_users(email, username).first()
                except Usuario.DoesNotExist:
                    user = None

                if user is not None:
                    # Intenta obtener el modelo `Usuario` relacionado
                    try:
                        usuario = Usuario.objects.get(ci_usuario=user.ci_usuario)
                    except Usuario.DoesNotExist:
                        usuario = None


                    # Procesa la solicitud si el formulario es válido
                    return self.form_valid(form)
                else:
                    self.extra_context = {'Nousuario': True}  # Usuario no encontrado
                    return self.form_invalid(form)

        # Si el formulario no es válido o faltan datos
        self.extra_context = {'CamposVacios': True}
        return self.form_invalid(form)

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name='autenticacion/password_reset_done.html'):
        email = self.request.POST.get('correo_inst')
        username = self.request.POST.get('username')

        user = None

        # Busca el usuario por email
        if email:
            users_by_email = CustomPasswordResetForm().get_users(email)

            if users_by_email.count() > 0:
                user = users_by_email[0]

        # Busca el usuario por username si no fue encontrado por email
        if username and not user:
            users_by_username = get_user_model()._default_manager.filter(
                username=username,
                is_active=True
            )

            if users_by_username.count() > 0:
                user = users_by_username[0]

        if user is not None and user.is_active:
            # Agregar el usuario al contexto si es encontrado
            context['user'] = user
            super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'autenticacion/password_reset_confirm.html'
    success_url = reverse_lazy('usuario:password_reset_complete')

    def form_valid(self, form):
        # Primero, completa el proceso de restablecimiento de contraseña
        response = super().form_valid(form)

        # Luego, actualiza el estado del cambio de contraseña
        user = form.user  # Obtiene el usuario que ha cambiado su contraseña
        usuario = get_object_or_404(Usuario, ci_usuario=user.ci_usuario)  # Tu modelo Usuario relacionado
        usuario.cambio_password = True  # Cambia el estado de cambio_password
        print("cambio de contraseña")
        usuario.save()  # Guarda el cambio en la base de datos
        return response

def enviar_correo_electronico(asunto, mensaje, destinatarios):       
    from_email = settings.DEFAULT_FROM_EMAIL      
    send_mail(asunto, mensaje, from_email, destinatarios, fail_silently=False)

def generar_password(longitud):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password


def reset_user_and_send_email(user):

    user.username = user.ci_usuario 
    new_password = generar_password(8)


    user.set_password(new_password)
    user.save()
    asunto = 'Restablecimiento de usuario y contraseña'
    mensaje = f'Hola, {user.nombre_usuario} {user.paterno} {user.materno}. Su nombre de usuario y contraseña ha sido restablecido.\n\nNombre de usuario: {user.username} \n\nSu nueva contraseña es: {new_password}\n\n Por favor, es recomendable que cambie su contraseña después de iniciar sesión.\n\nINSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”.'
    destinatarios = [user.correo_inst]
    enviar_correo_electronico(asunto, mensaje, destinatarios)
def reset_user_password_view(request, user_id):
    try:
        user = Usuario.objects.get(id=user_id)
        reset_user_and_send_email(user)
        return redirect("usuario:listar_usuarios")
        
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)

#********************************* Formato de correos ********************************************
#********************************* Formato de correo de activación de cuenta al momento de registro de usuario
def correo_activacion(ci_usuario,contrasena,correo):
    asunto_activacion = 'Activación de su cuenta en el Sistema de Seguimiento de Tesis de Maestría (SSTM)'    
    enlace_sistema = "sstm.usalesiana.edu.bo"  # Enlace al sistema
    mensaje_activacion = (
        f"Nos complace informarle que su cuenta en el Sistema de Seguimiento de Tesis de Maestría (SSTM) del "
        f"Instituto de Investigación y Postgrado 'Padre Juan Pablo Zabala Torrez' ha sido activada exitosamente.\n\n"
        f"A continuación, encontrará su nombre de usuario y contraseña para acceder al sistema:\n\n"
        f"Nombre de usuario:  {ci_usuario}\n\n"
        f"Contraseña:  {contrasena}\n\n"
        f"Le recomendamos cambiar su contraseña al iniciar sesión por primera vez para garantizar la seguridad de su cuenta. "
        f"Puede acceder al sistema a través del siguiente enlace: {enlace_sistema}.\n\n"
        f"Saludos cordiales.\n"
        f"Instituto de Investigación y Postgrado 'Padre Juan Pablo Zabala Torrez'\n"
        f"Universidad Salesiana de Bolivia"
    )

    enviar_correo_electronico(asunto_activacion, mensaje_activacion, correo)



# *************** Listas de usuarios *******************.

@method_decorator(login_required, name='dispatch')
class ListadoActividadesMaestrante(View):
    model=Maestrante
    template_name='usuario/listar_maestrante.html'
    def get_queryset(self):
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4 :
            return self.model.objects.filter(maestrante_habilitado=True)
        if self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(maestrante_habilitado=False)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')
class ListadoMaestrante(View):
    model=Maestrante
    template_name='usuario/listar_maestrante.html'
    def get_queryset(self):
        
        
            return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoMaestranteMatriculaVencida(View):
    model=Maestrante
    template_name='usuario/listar_maestrante_matricula.html'
    def get_queryset(self):

        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoMaestranteGraduado(View):
    model=Maestrante
    template_name='usuario/listar_maestrante_tesis_concluido.html'
    def get_queryset(self):
        
            return self.model.objects.filter(tesis_terminado=True)
        
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoPostulante(View):
    model=Maestrante
    template_name='usuario/listar_postulante.html'
    def get_queryset(self):

            return self.model.objects.filter(maestrante_habilitado=False).filter(tesis_terminado = False)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoTiempoActividad(View):
    model=Maestrante
    template_name='usuario/listar_tiempo_actividad.html'
    def get_queryset(self):
        return self.model.objects.filter( tiempo__lt = timezone.now()).filter( listacomunicacion = False)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['maestrantes']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.is_taff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoPrograma(View):
    model=Programa
    template_name='usuario/listar_programa.html'
    def get_queryset(self):
        return self.model.objects.all()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
     
@method_decorator(login_required, name='dispatch')
class ListadoSustentacionPerfil(View):
    model=Maestrante
    template_name='usuario/listar_sustentacion_perfil.html'
    def get_queryset(self):        
            return self.model.objects.filter(cronograma__fecha_3__isnull=False,avance_tesis=5)
        
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoSustentacionPerfilHistorial(View):
    model=SustentacionPerfilHistorial
    template_name='usuario/listar_sustentacion_perfil_historial.html'
    def get_queryset(self):
        return self.model.objects.all()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoSustentacionTesis(View):
    model=Maestrante
    template_name='usuario/listar_sustentacion_tesis.html'
    def get_queryset(self):        
            return self.model.objects.filter(cronograma2__fecha_sustentacion__isnull=False,avance_tesis=18)
        
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoSustentacionTesisHistorial(View):
    model=SustentacionTesisHistorial
    template_name='usuario/listar_sustentacion_tesis_historial.html'
    def get_queryset(self):        
            return self.model.objects.all().order_by('-id_sustentacion')
        
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoCentroActividades(View):
    model=Maestrante
    template_name='usuario/seguimiento_tesis_historial.html'
 

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name)
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoAsistencia(View):
    model=AsistenciaInduccion
    template_name='usuario/listar_asistencia.html'
    def get_queryset(self):
        return self.model.objects.all().order_by('-fecha_realizada')
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class RegistroAsistencia(View):
    model=Maestrante
    template_name='usuario/registrar_asistencia.html'
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ReestablecerUsuarioPassword(DetailView):
    model=Usuario
    template_name='usuario/registrar_reestablecer_usuario.html'
@method_decorator(login_required, name='dispatch')
class ListadoTesisMaestrante(View):
    model=Maestrante
    template_name='usuario/listar_tesis_maestrante.html'
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')



@method_decorator(login_required, name='dispatch')
class ListadoDocente(View):
    model=Docente
    template_name='usuario/listar_docente.html'
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador or self.request.user.tipo_usuario == 1:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListaTemaTesis(View):
    model=Maestrante
    template_name='usuario/listar_tema_tesis.html'
    def get_queryset(self):
        return self.model.objects.filter()
        #return self.model.objects.filter(user__is_active=True)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
#@method_decorator(login_required, name='dispatch')
#class ListaEvidencia(View):
 #   def  get(self, request):
 #       evidencias =  list(Requisitos1.objects.values().order_by('nro_requisito'))
 #       data =  dict()
 #       data['evidencias'] = evidencias
        
  #      return JsonResponse(data)
@method_decorator(login_required, name='dispatch')
class ListaEvidencia(View):
    model=Requisitos
    template_name='usuario/listar_evidencia.html'
    def get_queryset(self):
        return self.model.objects.all().order_by('nro_requisito')
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')
class ListaBancoNotificacion(View):
    model=BancoNotificacion
    template_name='usuario/listar_banco_notificacion.html'
    def get_queryset(self):
        return self.model.objects.all().order_by('numero_notificacion')
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListaAsesoramiento(View):
    model=AsistenciaInduccion
    template_name='usuario/listar_asesoramiento.html'
    def get_queryset(self):
        return self.model.objects.all().order_by('-id_asistencia')
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoAdministradores(ListView):
    model=Usuario
    template_name='usuario/listar_administradores.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        return self.model.objects.filter(Q(rol_tecnico_investigacion=True) | Q(rol_postgrado=True))
 
@method_decorator(login_required, name='dispatch')
class ListadoUsuarios(ListView):
    model=Usuario
    template_name='usuario/listar_usuarios.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        return self.model.objects.filter()
 
 

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneral(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoSegundoReporteGeneralGuia(View):
    model=ReporteGeneral
    template_name='usuario/listar_segundo_reporte_general_guia.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(activar_reporte2 = True)
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoSegundoReporteGeneral(View):
    model=ReporteGeneral
    template_name='usuario/listar_segundo_reporte_general.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(activar_reporte2 = True)
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(activar_reporte2 = True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneralTribunalInterno(View):
    model=ReporteGeneralTribunalInterno
    template_name='usuario/listar_reporte_general_tribunal_interno.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
          
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
           
            return self.model.objects.filter(tribunal=self.request.user.docente_revisor)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
           
        
 
 
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneralGuia(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general_guia.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.user.maestrante)
        
        
 
 
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

    
@method_decorator(login_required, name='dispatch')
class ListadoInformeGuia(View):
    model=InformeGuia
    template_name='usuario/listar_informe_guia.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())


@method_decorator(login_required, name='dispatch')
class ListadoInformeGuiaPendiente(View):
    model=InformeGuia
    template_name='usuario/listar_informe_guia.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_guia=False)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_guia=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoInformeGuiaRealizado(View):
    model=InformeGuia
    template_name='usuario/listar_informe_guia.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_guia=True)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_guia=True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneralPendiente(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor=False)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneralRealizado(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor=True)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())
@method_decorator(login_required, name='dispatch')
class ListadoSegundoReporteGeneralPendiente(View):
    model=ReporteGeneral
    template_name='usuario/listar_segundo_reporte_general.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor2=False).filter(activar_reporte2 = True)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor2=False).filter(activar_reporte2 = True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())
@method_decorator(login_required, name='dispatch')
class ListadoSegundoReporteGeneralRealizado(View):
    model=ReporteGeneral
    template_name='usuario/listar_segundo_reporte_general.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor2=True).filter(activar_reporte2 = True)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor2=True).filter(activar_reporte2 = True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarTesis(View):
    model=Usuario
    template_name='usuario/listar_tesis.html'
    context_object_name = 'actividades'
    queryset = Usuario.objects.filter()
    
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        context={}
        context['today'] = date.today()
    
        return context

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 1:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')

class ListadoInformeRevisor(View):
    model=Informe
    template_name='usuario/listar_informe_revisor.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)    
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
     
            return render(request,self.template_name,self.get_context_data())
@method_decorator(login_required, name='dispatch')

class ListadoInformeRevisorGuia(View):
    model=Informe
    template_name='usuario/listar_informe_revisor_guia.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
    
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
     
            return render(request,self.template_name,self.get_context_data())
@method_decorator(login_required, name='dispatch')

class ListadoInformeGuiaRevisor(View):
    model=Informe
    template_name='usuario/listar_informe_guia_revisor.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.user.maestrante)
    
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
     
            return render(request,self.template_name,self.get_context_data())
@method_decorator(login_required, name='dispatch')

class ListadoInformeRevisorPendiente(View):
    model=Informe
    template_name='usuario/listar_informe_revisor.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor=False)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')

class ListadoInformeRevisorRealizado(View):
    model=Informe
    template_name='usuario/listar_informe_revisor.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_revisor=True)            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)   
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())
       
@method_decorator(login_required, name='dispatch')    
class InformacionGeneral(TemplateView):
    template_name = 'usuario/informacion_general.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Filtrar datos según el usuario autenticado
        usuario_autenticado = self.request.user
        queryset = Maestrante.objects.filter(usuario=usuario_autenticado)
        context['programas'] = queryset
        return context
# *************** Registro de usuarios *******************.

@method_decorator(login_required, name='dispatch')
class RegistrarDocente(CreateView):
    model=Usuario
    form_class=RegistroDocenteForm
    template_name='usuario/agregar_docente.html'
    success_url = reverse_lazy('usuario:listar_docente')

    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).exists()
            usuario=None
            if usuario_existente:
                usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                docente_existente = Docente.objects.filter(user=usuario).exists() 
              
                
                if docente_existente:
                    
                    success_url = reverse_lazy('usuario:registrar_docente')
                    messages.success(self.request, "Ya existe un usuario con el Ci ingresado, no se registró al usuario.")
                    return HttpResponseRedirect(success_url)
                else:
                    
                    usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                    usuario.rol_docente = True
                    #usuario.registrado_rol_docente = True
                    usuario.save()
                    docente_data = {
                    'especialidad_docente': form.cleaned_data.get('especialidad_docente'),
                    'docente_interno': form.cleaned_data.get('docente_interno'),
                    'docente_externo': form.cleaned_data.get('docente_externo'),                
                    'user': usuario,
                }
                    Docente.objects.create(**docente_data)
                    DocenteProvisional.objects.create(user=usuario)            
                    Docente_Revisor.objects.create(user=usuario)
                    return HttpResponseRedirect(self.success_url)
            else:
                
                # Crear un nuevo usuario
                usuario = form.save(commit=False)
                usuario.username = ci_usuario
                contrasena_generada = generar_password(8)
  
                usuario.set_password(contrasena_generada)
                usuario.tipo_usuario = 2  
                usuario.rol_docente = True 
                #usuario.registrado_rol_docente = True
                usuario.save()

            # Asignar el valor de ci_usuario al formulario
            form.instance.ci_usuario = ci_usuario

            # Crear un maestrante asociado al usuario
            docente_data = {
                'especialidad_docente': form.cleaned_data.get('especialidad_docente'),
                'docente_interno': form.cleaned_data.get('docente_interno'),
                'docente_externo': form.cleaned_data.get('docente_externo'),                
                'user': usuario,
            }
            Docente.objects.create(**docente_data)
            DocenteProvisional.objects.create(user=usuario)            
            Docente_Revisor.objects.create(user=usuario)

            # Envía un correo electrónico al usuario con su nombre de usuario y contraseña
            if not usuario_existente:
                #asunto = 'Activación de cuenta'
                #mensaje = f'Se activó la cuenta del SISTEMA DE SEGUIMIENTO DE TESIS TE MAESTRÍA (SSTM) del INSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”. Su nombre de usuario y contraseña para el inicio de sesión son las siguientes: \n\nNombre de usuario: {ci_usuario}\n\nContraseña: {contrasena_generada}'
                destinatarios = [form.cleaned_data.get('correo_inst')]
                #enviar_correo_electronico(asunto, mensaje, destinatarios)                                
                correo_activacion(ci_usuario,contrasena_generada,destinatarios)

            # Redirige a la página de éxito
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

            
@method_decorator(login_required, name='dispatch')
class RegistrarNuevoDocente(CreateView):
    model=Usuario
    form_class=RegistroNuevoDocenteForm
    template_name='usuario/agregar_nuevo_docente.html'
    success_url = reverse_lazy('usuario:listar_docente')

    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).exists()
            usuario=None
            if usuario_existente:
                usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                docente_existente = Docente.objects.filter(user=usuario).exists() 
                
                
                if docente_existente:
                    
                    success_url = reverse_lazy('usuario:registrar_docente')
                    messages.success(self.request, "Ya existe un usuario con el Ci ingresado, no se registró al usuario.")
                    return HttpResponseRedirect(success_url)
                else:
                    
                    usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                    usuario.rol_docente = True
                    usuario.save()
                    docente_data = {
                    'especialidad_docente': form.cleaned_data.get('especialidad_docente'),
                    'docente_interno': form.cleaned_data.get('docente_interno'),
                    'docente_externo': form.cleaned_data.get('docente_externo'),                
                    'user': usuario,
                }
                    Docente.objects.create(**docente_data)
                    DocenteProvisional.objects.create(user=usuario)            
                    Docente_Revisor.objects.create(user=usuario)
                    return HttpResponseRedirect(self.success_url)
            else:
               
                # Crear un nuevo usuario
                usuario = form.save(commit=False)
                usuario.username = ci_usuario
                contrasena_generada = generar_password(8)

                usuario.set_password(contrasena_generada)
                usuario.tipo_usuario = 2  
                usuario.rol_docente = True 
                usuario.save()

            # Asignar el valor de ci_usuario al formulario
            form.instance.ci_usuario = ci_usuario

            # Crear un maestrante asociado al usuario
            docente_data = {
                'especialidad_docente': form.cleaned_data.get('especialidad_docente'),
                'docente_interno': form.cleaned_data.get('docente_interno'),
                'docente_externo': form.cleaned_data.get('docente_externo'),                
                'user': usuario,
            }
            Docente.objects.create(**docente_data)
            DocenteProvisional.objects.create(user=usuario)            
            Docente_Revisor.objects.create(user=usuario)

            # Envía un correo electrónico al usuario con su nombre de usuario y contraseña
            if not usuario_existente:
                #asunto = 'Activación de cuenta'
                #mensaje = f'Se activó la cuenta del SISTEMA DE SEGUIMIENTO DE TESIS TE MAESTRÍA (SSTM) del INSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”. Su nombre de usuario y contraseña para el inicio de sesión son las siguientes: \n\nNombre de usuario: {ci_usuario}\n\nContraseña: {contrasena_generada}'
                destinatarios = [form.cleaned_data.get('correo_inst')]
                #enviar_correo_electronico(asunto, mensaje, destinatarios)
                correo_activacion(ci_usuario,contrasena_generada,destinatarios)

            # Redirige a la página de éxito
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

            
    

@method_decorator(login_required, name='dispatch')
class RegistrarPrograma(CreateView):
    model=Programa
    form_class=FormularioPrograma
    template_name='usuario/agregar_programa.html'
    success_url = reverse_lazy('usuario:listar_programa')
 
@method_decorator(login_required, name='dispatch')
class RegistrarMaestrante(CreateView):
    template_name = 'usuario/agregar_maestrante.html'
    form_class = RegistroMaestranteForm  
    success_url = reverse_lazy('usuario:listar_postulante')

    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).exists()

            if usuario_existente:
                usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                usuario.rol_maestrante = True
                usuario.save()
                maestrante_data = {
                'programa': form.cleaned_data.get('programa'),
                'version': form.cleaned_data.get('version'),
                'tipo_maestrante': form.cleaned_data.get('tipo_maestrante'),
                'gestion': form.cleaned_data.get('gestion'),
                'usuario': usuario,
            }
                Maestrante.objects.create(**maestrante_data)
                return HttpResponseRedirect(self.success_url)
            else:
                # Crear un nuevo usuario
                usuario = form.save(commit=False)
                usuario.username = ci_usuario
                contrasena_generada = generar_password(8)           
                usuario.set_password(contrasena_generada)
                usuario.tipo_usuario = 1  
                usuario.rol_maestrante = True 
                usuario.save()

            # Asignar el valor de ci_usuario al formulario
            form.instance.ci_usuario = ci_usuario

            # Crear un maestrante asociado al usuario
            maestrante_data = {
                'programa': form.cleaned_data.get('programa'),
                'version': form.cleaned_data.get('version'),
                'tipo_maestrante': form.cleaned_data.get('tipo_maestrante'),
                'gestion': form.cleaned_data.get('gestion'),
                'usuario': usuario,
            }
            Maestrante.objects.create(**maestrante_data)

            # Envía un correo electrónico al usuario con su nombre de usuario y contraseña
            if not usuario_existente:
                #asunto = 'Activación de cuenta'
                #mensaje = f'Se activó la cuenta del SISTEMA DE SEGUIMIENTO DE TESIS TE MAESTRÍA (SSTM) del INSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”. Su nombre de usuario y contraseña para el inicio de sesión son las siguientes: \n\nNombre de usuario: {ci_usuario}\n\nContraseña: {contrasena_generada}'
                destinatarios = [form.cleaned_data.get('correo_inst')]
                correo_activacion(ci_usuario,contrasena_generada,destinatarios)
                

            # Redirige a la página de éxito
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))
@method_decorator(login_required, name='dispatch')
class RegistrarNuevoMaestrante(CreateView):
    template_name = 'usuario/agregar_nuevo_maestrante.html'
    form_class = RegistroNuevoMaestranteForm  
    success_url = reverse_lazy('usuario:listar_postulante')

    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).exists()

            if usuario_existente:
                usuario = Usuario.objects.get(ci_usuario=ci_usuario)
                usuario.rol_maestrante = True
                #usuario.registrado_rol_maestrante = True
                usuario.save()
                maestrante_data = {
                'programa': form.cleaned_data.get('programa'),
                'version': form.cleaned_data.get('version'),
                'tipo_maestrante': form.cleaned_data.get('tipo_maestrante'),
                'gestion': form.cleaned_data.get('gestion'),
                'usuario': usuario,
            }
                Maestrante.objects.create(**maestrante_data)
                return HttpResponseRedirect(self.success_url)
            else:
                # Crear un nuevo usuario
                usuario = form.save(commit=False)
                usuario.username = ci_usuario
                contrasena_generada = generar_password(8)

                usuario.set_password(contrasena_generada)
                usuario.tipo_usuario = 1  
                usuario.rol_maestrante = True 
                #usuario.registrado_rol_maestrante = True
                usuario.save()

            # Asignar el valor de ci_usuario al formulario
            form.instance.ci_usuario = ci_usuario

            # Crear un maestrante asociado al usuario
            maestrante_data = {
                'programa': form.cleaned_data.get('programa'),
                'version': form.cleaned_data.get('version'),
                'tipo_maestrante': form.cleaned_data.get('tipo_maestrante'),
                'gestion': form.cleaned_data.get('gestion'),
                'usuario': usuario,
            }
            Maestrante.objects.create(**maestrante_data)

            # Envía un correo electrónico al usuario con su nombre de usuario y contraseña
            if not usuario_existente:
                #asunto = 'Activación de cuenta'
                #mensaje = f'Se activó la cuenta del SISTEMA DE SEGUIMIENTO DE TESIS TE MAESTRÍA (SSTM) del INSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”. Su nombre de usuario y contraseña para el inicio de sesión son las siguientes: \n\nNombre de usuario: {ci_usuario}\n\nContraseña: {contrasena_generada}'
                destinatarios = [form.cleaned_data.get('correo_inst')]
                #enviar_correo_electronico(asunto, mensaje, destinatarios)
                correo_activacion(ci_usuario,contrasena_generada,destinatarios)

            # Redirige a la página de éxito
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))
@method_decorator(login_required, name='dispatch')
class RegistrarNuevoAdministradores(CreateView): 
    template_name = 'usuario/agregar_nuevo_administradores.html'
    form_class = FormularioAdministradoresNuevo  
    success_url = reverse_lazy('usuario:listar_administradores')

    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).exists()

            if usuario_existente:

                return HttpResponseRedirect(self.success_url)
            else:
                # Crear un nuevo usuario
                usuario = form.save(commit=False)
                tipo_usuario = form.cleaned_data.get('tipo_usuario')
                if tipo_usuario == "1":
                    usuario.rol_tecnico_investigacion = True
                    #usuario.registrado_rol_tecnico_investigacion = True
                    usuario.tipo_usuario = 3  
                if tipo_usuario == "2":
                    usuario.rol_postgrado = True
                    #usuario.registrado_rol_postgrado = True
                    usuario.tipo_usuario = 5   




                usuario.usuario_administrador = True
                usuario.is_staff = False
                usuario.username = ci_usuario
                contrasena_generada = generar_password(8)

                usuario.set_password(contrasena_generada)
     
        
                usuario.save()

            # Asignar el valor de ci_usuario al formulario
            form.instance.ci_usuario = ci_usuario



            # Envía un correo electrónico al usuario con su nombre de usuario y contraseña
            if not usuario_existente:
                #asunto = 'Activación de cuenta'
                #mensaje = f'Se activó la cuenta del SISTEMA DE SEGUIMIENTO DE TESIS TE MAESTRÍA (SSTM) del INSTITUTO DE INVESTIGACIÓN Y POSTGRADO “PADRE JUAN PABLO ZABALA TORREZ”. Su nombre de usuario y contraseña para el inicio de sesión son las siguientes: \n\nNombre de usuario: {ci_usuario}\n\nContraseña: {contrasena_generada}'
                destinatarios = [form.cleaned_data.get('correo_inst')]
                #enviar_correo_electronico(asunto, mensaje, destinatarios)
                correo_activacion(ci_usuario,contrasena_generada,destinatarios)

            # Redirige a la página de éxito
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))
@method_decorator(login_required, name='dispatch')
class RegistrarAdministradores(CreateView):
    model = Usuario
    form_class = FormularioAdministradores
    template_name = 'usuario/agregar_administradores.html'
    success_url = reverse_lazy('usuario:listar_administradores')

    def form_valid(self, form):
        ci_usuario = form.cleaned_data['ci_usuario']

        # Verificar si el usuario ya existe
        usuario_existente = Usuario.objects.filter(ci_usuario=ci_usuario).first()

        if usuario_existente:
            # Modificar usuario existente en lugar de crear uno nuevo
            tipo_usuario = form.cleaned_data['tipo_usuario']

            if tipo_usuario == "1":
                usuario_existente.rol_tecnico_investigacion = True

            if tipo_usuario == "2":
                usuario_existente.rol_postgrado = True
            usuario_existente.usuario_administrador = True  
            usuario_existente.is_staff = False
            usuario_existente.save()
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)




# *************** Actualizar datos de usuarios *******************.

@method_decorator(login_required, name='dispatch')
class ActualizarPrograma(UpdateView):

    model = Programa
    template_name = 'usuario/editar_programa.html'
    form_class = FormularioPrograma
    success_url = reverse_lazy('usuario:listar_programa')

@method_decorator(login_required, name='dispatch')
class ActualizarArchivosPerfil(UpdateView):

    model = SustentacionPerfilHistorial
    template_name = 'usuario/editar_archivos_perfil.html'
    form_class = FormularioHistorialArchivosPerfil
    success_url = reverse_lazy('usuario:listar_sustentacion_perfil_historial') 

@method_decorator(login_required, name='dispatch')
class ActualizarArchivosTesis(UpdateView):

    model = SustentacionTesisHistorial
    template_name = 'usuario/editar_archivos_tesis.html'
    form_class = FormularioHistorialArchivosTesis
    success_url = reverse_lazy('usuario:listar_sustentacion_tesis_historial') 


@method_decorator(login_required, name='dispatch')
class ActualizarArchivoEvidencia(UpdateView):

    model = CentroActividades
    template_name = 'usuario/editar_archivo_evidencia.html'
    form_class = FormularioArchivoEvidencia
    success_url = reverse_lazy('usuario:listar_historial')    


@method_decorator(login_required, name='dispatch')
class ActualizarAdministrador(UpdateView):

    model = Usuario
    template_name = 'usuario/editar_usuario.html'
    form_class = FormularioAdministradoresEditar
    success_url = reverse_lazy('usuario:listar_administradores')    

@method_decorator(login_required, name='dispatch')
class ActualizarUsuario(UpdateView):

    model = Usuario
    template_name = 'usuario/editar_usuario_sistema.html'
    form_class = FormularioUsuario
    success_url = reverse_lazy('usuario:listar_usuarios')    




@method_decorator(login_required, name='dispatch')
class EditarEvidencia(UpdateView):

    model = Requisitos
    template_name = 'usuario/editar_evidencia.html'
    form_class = FormularioEvidencia
    success_url = reverse_lazy('usuario:listado_evidencia') 

@method_decorator(login_required, name='dispatch')
class EditarBancoNotificacion(UpdateView):

    model = BancoNotificacion
    template_name = 'usuario/editar_banco_notificacion.html'
    form_class = FormularioBancoNotificacion
    success_url = reverse_lazy('usuario:listado_banco_notificacion')           


from django.contrib.auth import update_session_auth_hash
from django.contrib import messages 
def change_password(request):

    if request.method == 'POST':
        old_password = request.POST.get("q_Old_Password")
        new_password = request.POST.get("q_new_Password")
        confirmed_new_password = request.POST.get("q_confirm_new_Password")

        if old_password and new_password and confirmed_new_password:
            if request.user.is_authenticated:
                user = Usuario.objects.get(username= request.user.username)
                if not user.check_password(old_password):
                    messages.warning(request, "¡Tu antigua contraseña no es correcta!")
                else:
                    if new_password != confirmed_new_password:
                        messages.warning(request, "¡Su nueva contraseña no coincide con la contraseña confirmada!")
                   
                    
                    elif len(new_password) <= 8 :
                        messages.warning(request, "¡Tu contraseña es vulnerable!")


                    

                    else:
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)
                        
                        messages.success(request, "Su contraseña ha sido cambiada con éxito.!")
                        logout(request)
                        return redirect('/')

        else:
            messages.warning(request, " Todos los campos son obligatorios!")
 


    context = {

    }
    return render(request, "usuario/password_change_form.html", context)

#-------------------------------------------------------     
      



@method_decorator(login_required, name='dispatch')
class ActualizarDocente(UpdateView):

    model = Docente
    template_name = 'usuario/editar_docente.html'
    form_class = FormularioUsuarioDocente
    success_url = reverse_lazy('usuario:listar_docente')
   
@method_decorator(login_required, name='dispatch')      
class ActualizarMaestrante(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_maestrante.html'
    form_class = FormularioUsuarioMaestrante
    success_url = reverse_lazy('usuario:listar_maestrante')

@method_decorator(login_required, name='dispatch')      
class ActualizarMaestranteDictamen(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_maestrante_dictamen.html'
    form_class = FormularioUsuarioMaestranteDictamen
    success_url = reverse_lazy('usuario:listar_maestrante')

@method_decorator(login_required, name='dispatch')      
class ActualizarMatriculaMaestrante(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_maestrante_matricula.html'
    form_class = FormularioMatricula
    success_url = reverse_lazy('usuario:listado_maestrante_matricula')
@method_decorator(login_required, name='dispatch')    
class ActualizarMaestranteComplemento(UpdateView):

    model = Usuario
    template_name = 'usuario/editar_maestrante_complemento.html'
    form_class = FormularioUsuarioMaestranteComplemento
    success_url = reverse_lazy('usuario:informacion_general')
            
@method_decorator(login_required, name='dispatch')    
class ActualizarArchivoSeguimiento(UpdateView):

    model = Usuario
    template_name = 'usuario/editar_maestrante_complemento.html'
    form_class = FormularioUsuarioMaestranteComplemento
    success_url = reverse_lazy('usuario:informacion_general')
    
      
@method_decorator(login_required, name='dispatch')
class ActualizarCronograma(UpdateView):

    model = Cronograma
    template_name = 'usuario/editar_cronograma.html'
    form_class = FormularioCronograma
    success_url = reverse_lazy('usuario:cronograma') 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioCronograma(request.POST, instance=self.object)

        if form.is_valid():        
            self.object = form.save()
            CentroActividades.objects.create(usuario=request.user,fecha=timezone.now())
            return redirect(self.get_success_url())

        return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')
class ActualizarCronograma2(UpdateView):

    model = Cronograma2
    template_name = 'usuario/editar_cronograma2.html'
    form_class = FormularioCronograma2
    success_url = reverse_lazy('usuario:cronograma2') 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioCronograma2(request.POST, instance=self.object)

        if form.is_valid():        
            self.object = form.save()
            CentroActividades.objects.create(usuario=request.user,fecha=timezone.now())
            return redirect(self.get_success_url())

        return self.form_invalid(form)



 
        
        


  
 
@method_decorator(login_required, name='dispatch')
class RegistrarTemaTesis(UpdateView):

    model = Maestrante
    template_name = 'usuario/registrar_tema_tesis.html'
    form_class = FormularioTemaTesis
    success_url = reverse_lazy('usuario:listar_tema_tesis') 
      




@method_decorator(login_required, name='dispatch')    
class ActualizarDocenteProvisional(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_guia_provisional.html'
    form_class = FormularioDocenteProvisional
    success_url = reverse_lazy('usuario:seguimiento_tesis')    

@method_decorator(login_required, name='dispatch')    
class FechaHoraSustentacion(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_fecha_sustentacion.html'
    form_class = FormularioFechaSustentacion
    success_url = reverse_lazy('usuario:seguimiento_tesis')    


@method_decorator(login_required, name='dispatch')    
class HabilitarMaestranteGuia(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_maestrante_guia.html'
    form_class = FormularioMaestranteGuia
    success_url = reverse_lazy('usuario:listar_designar') 
    def form_valid(self, form):
        # Obtener el objeto actual antes de la modificación
        maestrante = self.get_object()

        # Guardar el formulario sin realizar la acción por defecto
        self.object = form.save(commit=False)

        # Comparar los campos modificados con los originales
        campos_modificados = {}
        for field in form.changed_data:
            campos_modificados[field] = {
                'antes': getattr(maestrante, field),
                'despues': form.cleaned_data.get(field)
            }

        # Aquí puedes hacer lo que quieras con los campos modificados
        

        # Continuar con la acción por defecto de form_valid()
        return super().form_valid(form)
@method_decorator(login_required, name='dispatch')    
class EditarTribunalPerfil(UpdateView):

    model = TribunalPerfil
    template_name = 'usuario/editar_tribunal_perfil.html'
    form_class = FormularioTribunalPerfil
    success_url = reverse_lazy('usuario:listar_tribunal_perfil') 
    
@method_decorator(login_required, name='dispatch')    
class EditarTribunalTesis(UpdateView):

    model = TribunalTesis
    template_name = 'usuario/editar_tribunal_tesis.html'
    form_class = FormularioTribunalTesis
    success_url = reverse_lazy('usuario:listar_tribunal_tesis') 
@method_decorator(login_required, name='dispatch')    
class EditarTribunalTesis(UpdateView):

    model = TribunalTesis
    template_name = 'usuario/editar_tribunal_tesis.html'
    form_class = FormularioTribunalTesis
    success_url = reverse_lazy('usuario:listar_tribunal_tesis') 
    



@method_decorator(login_required, name='dispatch')
class DesignarDocente(View):
    
    model=Maestrante
    template_name='usuario/designar_docente.html'
    context_object_name = 'actividades'
    queryset = Maestrante.objects.filter()
   
    
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')


@method_decorator(login_required, name='dispatch')
class DesignarTribunalPerfil(View):
    
    model=TribunalPerfil
    template_name='usuario/designar_tribunal_perfil.html'

    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')


@method_decorator(login_required, name='dispatch')
class DesignarTribunalTesis(View):
    
    model=TribunalTesis
    template_name='usuario/designar_tribunal_tesis.html'

    
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.usuario_administrador:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListarAvanceHistorial(ListView):

    model = AvanceHistorial
    template_name = 'usuario/listar_avance_historial.html'
    context_object_name = 'avance_historial'

    def get_queryset(self):
        # Obtener el nombre de usuario de los parámetros de consulta
        nombre_usuario = self.kwargs['pk']
        
      
        
        # Obtener el objeto User correspondiente al nombre de usuario
        usuario = Maestrante.objects.get(id_maestrante=nombre_usuario)
      
        # Filtrar los resultados según el usuario
        return AvanceHistorial.objects.filter(user=usuario)
@method_decorator(login_required, name='dispatch')    
class ListarAvance2Historial(ListView):

    model = Avance_2_Histoiral
    template_name = 'usuario/listar_avance_2_historial.html'
    context_object_name = 'avance_historial'

    def get_queryset(self):
  
        # Obtener el nombre de usuario de los parámetros de consulta
        nombre_usuario = self.kwargs['pk']
        
      
        
        # Obtener el objeto User correspondiente al nombre de usuario
        usuario = Maestrante.objects.get(id_maestrante=nombre_usuario)
      
        # Filtrar los resultados según el usuario
        return Avance_2_Histoiral.objects.filter(user=usuario)
@method_decorator(login_required, name='dispatch')
class ListarAvance(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
            
            return self.model.objects.filter(user__guia=self.request.user.docente)

        if self.request.user.tipo_usuario == 1:
            
            return self.model.objects.filter(user__usuario=self.request.user)
 
    def get_context_data(self, **kwargs):
        contexto = {}
        contexto['actividades'] = self.get_queryset()
        contexto['today'] = date.today() 
       
        return contexto     
 
         

    def get(self,request,**kwargs):       
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvancePendiente(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_avance=False)
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):       
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvanceRealizado(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_avance=True)
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.user.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):       
        return render(request,self.template_name,self.get_context_data())

 
        

@method_decorator(login_required, name='dispatch')
class ListarAvance2(View):
    
    model=Avance_2
    template_name='usuario/listar_avance_2.html'
    context_object_name = 'actividades'
    def get_queryset(self):     
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()       
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvance2Pendiente(View):
    
    model=Avance_2
    template_name='usuario/listar_avance_2.html'
    context_object_name = 'actividades'
    def get_queryset(self):     
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_avance=False)       
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        contexto['today'] = date.today() 
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvance2Realizado(View):
    
    model=Avance_2
    template_name='usuario/listar_avance_2.html'
    context_object_name = 'actividades'
    def get_queryset(self):     
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(aceptar_avance=True)       
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=True)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())
            
        

@method_decorator(login_required, name='dispatch')
class InformacionTesisTerminado(DetailView):
    model=Maestrante
    template_name='usuario/informacion_tesis_terminado.html' 
@method_decorator(login_required, name='dispatch')
class DetalleReporte(DetailView):
    model=ReporteGeneral
    template_name='usuario/detalle_reporte.html'    
@method_decorator(login_required, name='dispatch')    
class DetalleReportePDF(DetailView):
    model = ReporteGeneral  # Asegúrate de tener este modelo importado
    template_name = 'usuario/detalle_reporte_pdf.html'

    def render_to_pdf_response(self, context):
        template_path = self.template_name
        
        # Obtener el objeto del contexto
        reporte = context['object']
        
        # Generar un nombre personalizado para el archivo PDF
        filename = f"{self.object.user}_Reporte.pdf"  # Usa el atributo "titulo" del reporte
        
        # Crear la respuesta como archivo PDF
        response = HttpResponse(content_type='application/pdf')
        
        # Configurar el encabezado Content-Disposition para forzar la descarga con el nombre personalizado
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        # Renderizar el template para el PDF
        template = get_template(template_path)
        html = template.render(context)
        
        # Crear el archivo PDF
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        # Comprobar errores
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        
        return response

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)  
        return self.render_to_pdf_response(context)

@method_decorator(login_required, name='dispatch')    
class DetalleReporte2PDF(DetailView):
    model = ReporteGeneral
    template_name = 'usuario/detalle_reporte_2_pdf.html'

    def render_to_pdf_response(self, context):
        # Obtener el objeto del contexto para utilizar atributos en el nombre del archivo
        reporte = context.get('object')

        # Crear la respuesta con tipo de contenido para PDF
        response = HttpResponse(content_type='application/pdf')

        # Generar un nombre personalizado para el archivo PDF
        if reporte:
            filename = f"{self.object.user}_Reporte2.pdf"  # Puedes usar el título del reporte o cualquier otro atributo
        else:
            filename = "Reporte2.pdf"  # Nombre predeterminado en caso de no tener información suficiente

        # Configurar el encabezado Content-Disposition para forzar la descarga con el nombre personalizado
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Renderizar el template para el PDF
        template_path = self.template_name
        template = get_template(template_path)
        html = template.render(context)

        # Crear el archivo PDF con xhtml2pdf (pisa)
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Comprobar errores al crear el PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        
        return response

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtener el objeto a partir de los argumentos
        context = self.get_context_data(object=self.object)  # Obtener el contexto para el template
        return self.render_to_pdf_response(context)  # Generar la respuesta PDF

@method_decorator(login_required, name='dispatch')
class RegistrarPostulante(DetailView):
    model=Maestrante
    template_name='usuario/registrar_postulante.html'
@method_decorator(login_required, name='dispatch')
class DetalleReporte2(DetailView):
    model=ReporteGeneral
    template_name='usuario/detalle_reporte2.html'   

@method_decorator(login_required, name='dispatch')
class DetalleAvance(DetailView):
    model=Avance
    template_name='usuario/detalle_avance.html'

@method_decorator(login_required, name='dispatch')    
class GenerarAvancePDF(DetailView):
    model = Avance
    template_name = 'usuario/detalle_avance_pdf_template.html'

    def render_to_pdf_response(self, context):
        template_path = self.template_name
        
        # Crear la respuesta con tipo de contenido PDF
        response = HttpResponse(content_type='application/pdf')

        # Obtener el objeto y usarlo para crear un nombre personalizado para el archivo PDF
        avance = context.get('object')  # Asegurarse de obtener el objeto del contexto

        # Generar un nombre de archivo basado en el objeto
        if avance:
            filename = f"{self.object.user}_Formulario_avance.pdf"  # Usar el nombre o atributo relevante
        else:
            filename = "Avance_Report.pdf"  # Nombre predeterminado en caso de falta de datos

        # Configurar el encabezado Content-Disposition para forzar la descarga
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Renderizar el template a HTML y luego convertirlo a PDF
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verificar errores al generar el PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()  # Obtener el objeto correspondiente
        context = self.get_context_data(object=self.object)  # Obtener el contexto para el template
        return self.render_to_pdf_response(context)  # Generar la respuesta PDF
    
@method_decorator(login_required, name='dispatch')
class DetalleAvanceHistorial(DetailView):
    model=AvanceHistorial
    template_name='usuario/detalle_avance_historial.html'   
@method_decorator(login_required, name='dispatch')    
class GenerarAvanceHistorialPDF(DetailView):
    model = AvanceHistorial
    template_name = 'usuario/detalle_avance_pdf_template.html'

    def render_to_pdf_response(self, context):
        template_path = self.template_name
        
        # Crear la respuesta con tipo de contenido para PDF
        response = HttpResponse(content_type='application/pdf')
        
        # Obtener el objeto y usarlo para crear un nombre personalizado para el archivo PDF
        avance_historial = context.get('object')
        
        # Generar un nombre de archivo basado en el objeto AvanceHistorial
        if avance_historial:
            filename = f"{self.object.user}_formulario_avance.pdf"  # Usar el atributo relevante
        else:
            filename = "Avance_Historial.pdf"  # Nombre predeterminado en caso de falta de datos

        # Configurar el encabezado Content-Disposition para forzar la descarga con el nombre personalizado
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Renderizar el template a HTML y luego convertirlo a PDF
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verificar errores al generar el PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

    def get(self, request, *args, **kwargs):
        # Obtener el objeto AvanceHistorial
        self.object = self.get_object()  # Obtener el objeto correspondiente
        
        # Obtener el contexto
        context = self.get_context_data(object=self.object)  # Obtener el contexto para el template
        
        # Renderizar y devolver el PDF para descarga
        return self.render_to_pdf_response(context)
@method_decorator(login_required, name='dispatch')
class DetalleAvance2Historial(DetailView):
    model=Avance_2_Histoiral
    template_name='usuario/detalle_avance_2_historial.html'  
@method_decorator(login_required, name='dispatch')    
class GenerarAvanceHistorial_2_PDF(DetailView):
    model = Avance_2_Histoiral
    template_name = 'usuario/detalle_avance_2_pdf_template.html'

    def render_to_pdf_response(self, context):
        # Crear la respuesta como PDF
        response = HttpResponse(content_type='application/pdf')
        
        # Obtener el objeto del contexto para personalizar el nombre del archivo
        avance_2_historial = context.get('object')

        # Generar un nombre personalizado para el archivo PDF
        if avance_2_historial:
            filename = f"{self.object.user}_formulario_segundo_avance.pdf"  # Utilizar atributos del objeto
        else:
            filename = "Avance_Historial_2.pdf"  # Nombre predeterminado

        # Configurar el encabezado Content-Disposition para forzar la descarga con un nombre personalizado
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Renderizar el template para HTML y luego convertirlo a PDF
        template_path = self.template_name
        template = get_template(template_path)
        html = template.render(context)
        
        # Crear el PDF usando pisa
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Manejar errores durante la creación del PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)
        
        return response

    def get(self, request, *args, **kwargs):
        # Obtener el objeto Avance_2_Histoiral
        self.object = self.get_object()  # Obtener el objeto relacionado
        
        # Obtener el contexto para el template
        context = self.get_context_data(object=self.object)  # Obtener el contexto
        
        # Renderizar el PDF y devolver la respuesta para descarga
        return self.render_to_pdf_response(context)
@method_decorator(login_required, name='dispatch')
class DetalleAvance2(DetailView):
    model=Avance_2
    template_name='usuario/detalle_avance_2.html'  

@method_decorator(login_required, name='dispatch')    
class GenerarAvance_2PDF(DetailView):
    model = Avance_2
    template_name = 'usuario/detalle_avance_2_pdf_template.html'

    def render_to_pdf_response(self, context):
        # Obtener el objeto del contexto para personalizar el nombre del archivo
        avance_2 = context.get('object')

        # Crear la respuesta para PDF
        response = HttpResponse(content_type='application/pdf')

        # Generar un nombre personalizado para el archivo PDF
        if avance_2:
            filename = f"{self.object.user}_formulario_segundo_avance.pdf"  # Usar atributo relevante del modelo
        else:
            filename = "Avance_2_Report.pdf"  # Nombre predeterminado en caso de datos faltantes

        # Configurar el encabezado Content-Disposition para forzar la descarga con un nombre personalizado
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        # Renderizar el template a HTML y luego convertirlo a PDF
        template_path = self.template_name
        template = get_template(template_path)
        html = template.render(context)

        # Crear el PDF usando xhtml2pdf (pisa)
        pisa_status = pisa.CreatePDF(html, dest=response)

        # Verificar errores al generar el PDF
        if pisa_status.err:
            return HttpResponse('Error al generar el PDF', status=500)

        return response

    def get(self, request, *args, **kwargs):
        # Obtener el objeto Avance_2
        self.object = self.get_object()  # Obtener el objeto correspondiente
        
        # Obtener el contexto para el template
        context = self.get_context_data(object=self.object)  # Obtener el contexto necesario
        
        # Renderizar el PDF y devolver la respuesta para descarga
        return self.render_to_pdf_response(context)
@method_decorator(login_required, name='dispatch')
class DetalleAvance2(DetailView):
    model=Avance_2
    template_name='usuario/detalle_avance_2.html'   

@method_decorator(login_required, name='dispatch')
class FormularioAsistencia(DetailView):
    model=Maestrante
    template_name='usuario/formulario_asistencia.html'    
@method_decorator(login_required, name='dispatch')
class FormularioAsistenciaRealizada(DetailView):
    model=Maestrante
    template_name='usuario/formulario_asistencia_realizada.html'    
  
    
@method_decorator(login_required, name='dispatch')
class ListaCronograma(View):
    
    model=Cronograma
    template_name='usuario/cronograma.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        
        if  self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user__usuario=self.request.user)
        if self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1 or self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListaCronograma2(View):
    
    model=Cronograma2
    template_name='usuario/cronograma2.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        if  self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.user.maestrante)
        if  self.request.user.usuario_administrador:
            return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1 or self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')  
@method_decorator(login_required, name='dispatch')
class ListaActividades(View):
    
    model=Cronograma
    template_name='usuario/listar_actividades.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        
            return self.model.objects.filter()
      
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1 or self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class SeguimientoTesis(View):
    model= Requisitos   
    template_name='usuario/seguimiento_tesis.html'

    def get_queryset(self):
        if  self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 4:
            
            return self.model.objects.filter(requisito_habilitado=True).filter(rol1=True).filter(rol2=True).order_by('nro_requisito')
        if  self.request.user.tipo_usuario == 5:
            return self.model.objects.filter(requisito_habilitado=True).filter(rol3=True).order_by('nro_requisito')
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if   self.request.user.tipo_usuario == 3 or self.request.user.tipo_usuario == 5:
            return render(request,self.template_name,self.get_context_data())
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ActividadMaestranteGuia(View):
    model=Maestrante   
    template_name='usuario/actividad_maestrante_guia.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1:
            return render(request,self.template_name,self.get_context_data())

    
 
@method_decorator(login_required, name='dispatch')
class TesisPerfil(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_perfil.html'

@method_decorator(login_required, name='dispatch')
class TesisPerfilMejorado(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_perfil_mejorado.html'

@method_decorator(login_required, name='dispatch')
class TesisBorrador(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_borrador.html'
  
@method_decorator(login_required, name='dispatch')
class TesisMejorado(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_mejorado.html'
  
@method_decorator(login_required, name='dispatch')
class TesisAprobado(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_aprobado.html'

@method_decorator(login_required, name='dispatch')
class TesisOptimizado(DetailView):

    model = Maestrante
    template_name = 'usuario/tesis_optimizado.html'
   

def RegistroPerfilTesis(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES 
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.perfil_tesis=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis')
def RegistroPerfilMejorado(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES #returns a dict-like object
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.perfil_tesis_mejorado=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis')

def RegistroBorrador(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES #returns a dict-like object
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.borrador_tesis=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis')  

def RegistroTesisMejorado(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES #returns a dict-like object
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.tesis_mejorado=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis')  

def RegistroTesisAprobado(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES #returns a dict-like object
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.tesis_mejorado_aprobacion=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis')  






def RegistroTesisOptimizado(request,pk):
    if request.method =='POST':
        perfiltesis = request.FILES #returns a dict-like object
        doc_perfiltesis = perfiltesis['tesis']
        
        tesis = get_object_or_404(Maestrante,id_maestrante=pk)
        tesis.tesis_optimizado=doc_perfiltesis
        tesis.save()
    
    return redirect('usuario:listar_tesis') 



def DetalleInformeRevisor(request,pk):
    template_name="usuario/detalle_informe_revisor.html"
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    employers=InformeRevisor.objects.filter(user=activar)      
    context = { 'maestrantes':employers }
    return render(request,template_name,context) 

def DetalleInformeRevisorPDF(request, pk):
    maestrante = get_object_or_404(Maestrante, id_maestrante=pk)
    informes = InformeRevisor.objects.filter(user=maestrante)

    # Configurar el template y el contexto
    template_path = 'usuario/detalle_informe_revisor_pdf.html'
    context = {'maestrantes': informes}
    template = get_template(template_path)
    html = template.render(context)

    # Crear el archivo PDF
    response = HttpResponse(content_type='application/pdf')

    # Generar un nombre de archivo personalizado
    filename = f"{maestrante}_Informe_Revisor.pdf"  # Utiliza atributos del objeto para el nombre del archivo

    # Configurar el encabezado Content-Disposition para forzar la descarga con un nombre personalizado
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Generar el PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response
def DetalleInformeGuia(request,pk):
    template_name="usuario/detalle_informe_guia.html"
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    employers=InformeGuiaFormulario.objects.filter(user=activar)  
    
    context = { 'maestrantes':employers }
    return render(request,template_name,context) 

def DetalleInformeGuiaPDF(request, pk):
    # Obtenemos el objeto Maestrante y los informes correspondientes
    maestrante = get_object_or_404(Maestrante, id_maestrante=pk)  
    informes = InformeGuiaFormulario.objects.filter(user=maestrante)

    # Definimos el template y el contexto
    template_path = 'usuario/detalle_informe_guia_pdf.html'
    context = {'maestrantes': informes}
    template = get_template(template_path)
    html = template.render(context)

    # Creamos la respuesta como archivo PDF
    response = HttpResponse(content_type='application/pdf')

    # Creamos un nombre de archivo personalizado
    filename = f"{maestrante}_Informe_Guia.pdf"  # Nombre personalizado basado en el nombre del maestrante

    # Configuramos el encabezado Content-Disposition para forzar la descarga con el nombre personalizado
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Generamos el archivo PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificamos si hubo un error al crear el PDF
    if pisa_status.err:
        return HttpResponse('Error al generar el PDF', status=500)
    
    return response
def RegistrarInformeGuia(request,pk):
    template_name="usuario/registrar_informe_guia.html"
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    employers=InformeRevisor.objects.filter(user=activar)  
    
    context = { 'maestrantes':employers }
    return render(request,template_name,context) 


def EliminarPerfilTesis(request,pk):    
   
    tesis = get_object_or_404(Maestrante,id_maestrante=pk)
    tesis.perfil_tesis.delete()
            
    return redirect('usuario:listar_tesis_maestrante')  



def ProcedenteTema(request,pk):
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    activar.procedencia_tema=True
    activar.save()
    
    return redirect('usuario:listar_tesis_maestrante')
def ImProcedenteTema(request,pk):
    activar = get_object_or_404(Maestrante,id_maestrante=pk)   
    requisitos = get_object_or_404(Requisitos,nro_requisito=1)
    cronograma=get_object_or_404(Cronograma,user=activar.maestrante)
    
    cronograma.delete()
    
    activar.avance_tesis=1
   
    activar.docente_provicional=None
    activar.tema_tesis=None
    activar.tiempo=None
   
    activar.save()
    
    return redirect('usuario:seguimiento_tesis')

def QuitarLista(request,pk):
    activar = get_object_or_404(Maestrante,id_maestrante=pk)   
    activar.listacomunicacion=True   
    activar.save()
    
    return redirect('usuario:listado_tiempo')


@method_decorator(login_required, name='dispatch')
class RegistrarAvanceDocente(UpdateView):

    model = Avance
    template_name = 'usuario/registrar_avance.html'
    form_class = FormularioAvance
    success_url = reverse_lazy('usuario:listar_avance') 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioAvance(request.POST, instance=self.object)

        if form.is_valid():        
            

            notificar = BancoNotificacion.objects.get(numero_notificacion=9)
            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 

            cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
            if notificar.enviar:
                Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+", Docente guía: "+str(maestrante.guia),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
            maestrante.save()

            if notificar.enviar: 
                usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)

                for usuario in usuarios_administradores:
                    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+", Docente guía: "+str(maestrante.guia),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]")     
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    usuario.notificacion=True
                    usuario.save()
            requisitos = get_object_or_404(Requisitos,nro_requisito=8)  
            aprobo = form.cleaned_data['aprobacion']
            if aprobo == "si" :
                CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_avance1,fecha_realizado=timezone.now(),usuario=request.user,observacion="Formulario del primer avance aprobado - Docente guía : "+str(maestrante.guia))
            if aprobo == "no" :
                CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_avance1,fecha_realizado=timezone.now(),usuario=request.user,observacion="Formulario del primer avance sin aprobación - Docente guía : "+str(maestrante.guia))
            AvanceHistorial.objects.create(user=self.object.user,cap1=self.object.cap1,cap2=self.object.cap2,cap3=self.object.cap3,cap1_cualitativo=self.object.cap1_cualitativo,cap2_cualitativo=self.object.cap2_cualitativo,cap3_cualitativo=self.object.cap3_cualitativo,aprobacion=self.object.aprobacion,aceptar_avance=self.object.aceptar_avance ,fecha_programada=cronograma2.fecha_avance1, docete_guia=request.user)   
            self.object.docente=str(maestrante.guia)
            self.object.fecha_registro=timezone.now()
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)
     


@method_decorator(login_required, name='dispatch')
class RegistrarAvance2Docente(UpdateView):

    model = Avance_2
    template_name = 'usuario/registrar_avance_2.html'
    form_class = FormularioAvance2
    success_url = reverse_lazy('usuario:listar_avance_2') 
    def post(self, request, *args, **kwargs):       

        self.object = self.get_object()
        form = FormularioAvance2(request.POST, instance=self.object)

        if form.is_valid():        
            
            
            
            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 
            
            cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
            notificar = BancoNotificacion.objects.get(numero_notificacion=11)
            if notificar.enviar:
                Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+", Docente guía : "+str(maestrante.guia),maestrante=str(maestrante),programa=str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
                
                usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
                for usuario in usuarios_administradores:
                    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+", Docente guía : "+str(maestrante.guia),maestrante=str(maestrante),programa=str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]") 
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    usuario.notificacion=True
                    usuario.save()
            maestrante.save()       
            requisitos = get_object_or_404(Requisitos,nro_requisito=10)  
            aprobo = form.cleaned_data['aprobacion']
            if aprobo == "si" :
                CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_avance2,fecha_realizado=timezone.now(),usuario=request.user,observacion="Formulario del segundo avance aprobado - Docente guía : "+str(maestrante.guia))
            if aprobo == "no" :
                CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_avance2,fecha_realizado=timezone.now(),usuario=request.user,observacion="Formulario del segundo avance sin aprobación - Docente guía : "+str(maestrante.guia))
            Avance_2_Histoiral.objects.create(user=self.object.user,cap4=self.object.cap4,cap5=self.object.cap5,cap6=self.object.cap6,cap7=self.object.cap7, cap4_cualitativo=self.object.cap4_cualitativo,cap5_cualitativo=self.object.cap5_cualitativo,cap6_cualitativo=self.object.cap6_cualitativo,cap7_cualitativo=self.object.cap7_cualitativo,aprobacion=self.object.aprobacion,aceptar_avance=self.object.aceptar_avance,fecha_programada=cronograma2.fecha_avance2, docete_guia=request.user)   
            self.object.fecha=timezone.now()
            self.object.docente=str(maestrante.guia)
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)
     

def MaestranteEliminar(request,pk):
    paso = get_object_or_404(Maestrante,id_maestrante=pk)
    paso.bloqueo_maestrante=True
    paso.save()    
    return redirect('usuario:listado_maestrante_matricula')

def MaestranteHabilitar(request,pk):
    paso = get_object_or_404(Maestrante,id_maestrante=pk)
    paso.bloqueo_maestrante=False
    paso.save()    
    return redirect('usuario:listado_maestrante_matricula')


def DocenteEliminar(request,pk):
    paso = get_object_or_404(Docente,id_docente=pk)
    revisor = get_object_or_404(Docente_Revisor,user=paso.user)
    revisor.docente_activo=False
    revisor.save()
    paso.docente_activo=False
    paso.save()    
    return redirect('usuario:listar_docente')
def DocenteHabilitar(request,pk):
    paso = get_object_or_404(Docente,id_docente=pk)
    revisor = get_object_or_404(Docente_Revisor,user=paso.user)
    revisor.docente_activo=True
    revisor.save()
    paso.docente_activo=True
    paso.save()    
    return redirect('usuario:listar_docente')
def HabilitarNumero(request,pk):
    paso = get_object_or_404(Docente,id_docente=pk)
    paso.mostrar_numero=True
    paso.save()    
    return redirect('usuario:listar_docente')
def DeshabilitarNumero(request,pk):
    
    paso = get_object_or_404(Docente,id_docente=pk)
    paso.mostrar_numero=False
    paso.save()    
    return redirect('usuario:listar_docente')

def AsistenciaRealizada(request):
    if request.method =='POST':
        idmaestrante = request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)        
        cronograma = get_object_or_404(Cronograma,user=maestrante)
        cronograma.reunion_realizada = True
        fecha = request.POST['fecharealizada']
       
        hora = request.POST['horarealizada']
        enlace_reunion = request.POST['enlace']
        observaciones = request.POST['observacion']

        data = request.FILES
        if 'archivo' in data:
            documento_respaldo = request.FILES
            documentorespaldo = documento_respaldo['archivo']  
            AsistenciaInduccion.objects.create(maestrante= maestrante,
                fecha_asesoramiento=cronograma.fecha_induccion,
                                            hora_asesoramiento=cronograma.hora_induccion, 
                                            fecha_realizada = fecha,
                                            hora_realizada = hora,
                                            enlace_reunion = enlace_reunion,
                                            obs=observaciones,
                                            hoja_reunion=documentorespaldo  
                                                ) 
        else:
            AsistenciaInduccion.objects.create(maestrante= maestrante,
                fecha_asesoramiento=cronograma.fecha_induccion,
                                            hora_asesoramiento=cronograma.hora_induccion, 
                                            fecha_realizada = fecha,
                                            hora_realizada = hora,
                                            enlace_reunion = enlace_reunion,
                                            obs=observaciones 
                                                ) 
        cronograma.save()

        return redirect('usuario:seguimiento_tesis')  

def Asistencia(request):
    if request.method =='POST':
        idmaestrante = request.POST['id_maestrante']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        
        
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)
        
        cronograma = get_object_or_404(Cronograma,user=maestrante)
        cronograma.fecha_induccion = fecha
        cronograma.hora_induccion=hora
        cronograma.save()
        date_obj = datetime.strptime(fecha, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")

        notificar = BancoNotificacion.objects.get(numero_notificacion=99)
        if  notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(formatted_date)+" a horas: "+hora,maestrante=str(maestrante),programa=str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
        maestrante.save()
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,evidencia="Fecha programada de asesoramiento para la elaboración de perfil de tesis : "+str(formatted_date)+" a horas: "+hora) 
        return redirect('usuario:seguimiento_tesis')



#Actividad 13---------- Formulario para informe de docente revisor de tesis de maestría
@method_decorator(login_required, name='dispatch')    
class RegistrarInformeRevisor(DetailView):

    model = Informe
    template_name = 'usuario/registrar_informe_revisor.html'

@login_required()
def GuardarInformeRevisor(request):
    if request.method =='POST':
        idmaestrante = request.POST['id_maestrante'] 
        otras_obs = request.POST['otras_obs'] 
        capitulo = []     
        descripcion= []       
        sugerencia = []
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)
        maestrante.avance_tesis=14
        
        usuario_existe = InformeGuia.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            InformeGuia.objects.create(user=maestrante)
        informe = get_object_or_404(Informe,user=maestrante)
        informe.aceptar_revisor=True
        informe.otras_obs=otras_obs
        informe.docente=str(maestrante.revisor)
        informe.fecha_registro=timezone.now()
        informe.save()
        for date1 in request.POST.getlist('cap'):
            capitulo.append(date1)     

        for date3 in request.POST.getlist('desc'):
            descripcion.append(date3)
      
        for date5 in request.POST.getlist('sug'):
            sugerencia.append(date5)
        i=0
        for datos in capitulo:
            InformeRevisor.objects.create(user=maestrante,capitulo=capitulo[i],descripcion=descripcion[i],sugerencia=sugerencia[i])
            i += 1
   
        new_date=timezone.now()
        requisitos = get_object_or_404(Requisitos,nro_requisito=14)        
        
        con=1
        dia=1
        while con<=requisitos.tiempo:
            final_date=new_date+timedelta(days=dia)
            if final_date.weekday() == 5 or final_date.weekday() == 6:
                pass
            else:        
                con=con+1
            dia=dia+1

        cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
        cronograma2.fecha_formulario_guia=final_date
        cronograma2.save()
        requisitosd = get_object_or_404(Requisitos,nro_requisito=13) 
        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitosd,fecha_programada=cronograma2.fecha_formulario_revisor,fecha_realizado=timezone.now()) 
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=13)  
        if notificar.enviar:
            Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(maestrante.revisor),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente guía ]")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
            guia.notificacion=True
            guia.save()
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+",  Docente revisor : "+str(maestrante.revisor),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True

            usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(maestrante.revisor),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]")      
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=14)
        if notificar.enviar:
            Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version), cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente guía ]")            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
            guia.notificacion=True
            guia.save()
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")               
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
        maestrante.save()
    return redirect('usuario:listar_informe_revisor')

@method_decorator(login_required, name='dispatch')
class SegundoReporteGeneral(DetailView):
    model=Maestrante
    template_name="usuario/registrar_segundo_reporte_general.html" 
@login_required()
def RegistrarSegundoReporteGeneral(request):
    if request.method =='POST':
        idmaestrante = request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)        
        cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
        reportegeneral = get_object_or_404(ReporteGeneral,user=maestrante)
        reportegeneral.activar_reporte2 = True
        reportegeneral.save()
        fecha = request.POST['fecha']
    

        cronograma2.fecha_reporte_general2=fecha
        cronograma2.save()
       
        date_obj = datetime.strptime(fecha, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y") 
        notificar = BancoNotificacion.objects.get(numero_notificacion=92)
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True

            Post.objects.create(user=maestrante.revisor.user,title=notificar.titulo,text=notificar.contenido+" : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente revisor ]")   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            revisor = get_object_or_404(Usuario,username=maestrante.revisor.user.username)  
            revisor.notificacion=True
            revisor.save()
        maestrante.save()

        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,observacion="Se habilitó el segundo reporte general, fecha límite de presentación: "+str(formatted_date))
 
        return redirect('usuario:seguimiento_tesis')  


#Actividad 14---------- Formulario de informe final de docente guía y Tesis mejorada
@login_required()
def GuardarInformeGuia(request):
    
    if request.method =='POST':
        
        
        idmaestrante = request.POST['id_maestrante']
        if 'tesismejorada' in request.FILES:
            tesis_mejorada = request.FILES #returns a dict-like object
            doc_tesismejorada = tesis_mejorada['tesismejorada']

        else:
            doc_tesismejorada = None


        otras_obs = request.POST['otras_obs'] 
        capitulo = []
        descripcion= []
        opcion = []
        pagina = []
        funda = []
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)
        maestrante.avance_tesis = 15
        maestrante.tesis_mejorado=doc_tesismejorada
        
        informe = get_object_or_404(InformeGuia,user=maestrante)
        informe.aceptar_guia=True   
        informe.otras_obs=otras_obs  
        informe.fecha_registro=timezone.now()
        informe.docente=str(maestrante.guia)
        informe.save()


        for date1 in request.POST.getlist('cap'):
            capitulo.append(date1)

        for date2 in request.POST.getlist('desc'):
            descripcion.append(date2)

        for date3 in request.POST.getlist('opcion'):
            opcion.append(date3)

        for date4 in request.POST.getlist('pag'):
            pagina.append(date4)

        for date5 in request.POST.getlist('fun'):
            funda.append(date5)
        i=0
        for datos in capitulo:
            InformeGuiaFormulario.objects.create(user=maestrante,capitulo=capitulo[i],obs=descripcion[i],opcion=opcion[i],pagina=pagina[i],fundamentacion=funda[i])
            i += 1
        cronograma= get_object_or_404(Cronograma2,user=maestrante)
        requisitos = get_object_or_404(Requisitos,nro_requisito=14) 
        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,fecha_programada=cronograma.fecha_formulario_guia,fecha_realizado=timezone.now(),observacion="Adjunto documento de tesis mejorada",archivo_documento=doc_tesismejorada) 
        
        usuario_existe = ReporteGeneral.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            ReporteGeneral.objects.create(user=maestrante)
        notificar = BancoNotificacion.objects.get(numero_notificacion=15)
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
        
            usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]")  
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save() 
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=15) 
        new_date=timezone.now()
        con=1
        dia=1
        while con<=requisitos.tiempo:
            final_date=new_date+timedelta(days=dia)
            if final_date.weekday() == 5 or final_date.weekday() == 6:
                pass
            else:        
                con=con+1
            dia=dia+1
        
        cronograma.fecha_reporte_general=final_date
        cronograma.save()

        notificar = BancoNotificacion.objects.get(numero_notificacion=16)
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
                    
            Post.objects.create(user=maestrante.revisor.user,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente revisor ]")  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            revisor = get_object_or_404(Usuario,username=maestrante.revisor.user.username)  
            revisor.notificacion=True
            revisor.save()
        #usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
        #for usuario in usuarios_administradores:
        #    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
        maestrante.save()
    return redirect('usuario:listar_informe_guia')

    
#Actividad 15---------- Formulario de Reporte general
@method_decorator(login_required, name='dispatch')    
class RegistrarReporteGeneral(UpdateView):

    model = ReporteGeneral
    template_name = 'usuario/registrar_reporte_general.html'
    form_class = FormularioReporteGeneral
    success_url = reverse_lazy('usuario:listar_reporte_general') 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioReporteGeneral(request.POST, instance=self.object)

        if form.is_valid():        

            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 
            
            cronograma2= get_object_or_404(Cronograma2,user=maestrante)
            notificar = BancoNotificacion.objects.get(numero_notificacion=17)
            if notificar.enviar:
                Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+", Docente revisor: "+str(maestrante.revisor),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
                
                #Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version))  
                #channel_layer = get_channel_layer()
                #async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                #guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
                #guia.notificacion=True
                #guia.save()
                usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
                for usuario in usuarios_administradores:
                    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+", Docente revisor: "+str(maestrante.revisor),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]")  
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    usuario.notificacion=True
                    usuario.save()

            maestrante.save()
            CentroActividades.objects.create(maestrante=maestrante,fecha_realizado=timezone.now(),fecha_programada=cronograma2.fecha_reporte_general,usuario=request.user,observacion="Reporte general emitido : "+str(maestrante.revisor))
            self.object.fecha_registro=timezone.now()
            self.object.docente=str(maestrante.revisor)
            self.object = form.save()
            return redirect(self.get_success_url())

#Actividad 15---------- Formulario de Reporte general Segundo    
@method_decorator(login_required, name='dispatch')    
class RegistrarReporteGeneral2(UpdateView):

    model = ReporteGeneral
    template_name = 'usuario/registrar_reporte_general2.html'
    form_class = FormularioReporteGeneral2
    success_url = reverse_lazy('usuario:listado_segundo_reporte_general') 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioReporteGeneral2(request.POST, instance=self.object)

        if form.is_valid():        

            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 
            
            cronograma2= get_object_or_404(Cronograma2,user=maestrante)
            notificar = BancoNotificacion.objects.get(numero_notificacion=93)
            if notificar.enviar:
                Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ] ")  
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
                
                #Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente guía ] ")  
                #channel_layer = get_channel_layer()
                #async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                #guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
                #guia.notificacion=True
                #guia.save()
                usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
                for usuario in usuarios_administradores:
                    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Técnico-Coordinación de Investigación ]")  
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    usuario.notificacion=True
                    usuario.save()
            maestrante.save()
            requisitos = get_object_or_404(Requisitos,nro_requisito=15) 
            #CentroActividades.objects.create(maestrante=maestrante.maestrante,fecha_programada=cronograma2.fecha_reporte_general,usuario=request.user,evidencia=requisitos.actividad+" Emitido - Docente revisor : "+str(maestrante.revisor))
            CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_realizado=timezone.now(),fecha_programada=cronograma2.fecha_reporte_general2,usuario=request.user,observacion="Segundo reporte general emitido : "+str(maestrante.revisor))
            self.object.docente=str(maestrante.revisor)
            self.object.fecha_registro2 = timezone.now()
            form.save()
            return redirect(self.get_success_url())           
            


@method_decorator(login_required, name='dispatch')
class RegistrarProrrogaBorrador(DetailView):
    model=Maestrante
    template_name="usuario/registrar_prorroga_borrador.html"  
@login_required()
def ProrrogaBorrador(request):
    if request.method =='POST':
        idmaestrante = request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)        
        cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
        
        fecha = request.POST['fecha']
    

        cronograma2.fecha_borrador_prorroga=fecha
        cronograma2.save()
        date_obj = datetime.strptime(fecha, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,observacion="Maestrante habilitado para prorroga, fecha límite de presentación del borrador: "+str(formatted_date))
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=111)
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
        maestrante.save()
 

        return redirect('usuario:seguimiento_tesis')  


@method_decorator(login_required, name='dispatch')
class Act1Confirmar(DetailView):
    model=Maestrante
    template_name="usuario/act/act1_confirmar.html"  

@method_decorator(login_required, name='dispatch')
class RegistrarAct7obs(UpdateView):
    model = Maestrante
    form_class = FormularioTribunalPerfil
    second_form_class = FormularioFechaSustentacion
    template_name = 'usuario/act1_confirmar.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST, instance=self.object.tribunalperfil)
            context['form2'] = self.second_form_class(self.request.POST, instance=self.object.cronograma)
        else:
            context['form'] = self.form_class(instance=self.object.tribunalperfil)
            context['form2'] = self.second_form_class(instance=self.object.cronograma)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form = context['form']
        form2 = context['form2']
        if form.is_valid() and form2.is_valid():
            
            form.save()
            form2.save()
            self.adicional(self.object.pk)
        return super().form_valid(form)
    
    def adicional(self,pk):
        maestranteid = get_object_or_404(Maestrante,id_maestrante=pk)  
        #requisitos = get_object_or_404(Requisitos,nro_requisito=(maestranteid.avance_tesis+1))                
        CentroActividades.objects.create(maestrante=maestranteid.maestrante,usuario=self.request.user,fecha_programada=maestranteid.tiempo)
        maestranteid.listacomunicacion=False
        maestranteid.avance_tesis=5
        
        maestranteid.save()    



@login_required()
def busquedatesishistorial(request):


    
    if request.method =='GET'  :
        template_name="usuario/listar_sustentacion_tesis_historial.html"
        busmaes=request.GET["busmaestrante"]
     
        employers=SustentacionTesisHistorial.objects.filter(user__ru=busmaes)  
       
        context = { 'maestrantes':employers }
        return render(request,template_name,context) 
       
@login_required()
def BusquedaHistorial(request):


    
    if request.method =='GET'  :
        template_name="usuario/seguimiento_tesis_historial.html"
        busmaes=request.GET["busmaes"]
     
        employers=CentroActividades.objects.filter(maestrante__ci=busmaes).order_by('id_actividad')   
       
        context = { 'maestrantes':employers }
        return render(request,template_name,context) 

@login_required()
def BusquedaHistorialIndividual(request):

    if request.method =='GET'  :
        template_name="usuario/seguimiento_tesis_historial_m.html"
        busmaes=request.GET["busmaes"]
     
        employers=CentroActividades.objects.filter(maestrante__ru=busmaes).order_by('id_actividad')   
        avance = 4
        falta = 2
        
        #fechas_programadas = []
        #fechas = []
        #for evento in employers:
        #    if evento.fecha_programada:
        #        fechas_programadas.append(evento.fecha_programada.strftime('%Y-%m-%d'))
        #    else:
        #        fechas_programadas.append('')  # Otra opción es agregar una cadena vacía ('') en lugar de None

        #    if evento.fecha:
        #        fechas.append(evento.fecha.strftime('%Y-%m-%d'))
        #    else:
        #        fechas.append('')

    #   
    #    context = { 'maestrantes':employers }
    #    return render(request,template_name,context)          
        return render(request, template_name, {'avance': avance,'falta': falta, })
        #return render(request, template_name, {'fechas_programadas': fechas_programadas,  'fechas': fechas,})

    #return render(request, 'usuario/seguimiento_tesis_historial_m.html', {'data': data})    
    
def BusquedaAsistencia(request):
    if request.method =='GET':
        template_name="usuario/registrar_asistencia.html"
        busmaes=request.GET["busmaes"]
        employers=Maestrante.objects.filter(ru=busmaes)

        context = { 'maestrantes':employers }
        return render(request,template_name,context)
    
def BusquedaTesis(request):
    if request.method =='GET':
        template_name="usuario/listar_tesis_maestrante.html"
        busmaes=request.GET["busmaes"]
        employers=Maestrante.objects.filter(ru=busmaes)

        context = { 'maestrantes':employers }
        return render(request,template_name,context)



    return render(request,template_name,context)

def SeguimientoTesisActividades(request,seguimiento):
    
    employers=Maestrante.objects.filter(avance_tesis=seguimiento).filter(maestrante_habilitado=True) 
    if seguimiento == 0: 
        template_name = 'usuario/act/act0.html'
    elif seguimiento == 1: 
        template_name = 'usuario/act/act1.html'
    elif seguimiento == 2: 
        template_name = 'usuario/act/act2.html'
    elif seguimiento == 3: 
        template_name = 'usuario/act/act3.html'
    elif seguimiento == 4: 
        template_name = 'usuario/act/act4.html'
    elif seguimiento == 5: 
        template_name = 'usuario/act/act5.html'
    elif seguimiento == 6: 
        template_name = 'usuario/act/act6.html'
    elif seguimiento == 7: 
        template_name = 'usuario/act/act7.html'
    elif seguimiento == 8: 
        template_name = 'usuario/act/act8.html'
    elif seguimiento == 9: 
        template_name = 'usuario/act/act9.html'
    elif seguimiento == 10: 
        template_name = 'usuario/act/act10.html'
    elif seguimiento == 11: 
        template_name = 'usuario/act/act11.html'
    elif seguimiento == 12: 
        template_name = 'usuario/act/act12.html'
    elif seguimiento == 13: 
        template_name = 'usuario/act/act13.html'
    elif seguimiento == 14: 
        template_name = 'usuario/act/act14.html'
    elif seguimiento == 15: 
        template_name = 'usuario/act/act15.html'
    elif seguimiento == 16: 
        template_name = 'usuario/act/act16.html'     
    elif seguimiento == 17: 
        template_name = 'usuario/act/act17.html'      
    elif seguimiento == 18: 
        template_name = 'usuario/act/act18.html'    
    elif seguimiento == 19: 
        template_name = 'usuario/act/act19.html' 
    elif seguimiento == 20: 
        template_name = 'usuario/act/act20.html' 
    elif seguimiento == 21: 
        template_name = 'usuario/act/act21.html' 
    elif seguimiento == 22: 
        template_name = 'usuario/act/act22.html' 
    elif seguimiento == 23: 
        template_name = 'usuario/act/act23.html' 
    elif seguimiento == 24: 
        template_name = 'usuario/act/act24.html' 
    elif seguimiento == 25: 
        template_name = 'usuario/act/act25.html' 
    actividad=Requisitos.objects.filter(nro_requisito=seguimiento)   
    context = { 'maestrantesevi':employers,'actividad':actividad,"today":date.today() } 
   
    return render(request,template_name,context)

   
@login_required()
def Busqueda(request):
    if request.user.usuario_administrador: 
        template_name = 'usuario/act/act.html'       
        busmaestrantetexto = request.GET.get("userId")
        busmaestrante = request.GET.get("busmaestrante") 
        if busmaestrante:                
            try:
                
                usuario = Usuario.objects.get(ci_usuario=busmaestrante)
                employers=Maestrante.objects.filter(usuario=usuario)
                context = { 'maestrantesevi':employers}
                return render(request,template_name,context)
           
            except Usuario.DoesNotExist:
            
                return HttpResponseForbidden('Error, El usuario seleccionado no es maestrante, favor de verificar los datos.')    
             
        elif busmaestrantetexto:                
            try:
                
                usuario = Usuario.objects.get(id=busmaestrantetexto)
                employers=Maestrante.objects.filter(usuario=usuario)
                context = { 'maestrantesevi':employers}
                return render(request,template_name,context)
           
            except Usuario.DoesNotExist:
            
                return HttpResponseForbidden('Error, El usuario seleccionado no es maestrante, favor de verificar los datos.')    
        else :
            return HttpResponseForbidden('Error, verifique los datos')


       
    return HttpResponseForbidden('Error')
@login_required()
def BusquedaCentroActividad(request):
    if request.user.usuario_administrador: 
        template_name = 'usuario/seguimiento_historial.html'       
        busmaestrantetexto = request.GET.get("userId")
        busmaestrante = request.GET.get("busmaestrante") 
        
        if busmaestrante:                
            try:
                usuario = Usuario.objects.get(ci_usuario=busmaestrante)
                employers=Maestrante.objects.filter(usuario=usuario)
                context = { 'maestrantesevi':employers}
                return render(request, template_name, context)
           
            except Usuario.DoesNotExist:
                return HttpResponseForbidden('Error, El usuario seleccionado no es maestrante, favor de verificar los datos.')    
             
        if busmaestrantetexto:                
            try:
                usuario = Usuario.objects.get(id=busmaestrantetexto)
                employers=Maestrante.objects.filter(usuario=usuario)
                context = { 'maestrantesevi':employers}
                return render(request, template_name, context)
           
            except Usuario.DoesNotExist:
                return HttpResponseForbidden('Error, El usuario seleccionado no es maestrante, favor de verificar los datos.')    
        
        # Respuesta predeterminada si ninguno de los casos anteriores se cumple
        return HttpResponseForbidden('Error, No se proporcionaron datos de usuario válidos')

@login_required()
def BusquedaHistorialVarios(request):
    if request.user.usuario_administrador:        
        busmaestrantetexto = request.GET.get("userId")
        busmaestrante = request.GET.get("busmaestrante")      
        if busmaestrantetexto:                
            try:
                maestrante = Maestrante.objects.get(id_maestrante=busmaestrantetexto)
                busmaestrante = maestrante.ru
            except Usuario.DoesNotExist:
                # Manejar el caso en el que no se encuentra un usuario con el ID especificado
                return HttpResponseForbidden('Error, El usuario seleccionado no es maestrante, favor de verificar los datos.')    
            employers=Maestrante.objects.filter(ru=busmaestrante).filter(maestrante_habilitado=True)        
            template_name = 'usuario/act/act.html'
            context = { 'maestrantesevi':employers}
            return render(request,template_name,context)
        else:
        
            return HttpResponseForbidden('Error, verifique los datos')

    return HttpResponseForbidden('Error')   


@method_decorator(login_required, name='dispatch')
class CronogramaMaestrante(DetailView):
    model=Cronograma
    template_name='usuario/maestrante_cronograma.html'     

#@login_required()
#def CronogramMaestrante(request,pk):    
#    cronograma = Cronograma.objects.filter(id_cronograma=pk)   
#    template_name = 'usuario/maestrante_cronograma.html'
#    context = { 'cronograma':cronograma }
#    return render(request,template_name,context)

@method_decorator(login_required, name='dispatch')
class CronogramaMaestrante2(DetailView):
    model=Cronograma2
    template_name='usuario/maestrante_cronograma2.html'  

#@login_required()
#def CronogramMaestrante2(request,pk):    
#    cronograma = Cronograma2.objects.filter(id_cronograma=pk)   
#    template_name = 'usuario/maestrante_cronograma2.html'
#    context = { 'cronograma2':cronograma }
#    return render(request,template_name,context)

@login_required()
def CronogramMaestranteIndividual(request):    
    cronograma = Cronograma.objects.filter(user__usuario=request.user)
    cronograma2 = Cronograma2.objects.filter(user__usuario=request.user)
    
   
    template_name = 'usuario/maestrante_cronograma_individual.html'
    context = { 'cronograma':cronograma,'cronograma2':cronograma2 }
    return render(request,template_name,context)

@login_required()
def BusquedaVariosHistorial(request,pk,ci_usuario):
    programa = get_object_or_404(Programa,id_programa=pk)
    usuario = get_object_or_404(Usuario,ci_usuario=ci_usuario)
   
    if request.user.usuario_administrador:
        
        employers=CentroActividades.objects.filter(maestrante__programa=programa).filter(maestrante__usuario=usuario)
        template_name = 'usuario/seguimiento_tesis_historial.html'
        if employers:
            context = { 'maestrantes':employers }
        else:
        
            return HttpResponseForbidden('El maestrante no realizó actividad')
        return render(request,template_name,context)
    return HttpResponseForbidden('Error')
  
@login_required()
def BusquedaVarios(request,pk):

    if request.user.usuario_administrador:
        
        employers=Maestrante.objects.filter(id_maestrante=pk).filter(maestrante_habilitado=True)
        
        template_name = 'usuario/act/act.html'
        if employers:
        
            paso = get_object_or_404(Maestrante,id_maestrante=pk)
            if paso.avance_tesis == 0: 
                template_name = 'usuario/act/act0.html'
            elif paso.avance_tesis == 1: 
                template_name = 'usuario/act/act1.html'
            elif paso.avance_tesis == 2: 
                template_name = 'usuario/act/act2.html'
            elif paso.avance_tesis == 3: 
                template_name = 'usuario/act/act3.html'
            elif paso.avance_tesis == 4: 
                template_name = 'usuario/act/act4.html'
            elif paso.avance_tesis == 5: 
                template_name = 'usuario/act/act5.html'
            elif paso.avance_tesis == 6: 
                template_name = 'usuario/act/act6.html'                 
            elif paso.avance_tesis == 7: 
                template_name = 'usuario/act/act7.html'  
            elif paso.avance_tesis == 8: 
                template_name = 'usuario/act/act8.html'  
            elif paso.avance_tesis == 9: 
                template_name = 'usuario/act/act9.html'  
            elif paso.avance_tesis == 10: 
                template_name = 'usuario/act/act10.html' 
            elif paso.avance_tesis == 11: 
                template_name = 'usuario/act/act11.html' 
            elif paso.avance_tesis == 12: 
                template_name = 'usuario/act/act12.html' 
            elif paso.avance_tesis == 13: 
                template_name = 'usuario/act/act13.html' 
            elif paso.avance_tesis == 14: 
                template_name = 'usuario/act/act14.html'                 
            elif paso.avance_tesis == 15: 
                template_name = 'usuario/act/act15.html'  
            elif paso.avance_tesis == 16: 
                template_name = 'usuario/act/act16.html'  
            elif paso.avance_tesis == 17: 
                template_name = 'usuario/act/act17.html'  
            elif paso.avance_tesis == 18: 
                template_name = 'usuario/act/act18.html'  
            elif paso.avance_tesis == 19: 
                template_name = 'usuario/act/act19.html'                
            elif paso.avance_tesis == 20: 
                template_name = 'usuario/act/act20.html'  
            elif paso.avance_tesis == 21: 
                template_name = 'usuario/act/act21.html' 
            elif paso.avance_tesis == 22: 
                template_name = 'usuario/act/act22.html' 
            elif paso.avance_tesis == 23: 
                template_name = 'usuario/act/act23.html'  
            elif paso.avance_tesis == 24: 
                template_name = 'usuario/act/act24.html' 
            elif paso.avance_tesis == 25: 
                template_name = 'usuario/act/act25.html'              
              
            mensaje=""
            if request.user.tipo_usuario == 3:
                mensaje="El maestrante se encuentra en una actividad que esta a cargo de Coordinación de Postgrado"

            if request.user.tipo_usuario == 5:
                mensaje="El maestrante se encuentra en una actividad que esta a cargo de Tecnico de Postgrado/Coordinación de investigación"

            if request.user.tipo_usuario == 3:               
                actividad=Requisitos.objects.filter(nro_requisito=paso.avance_tesis).filter(rol1=True)

            elif request.user.tipo_usuario == 4:               
                actividad=Requisitos.objects.filter(nro_requisito=paso.avance_tesis).filter(rol2=True)                
               
            elif request.user.tipo_usuario == 5:                             
                actividad=Requisitos.objects.filter(nro_requisito=paso.avance_tesis).filter(rol3=True)
               
            if actividad:
                context = { 'maestrantesevi':employers,'actividad':actividad ,"today":date.today() }
            else:
                context = { 'mensaje':mensaje}              
            
            return render(request,template_name,context)

        else:
        
            return HttpResponseForbidden('Error, verifique los datos')

    return HttpResponseForbidden('Error')
  

import subprocess
from django.http import HttpResponse
from django.shortcuts import render
from .forms import BackupForm
from pathlib import Path

def backup_database(request):
    if request.method == 'POST':
        form = BackupForm(request.POST)
        if form.is_valid():
            output_directory = form.cleaned_data['output_directory']
            output_filename = form.cleaned_data['output_filename']

            # Valida si se proporciona un directorio personalizado y un nombre de archivo
            if output_directory and output_filename:
                output_path = Path(output_directory) / output_filename
            else:
                # Si no se proporciona, utiliza una ubicación y un nombre predeterminados
                output_path = Path("/ruta/del/archivo/de/salida.sql")

            # Ejecuta la copia de seguridad en la ubicación especificada
            cmd = f"pg_dump -U postgres -d dbpostgrado -f {output_path}"
            subprocess.run(cmd, shell=True)

            return HttpResponse("Copia de seguridad realizada con éxito.")

    else:
        form = BackupForm()

    return render(request, 'usuario/backup_form.html', {'form': form})



from django.shortcuts import render
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def enviar_mensaje_por_defecto(request):
    # Obtén el nombre de la sala y el mensaje por defecto
    room_name = 'docente'  # Reemplaza 'tu_sala' con el nombre de tu sala real
    message = '¡Este es un mensaje por defecto!'

    # Envia el mensaje por defecto usando el canal de Django Channels
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'chat_{room_name}',
        {
            'type': 'chat_message',
            'message': message,
            'username': 'System'  # Puedes personalizar el nombre del remitente
        }
    )
    return JsonResponse({'status': 'Mensaje por defecto enviado'})




def search_users(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query', '')

        # Filter Usuario objects based on nombre_usuario containing the query string
        maestrantes = Usuario.objects.filter(
            Q(nombre_usuario__icontains=query)
        )

        # Construct a list of dictionaries containing id_maestrante and username
        results = [{'id_maestrante': maestrante.id, 'username': maestrante.nombre_completo()} 
                   for maestrante in maestrantes]

        return JsonResponse(results, safe=False)
    return JsonResponse({}, status=400)



