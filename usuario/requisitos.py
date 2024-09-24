from django.shortcuts import redirect,get_object_or_404,render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from usuario.models import TribunalTesis,Docente_Revisor,SustentacionTesisHistorial,ReporteGeneralTribunalInterno,ReporteGeneral,TribunalTesis,BancoNotificacion,Informe,Docente,AsistenciaInduccion,Cronograma2,SustentacionPerfilHistorial,TribunalPerfil,Avance,Avance_2,Cronograma,Cronograma2,Post,Administracion,Requisitos,CentroActividades,Usuario,Maestrante
from datetime import datetime, timedelta, date

from django.utils import timezone
from .forms import FormularioFechaSustentacionTesis,FormularioTribunalTesis,FormularioDocenteRevisorCompartido,FormularioDocenteRevisor,FormularioDocenteGuia,FormularioFechaSustentacion,FormularioTribunalPerfil,FormularioDocenteProvisional,FormularioActividad2
from django.views.generic import View,TemplateView,UpdateView,DetailView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@login_required()
def RegistrarPostulanteFuncion(request):
    if request.method =='POST': 
    
        pk =  request.POST['id_maestrante']          
        documento_respaldo = request.FILES
        documentorespaldo = documento_respaldo['informe'] 
        new_date=date.today() 
        maestrante = get_object_or_404(Maestrante,id_maestrante=pk)        

        if maestrante.tipo_maestrante == "2":
            dia_mes=date.today() 
            vigencia_meses = Requisitos.objects.get(nro_requisito=111) 
            final_vigencia_meses=dia_mes+timedelta(days=vigencia_meses.tiempo)  
            maestrante.vigencia_matricula_antiguo = final_vigencia_meses
        
        if maestrante.tipo_maestrante == "2":
            dia_final_antiguo=date.today() 
            vigencia_final_antiguo = Requisitos.objects.get(nro_requisito=113) 
            final_vigencia_antiguo=dia_final_antiguo+timedelta(days=vigencia_final_antiguo.tiempo)  
            maestrante.vigencia_matricula_antiguo_total = final_vigencia_antiguo  
        
        if maestrante.tipo_maestrante == "1":
            dia_final_regular=date.today() 
            vigencia_final_regular = Requisitos.objects.get(nro_requisito=112) 
            final_vigencia_regular=dia_final_regular+timedelta(days=vigencia_final_regular.tiempo)  
            maestrante.vigencia_matricula_regular_total = final_vigencia_regular
        requisitos = Requisitos.objects.get(nro_requisito=1) 
        
        con=1
        dia=1
        while con<=requisitos.tiempo:
            final_date=new_date+timedelta(days=dia)
            if final_date.weekday() == 5 or final_date.weekday() == 6:
                pass
            else:        
                con=con+1
            dia=dia+1
        maestrante.fecha_derivacion=date.today()
        maestrante.avance_tesis=0
        maestrante.maestrante_habilitado=True    

        usuario_existe = Cronograma.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            Cronograma.objects.create(user=maestrante,fecha_1=final_date)


        usuario_existe = TribunalPerfil.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            TribunalPerfil.objects.create(user=maestrante)


        notificar = BancoNotificacion.objects.get(numero_notificacion=0)
        
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
            for usuario in usuarios_administradores:            
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
        #requisitos = get_object_or_404(Requisitos,nro_requisito=100)
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,observacion="Maestrante derivado para el proceso de Tesis",archivo_documento=documentorespaldo) 
        
        maestrante.save()  
        
        return redirect('usuario:listar_postulante')     
# Actividad 0 ------------ Solicitud a inducción
@login_required()
def RegistrarActividad01(request,pk):

    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    if maestrante.avance_tesis == 0:
        maestrante.avance_tesis = 1    
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=0)        
        
        cronograma= get_object_or_404(Cronograma,user=maestrante)
        notificar = BancoNotificacion.objects.get(numero_notificacion=1)      
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(cronograma.fecha_1.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)           
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})        
            maestrante.notificacion=True
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos )
        maestrante.save()
        return redirect('usuario:seguimiento_tesis')
    else:
        template_name = 'usuario/act/actduo.html'
        mensaje="El maestrante ya realizo la actividad"
        context = { 'mensaje':mensaje} 
        return render(request,template_name,context)


#Nota: días hábiles desde la derivación de postgrado, actividad de días requisito-1

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
        maestrante.avance_tesis =2
        requisitosactividad = get_object_or_404(Requisitos,nro_requisito=1) 
        requisitos = get_object_or_404(Requisitos,nro_requisito=3) 
        cronograma = get_object_or_404(Cronograma,user=maestrante)                
        new_date=date.today()
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
        
        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitosactividad,fecha_programada=cronograma.fecha_1,fecha_realizado=date.today() ,archivo_documento=form_habilitacion_doc) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=2)
        if notificar.enviar:
            Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestrante.notificacion=True
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 



# Actividad 2 -------------- Aceptación de docente guía provisional a solicitud de asesoramiento hecha por el postulante
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
            self.object.avance_tesis = 3           
            
            requisitos = get_object_or_404(Requisitos,nro_requisito=2) 
            
            CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Docente guía provisional designado: "+str(self.object.provisional)) 
            
            
            notificar = BancoNotificacion.objects.get(numero_notificacion=3)
            if notificar.enviar:
                Post.objects.create(user=self.object.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(self.object.provisional),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                self.object.notificacion=True

            self.object = form.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)


# Actividad 3 ------------- Registro del perfil de tesis ****compartido
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
            self.object.avance_tesis = 4
            
            self.object = form.save()
            requisitos = get_object_or_404(Requisitos,nro_requisito=3)
         
            CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Se presentaron: Perfil de tesis con aval de docente guía  y Nota de solicitud de acto de sustentación de tema") 
            self.object.save()
            return redirect(self.get_success_url())

        return self.form_invalid(form)

#********************** actividad 3 compartido
@method_decorator(login_required, name='dispatch')
class RegistrarActividad2Compartido(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_2_compartido.html'
@login_required()
def FormularioActividad2Compartido(request,pk):
    if  request.method =='POST':
     
        maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
        
        perfil_tema = request.POST['perfil']
        perfil_tema=perfil_tema.upper()
        maestrante.tema_perfil_postulado = perfil_tema    
        notificar = BancoNotificacion.objects.get(numero_notificacion=4)
        requisitos = get_object_or_404(Requisitos,nro_requisito=3)
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido,maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                         
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion= True
                usuario.save()
        cronograma = get_object_or_404(Cronograma,user=maestrante) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,fecha_programada=cronograma.fecha_2,fecha_realizado=date.today(),observacion="Tema perfil postulado: "+str(perfil_tema)) 
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis')
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
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=5)
        
        tribunalperfil = get_object_or_404(TribunalPerfil,user=maestranteid)
        cronograma = get_object_or_404(Cronograma,user=maestranteid)
        fecha_formateada = cronograma.fecha_3.strftime("%d-%m-%Y")
        hora_formateada = cronograma.hora_sustentacion.strftime("%H:%M")
        
        CentroActividades.objects.create(maestrante=maestranteid,usuario=self.request.user,actividad=requisitos,observacion="TRIBUNAL 1 : "+str(tribunalperfil.tribunal_perfil_1)+", TRIBUNAL 2 : "+str(tribunalperfil.tribunal_perfil_2)+", Fecha del acto de sustentación : "+fecha_formateada+", Hora del acto de sustentación : "+hora_formateada)
        if notificar.enviar:
            Post.objects.create(user=maestranteid.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(fecha_formateada)+" - hora: "+str(hora_formateada),maestrante= str(maestranteid),programa = str(maestranteid.programa)+" - "+str(maestranteid.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestranteid.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestranteid.notificacion=True
        maestranteid.listacomunicacion=False
        maestranteid.avance_tesis=5        
        maestranteid.save()    

# Actividad 5 ------------ Registro de dictamen del acto de sustentación del tema
@login_required()
def ProcedentePerfil(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=6) 
    requisitosactividad = get_object_or_404(Requisitos,nro_requisito=5)
    cronograma = get_object_or_404(Cronograma,user=maestrante)
    usuario_existe = Cronograma2.objects.filter(user=maestrante).exists()
    if not usuario_existe:
        Cronograma2.objects.create(user=maestrante)  

    maestrante.procedencia_tema=True
    maestrante.avance_tesis=6
    
    new_date=date.today() 


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
    requisitos = get_object_or_404(Requisitos,nro_requisito=11)
    fecha_2=new_date+timedelta(days=requisitos.tiempo)

    #if  maestrante.tipo_maestrante == "1":
    #    requisitos = get_object_or_404(Requisitos,nro_requisito=101)
    #    fecha_2=new_date+timedelta(days=requisitos.tiempo)
    #if  maestrante.tipo_maestrante == "2":
    #    requisitos = get_object_or_404(Requisitos,nro_requisito=102)
    #    fecha_2=new_date+timedelta(days=requisitos.tiempo)
    #if  maestrante.tipo_maestrante == "3":
    #    requisitos = get_object_or_404(Requisitos,nro_requisito=103)
    #    fecha_2=new_date+timedelta(days=requisitos.tiempo)  

    cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
    cronograma2.fecha_borrador= fecha_2
    cronograma2.save()

    final_date = final_date.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(final_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d/%m/%Y")  
    notificar = BancoNotificacion.objects.get(numero_notificacion=7)
    if notificar.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" fecha : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)      
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
    notificar = BancoNotificacion.objects.get(numero_notificacion=6)
    if notificar.enviar:
        usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)      
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()
    
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitosactividad,observacion="Tema del perfil de tesis procedente")
    maestrante.save()
    return redirect('usuario:seguimiento_tesis')

# Actividad 5 ------------ Registro de dictamen del acto de sustentación del tema
@login_required()
def ImProcedentePerfil(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.procedencia_tema=False
    maestrante.avance_tesis=6
    notificar = BancoNotificacion.objects.get(numero_notificacion=91)
    if notificar.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido,maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)           
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})        
        maestrante.notificacion=True

    notificar = BancoNotificacion.objects.get(numero_notificacion=6)
    
    if notificar.enviar:
        usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido,maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)      
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()
    requisitosactividad = get_object_or_404(Requisitos,nro_requisito=5)
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitosactividad,observacion="Tema del perfil de tesis improcedente")
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
            tema_perfil=tema_perfil.upper()
            fecha_recepcion_doc = self.request.POST['recepcion_documentos']
            acta_sustentacion = self.request.FILES.get('acta')
            hojaevaluacion = self.request.FILES.get('hoja')
            cartadesignacion = self.request.FILES.get('carta_designacion')
            documentorespaldo = self.request.FILES.get('respaldo')
            self.object.tema_tesis_perfil = tema_perfil
            cronograma = get_object_or_404(Cronograma,user=self.object)

            requisitos = get_object_or_404(Requisitos,nro_requisito=6)
            if self.object.procedencia_tema == True:   

                resultado=True
                cartaexterna = self.request.FILES.get('carta')
                fecha_recepcion = self.request.POST['recepcion_perfil']
                self.object.avance_tesis = 7    
                usuario_existe = Avance.objects.filter(user=self.object).exists()
                if not usuario_existe:
                    Avance.objects.create(user=self.object)     
                   
                SustentacionPerfilHistorial.objects.create(user=self.object,
                                                        fecha_recibido_documentos=fecha_recepcion_doc,
                                                        tema_perfil=tema_perfil, 
                                                        fecha_sustentacion=cronograma.fecha_3,  
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
                cronograma2 = get_object_or_404(Cronograma2,user=self.object)
                
                notificar = BancoNotificacion.objects.get(numero_notificacion=97)
                if notificar.enviar:
                    Post.objects.create(user=self.object.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(cronograma2.fecha_borrador.strftime("%d-%m-%Y")),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                     
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{self.object.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    self.object.notificacion=True
                docente_guia = form.cleaned_data['guia']
                notificar = BancoNotificacion.objects.get(numero_notificacion=83)
                if notificar.enviar:
                    Post.objects.create(user=self.object.usuario,title=notificar.titulo,text=notificar.contenido+", docente guía: "+str(docente_guia),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol) 
                
                fecha_recepcion = datetime.strptime(fecha_recepcion_doc, "%Y-%m-%d")
                fecha_formateada = fecha_recepcion.strftime("%d-%m-%Y")
                cronograma = get_object_or_404(Cronograma,user=self.object)
                
                CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Docente guia designado: "+str(docente_guia))
                CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Fecha de recepción del perfil mejorado: "+fecha_formateada,fecha_programada=cronograma.fecha_4,fecha_realizado=fecha_recepcion)
                


            if self.object.procedencia_tema == False:   
                
                resultado=False
                SustentacionPerfilHistorial.objects.create(user=self.object,
                                                        tema_perfil=tema_perfil, 
                                                        fecha_recibido_documentos=fecha_recepcion_doc,
                                                        fecha_sustentacion=cronograma.fecha_3, 
                                                        docente_guia=self.object.provisional,
                                                        resultado =resultado,
                                                        acta=acta_sustentacion,
                                                        hoja_evaluacion=hojaevaluacion,
                                                        documento_respaldo=documentorespaldo,
                                                        carta_externa_designacion=cartadesignacion,
                                                        tribunal_perfil_1=self.object.tribunalperfil.tribunal_perfil_1,
                                                        tribunal_perfil_2=self.object.tribunalperfil.tribunal_perfil_2, 
                                                        instancia=self.object.instancia)
                CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Derivación del maestrante al modulo de maestrante postulante por tema del perfil de tesis improcedente, Título del tema del perfil de tesis: "+str(tema_perfil))
                
                cronograma=get_object_or_404(Cronograma,user=self.object)
                tribunalperfil=get_object_or_404(TribunalPerfil,user=self.object)            
                           
                tribunalperfil.delete()
                cronograma.delete()
                

        
                self.object.provisional=None
                self.object.instancia += 1           
                self.object.maestrante_habilitado=False
                self.object.avance_tesis= None
                self.object.tema_perfil_postulado= None

                notificar = BancoNotificacion.objects.get(numero_notificacion=96)
                if notificar.enviar:
                    usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)
                    for usuario in usuarios_administradores:
                        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
                        channel_layer = get_channel_layer()
                        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                        usuario.notificacion=True
                        usuario.save()          
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
                maestrante.avance_tesis =8                              
                
                cronograma2=get_object_or_404(Cronograma2,user=maestrante)
                cronograma2.fecha_avance1=fecha
                cronograma2.save()
                notificar = BancoNotificacion.objects.get(numero_notificacion=8)
                
                date_obj = datetime.strptime(fecha, "%Y-%m-%d")
                foratted_date = date_obj.strftime("%d/%m/%Y")  
                if notificar.enviar:                                               
                    Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+" : "+str(foratted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente guía ]") 
                    guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
                    guia.notificacion=True
                    guia.save()
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})

                    Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(foratted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")  
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    maestrante.notificacion=True

                CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Fecha límite de presentación del primer avance programada: "+str(foratted_date)) 
                maestrante.save()
        
    return redirect('usuario:seguimiento_tesis') 


#Actividad 8---------- 	Registro de primer avance
#----- 	Registro de primer avance no aprobado
@login_required()
def RegistrarAvance(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    avance = get_object_or_404(Avance,user=maestrante)
    cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
    cronograma2.fecha_avance1=None
    cronograma2.save()
    avance.cap1=None
    avance.cap2=None
    avance.cap3=None
    avance.cap1_cualitativo = None
    avance.cap2_cualitativo = None
    avance.cap3_cualitativo = None
    avance.aceptar_avance=False
    avance.aprobacion=1
    avance.fecha_registro=None
    avance.save()
    maestrante.avance_tesis=7
    
    requisitos = get_object_or_404(Requisitos,nro_requisito=8)
    requisitos3 = get_object_or_404(Requisitos,nro_requisito=7)
    CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,usuario=request.user,observacion="Formulario del primer avance sin aprobación, Derivado a la actividad: "+str(requisitos3.actividad))

    maestrante.save()    
    return redirect('usuario:seguimiento_tesis')

#----- 	Registro de avance aprobado
@login_required()
def RegistrarAvanceAprobado(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.avance_tesis+=1
    
    
    if maestrante.avance_tesis == 9:
        
        usuario_existe = Avance_2.objects.filter(user=maestrante).exists()
        if not usuario_existe:
            Avance_2.objects.create(user=maestrante) 
        requisitos = get_object_or_404(Requisitos,nro_requisito=8)
        requisitos3 = get_object_or_404(Requisitos,nro_requisito=9)       
        CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,usuario=request.user,observacion="Primer avance aprobado, Derivado a la actividad: "+str(requisitos3.actividad))
     
    if maestrante.avance_tesis == 11:
        requisitos = get_object_or_404(Requisitos,nro_requisito=10)      
        requisitos3 = get_object_or_404(Requisitos,nro_requisito=11)  
        CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,usuario=request.user,observacion="Segundo avance aprobado, Derivado a la actividad: "+str(requisitos3.actividad))
        
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
                maestrante.avance_tesis =10
                
                
                cronograma2=get_object_or_404(Cronograma2,user=maestrante)
                cronograma2.fecha_avance2=fecha
                cronograma2.save()
                notificar = BancoNotificacion.objects.get(numero_notificacion=10)
                date_obj = datetime.strptime(fecha, "%Y-%m-%d")
                foratted_date = date_obj.strftime("%d/%m/%Y") 
                if notificar.enviar:                                                 
                    Post.objects.create(user=maestrante.guia.user,title=notificar.titulo,text=notificar.contenido+" : "+str(foratted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente guía ]")  
                    
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.guia.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    guia=get_object_or_404(Docente,id_docente=maestrante.guia.id_docente)
                    guia.notificacion=True
                    guia.save()
                    Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(foratted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]")   
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    maestrante.notificacion=True

                requisitos = get_object_or_404(Requisitos,nro_requisito=9) 
                CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Fecha límite de presentación de segundo avance programada: "+str(foratted_date)) 
                maestrante.save()
    return redirect('usuario:seguimiento_tesis') 


#Actividad 10---------- 	Registro de segundo avance
#----- 	Registro de segundo avance no aprobado
@login_required()
def RegistrarAvance2(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    avance = get_object_or_404(Avance_2,user=maestrante)
    cronograma2 = get_object_or_404(Cronograma2,user=maestrante)
    cronograma2.fecha_avance2=None
    cronograma2.save()
    avance.cap4=None
    avance.cap5=None
    avance.cap6=None
    avance.cap7=None
    avance.cap4_cualitativo = None
    avance.cap5_cualitativo = None
    avance.cap6_cualitativo = None
    avance.cap7_cualitativo = None
    avance.aceptar_avance = False
    avance.aprobacion=1
    avance.fecha = None
    avance.save()
    maestrante.avance_tesis=9
    requisitos = get_object_or_404(Requisitos,nro_requisito=10)
    requisitos3 = get_object_or_404(Requisitos,nro_requisito=9)
    CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,usuario=request.user,observacion="Formulario del segundo avance sin aprobación, Derivado a la actividad: "+str(requisitos3.actividad))
   
  
    maestrante.save() 
    return redirect('usuario:seguimiento_tesis')


# habilitacion de dias de prorroga 90 dias----------------------------
@login_required()
def HabilitarProrroga(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    cronograma2=get_object_or_404(Cronograma2,user=maestrante.maestrante)  
    requisitos = get_object_or_404(Requisitos,nro_requisito=104)   
    cronograma2.fecha_borrador_prorroga = cronograma2.fecha_borrador +timedelta(days=requisitos.tiempo)
    cronograma2.save()
    notificar = BancoNotificacion.objects.get(numero_notificacion=98)
    Post.objects.create(user=maestrante,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version)) 
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


#Actividad 11---------- Registro borrador de tesis ****compartido
@method_decorator(login_required, name='dispatch')
class RegistrarActividad11(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_11.html'
@login_required()
def FormularioActividad11(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        fecha_recepcion_borrador = request.POST['recepcion_borrador']        
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        cronograma2 = get_object_or_404(Cronograma2,user=maestrante)        
        maestrante.avance_tesis=12       
        cronograma2.fecha_recepcion_borrador=fecha_recepcion_borrador        
        cronograma2.save()
        requisitos = get_object_or_404(Requisitos,nro_requisito=11)  
        date_obj = datetime.strptime(fecha_recepcion_borrador, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%d/%m/%Y")  
        CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_borrador,fecha_realizado=fecha_recepcion_borrador,usuario=request.user,observacion="Fecha de recepción de borrador de tesis: "+str(formatted_date))
        CentroActividades.objects.create(maestrante=maestrante,actividad=requisitos,fecha_programada=cronograma2.fecha_borrador,fecha_realizado=fecha_recepcion_borrador,usuario=request.user,observacion="Borrador de tesis con aval de docente guia")
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 

@method_decorator(login_required, name='dispatch')
class RegistrarActividad11Compartido(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_11_compartido.html'
@login_required()
def FormularioActividad11Compartido(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        tema = request.POST['titulo']
        tema=tema.upper()
        nombramiento = request.FILES #returns a dict-like object
        nombramiento_revisor = nombramiento['nombramiento']
        
        documento_respaldo = request.FILES
        documentorespaldo = documento_respaldo['respaldo']       

        
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        cronograma2 = get_object_or_404(Cronograma2,user=maestrante)

        maestrante.tema_borrador_tesis=tema 
         
               
        cronograma2.borrador_tesis=True
        cronograma2.save()
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=11)  
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Título del borrador de tesis : "+str(tema)) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Solicitud de nombramiento de docente revisor",archivo_documento=nombramiento_revisor) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Otros documentos de respaldo (borrador de tesis,aval del docente guía, otros)",archivo_documento=documentorespaldo) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=112)
        
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)
            for usuario in usuarios_administradores:            
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 


#Actividad 12---------- Designar docente revisor ****compartido
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
            docente_revisor = form.cleaned_data['revisor']
            notificar = BancoNotificacion.objects.get(numero_notificacion=113)
            if notificar.enviar:
                usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)
                for usuario in usuarios_administradores:
                    Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
                    channel_layer = get_channel_layer()
                    async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                    usuario.notificacion=True
                    usuario.save() 
            requisitos = get_object_or_404(Requisitos,nro_requisito=12)  
            CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos,observacion="Docente revisor designado: "+str(docente_revisor)) 
            self.object = form.save()
            
            return redirect(self.get_success_url())

        return self.form_invalid(form)    
  


@method_decorator(login_required, name='dispatch')
class RegistrarActividad12Compartido(UpdateView):

    model = Maestrante
    template_name = 'usuario/act/actividad_12_compartido.html'
    form_class = FormularioDocenteRevisorCompartido
    success_url = reverse_lazy('usuario:seguimiento_tesis')
    
    def post(self, request, *args, **kwargs):       

        self.object = self.get_object()

        form = FormularioDocenteRevisorCompartido(request.POST, request.FILES, instance=self.object)

        if form.is_valid():        
            self.object = form.save(commit=False)
            self.object.avance_tesis = 13
          
            
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

           
            cronograma2 = get_object_or_404(Cronograma2,user=self.object)
            cronograma2.fecha_formulario_revisor=final_date
            cronograma2.save()
        
            requisitos2 = get_object_or_404(Requisitos,nro_requisito=12)  
            
            archivo_adjunto = request.FILES.get('nombramiento_revisor')
            self.object.archivo_documento = archivo_adjunto


            fecha_nombramiento = form.cleaned_data['fecha_nombramiento']
            
            fecha_formateada = fecha_nombramiento.strftime("%d-%m-%Y")
            CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos2,observacion="Solicitud de nombramiento de docente revisor",archivo_documento=self.object.archivo_documento)
            CentroActividades.objects.create(maestrante=self.object,usuario=request.user,actividad=requisitos2,observacion="Fecha de notificación del nombramiento y entrega de borrador: "+str(fecha_formateada)) 
            notificar = BancoNotificacion.objects.get(numero_notificacion=19)
            if notificar.enviar:
                Post.objects.create(user=self.object.usuario,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(self.object.revisor),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]") 
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                self.object.notificacion=True

                Post.objects.create(user=self.object.revisor.user,title=notificar.titulo,text=notificar.contenido+", Docente revisor : "+str(self.object.revisor),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente revisor ]") 
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                revisor = get_object_or_404(Usuario,username=self.object.revisor.user.username)  
                revisor.notificacion=True
                revisor.save()
            notificar = BancoNotificacion.objects.get(numero_notificacion=12)
            if notificar.enviar:
                Post.objects.create(user=self.object.usuario,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ]") 
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                self.object.notificacion=True 

                Post.objects.create(user=self.object.revisor.user,title=notificar.titulo,text=notificar.contenido+" : "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(self.object),programa = str(self.object.programa)+" - "+str(self.object.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente revisor ]") 
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{self.object.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                revisor = get_object_or_404(Usuario,username=self.object.revisor.user.username)  
                revisor.notificacion=True
                revisor.save()
            usuario_existe = Informe.objects.filter(user=self.object).exists()
            if not usuario_existe:   
                Informe.objects.create(user=self.object) 
            self.object = form.save()

            
            return redirect(self.get_success_url())

        return self.form_invalid(form)
# Actividad 15 ------------ R-0877 Reporte general
@login_required()
def ProcedenteReporte(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=16) 
    maestrante.avance_tesis=16
    
    new_date=date.today()
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
    
    cronograma2.fecha_tesis_habilitada= final_date
    cronograma2.save()

    final_date = final_date.strftime("%Y-%m-%d")
    date_obj = datetime.strptime(final_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%d/%m/%Y")  

    notificarm = BancoNotificacion.objects.get(numero_notificacion=23)
    if notificarm.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificarm.titulo,text=notificarm.contenido+", fecha límite de presentación: "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificarm.numero_notificacion),rol=notificarm.rol)  
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
    requisitos2 = get_object_or_404(Requisitos,nro_requisito=15)
    
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos2,observacion="Reportes aprobados ")

    maestrante.save()
    return redirect('usuario:seguimiento_tesis')
@login_required()
def ActivarReporte2(request,pk):
    
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    reporte=get_object_or_404(ReporteGeneral,user=maestrante)
    reporte.activar_reporte2=True
    requisitos = get_object_or_404(Requisitos,nro_requisito=105)
    new_date=date.today()
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
    cronograma2.fecha_reporte_general2=final_date
    cronograma2.save()
    
    
    
    formatted_date =  final_date.strftime("%d/%m/%Y")

    notificar = BancoNotificacion.objects.get(numero_notificacion=92)
    if notificar.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificar.titulo,text=notificar.contenido+", fecha límite de presentación : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Maestrante ] ")   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True

        Post.objects.create(user=maestrante.revisor.user,title=notificar.titulo,text=notificar.contenido+", fecha límite de presentación : "+str(formatted_date),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol="[ Docente revisor ]")    
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.revisor.user.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        revisor = get_object_or_404(Usuario,username=maestrante.revisor.user.username)  
        revisor.notificacion=True
        revisor.save()
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,fecha_programada=cronograma2.fecha_reporte_general,fecha_realizado=reporte.fecha_registro) 
    
    reporte.save()

    return redirect('usuario:seguimiento_tesis')

# Actividad 16 ------------ Tesis para habilitación a defensa  ****compartido
@method_decorator(login_required, name='dispatch')
class RegistrarActividad16(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_16.html'
@login_required()
def FormularioActividad16(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  

        maestrante.avance_tesis=17
        usuario_existe = TribunalTesis.objects.filter(user=maestrante).exists()
        if not usuario_existe:          
            TribunalTesis.objects.create(user=maestrante)
        requisitos = get_object_or_404(Requisitos,nro_requisito=16) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Registro de solicitud de pago de docente revisor adjunto reporte") 
        maestrante.save()
    return redirect('usuario:seguimiento_tesis') 

@method_decorator(login_required, name='dispatch')
class RegistrarActividad16Compartido(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_16_compartido.html'
@login_required()
def FormularioActividad16Compartido(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        tema = request.POST['titulo']
        informe = request.FILES 
        informe_aval = informe['informe']  
        tesis = request.FILES
        tesis_documento = tesis['tesis']   
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)  
        maestrante.tema_tesis=tema      
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=16)
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Registro titulo del tema: "+tema.upper()) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Informe aval de docente guía",archivo_documento=informe_aval) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Documento de tesis",archivo_documento=tesis_documento) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=114)
        
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)
            for usuario in usuarios_administradores:            
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
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

        cronograma2 = get_object_or_404(Cronograma2,user=maestranteid)
        
        fecha_formateada = cronograma2.fecha_sustentacion.strftime("%d-%m-%Y")
        hora_formateada = cronograma2.hora_sustentacion.strftime("%H:%M")
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=17)
        tribunaltesis = get_object_or_404(TribunalTesis,user=maestranteid)
        

        CentroActividades.objects.create(maestrante=maestranteid,usuario=self.request.user,actividad=requisitos,observacion="Tribunal interno 1 designado (Presidente de Tribunal): "+str(tribunaltesis.tribunal_tesis_1)+", Tribunal interno 2 designado (Docente de Área - Revisor): "+str(tribunaltesis.tribunal_tesis_2)+", Fecha del acto de sustentación : "+fecha_formateada+", Hora del acto de sustentación : "+hora_formateada)
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=20)
        if notificar.enviar:
            Post.objects.create(user=maestranteid.usuario,title=notificar.titulo,text=notificar.contenido+", fecha: "+str(fecha_formateada)+" - hora: "+str(hora_formateada),maestrante= str(maestranteid),programa = str(maestranteid.programa)+" - "+str(maestranteid.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{maestranteid.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            maestranteid.notificacion=True
        maestranteid.avance_tesis=18       
        maestranteid.save()

# Actividad 18 ------------- Dictamen de la defensa de tesis.
@login_required()
def ProcedenteTesis(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.procedencia_tesis=True
    maestrante.avance_tesis=19
    
    requisitos = get_object_or_404(Requisitos,nro_requisito=20)
    new_date=date.today()
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
    cronograma2.fecha_tesis_mejorada = final_date
    cronograma2.save()
    notificarmaes = BancoNotificacion.objects.get(numero_notificacion=89)
    if notificarmaes.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificarmaes.titulo,text=notificarmaes.contenido+", fecha: "+str(final_date.strftime("%d-%m-%Y")),maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificarmaes.numero_notificacion),rol=notificarmaes.rol)   
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True

    notificar = BancoNotificacion.objects.get(numero_notificacion=22)
    if notificar.enviar:
        usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)    
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()

    requisitos = get_object_or_404(Requisitos,nro_requisito=18)
    
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Tesis procedente")
    maestrante.save()
    return redirect('usuario:seguimiento_tesis') 
@login_required()
def ImProcedenteTesis(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    maestrante.procedencia_tesis=False
    maestrante.avance_tesis=19
    notificarmaes = BancoNotificacion.objects.get(numero_notificacion=88)
    if notificarmaes.enviar:
        Post.objects.create(user=maestrante.usuario,title=notificarmaes.titulo,text=notificarmaes.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificarmaes.numero_notificacion),rol=notificarmaes.rol)  
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f'chat_{maestrante.usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        maestrante.notificacion=True
    notificar = BancoNotificacion.objects.get(numero_notificacion=22)
    if notificar.enviar:
        usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)    
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()
    requisitos = get_object_or_404(Requisitos,nro_requisito=18)
    CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Tesis improcedente")
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
        maestrante.titulo_de_tesis=tema
        maestrante.dictamen_escala=escala 
        maestrante.dictamen_nota=numeral
        if maestrante.procedencia_tesis:
            maestrante.avance_tesis=20
        else:
            maestrante.avance_tesis=24
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=19)
        SustentacionTesisHistorial.objects.create(user=maestrante,
                                                   fecha=date.today(),     
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
                                                   instancia=maestrante.instancia_defensa,
                                                   ) 
        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos) 



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
        #notificar = BancoNotificacion.objects.get(numero_notificacion=87)
        #if notificar.enviar:
        #    usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)    
        #    for usuario in usuarios_administradores:
        #        Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)  
        #        channel_layer = get_channel_layer()
        #        async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
        #        usuario.notificacion=True
        #        usuario.save()          
 
        maestrante.avance_tesis=21
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=20)
        if not obs:
            obs = "Ninguno"

        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Aprobación para empaste de Tesis, Observaciones: "+obs) 
        
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 


# Actividad 21 ------------- Solicitud de pago a docente guia *****compartido
@method_decorator(login_required, name='dispatch')
class RegistrarActividad21(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_21.html'
@login_required()
def FormularioActividad21(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)   
        maestrante.avance_tesis=22        
        requisitos = get_object_or_404(Requisitos,nro_requisito=21) 
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Confirmación de la fecha de recepción de solicitud de pago") 
        
        maestrante.save() 

    return redirect('usuario:seguimiento_tesis') 


@method_decorator(login_required, name='dispatch')
class RegistrarActividad21Compartido(DetailView):

    model = Maestrante
    template_name = 'usuario/act/actividad_21_compartido.html'
@login_required()
def FormularioActividad21Compartido(request):
    if  request.method =='POST':
        id_maestrante =  request.POST['id_maestrante']
        maestrante = get_object_or_404(Maestrante,id_maestrante=id_maestrante)
        fecha_recepcion = request.POST['fecha_recepcion']  
        obs = request.POST['obs']
        maestrante.recepcion_solicitud = fecha_recepcion  
        maestrante.observacion_pago = obs         

        fecha_recepcion = datetime.strptime(fecha_recepcion, "%Y-%m-%d")
        fecha_formateada = fecha_recepcion.strftime("%d-%m-%Y")
        requisitos = get_object_or_404(Requisitos,nro_requisito=21)
 
        if not obs:
            obs = "Ninguno"
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Fecha de recepción de solicitud de coordinación de investigación: "+fecha_formateada+", Observaciones: "+obs) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=115)
        
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)
            for usuario in usuarios_administradores:            
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)                
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()
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
        
        maestrante.avance_tesis=23
        
        requisitos = get_object_or_404(Requisitos,nro_requisito=22)

        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos) 
        notificar = BancoNotificacion.objects.get(numero_notificacion=85)
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True)    
            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()  
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
   
        maestrante.avance_tesis =1000
        #1000 maestrante graduado
        maestrante.tesis_terminado = True
        maestrante.maestrante_habilitado = False
        requisitos = get_object_or_404(Requisitos,nro_requisito=23)
 
        
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,observacion="Registro de ecepción de empastado y CD para archivo, Año de empastado :"+gestion) 
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
        reporte = request.FILES
        reporte_segunda_instancia = reporte['reporte_general']
        tribunaltesis=get_object_or_404(TribunalTesis,user=maestrante)   
        ReporteGeneralTribunalInterno.objects.create(user=maestrante,tribunal=tribunaltesis.tribunal_tesis_2,reporte=reporte_segunda_instancia,fecha_registro=timezone.now())
        maestrante.avance_tesis=16 
        maestrante.instancia_defensa += 1 
        
        
        notificar = BancoNotificacion.objects.get(numero_notificacion=21)
        if notificar.enviar:
            usuarios_administradores = Usuario.objects.filter(rol_tecnico_investigacion=True) 

            for usuario in usuarios_administradores:
                Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)     
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
                usuario.notificacion=True
                usuario.save()       
        
        if maestrante.procedencia_tesis == False:
            cronograma2=get_object_or_404(Cronograma2,user=maestrante)
             
            tribunaltesis.tribunal_tesis_1 = None
            tribunaltesis.tribunal_tesis_2 = None
            cronograma2.fecha_sustentacion = None
            cronograma2.hora_sustentacion = None
            maestrante.tema_tesis = None
            cronograma2.save()
            tribunaltesis.save()
        requisitos=get_object_or_404(Requisitos,nro_requisito=24)
        CentroActividades.objects.create(maestrante=maestrante,usuario=request.user,actividad=requisitos,archivo_documento=reporte_segunda_instancia) 
        maestrante.save()   


    return redirect('usuario:seguimiento_tesis') 
# Actividad 25 ------------ Reporte general de tribunal interno
@login_required()
def ProcedenteReporteTribunalInterno(request,pk):
    maestrante = get_object_or_404(Maestrante,id_maestrante=pk)
    requisitos = get_object_or_404(Requisitos,nro_requisito=25) 
    maestrante.avance_tesis=16 
    maestrante.instancia_defensa += 1 

    #notificarmaes = BancoNotificacion.objects.get(numero_notificacion=23)
    #Post.objects.create(user=maestrante,title=notificarmaes.titulo,text=notificarmaes.contenido+" : "+str(maestrante)+", fecha: "+str(final_date.strftime("%d-%m-%Y"))) 
    #channel_layer = get_channel_layer()
    #async_to_sync(channel_layer.group_send)(f'chat_{maestrante.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
   # maestrante.notificacion=True
    
    notificar = BancoNotificacion.objects.get(numero_notificacion=21)
    if notificar.enviar:
        usuarios_administradores = Usuario.objects.filter(rol_postgrado=True)    
        for usuario in usuarios_administradores:
            Post.objects.create(user=usuario,title=notificar.titulo,text=notificar.contenido+" : ",maestrante= str(maestrante),programa = str(maestrante.programa)+" - "+str(maestrante.version),cod_notificacion=str(notificar.numero_notificacion),rol=notificar.rol)   
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(f'chat_{usuario.username}',{'type': 'chat_message','message': 'Notificar','username': 'System'})
            usuario.notificacion=True
            usuario.save()       

    CentroActividades.objects.create(maestrante=maestrante.maestrante,usuario=request.user,evidencia=requisitos.actividad)
    if maestrante.procedencia_tesis == False:
        cronograma2=get_object_or_404(Cronograma2,user=maestrante.maestrante)
        tribunaltesis=get_object_or_404(TribunalTesis,user=maestrante.maestrante)  
        tribunaltesis.tribunal_tesis_1 = None
        tribunaltesis.tribunal_tesis_2 = None
        cronograma2.fecha_sustentacion = None
        cronograma2.hora_sustentacion = None
        cronograma2.save()
        tribunaltesis.save()
    maestrante.save()

    return redirect('usuario:seguimiento_tesis')
