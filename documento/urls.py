from django.urls import path,re_path
from . import views
urlpatterns = [
    path('agregar_documento/', views.AgregarDocumento.as_view(), name='agregar_documento'),
    path('listar_documento/',views.ListadoDocumento.as_view(), name='listar_documento'),
    path('editar_documento/<int:pk>',views.ActualizarDocumento.as_view(), name = 'editar_documento'),
    path('eliminar_documento/<int:pk>',views.EliminarDocumento.as_view(), name = 'eliminar_documento')
    ]