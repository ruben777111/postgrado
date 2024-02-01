from django.shortcuts import redirect,get_object_or_404,render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from usuario.models import Docente_Revisor,SustentacionTesisHistorial,ReporteGeneralTribunalInterno,ReporteGeneral,TribunalTesis,BancoNotificacion,Informe,Docente,AsistenciaInduccion,Cronograma2,SustentacionPerfilHistorial,TribunalPerfil,Avance,Avance_2,Cronograma,Cronograma2,Post,Administracion,Requisitos,CentroActividades,Usuario,Maestrante
from datetime import datetime, timedelta
from django.utils import timezone
from .forms import FormularioFechaSustentacionTesis,FormularioTribunalTesis,FormularioDocenteRevisor,FormularioDocenteGuia,FormularioFechaSustentacion,FormularioTribunalPerfil,FormularioDocenteProvisional,FormularioActividad2
from django.views.generic import View,TemplateView,UpdateView,DetailView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
@login_required()
def enviar_correo_electronico(asunto, mensaje, destinatarios):
    send_mail(asunto, mensaje, 'pedroperespereira2023@hotmail.com', destinatarios, fail_silently=False)

#Actividad 
@login_required()
def MaestranteHabilitar(request,pk):
    
    new_date=timezone.now()       
    requisitos = Requisitos.objects.get(nro_requisito=1) 
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)  
    con=1
    dia=1
    while con<=requisitos.tiempo:
        final_date=new_date+timedelta(days=dia)
        if final_date.weekday() == 5 or final_date.weekday() == 6:
            pass
        else:        
            con=con+1
        dia=dia+1
    maestrante.fecha_derivacion=timezone.now()
    maestrante.avance_tesis=0
    maestrante.maestrante_habilitado=True    

    usuario_existe = Cronograma.objects.filter(user=maestrante).exists()
    if not usuario_existe:
        Cronograma.objects.create(user=maestrante,fecha_1=final_date)


    usuario_existe = TribunalPerfil.objects.filter(user=maestrante).exists()
    if not usuario_existe:
        TribunalPerfil.objects.create(user=maestrante)


    usuario_existe = AsistenciaInduccion.objects.filter(maestrante=maestrante).exists()
    if not usuario_existe:
        AsistenciaInduccion.objects.create(maestrante=maestrante) 
  
    notificar = BancoNotificacion.objects.get(numero_notificacion=0)
    usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
    
    for usuario in usuarios_administradores:
       
       Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+ str(maestrante)+" R.U.:"+ str(maestrante.ru))   
       #room_name = usuario.username         
       channel_layer = get_channel_layer()
       async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
       usuario.notificacion=True
       usuario.save()
    requisitos = get_object_or_404(Requisitos,nro_requisito=100)
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
    
    maestrante.save()  
    
    return redirect('usuario:listar_postulante')

    
# Actividad 0 ------------ Solicitud a inducción
@login_required()
def RegistrarActividad01(request,pk):

    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.avance_tesis += 1    
      
    requisitos = get_object_or_404(Requisitos,nro_requisito=0)        
      
    cronograma= get_object_or_404(Cronograma,user=maestrante)
    notificar = BancoNotificacion.objects.get(numero_notificacion=1)
    Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(cronograma.fecha_1.strftime("%d-%m-%Y")))   
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,evidencia=requisitos.actividad) 
    maestrante.notificacion=True

    maestrante.save()
    return redirect('usuario:seguimiento_tesis')


# Actividad 1 ---------------- Registro de formulario de habilitación
@method_decorator(login_required, name='dispatch')

class RegistrarActividad0(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_0.html'
def FormularioActividad0(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']


        form_habilitacion = request.FILES #returns a dict-like object
        form_habilitacion_doc = form_habilitacion['form_habilitacion']    
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        maestrante.avance_tesis+=1
        requisitosactividad = get_object_or_404(Requisitos,nro_requisito=1) 
        requisitos = get_object_or_404(Requisitos,nro_requisito=3) 
        cronograma = get_object_or_404(Cronograma,user=maestrante)                
        new_date=timezone.now()
        final_date = None
        con=1
        dia=1
        while con<=requisitos.tiempo:
            
            final_date=new_date+timedelta(days=dia)
            if final_date.weekday() == 5 or final_date.weekday() == 6:
                pass
            else:        
                con=con+1
            dia=dia+1        
        cronograma.fecha_2=final_date
        cronograma.save()

        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,evidencia=requisitosactividad.actividad,fecha_programada=cronograma.fecha_1,archivo_documento=form_habilitacion_doc) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=2)
        Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 



# Actividad 2 -------------- Aceptación de docente guía a solicitud de asesoramiento hecha por el postulante
@method_decorator(login_required, name='dispatch')
class RegistrarActividad1(UpdateView):

    model = Maestrante
    template_name = 'usuario/act/actividad_1.html'
    form_class = FormularioDocenteProvisional
    success_url = reverse_lazy('usuario:seguimiento_tesis')
    
    def post(self, request, *args, **kwargs):     
        self.object = self.get_object()
        form = FormularioDocenteProvisional(request.POST, instance=self.object)

        if form.is_valid():        
            self.object = form.save(commit=False)
            self.object.avance_tesis += 1           
            
            requisitos = get_object_or_404(Requisitos,nro_requisito=2) 
            CentroActividades.objects.create(maestrante=self.object.maestrante,usuario=request.user,evidencia=requisitos.actividad+", Docente guía provisional : "+str(self.object.provisional)) 
            
            
            notificar = BancoNotificacion.objects.get(numero_notificacion=3)
            Post.objects.create(user=self.object,title=notificar.titulo,text=notificar.contenido+", Docente guía : "+str(self.object.provisional))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{self.object.maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            self.object.notificacion=True
            notificar = BancoNotificacion.objects.get(numero_notificacion=4)

            usuarios_administradores = Usuario.objects.filter(tipo_usuario=5)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(self.object.maestrante)+" R.U.:"+ str(self.object.ru))                          
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion= True
                usuario.save()
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)


# Actividad 3 ------------- Registro del perfil de tesis
@method_decorator(login_required, name='dispatch')
class RegistrarActividad2(UpdateView):

    model = Maestrante
    template_name = 'usuario/act/actividad_2.html'
    form_class = FormularioActividad2
    success_url = reverse_lazy('usuario:seguimiento_tesis')
    
    def post(self, request, *args, **kwargs):       

        self.object = self.get_object()
        form = FormularioActividad2(request.POST, instance=self.object)

        if form.is_valid():        
            self.object = form.save(commit=False)
            self.object.avance_tesis += 1
            
            self.object = form.save()
            requisitos = get_object_or_404(Requisitos,nro_requisito=3)
            cronograma = get_object_or_404(Cronograma,user=self.object.maestrante) 
            CentroActividades.objects.create(maestrante=self.object.maestrante,usuario=request.user,evidencia=requisitos.actividad,fecha_programada=cronograma.fecha_2) 
            self.object.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)
# Actividad 4 ------------- Designación de fecha y hora para acto de Sustentación de tema.
@method_decorator(login_required, name='dispatch')
class RegistrarActividad3(UpdateView):
    model = Maestrante
    form_class = FormularioTribunalPerfil
    second_form_class = FormularioFechaSustentacion
    template_name = 'usuario/act/actividad_3.html'
    success_url = reverse_lazy('usuario:seguimiento_tesis')

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
        requisitos = get_object_or_404(Requisitos,nro_requisito=4)
        CentroActividades.objects.create(maestrante=maestranteid.maestrante,usuario=self.request.user,evidencia=requisitos.actividad)
        notificar = BancoNotificacion.objects.get(numero_notificacion=5)

        Post.objects.create(user=maestranteid,title=notificar.titulo,text=notificar.contenido)   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestranteid.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestranteid.notificacion=True
        maestranteid.listacomunicacion=False
        maestranteid.avance_tesis=maestranteid.avance_tesis+1        
        maestranteid.save()    

# Actividad 5 ------------ Registro de dictamen del acto de sustentación del tema
@login_required()
def ProcedentePerfil(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=6) 
    requisitosactividad = get_object_or_404(Requisitos,nro_requisito=5)
    cronograma = get_object_or_404(Cronograma,user=maestrante.maestrante)
    usuario_existe = Cronograma2.objects.filter(user=maestrante.maestrante).exists()
    if not usuario_existe:
        Cronograma2.objects.create(user=maestrante.maestrante)  

    maestrante.procedencia_tema=True
    maestrante.avance_tesis+=1
    
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
    
    cronograma.fecha_4=final_date
    cronograma.save()
  
    fecha_2=None
    if  maestrante.programa_regular:
        requisitos = get_object_or_404(Requisitos,nro_requisito=101)
        fecha_2=new_date+timedelta(days=requisitos.tiempo)
    if  maestrante.reincorporacion:
        requisitos = get_object_or_404(Requisitos,nro_requisito=102)
        fecha_2=new_date+timedelta(days=requisitos.tiempo)
    if  maestrante.vigencia_matricula:
        requisitos = get_object_or_404(Requisitos,nro_requisito=103)
        fecha_2=new_date+timedelta(days=requisitos.tiempo)  

    cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
    cronograma2.fecha_borrador= fecha_2
    cronograma2.save()

    final_date = final_date.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(final_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d/%m/%Y")  
    notificar = BancoNotificacion.objects.get(numero_notificacion=7)
    Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" fecha : "+str(formatted_date))   
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True
    notificar = BancoNotificacion.objects.get(numero_notificacion=6)
    usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
    for usuario in usuarios_administradores:
        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+ str(maestrante.maestrante)+" R.U.:"+ str(maestrante.ru))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        usuario.notificacion=True
        usuario.save()
    
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitosactividad.actividad+" : Tema PROCEDENTE")
    maestrante.save()
    return redirect('usuario:seguimiento_tesis')

# Actividad 5 ------------ Registro de dictamen del acto de sustentación del tema
@login_required()
def ImProcedentePerfil(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.procedencia_tema=False
    maestrante.avance_tesis+=1
    notificar_1 = BancoNotificacion.objects.get(numero_notificacion=96)
    Post.objects.create(user=maestrante,title=notificar_1.titulo,text=notificar_1.contenido)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True
        
    notificar = BancoNotificacion.objects.get(numero_notificacion=6)
    usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)
    for usuario in usuarios_administradores:
        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+ str(maestrante.maestrante)+" R.U.:"+ str(maestrante.ru))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        usuario.notificacion=True
        usuario.save()
    requisitosactividad = get_object_or_404(Requisitos,nro_requisito=5)
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitosactividad.actividad+" : Tema IMPROCEDENTE")
    maestrante.save() 
    return redirect('usuario:seguimiento_tesis')



# actividad 6 ---------- Registro de documentos posteriores a la sustentación del tema y designación de docente guía
@method_decorator(login_required, name='dispatch')
class RegistrarDocenteGuia(UpdateView):
    model = Maestrante
    form_class = FormularioDocenteGuia
    template_name = 'usuario/act/actividad_4.html'
    success_url = reverse_lazy('usuario:seguimiento_tesis')
    def post(self, request, *args, **kwargs):  
        self.object = self.get_object()
        form = FormularioDocenteGuia(request.POST, instance=self.object)
        if form.is_valid():        
            self.object = form.save(commit=False)
             
            tema_perfil = request.POST['tema']
            acta_sustentacion = self.request.FILES.get('acta')
            hojaevaluacion = self.request.FILES.get('hoja')
            cartadesignacion = self.request.FILES.get('carta_designacion')
            documentorespaldo = self.request.FILES.get('respaldo')
            self.object.tema_tesis_perfil = tema_perfil
            cronograma = get_object_or_404(Cronograma,user=self.object.maestrante)

            requisitos = get_object_or_404(Requisitos,nro_requisito=6)
            if self.object.procedencia_tema == True:   

                resultado=True
                cartaexterna = self.request.FILES.get('carta')
                fecha_recepcion = self.request.POST['recepcion_perfil']
                self.object.avance_tesis += 1    
                usuario_existe = Avance.objects.filter(user=self.object.maestrante).exists()
                if not usuario_existe:
                    Avance.objects.create(user=self.object.maestrante)     
                   
                SustentacionPerfilHistorial.objects.create(user=self.object.maestrante,
                                                        tema_perfil=tema_perfil, 
                                                        fecha_sustentacion=timezone.now(), 
                                                        docente_guia=self.object.provisional,
                                                        resultado =resultado,
                                                        acta=acta_sustentacion,
                                                        hoja_evaluacion=hojaevaluacion,
                                                        carta_externa=cartaexterna,                                                        
                                                        documento_respaldo=documentorespaldo,
                                                        carta_externa_designacion=cartadesignacion,
                                                        fecha_recibido_perfil = fecha_recepcion,
                                                        tribunal_perfil_1=self.object.tribunalperfil.tribunal_perfil_1,
                                                        tribunal_perfil_2=self.object.tribunalperfil.tribunal_perfil_2, 
                                                        instancia=self.object.instancia)
                cronograma2 = get_object_or_404(Cronograma2,user=self.object.maestrante)
                
                notificar = BancoNotificacion.objects.get(numero_notificacion=97)
                Post.objects.create(user=self.object.maestrante,title=notificar.titulo,text=notificar.contenido+", fecha: "+str(cronograma2.fecha_borrador))
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                self.object.notificacion=True

                cronograma = get_object_or_404(Cronograma,user=self.object.maestrante)
                CentroActividades.objects.create(maestrante=self.object.maestrante,usuario=request.user,evidencia=requisitos.actividad+": Fecha de recepción del perfil mejorado (registrada en Postgrado)): "+fecha_recepcion,fecha_programada=cronograma.fecha_4)
                


            if self.object.procedencia_tema == False:   
                
                resultado=False
                SustentacionPerfilHistorial.objects.create(user=self.object.maestrante,
                                                        tema_perfil=tema_perfil, 
                                                        fecha_sustentacion=timezone.now(), 
                                                        docente_guia=self.object.provisional,
                                                        resultado =resultado,
                                                        acta=acta_sustentacion,
                                                        hoja_evaluacion=hojaevaluacion,
                                                        documento_respaldo=documentorespaldo,
                                                        carta_externa_designacion=cartadesignacion,
                                                        tribunal_perfil_1=self.object.tribunalperfil.tribunal_perfil_1,
                                                        tribunal_perfil_2=self.object.tribunalperfil.tribunal_perfil_2, 
                                                        instancia=self.object.instancia)
                CentroActividades.objects.create(maestrante=self.object.maestrante,usuario=request.user,evidencia=requisitos.actividad)

                cronograma=get_object_or_404(Cronograma,user=self.object.maestrante)
                tribunalperfil=get_object_or_404(TribunalPerfil,user=self.object.maestrante)            
                asistenciainduccion=get_object_or_404(AsistenciaInduccion,maestrante=self.object.maestrante)            
                tribunalperfil.delete()
                cronograma.delete()
                asistenciainduccion.delete()

        
                self.object.provisional=None
                self.object.instancia += 1           
                self.object.maestrante_habilitado=False
                self.object.avance_tesis= None
          
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)
    
@method_decorator(login_required, name='dispatch')
class RegistrarActividad7(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_7.html'


#Actividad 7---------- Programar fecha de presentacion del formulario de avance
@login_required()
def RegistrarActividad6(request):
    requisitos = get_object_or_404(Requisitos,nro_requisito=7) 
    if request.method =='POST':        
        fecha = request.POST['fecha']        
        check = request.POST.getlist('checks[]')        
        if check:
            for i in check:  
                maestrante=get_object_or_404(Maestrante,id_maestrante=i)                
                maestrante.avance_tesis +=1                              
                
                cronograma2=get_object_or_404(Cronograma2,user=maestrante.maestrante)
                cronograma2.fecha_avance1=fecha
                cronograma2.save()
                notificar = BancoNotificacion.objects.get(numero_notificacion=8)
                                                
                Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante.maestrante)) 
                guia=get_object_or_404(Docente,id_docente=maestrante.maestrante.guia.id_docente)
                guia.notificacion=True
                guia.save()
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
  
                Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante.maestrante))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
                date_obj = datetime.strptime(fecha, "%Y-%m-%d")
                foratted_date = date_obj.strftime("%d/%m/%Y")
                CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad+" : "+str(foratted_date)) 
                maestrante.save()
        
    return redirect('usuario:seguimiento_tesis') 


#Actividad 8---------- 	Registro de primer avance
#----- 	Registro de primer avance no aprobado
@login_required()
def RegistrarAvance(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    avance = get_object_or_404(Avance,user=maestrante.maestrante)
    avance.aceptar_avance=False
    avance.aprobacion=1
    avance.save()
    maestrante.avance_tesis-=1
    
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro del formulario del primer avance : NO APROBADO") 
    maestrante.save()    
    return redirect('usuario:seguimiento_tesis')

#----- 	Registro de avance aprobado
@login_required()
def RegistrarAvanceAprobado(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.avance_tesis+=1
    
    if maestrante.avance_tesis == 9:
        
        usuario_existe = Avance_2.objects.filter(user=maestrante.maestrante).exists()
        if not usuario_existe:
            Avance_2.objects.create(user=maestrante.maestrante) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro del formulario del primer avance : APROBADO") 
    if maestrante.avance_tesis == 11:
       
        notificar = BancoNotificacion.objects.get(numero_notificacion=18)
        usuarios_administradores = Usuario.objects.filter(tipo_usuario=5)
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()

        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro del formulario del segundo avance : APROBADO") 
    maestrante.save() 
    return redirect('usuario:seguimiento_tesis')


#Actividad 9 ---------- 	Programar fecha de presentacion del formulario de segundo avance
@login_required()
def RegistrarActividad9(request):
    
    if request.method =='POST':        
        fecha = request.POST['fecha']        
        check = request.POST.getlist('checks[]')        
        if check:
            for i in check:  
                maestrante=get_object_or_404(Maestrante,id_maestrante=i)
                maestrante.avance_tesis +=1
                
                
                cronograma2=get_object_or_404(Cronograma2,user=maestrante.maestrante)
                cronograma2.fecha_avance2=fecha
                cronograma2.save()
                notificar = BancoNotificacion.objects.get(numero_notificacion=10)
                                                  
                Post.objects.create(user=maestrante.guia,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante.maestrante))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                guia=get_object_or_404(Docente,id_docente=maestrante.maestrante.guia.id_docente)
                guia.notificacion=True
                guia.save()
                Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante.maestrante))   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                maestrante.notificacion=True
                date_obj = datetime.strptime(fecha, "%Y-%m-%d")
                foratted_date = date_obj.strftime("%d/%m/%Y")
                requisitos = get_object_or_404(Requisitos,nro_requisito=9) 
                CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad+" : "+str(foratted_date)) 
                maestrante.save()
    return redirect('usuario:seguimiento_tesis') 


#Actividad 10---------- 	Registro de segundo avance
#----- 	Registro de segundo avance no aprobado
@login_required()
def RegistrarAvance2(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    avance = get_object_or_404(Avance_2,user=maestrante.maestrante)
    avance.aceptar_avance=False
    avance.aprobacion=1
    avance.save()
    maestrante.avance_tesis-=1
       
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro del formulario del segundo avance : NO APROBADO") 
    maestrante.save() 
    return redirect('usuario:seguimiento_tesis')


# habilitacion de diaas de prorroga 90 dias----------------------------
@login_required()
def HabilitarProrroga(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    cronograma2=get_object_or_404(Cronograma2,user=maestrante.maestrante)  
    requisitos = get_object_or_404(Requisitos,nro_requisito=104)   
    cronograma2.fecha_borrador_prorroga = cronograma2.fecha_borrador +timedelta(days=requisitos.tiempo)
    cronograma2.save()
    notificar = BancoNotificacion.objects.get(numero_notificacion=98)
    Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante.maestrante))   
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True
    requisitos = get_object_or_404(Requisitos,nro_requisito=104)
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
    maestrante.save()
    return redirect('usuario:seguimiento_tesis') 


@method_decorator(login_required, name='dispatch')
class RegistrarActividad10(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_10.html'


#Actividad 11---------- Registro borrador de tesis
@method_decorator(login_required, name='dispatch')
class RegistrarActividad11(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_11.html'
@login_required()
def FormularioActividad11(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        tema = request.POST['titulo']
        nombramiento = request.FILES #returns a dict-like object
        nombramiento_revisor = nombramiento['nombramiento']
        fecha_recepcion_borrador = request.POST['recepcion_borrador']
        documento_respaldo = request.FILES
        documentorespaldo = documento_respaldo['respaldo']       

        
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)

        maestrante.tema_tesis=tema 
        maestrante.avance_tesis+=1       
        cronograma2.fecha_recepcion_borrador=fecha_recepcion_borrador        
        cronograma2.borrador_tesis=True
        cronograma2.save()
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro borrador de tesis",fecha_programada=cronograma2.fecha_borrador) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro borrador de tesis: Solicitud de nombramiento de docente revisor (PDF)",fecha_programada=cronograma2.fecha_borrador,archivo_documento=nombramiento_revisor) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro borrador de tesis: Otros documentos de respaldo (borrador de tesis,aval del docente guía, otros) (PDF)",fecha_programada=cronograma2.fecha_borrador,archivo_documento=documentorespaldo) 
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 

#Actividad 12---------- Registro borrador de tesis
@method_decorator(login_required, name='dispatch')
class RegistrarActividad12(UpdateView):

    model = Maestrante
    template_name = 'usuario/act/actividad_12.html'
    form_class = FormularioDocenteRevisor
    success_url = reverse_lazy('usuario:seguimiento_tesis')
    
    def post(self, request, *args, **kwargs):       

        self.object = self.get_object()

        form = FormularioDocenteRevisor(request.POST, instance=self.object)

        if form.is_valid():        
            self.object = form.save(commit=False)
            self.object.avance_tesis += 1
          
            
            con=1
            dia=1
            requisitos = get_object_or_404(Requisitos,nro_requisito=13)  
            final_date=None
            while con<=requisitos.tiempo:
                final_date=self.object.fecha_nombramiento+timedelta(days=dia)
                if final_date.weekday() == 5 or final_date.weekday() == 6:
                    pass
                else:        
                    con=con+1
                dia=dia+1

           
            cronograma2 = get_object_or_404(Cronograma2,user=self.object.maestrante)
            cronograma2.fecha_formulario_revisor=final_date
            cronograma2.save()
        
            requisitos2 = get_object_or_404(Requisitos,nro_requisito=12)  
    
            CentroActividades.objects.create(maestrante=self.object.maestrante,usuario=request.user,evidencia=requisitos2.requisito) 
            notificar = BancoNotificacion.objects.get(numero_notificacion=19)
            Post.objects.create(user=self.object,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(self.object.revisor)+", Maestrante : "+str(self.object))   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{self.object.maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            self.object.notificacion=True

            Post.objects.create(user=self.object.revisor.user,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(self.object.revisor)+", Maestrante : "+str(self.object))  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{self.object.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            revisor = get_object_or_404(Usuario,username=self.object.revisor.user.username)  
            revisor.notificacion=True
            revisor.save()
            notificar = BancoNotificacion.objects.get(numero_notificacion=12)
            Post.objects.create(user=self.object,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(self.object)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y")))
                                              
            Post.objects.create(user=self.object.revisor.user,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(self.object)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y")))  
            usuario_existe = Informe.objects.filter(user=self.object.maestrante).exists()
            if not usuario_existe:   
                Informe.objects.create(user=self.object.maestrante) 
            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)

# Actividad 15 ------------ Registro de dictamen del acto de sustentación del tema
@login_required()
def ProcedenteReporte(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=16) 
    maestrante.avance_tesis+=1
    
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
    


  
    cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
    cronograma2.fecha_tesis_habilitada= final_date
    cronograma2.save()

    final_date = final_date.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(final_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d/%m/%Y")  

    notificarm = BancoNotificacion.objects.get(numero_notificacion=24)
    Post.objects.create(user=maestrante,title=notificarm.titulo,text=notificarm.contenido+" : "+str(maestrante)) 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True


    notificar = BancoNotificacion.objects.get(numero_notificacion=21)
    usuarios_administradores = Usuario.objects.filter(tipo_usuario=5)
  
    for usuario in usuarios_administradores:
        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        usuario.notificacion=True
        usuario.save()


    
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad)
    maestrante.save()
    return redirect('usuario:seguimiento_tesis')
@login_required()
def ActivarReporte2(request,pk):
    
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    reporte=get_object_or_404(ReporteGeneral,user=maestrante.maestrante)
    reporte.activar_reporte2=True
    requisitos = get_object_or_404(Requisitos,nro_requisito=105)
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
    notificar = BancoNotificacion.objects.get(numero_notificacion=92)
    Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(maestrante)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y"))) 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True

    Post.objects.create(user=maestrante.revisor.user,title=notificar.titulo,text=notificar.contenido+". Maestrante: "+str(maestrante)+", fecha de presentación : "+str(final_date.strftime("%d-%m-%Y")))  
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    revisor = get_object_or_404(Usuario,username=maestrante.revisor.user.username)  
    revisor.notificacion=True
    revisor.save()

    cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
    cronograma2.fecha_reporte_general2=final_date
    cronograma2.save()
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad,fecha_programada=final_date) 
    reporte.save()

    return redirect('usuario:seguimiento_tesis')


@method_decorator(login_required, name='dispatch')
class RegistrarActividad16(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_16.html'
@login_required()
def FormularioActividad16(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        tema = request.POST['titulo']

        informe = request.FILES #returns a dict-like object
        informe_aval = informe['informe']
        
        
        tesis = request.FILES
        tesis_documento = tesis['tesis']       

        
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  


        maestrante.tema_tesis=tema 
        maestrante.avance_tesis+=1
        usuario_existe = TribunalTesis.objects.filter(user=maestrante.maestrante).exists()
        if not usuario_existe:          
            TribunalTesis.objects.create(user=maestrante.maestrante) 

        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Registro titulo del tema: "+tema) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Informe aval de docente guia (PDF)",archivo_documento=informe_aval) 
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia="Documento de tesis (PDF)",archivo_documento=tesis_documento) 
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 



# Actividad 17 ------------- Designación de fecha y hora para acto de Sustentación de tema.
@method_decorator(login_required, name='dispatch')
class RegistrarActividad17(UpdateView):
    model = Maestrante
    form_class = FormularioTribunalTesis
    second_form_class = FormularioFechaSustentacionTesis
    template_name = 'usuario/act/actividad_17.html'
    success_url = reverse_lazy('usuario:seguimiento_tesis')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST, instance=self.object.tribunaltesis)
            context['form2'] = self.second_form_class(self.request.POST, instance=self.object.cronograma2)
        else:
            context['form'] = self.form_class(instance=self.object.tribunaltesis)
            context['form2'] = self.second_form_class(instance=self.object.cronograma2)
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
        requisitos = get_object_or_404(Requisitos,nro_requisito=17)
        CentroActividades.objects.create(maestrante=maestranteid.maestrante,usuario=self.request.user,evidencia=requisitos.actividad)
        notificar = BancoNotificacion.objects.get(numero_notificacion=20)

        Post.objects.create(user=maestranteid,title=notificar.titulo,text=notificar.contenido)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestranteid.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})

        #maestranteid.notificacion=True
        maestranteid.listacomunicacion=False
        maestranteid.avance_tesis=maestranteid.avance_tesis+1        
        maestranteid.save()

# Actividad 18 ------------- Dictamen de la defensa de tesis.
@login_required()
def ProcedenteTesis(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.procedencia_tesis=True
    maestrante.avance_tesis+=1
    
    requisitos = get_object_or_404(Requisitos,nro_requisito=20)
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
    cronograma2 = get_object_or_404(Cronograma2,user=maestrante.maestrante)
    cronograma2.fecha_tesis_mejorada = final_date
    cronograma2.save()
    notificarm = BancoNotificacion.objects.get(numero_notificacion=23)
    Post.objects.create(user=maestrante,title=notificarm.titulo,text=notificarm.contenido+" : "+str(maestrante)+", fecha: "+str(final_date)) 
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
    maestrante.notificacion=True

    notificar = BancoNotificacion.objects.get(numero_notificacion=22)
    usuarios_administradores = Usuario.objects.filter(tipo_usuario=3)    
    for usuario in usuarios_administradores:
        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(maestrante))   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        usuario.notificacion=True
        usuario.save()

    requisitos = get_object_or_404(Requisitos,nro_requisito=18)
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad+" Tesis aprobada")
    maestrante.save()
    return redirect('usuario:seguimiento_tesis') 
@login_required()
def ImProcedenteTesis(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
 
    maestrante.avance_tesis+=1


    requisitos = get_object_or_404(Requisitos,nro_requisito=18)
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad+" Tesis Improcedente")
    maestrante.save()
    return redirect('usuario:seguimiento_tesis') 

# Actividad 19 ------------- Registro de documentos posteriores a la defensa de tesis.
@method_decorator(login_required, name='dispatch')
class RegistrarActividad19(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_19.html'
@login_required()
def FormularioActividad19(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        tema = request.POST['tema']
        escala = request.POST['cualitativo']
        numeral = request.POST['numeral']

        acta = request.FILES #returns a dict-like object
        acta_doc = acta['acta']


        hoja = request.FILES
        hoja_doc = hoja['hoja']       

        carta_designacion = request.FILES
        carta_designacion_doc = carta_designacion['carta_designacion']       


        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        maestrante.tema_tesis=tema
        maestrante.dictamen_escala=escala 
        maestrante.dictamen_nota=numeral
        if maestrante.procedencia_tesis:
            maestrante.avance_tesis+=1
        else:
            maestrante.avance_tesis=24
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=19)
        SustentacionTesisHistorial.objects.create(user=maestrante.maestrante,
                                                   fecha=timezone.now(),     
                                                   tema_tesis=tema,
                                                   fecha_sustentacion=maestrante.cronograma2.fecha_sustentacion,
                                                   hora_sustentacion=maestrante.cronograma2.hora_sustentacion,
                                                   docente_guia=maestrante.guia,
                                                   tribunal_1=str(maestrante.tribunaltesis.tribunal_tesis_1),
                                                   tribunal_2=str(maestrante.tribunaltesis.tribunal_tesis_2),
                                                   resultado=maestrante.procedencia_tesis,
                                                   acta=acta_doc,
                                                   hoja_evaluacion=hoja_doc,
                                                   designacion=carta_designacion_doc,
                                                   dictamen_nota=numeral,
                                                   dictamen_escala=escala,
                                                   ) 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
        maestrante.save() 
        #SustentacionTesisHistorial
    return redirect('usuario:seguimiento_tesis') 

# Actividad 20 ------------- Aprobación a empaste
@method_decorator(login_required, name='dispatch')
class RegistrarActividad20(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_20.html'
@login_required()
def FormularioActividad20(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        if 'aprobacion'  in request.POST: 
            maestrante.aprobacion_empaste = True
        if 'recomendado'  in request.POST: 
            maestrante.tesis_recomendada = True  
        obs = request.POST['obs']
        maestrante.observacion_empaste = obs       
          
 
        maestrante.avance_tesis+=1
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=20)
 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad,observacion=obs) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 


# Actividad 21 ------------- Solicitud de pago a docente guia
@method_decorator(login_required, name='dispatch')
class RegistrarActividad21(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_21.html'
@login_required()
def FormularioActividad21(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        fecha_recepcion = request.POST['fecha_recepcion']  
        obs = request.POST['obs']
        maestrante.recepcion_solicitud = fecha_recepcion  
        maestrante.observacion_pago = obs         
        
        maestrante.avance_tesis+=1
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=21)
 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad,observacion=obs) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 
# Actividad 22 ------------- Asignación de codigo a empaste 
@method_decorator(login_required, name='dispatch')
class RegistrarActividad22(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_22.html'

@login_required()
def FormularioActividad22(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        
        codigo_empaste = request.POST['codigo']
      
        maestrante.codigo_empaste = codigo_empaste         
        
        maestrante.avance_tesis+=1
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=22)
 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 

# Actividad 23 ------------- Recepción de empastado y CD para archivo 
@method_decorator(login_required, name='dispatch')
class RegistrarActividad23(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_23.html'

@login_required()
def FormularioActividad23(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        gestion = request.POST['empastado']
        maestrante.gestion_empastado = gestion
        if 'empastado'  in request.POST: 
            maestrante.empaste_cd = True
        if 'revision'  in request.POST: 
            maestrante.articulos_revision = True      
        if 'original'  in request.POST: 
            maestrante.articulos_original = True      
        if 'ambos'  in request.POST: 
            maestrante.articulos_revision_original = True    
        maestrante.avance_tesis =1000
        #1000 maestrante graduado
        maestrante.tesis_terminado = True
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=23)
 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 

# Actividad 24 ------------- Derivación de tesis postergada a tribunal interno (Tesis postergada)
@method_decorator(login_required, name='dispatch')
class RegistrarActividad24(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_24.html' 
@login_required()
def FormularioActividad24(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        tesis_segunda = request.FILES
        tesis_segunda_instancia = tesis_segunda['tesis_segunda']  
        hoja = request.FILES
        hoja_doc = hoja['hoja']  
        observacion = request.POST['obs']
        maestrante.observacion_segunda_instancia = observacion

        maestrante.tesis_segunda_instancia = tesis_segunda_instancia
        maestrante.hoja_de_evaluacion = hoja_doc
        maestrante.avance_tesis+=1
       
        maestrante.tesis_terminado = True
        usuario_existe = ReporteGeneralTribunalInterno.objects.filter(user=maestrante.maestrante).exists()
        if not usuario_existe:
            ReporteGeneralTribunalInterno.objects.create(user=maestrante.maestrante)         
        requisitos = get_object_or_404(Requisitos,nro_requisito=24)
 
        
        CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 
# Actividad 25 ------------ Reporte general de tribunal interno
@login_required()
def ProcedenteReporteTribunalInterno(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=25) 
    maestrante.avance_tesis=16 
    maestrante.instancia_defensa += 1  
    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad)
    maestrante.save()
    return redirect('usuario:seguimiento_tesis')