from django.shortcuts import render,redirect

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from .forms import VideoForm
from video.models import Video
from django.views.generic import View,TemplateView,ListView,UpdateView, CreateView,DeleteView
from django.urls import reverse_lazy


# Create your views here.
#vistas basada en Clases
#class ListadoGuia(ListView):


@method_decorator(login_required, name='dispatch')
class ListadoVideo(View):
    
    model = Video
    template_name = 'video/listar_video.html'
    context_object_name = 'videos'
    queryset = Video.objects.filter(estado_video = True)
    
    def get_queryset(self):
        return self.model.objects.filter(estado_video=True)
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['videos']=self.get_queryset()
        return contexto
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())
    


@method_decorator(login_required, name='dispatch')
class ActualizarVideo(UpdateView):

    model = Video
    template_name = 'video/editar_video.html'
    form_class = VideoForm
    success_url = reverse_lazy('video:listar_video')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['videos'] = Video.objects.filter(estado_video = True)
        return context

        
@method_decorator(login_required, name='dispatch')
class AgregarVideo(CreateView):
    model = Video    
    form_class = VideoForm
    template_name = 'video/agregar_video.html'
    success_url = reverse_lazy('video:listar_video')

@method_decorator(login_required, name='dispatch')
class EliminarVideo(DeleteView):
    model = Video

    def post(self,request,pk,*args,**kwargs):
        object = Video.objects.get(id_video = pk)
        object.estado_video = False
        object.save()
        return redirect ('video:listar_video')
