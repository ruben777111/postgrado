"""sispostgrado URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path,include,re_path
from postgradoApp.views import index,exit
from django.contrib.auth import views as auth_views
from usuario.models import Usuario
urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('usuario/',include(('usuario.urls','usuario'))),
  
    path('video/', include(('video.urls','video'))),
    path('documento/', include(('documento.urls','documento'))),
    path('', index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('rooms/', include('room.urls')),
    path('notificacion/', include('notify.urls')),
    path('notipostgrado/', include('notipostgrado.urls')),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="autenticacion/password-reset.html"), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="autenticacion/password-confirm.html"), name='password_reset_confirm'),
    path('reset_password/complete/', auth_views.PasswordResetCompleteView.as_view(template_name="autenticacion/password_reset_complete.html"), name='password_reset_complete'),
    
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
   path('notification/',include('notification.urls')),
    ]

urlpatterns += [
    re_path(r'^tesis/(?P<path>.*)$',serve,{
        'document_root':settings.MEDIA_ROOT,

    })
]