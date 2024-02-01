from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    
   
    
     path('notificar_usuario/<int:user_id>/', views.notificar_usuario, name='notificar_usuario'),
]