from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.VerNotificaciones, name='notifications'),
     path('send_notification/', views.send_notification, name='send_notification'),
    # Otras rutas URL de tu aplicación
]