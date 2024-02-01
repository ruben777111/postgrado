from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from notify.models import Notification

from django.views.generic import ListView,View,DetailView

from swapper import load_model

Notificacion = load_model('notify', 'Notification')
@method_decorator(login_required, name='dispatch')
class ListaNotificaciones(ListView):
    model=Notification
    template_name='notificacion/listar_notificacion.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        return self.request.user.notificaciones.all().order_by('-id')
 
@method_decorator(login_required, name='dispatch')
class ListaNotificacionesNoLeido(ListView):
    model=Notification
    template_name='notificacion/listar_notificacion.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        return self.request.user.notificaciones.filter(read=False)
 
@method_decorator(login_required, name='dispatch')
class ListaNotificacionesLeido(ListView):
    model=Notification
    template_name='notificacion/listar_notificacion.html'
    context_object_name = 'actividades'
    
    def get_queryset(self):
        return self.request.user.notificaciones.filter(read=True)
 


		

@method_decorator(login_required, name='dispatch')
class NotificationList(ListView):
	model = Notificacion
	template_name = 'notificacion/notify.html'
	context_object_name = 'notify'


	def dispatch(self, requets, *args, **kwargs):
		return super(NotificationList, self).dispatch(requets, *args, **kwargs)


	def get_queryset(self):
          if  self.request.user.notificacion: 
        
            self.request.user.notificacion=False
            self.request.user.save()
          return self.request.user.notificaciones.all().order_by('-id').filter(read=False)


def VerNotificacion(request,slug):
	noticacionid = get_object_or_404(Notificacion,slug=slug)
	template_name="notificacion/detalle_notificacion.html"
	
	if not noticacionid.read:
		noticacionid.read=True
		noticacionid.save()
	employers=Notificacion.objects.filter(slug=slug)

	context = { 'maestrantes':employers }
	return render(request,template_name,context)

