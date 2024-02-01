from django.urls import path
from django.conf import settings
from django.contrib.staticfiles.urls import static
from .views import exit
from postgradoApp.views import index,exit

#path('inicio', views.index, name='index')
urlpatterns = [

    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)