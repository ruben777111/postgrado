from django.urls import path
from . import views
from .views import NotificationList,ListaNotificaciones,VerNotificacion

urlpatterns = [

	path('notify/', NotificationList.as_view(), name='notify'),
    path('vernotificaciondel_usuario/<slug:slug>',views.VerNotificacion, name = 'vernotificacion'),
    
    
    path('lista_notificacion/',views.ListaNotificaciones.as_view(), name = 'lista_notificacion'),
    path('lista_notificacion_no_leido/',views.ListaNotificacionesNoLeido.as_view(), name = 'lista_notificacion_no_leido'),
    path('lista_notificacion_leido/',views.ListaNotificacionesLeido.as_view(), name = 'lista_notificacion_leido')
]