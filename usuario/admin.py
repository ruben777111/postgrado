from django.contrib import admin
from usuario.models import ReporteGeneralTribunalInterno,SustentacionTesisHistorial,BancoNotificacion,AvanceHistorial,Avance_2_Histoiral,SustentacionPerfilHistorial,DocenteProvisional,TribunalPerfil,TribunalTesis,InformeGuiaFormulario,InformeGuia,InformeRevisor,Post,AsistenciaInduccion,Avance,Avance_2,Informe,ReporteGeneral,Programa,Requisitos,Cronograma,Cronograma2,CentroActividades,Docente_Revisor,Usuario,Maestrante,Administracion,Docente
# Register your models here.
admin.site.register(Usuario)

admin.site.register(SustentacionTesisHistorial)
admin.site.register(BancoNotificacion)
admin.site.register(ReporteGeneralTribunalInterno)
admin.site.register(Maestrante)
admin.site.register(Administracion)
admin.site.register(SustentacionPerfilHistorial)
admin.site.register(Docente)
admin.site.register(DocenteProvisional)

admin.site.register(Docente_Revisor)
admin.site.register(CentroActividades)

admin.site.register(Cronograma)
admin.site.register(Cronograma2)

admin.site.register(Requisitos)
admin.site.register(ReporteGeneral)
admin.site.register(Programa)
admin.site.register(Informe)
admin.site.register(AsistenciaInduccion)
admin.site.register(Avance)
admin.site.register(Avance_2)
admin.site.register(AvanceHistorial)
admin.site.register(Avance_2_Histoiral)
admin.site.register(Post)
admin.site.register(InformeRevisor)
admin.site.register(InformeGuia)
admin.site.register(InformeGuiaFormulario)
admin.site.register(TribunalTesis)
admin.site.register(TribunalPerfil)



