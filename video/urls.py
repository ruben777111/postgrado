from django.urls import path,re_path
from . import views
urlpatterns = [
    path('agregar_video/', views.AgregarVideo.as_view(), name='agregar_video'),
    path('listar_video/',views.ListadoVideo.as_view(), name='listar_video'),
    path('editar_video/<int:pk>',views.ActualizarVideo.as_view(), name = 'editar_video'),
    path('eliminar_video/<int:pk>',views.EliminarVideo.as_view(), name = 'eliminar_video')
    ]