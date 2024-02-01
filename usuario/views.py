from typing import Any, Dict, Optional
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.utils import timezone
import time
from django.http import JsonResponse
from datetime import datetime

from .forms import FormularioReporteGeneralTribunalInterno,FormularioBancoNotificacion,FormularioPrograma,FormularioAvance2,FormularioTribunalTesis,FormularioTribunalPerfil,FormularioCronograma2,FormularioEvidencia,FormularioUsuarioDocente,FormularioUsuarioMaestrante,FormularioAvance,FormularioDocenteProvisional,FormularioTesisOptimizado,FormularioTesisMejoradoAprobacion,FormularioTesisMejorado,FormularioPerfilTesisMejorado,FormularioBorradorTesis,FormularioPerfilTesis,FormularioTemaTesis,FormularioReporteGeneral2,FormularioReporteGeneral,FormularioCronograma,FormularioFechaSustentacion,FormularioAdministradores,FormularioMaestranteGuia
from usuario.models import ReporteGeneralTribunalInterno,DocenteProvisional,SustentacionTesisHistorial,BancoNotificacion,Programa,AvanceHistorial,Avance_2_Histoiral,Avance_2,Cronograma2,SustentacionPerfilHistorial,TribunalPerfil,TribunalTesis,InformeGuiaFormulario,InformeGuia,InformeRevisor,Post,Requisitos1,Administracion,AsistenciaInduccion,Avance,Informe,ReporteGeneral,Requisitos,Cronograma,CentroActividades,Docente_Revisor,Docente,ActividadesMaestrante,Usuario,Maestrante
from room.models import Room 
from django.views.generic import View,TemplateView,UpdateView, CreateView,DeleteView,DetailView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from datetime import date,datetime,timedelta
from django.core import serializers
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import random
import string

from .forms import CustomPasswordResetForm
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.views import PasswordResetView



class CustomPasswordResetView(PasswordResetView):
    
    form_class = CustomPasswordResetForm

    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        email = self.request.POST.get('correo_inst')
        print(email)
        if username and email:
            user = self.get_form().get_users(email, username).first()
            
            if user is not None:
                self.user = user
                form = self.get_form() 
                
                if form.is_valid():  
                   
                    return self.form_valid(form)
                else:
                    print(form.errors)
                    self.extra_context = {'CamposVacios': True}
            else:
                self.extra_context = {'Nousuario': True}  # Agregamos token_expired al contexto
                return super().form_invalid(self.get_form())
        return self.form_invalid(self.get_form())

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        email = self.request.POST.get('correo_inst')
        username = self.request.POST.get('username')
        context['user'] = user
 
        # Valida que al menos se proporcione un email o un nombre de usuario
        if not email and not username:
            return

        user = None

        if email:
        
            users_by_email = CustomPasswordResetForm().get_users(email)

            if users_by_email.count() > 0:
                user = users_by_email[0]

        if username and not user:
            user_by_username = get_user_model()._default_manager.filter(
                username=username,
                is_active=True
            )

            if user_by_username.count() > 0:
                user = user_by_username[0]

        if user is not None and user.is_active:
            super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)
def enviar_correo_electronico(asunto, mensaje, destinatarios):
    send_mail(asunto, mensaje, 'pedroperespereira2023@hotmail.com', destinatarios, fail_silently=False)

def generar_password(longitud):
    caracteres = string.ascii_letters + string.digits
    password = ''.join(random.choice(caracteres) for _ in range(longitud))
    return password
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')
class ListadoMaestrante(View):
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')
class ListadoMaestranteGraduado(View):
    model=Maestrante
    template_name='usuario/listar_maestrante_tesis_concluido.html'
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoPostulante(View):
    model=Maestrante
    template_name='usuario/listar_postulante.html'
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
    
@method_decorator(login_required, name='dispatch')
class ListadoSustentacionPerfilHistorial(View):
    model=SustentacionPerfilHistorial
    template_name='usuario/listar_sustentacion_perfil_historial.html'
    def get_queryset(self):        
            return self.model.objects.all().order_by('-id_sustentacion')
        
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        return self.model.objects.all().order_by('-fecha')
 
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
        if self.request.user.is_staff or self.request.user.tipo_usuario == 1:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoAdministradores(View):
    model=Usuario
    template_name='usuario/listar_administradores.html'
    context_object_name = 'actividades'

    def get_queryset(self):
        return self.model.objects.exclude(tipo_usuario = 1 ).exclude(tipo_usuario = 2 )
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == None:
            return render(request,self.template_name,self.get_context_data())
        return HttpResponseForbidden('Error')

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneral(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if self.request.user.is_staff:
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
class ListadoReporteGeneralTribunalInterno(View):
    model=ReporteGeneralTribunalInterno
    template_name='usuario/listar_reporte_general_tribunal_interno.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if self.request.user.is_staff:
           
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
            
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 1:
            
            return self.model.objects.filter()
        
 
 
    def get_context_data(self, **kwargs):
        contexto={}
        
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):

        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoReporteGeneralGuia(View):
    model=ReporteGeneral
    template_name='usuario/listar_reporte_general.html'
    context_object_name = 'actividades'
   
    def get_queryset(self):
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
class ListadoInformeGuiaPendiente(View):
    model=InformeGuia
    template_name='usuario/listar_informe_guia.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_guia=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListadoInformeGuiaRealizado(View):
    model=InformeGuia
    template_name='usuario/listar_informe_guia.html'
    context_object_name = 'actividades'
    def get_queryset(self):
        if self.request.user.is_staff:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_guia=True)
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
        if self.request.user.is_staff:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor)
    
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
        if self.request.user.is_staff:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=False)
    
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
        if self.request.user.is_staff:
            return self.model.objects.filter()            
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__revisor=self.request.user.docente_revisor).filter(aceptar_revisor=True)
    
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())
       
    
class InformacionGeneral(TemplateView):
    template_name = 'usuario/informacion_general.html'
# *************** Registro de usuarios *******************.

@method_decorator(login_required, name='dispatch')
class RegistrarDocente(CreateView):
    model=Usuario
    form_class=FormularioUsuarioDocente
    template_name='usuario/agregar_docente.html'
    success_url = reverse_lazy('usuario:listar_docente')
    def form_valid(self, form):
        try:
            ci_usuario = form.cleaned_data.get('ci_usuario')
            if Usuario.objects.filter(username=ci_usuario).exists():
                # Agregar un distintivo (por ejemplo, un número)
                i = 1
                while Usuario.objects.filter(username=f'{ci_usuario}_{i}').exists():
                    i += 1
                username = f'{ci_usuario}_{i}'
            else:
                username = ci_usuario
            
    
            form.instance.username = username
            
            contrasena_generada = generar_password(15)
            form.instance.set_password(contrasena_generada)


            asunto = 'Activación de cuanta'
            mensaje = 'Se activó la cuenta del Sitema de Seguimiento y Control de Tesis de Postgrado. Su usuario para el inicio de sesión es: '+ str(username)   + ' La contraseña es: '+str (contrasena_generada)
            
            destinatarios = [form.cleaned_data.get('correo_inst')]

            enviar_correo_electronico(asunto, mensaje, destinatarios)

            response = super().form_valid(form)
            usuario_docente = self.object
            DocenteProvisional.objects.create(user=usuario_docente)
            Docente_Revisor.objects.create(user=usuario_docente)
            
        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

        return response
    

@method_decorator(login_required, name='dispatch')
class RegistrarPrograma(CreateView):
    model=Programa
    form_class=FormularioPrograma
    template_name='usuario/agregar_programa.html'
    success_url = reverse_lazy('usuario:listar_programa')
 


        
    
@method_decorator(login_required, name='dispatch')
class RegistrarMaestrante(CreateView):
    model=Usuario
    form_class = FormularioUsuarioMaestrante
    template_name='usuario/agregar_maestrante.html'
    success_url = reverse_lazy('usuario:listar_postulante') 
    def form_valid(self, form):
        try:

            ci_usuario = form.cleaned_data.get('ci_usuario')
            if Usuario.objects.filter(username=ci_usuario).exists():
                # Agregar un distintivo (por ejemplo, un número)
                i = 1
                while Usuario.objects.filter(username=f'{ci_usuario}_{i}').exists():
                    i += 1
                username = f'{ci_usuario}_{i}'
            else:
                username = ci_usuario
            
    
            form.instance.username = username
            
            contrasena_generada = generar_password(15)
            form.instance.set_password(contrasena_generada)


            asunto = 'Activación de cuanta'
            mensaje = 'Se activó la cuenta del Sitema de Seguimiento y Control de Tesis de Postgrado. Su usuario para el inicio de sesión es: '+ str(username)   + ' La contraseña es: '+str (contrasena_generada)
            
            destinatarios = [form.cleaned_data.get('correo_inst')]

            enviar_correo_electronico(asunto, mensaje, destinatarios)

            response = super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

        return response


@method_decorator(login_required, name='dispatch')
class RegistrarAdministradores(CreateView):
    model=Usuario
    form_class=FormularioAdministradores
    template_name='usuario/agregar_administradores.html'
    success_url = reverse_lazy('usuario:listar_administradores')
    def form_valid(self, form):              

        try:
            form.instance.is_staff = True
            ci_usuario = form.cleaned_data.get('ci_usuario')
            if Usuario.objects.filter(username=ci_usuario).exists():
                # Agregar un distintivo (por ejemplo, un número)
                i = 1
                while Usuario.objects.filter(username=f'{ci_usuario}_{i}').exists():
                    i += 1
                username = f'{ci_usuario}_{i}'
            else:
                username = ci_usuario
            
    
            form.instance.username = username
            
            contrasena_generada = generar_password(15)
            form.instance.set_password(contrasena_generada)


            asunto = 'Activación de cuanta'
            mensaje = 'Se activó la cuenta del Sitema de Seguimiento y Control de Tesis de Postgrado. Su usuario para el inicio de sesión es: '+ str(username)   + ' La contraseña es: '+str (contrasena_generada)
            
            destinatarios = [form.cleaned_data.get('correo_inst')]

            enviar_correo_electronico(asunto, mensaje, destinatarios)

            response = super().form_valid(form)
        except Exception as e:
            messages.error(self.request, f"Error durante el registro: {str(e)}")
            return self.render_to_response(self.get_context_data(form=form))

        return response

   




# *************** Actualizar datos de usuarios *******************.

@method_decorator(login_required, name='dispatch')
class ActualizarPrograma(UpdateView):

    model = Programa
    template_name = 'usuario/editar_programa.html'
    form_class = FormularioPrograma
    success_url = reverse_lazy('usuario:listar_programa')    


@method_decorator(login_required, name='dispatch')
class ActualizarAdministrador(UpdateView):

    model = Usuario
    template_name = 'usuario/editar_usuario.html'
    form_class = FormularioAdministradores
    success_url = reverse_lazy('usuario:listar_administradores')    




#administrar archivos de tesis vista tecnico---------------------
@method_decorator(login_required, name='dispatch')
class EditarPerfilTesis(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_perfil_tesis.html'
    form_class = FormularioPerfilTesis
    success_url = reverse_lazy('usuario:listar_tesis_maestrante') 
    


@method_decorator(login_required, name='dispatch')

class EditarPerfilMejorado(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_perfil_mejorado.html'
    form_class = FormularioPerfilTesisMejorado
    success_url = reverse_lazy('usuario:listar_tesis_maestrante') 

@method_decorator(login_required, name='dispatch')
class EditarBorradorTesis(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_borrador_tesis.html'
    form_class = FormularioBorradorTesis
    success_url = reverse_lazy('usuario:listar_tesis_maestrante') 

@method_decorator(login_required, name='dispatch')
class EditarTesisMejorado(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_tesis_mejorado.html'
    form_class = FormularioTesisMejorado
    success_url = reverse_lazy('usuario:listar_tesis_maestrante') 

@method_decorator(login_required, name='dispatch')   
class EditarTesisAprobacion(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_tesis_aprobacion.html'    
    form_class = FormularioTesisMejoradoAprobacion
    success_url = reverse_lazy('usuario:listar_tesis_maestrante') 

@method_decorator(login_required, name='dispatch')
class EditarTesisOptimizado(UpdateView):

    model = Maestrante
    template_name = 'usuario/editar_tesis_optimizado.html'
    form_class = FormularioTesisOptimizado
    success_url = reverse_lazy('usuario:listar_tesis_maestrante')   

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
class Actividades_Maestrante(View):
    
    model=ActividadesMaestrante
    template_name='usuario/actividades_maestrante.html'
    context_object_name = 'actividadess'
    queryset = ActividadesMaestrante.objects.filter()
    
    def get_queryset(self):
        return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividadess']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if self.request.user.tipo_usuario == 1:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')


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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
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
        if self.request.user.is_staff:
            return render(request,self.template_name,self.get_context_data())
            
        return HttpResponseForbidden('Error')
@method_decorator(login_required, name='dispatch')
class ListarAvance(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.is_staff:
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
class ListarAvancePendiente(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.is_staff:
            return self.model.objects.filter()
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):       
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvanceRealizado(View):
    
    model=Avance
    template_name='usuario/listar_avance.html'
    context_object_name = 'actividades'
    def get_queryset(self):            
        if self.request.user.is_staff:
            return self.model.objects.filter()
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
        if self.request.user.is_staff:
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
class ListarAvance2Pendiente(View):
    
    model=Avance_2
    template_name='usuario/listar_avance_2.html'
    context_object_name = 'actividades'
    def get_queryset(self):     
        if self.request.user.is_staff:
            return self.model.objects.filter()       
        if self.request.user.tipo_usuario == 2:
            return self.model.objects.filter(user__guia=self.request.user.docente).filter(aceptar_avance=False)
        if self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.maestrante)
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        return render(request,self.template_name,self.get_context_data())

@method_decorator(login_required, name='dispatch')
class ListarAvance2Realizado(View):
    
    model=Avance_2
    template_name='usuario/listar_avance_2.html'
    context_object_name = 'actividades'
    def get_queryset(self):     
        if self.request.user.is_staff:
            return self.model.objects.filter()       
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
class DetalleReporte(DetailView):
    model=ReporteGeneral
    template_name='usuario/detalle_reporte.html'    

@method_decorator(login_required, name='dispatch')
class DetalleReporte2(DetailView):
    model=ReporteGeneral
    template_name='usuario/detalle_reporte2.html'   
@method_decorator(login_required, name='dispatch')
class DetalleReporteSegundaInstancia(DetailView):
    model=ReporteGeneralTribunalInterno
    template_name='usuario/detalle_reporte_segunda_instancia.html'   

@method_decorator(login_required, name='dispatch')
class DetalleAvance(DetailView):
    model=Avance
    template_name='usuario/detalle_avance.html'    
@method_decorator(login_required, name='dispatch')
class DetalleAvance2(DetailView):
    model=Avance_2
    template_name='usuario/detalle_avance_2.html'  
@method_decorator(login_required, name='dispatch')
class DetalleAvance2(DetailView):
    model=Avance_2
    template_name='usuario/detalle_avance_2.html'   

@method_decorator(login_required, name='dispatch')
class FormularioAsistencia(DetailView):
    model=Maestrante
    template_name='usuario/formulario_asistencia.html'    
 
    
@method_decorator(login_required, name='dispatch')
class ListaCronograma(View):
    
    model=Cronograma
    template_name='usuario/cronograma.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        
        if  self.request.user.tipo_usuario == 1:
            return self.model.objects.filter(user=self.request.user.maestrante)
        if  self.request.user.is_staff:
            return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1 or self.request.user.is_staff:
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
        if  self.request.user.is_staff:
            return self.model.objects.filter()
 
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['actividades']=self.get_queryset()
        return contexto

    def get(self,request,**kwargs):
        if  self.request.user.tipo_usuario == 1 or self.request.user.is_staff:
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
        if  self.request.user.tipo_usuario == 1 or self.request.user.is_staff:
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
        if  self.request.user.is_staff:
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
    employers=InformeRevisor.objects.filter(user=activar.maestrante)  
    
    context = { 'maestrantes':employers }
    return render(request,template_name,context) 

def DetalleInformeGuia(request,pk):
    template_name="usuario/detalle_informe_guia.html"
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    employers=InformeGuiaFormulario.objects.filter(user=activar.maestrante)  
    
    context = { 'maestrantes':employers }
    return render(request,template_name,context) 

def RegistrarInformeGuia(request,pk):
    template_name="usuario/registrar_informe_guia.html"
    activar = get_object_or_404(Maestrante,id_maestrante=pk)
    employers=InformeRevisor.objects.filter(user=activar.maestrante)  
    
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
            
            AvanceHistorial.objects.create(user=self.object.user,cap1=self.object.cap1,cap2=self.object.cap2,cap3=self.object.cap3,cap4=self.object.cap4,cap5=self.object.cap5,aprobacion=self.object.aprobacion,aceptar_avance=self.object.aceptar_avance)   
            notificar = BancoNotificacion.objects.get(numero_notificacion=9)
            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 

            cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
            Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente guía : "+str(maestrante.guia))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
            maestrante.save() 
            usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)

            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente guía : "+str(maestrante.guia))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
            CentroActividades.objects.create(maestrante=maestrante.maestrante,fecha_programada=cronograma2.fecha_avance1,usuario=request.user,evidencia=notificar.contenido+" - Docente guía : "+str(maestrante.guia))
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
            
            AvanceHistorial.objects.create(user=self.object.user,cap1=self.object.cap1,cap2=self.object.cap2,cap3=self.object.cap3,cap4=self.object.cap4,cap5=self.object.cap5,aprobacion=self.object.aprobacion,aceptar_avance=self.object.aceptar_avance)   
            notificar = BancoNotificacion.objects.get(numero_notificacion=11)
            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 
            
            cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
            notificar = BancoNotificacion.objects.get(numero_notificacion=11)
            Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente guía : "+str(maestrante.guia))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
            maestrante.save()
            usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente guía : "+str(maestrante.guia))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
            CentroActividades.objects.create(maestrante=maestrante.maestrante,fecha_programada=cronograma2.fecha_avance2,usuario=request.user,evidencia=notificar.contenido+" - Docente guía : "+str(maestrante.guia))
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)
     

def MaestranteEliminar(request,pk):
    paso = get_object_or_404(Maestrante,id_maestrante=pk)
    paso.maestrante_activo=False
    paso.save()    
    return redirect('usuario:listar_maestrante')




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
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(formatted_date)+" a horas: "+hora)   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
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
        maestrante.avance_tesis+=1
        
        usuario_existe = InformeGuia.objects.filter(user=maestrante.maestrante).exists()
        if not usuario_existe:
            InformeGuia.objects.create(user=maestrante.maestrante)
        informe = get_object_or_404(Informe,user=maestrante.maestrante)
        informe.aceptar_revisor=True
        informe.otras_obs=otras_obs
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
            InformeRevisor.objects.create(user=maestrante.maestrante,capitulo=capitulo[i],descripcion=descripcion[i],sugerencia=sugerencia[i])
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

        cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
        cronograma2.fecha_formulario_guia=final_date
        cronograma2.save()
        requisitosd = get_object_or_404(Requisitos,nro_requisito=13) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitosd.actividad,fecha_programada=cronograma2.fecha_formulario_revisor) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=13)    
        Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        guia=get_object_or_404(Docente,id_docente=maestrante.maestrante.guia.id_docente)
        guia.notificacion=True
        guia.save()
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
        #usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
        #for usuario in usuarios_administradores:
        #    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
        notificar = BancoNotificacion.objects.get(numero_notificacion=14)
        Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y"))+". "+str(maestrante))
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y"))+". "+str(maestrante))   
        maestrante.save()
    return redirect('usuario:listar_informe_revisor')
#Actividad 14---------- Formulario de informe final de docente guía y Tesis mejorada
@login_required()
def GuardarInformeGuia(request):
    
    if request.method =='POST':
        tesis_mejorada = request.FILES #returns a dict-like object
        doc_tesismejorada = tesis_mejorada['tesismejorada']
        idmaestrante = request.POST['id_maestrante']
        otras_obs = request.POST['otras_obs'] 
        capitulo = []
        descripcion= []
        opcion = []
        pagina = []
        funda = []
        maestrante = get_object_or_404(Maestrante,id_maestrante=idmaestrante)
        maestrante.avance_tesis += 1
        maestrante.tesis_mejorado=doc_tesismejorada
        
        informe = get_object_or_404(InformeGuia,user=maestrante.maestrante)
        informe.aceptar_guia=True   
        informe.otras_obs=otras_obs  
        informe.fecha_registro=timezone.now()
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
            InformeGuiaFormulario.objects.create(user=maestrante.maestrante,capitulo=capitulo[i],obs=descripcion[i],opcion=opcion[i],pagina=pagina[i],fundamentacion=funda[i])
            i += 1
        cronograma= get_object_or_404(Cronograma2,user=maestrante)
        requisitos = get_object_or_404(Requisitos,nro_requisito=14) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad,fecha_programada=cronograma.fecha_formulario_guia,archivo_documento=doc_tesismejorada) 
        usuario_existe = ReporteGeneral.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            ReporteGeneral.objects.create(user=maestrante.maestrante)
        notificar = BancoNotificacion.objects.get(numero_notificacion=15)
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente guía : "+str(maestrante.guia))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
        
      
        
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
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(maestrante)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y"))) 
      
        Post.objects.create(user=maestrante.revisor.user,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(maestrante)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y")))  
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
            Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
            maestrante.save()
            Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            guia=get_object_or_404(Docente,id_docente=maestrante.maestrante.guia.id_docente)
            guia.notificacion=True
            guia.save()
            usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()

            requisitos = get_object_or_404(Requisitos,nro_requisito=105) 
            CentroActividades.objects.create(maestrante=maestrante.maestrante,fecha_programada=cronograma2.fecha_reporte_general,usuario=request.user,evidencia=requisitos.actividad+" - Docente revisor : "+str(maestrante.revisor))
            self.object = form.save()
            return redirect(self.get_success_url())

#Actividad 15---------- Formulario de Reporte general Segundo    
@method_decorator(login_required, name='dispatch')    
class RegistrarReporteGeneral2(UpdateView):

    model = ReporteGeneral
    template_name = 'usuario/registrar_reporte_general2.html'
    form_class = FormularioReporteGeneral2
    success_url = reverse_lazy('usuario:listar_reporte_general') 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = FormularioReporteGeneral2(request.POST, instance=self.object)

        if form.is_valid():        

            maestrante=get_object_or_404(Maestrante,id_maestrante=self.object.user.id_maestrante) 
            
            cronograma2= get_object_or_404(Cronograma2,user=maestrante)
            notificar = BancoNotificacion.objects.get(numero_notificacion=93)
            Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
            maestrante.save()
            Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            guia=get_object_or_404(Docente,id_docente=maestrante.maestrante.guia.id_docente)
            guia.notificacion=True
            guia.save()
            usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante)+" - Docente revisor : "+str(maestrante.revisor))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()

            requisitos = get_object_or_404(Requisitos,nro_requisito=105) 
            CentroActividades.objects.create(maestrante=maestrante.maestrante,fecha_programada=cronograma2.fecha_reporte_general,usuario=request.user,evidencia=requisitos.actividad+" Emitido - Docente revisor : "+str(maestrante.revisor))
            self.object = form.save()
            return redirect(self.get_success_url())           
            
#Actividad 25---------- Formulario de Reporte general Segundo     
@method_decorator(login_required, name='dispatch')
class RegistrarReporteGeneralTribunalInterno(UpdateView):

    model = ReporteGeneralTribunalInterno
    template_name = 'usuario/registrar_reporte_general_tribunal_interno.html'
    form_class = FormularioReporteGeneralTribunalInterno
    success_url = reverse_lazy('usuario:listar_reporte_general_tribunal_interno') 
@method_decorator(login_required, name='dispatch')
class Act1Confirmar(DetailView):
    model=Maestrante
    template_name="usuario/act/act1_confirmar.html"  


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
        maestranteid.avance_tesis=maestranteid.avance_tesis+1
        
        maestranteid.save()    


@login_required()
def busquedaperfilhistorial(request):


    
    if request.method =='GET'  :
        template_name="usuario/listar_sustentacion_perfil_historial.html"
        busmaes=request.GET["busmaestrante"]
     
        employers=SustentacionPerfilHistorial.objects.filter(user__ru=busmaes)  
       
        context = { 'maestrantes':employers }
        return render(request,template_name,context) 
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
     
        employers=CentroActividades.objects.filter(maestrante__ru=busmaes).order_by('id_actividad')   
       
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

    if request.user.is_staff:
        busmaestrante = request.GET.get("busmaestrante")
        employers=Maestrante.objects.filter(ru=busmaestrante).filter(maestrante_habilitado=True)
        
        template_name = 'usuario/act/act.html'
        if employers.count()==1:
        
            paso = get_object_or_404(Maestrante,ru=busmaestrante)
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
            mensaje="Esta actividad no esta disponible para este rol"
            

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
        elif employers.count()>1:
            context = { 'maestrantesevi':employers}
            return render(request,template_name,context)
        else:
        
            return HttpResponseForbidden('Error, verifique los datos')

    return HttpResponseForbidden('Error')
    
@login_required()
def CronogramMaestrante(request):
    cronograma=Cronograma.objects.filter(user=request.user.maestrante)
    cronograma2=Cronograma2.objects.filter(user=request.user.maestrante)
    template_name = 'usuario/maestrante_cronograma.html'
    context = { 'cronograma':cronograma,'cronograma2':cronograma2 }
    return render(request,template_name,context)



@login_required()
def BusquedaVarios(request,pk):

    if request.user.is_staff:
        
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
            mensaje="Esta actividad no esta disponible para este rol"
            

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