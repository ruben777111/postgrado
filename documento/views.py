from django.shortcuts import render,redirect

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.messages.views import SuccessMessageMixin
from .forms import DocumentoForm
from documento.models import Documento
from django.views.generic import View,TemplateView,ListView,UpdateView, CreateView,DeleteView
from django.urls import reverse_lazy


# Create your views here.
#vistas basada en Clases
#class ListadoGuia(ListView):


@method_decorator(login_required, name='dispatch')
class ListadoDocumento(View):
    
    model = Documento
    template_name = 'documento/listar_documento.html'
    context_object_name = 'documentos'
    queryset = Documento.objects.filter(estado_documento = True)
    
    def get_queryset(self):
        return self.model.objects.filter(estado_documento=True)
    def get_context_data(self, **kwargs):
        contexto={}
        contexto['documentos']=self.get_queryset()
        return contexto
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name,self.get_context_data())
    


@method_decorator(login_required, name='dispatch')
class ActualizarDocumento(UpdateView):

    model = Documento
    template_name = 'documento/editar_documento.html'
    form_class = DocumentoForm
    success_url = reverse_lazy('documento:listar_documento')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['documentos'] = Documento.objects.filter(estado_documento = True)
        return context

        
@method_decorator(login_required, name='dispatch')
class AgregarDocumento(CreateView):
    model = Documento    
    form_class = DocumentoForm
    template_name = 'documento/agregar_documento.html'
    success_url = reverse_lazy('documento:listar_documento')

@method_decorator(login_required, name='dispatch')
class EliminarDocumento(DeleteView):
    model = Documento

    def post(self,request,pk,*args,**kwargs):
        object = Documento.objects.get(id_documento = pk)
        object.estado_documento = False
        object.save()
        return redirect ('documento:listar_documento')