from django.urls import path, re_path
from django.views.generic.base import TemplateView
from django.contrib.admin.views.decorators import staff_member_required
from . import views,requisitos
from django.contrib.auth import views as auth_views
urlpatterns=[
   
   
    path('password/',views.CustomPasswordResetView.as_view(template_name="autenticacion/password-reset.html"), name='password'),
    path('backup/', views.backup_database, name='backup_database'),
    
    #path('password/',views.CustomPasswordResetView.as_view(),name='password'),
    path('listado_docente/',views.ListadoDocente.as_view(),name='listar_docente'),
    path('listado_maestrante/',staff_member_required(views.ListadoMaestrante.as_view(),login_url='index'),name='listar_maestrante'),
    path('listado_maestrante_tesis_concluido/',staff_member_required(views.ListadoMaestranteGraduado.as_view(),login_url='index'),name='listado_maestrante_tesis_concluido'),
    path('listado_postulante/',staff_member_required(views.ListadoPostulante.as_view(),login_url='index'),name='listar_postulante'),
    path('listado_administradores/',staff_member_required(views.ListadoAdministradores.as_view(),login_url='index'),name='listar_administradores'),     
    path('listado_programa/',staff_member_required(views.ListadoPrograma.as_view(),login_url='index'),name='listar_programa'),
    path('inicio_evidencia/',TemplateView.as_view(template_name='usuario/listar_evidencia.html'),name='inicio_evidencia'),
    path('listado_evidencia/',staff_member_required(views.ListaEvidencia.as_view(),login_url='index'),name='listado_evidencia'),    
    path('listado_banco_notificacion/',staff_member_required(views.ListaBancoNotificacion.as_view(),login_url='index'),name='listado_banco_notificacion'),    
    path('listado_historial/',staff_member_required(views.ListadoCentroActividades.as_view(),login_url='index'),name='listar_historial'),   
    path('listado_tiempo/',staff_member_required(views.ListadoTiempoActividad.as_view(),login_url='index'),name='listado_tiempo'),   
    path('listado_designar/',staff_member_required(views.DesignarDocente.as_view(),login_url='index'),name='listar_designar'), 
    path('listado_asesoramiento/',staff_member_required(views.ListaAsesoramiento.as_view(),login_url='index'),name='listar_asesoramiento'), 
    path('listado_tribunal_perfil/',staff_member_required(views.DesignarTribunalPerfil.as_view(),login_url='index'),name='listar_tribunal_perfil'), 
    path('listado_tribunal_tesis/',staff_member_required(views.DesignarTribunalTesis.as_view(),login_url='index'),name='listar_tribunal_tesis'), 
    path('listado_actividades/',staff_member_required(views.ListaActividades.as_view(),login_url='index'),name='listar_actividades'), 
    

    path('listado_tema_tesis/',staff_member_required(views.ListaTemaTesis.as_view(),login_url='index'),name='listar_tema_tesis'),
    path('listado_tesis_maestrante/',staff_member_required(views.ListadoTesisMaestrante.as_view(),login_url='index'),name='listar_tesis_maestrante'),   
    path('seguimiento_tesis/',staff_member_required(views.SeguimientoTesis.as_view(),login_url='index'),name='seguimiento_tesis'),
    path('registrar_docente/',staff_member_required(views.RegistrarDocente.as_view(),login_url='index'),name='registrar_docente'),
    path('listado_sustentacion_perfil/',staff_member_required(views.ListadoSustentacionPerfil.as_view(),login_url='index'),name='listar_sustentacion_perfil'),   
    path('listado_sustentacion_perfil_historial/',staff_member_required(views.ListadoSustentacionPerfilHistorial.as_view(),login_url='index'),name='listar_sustentacion_perfil_historial'),   
    path('listado_sustentacion_tesis_historial/',staff_member_required(views.ListadoSustentacionTesisHistorial.as_view(),login_url='index'),name='listar_sustentacion_tesis_historial'),   
    
    path('listado_sustentacion_tesis/',staff_member_required(views.ListadoSustentacionTesis.as_view(),login_url='index'),name='listar_sustentacion_tesis'),   

    path('registrar_docente_provisional/<int:pk>',staff_member_required(views.ActualizarDocenteProvisional.as_view(),login_url='index'),name='registrar_docente_provisional'),
    path('registrar_fecha_sustentacion/<int:pk>',staff_member_required(views.FechaHoraSustentacion.as_view(),login_url='index'),name='registrar_fecha_sustentacion'),
    path('registrar_maestrante/',staff_member_required(views.RegistrarMaestrante.as_view(),login_url='index'),name='registrar_maestrante'),    
    path('registrar_programa/',staff_member_required(views.RegistrarPrograma.as_view(),login_url='index'),name='registrar_programa'),    
    path('registrar_administradores/',staff_member_required(views.RegistrarAdministradores.as_view(),login_url='index'),name='registrar_administradores'),
    path('listado_asistencia/',staff_member_required(views.ListadoAsistencia.as_view(),login_url='index'),name='listar_asistencia'),
    path('registrar_asistencia/',staff_member_required(views.RegistroAsistencia.as_view(),login_url='index'),name='registrar_asistencia'),
    path('asistencia/',staff_member_required(views.Asistencia,login_url='index'),name='asistencia'),
    path('formulario_asistencia/<int:pk>',staff_member_required(views.FormularioAsistencia.as_view(),login_url='index'),name='formulario_asistencia'),
    path('editar_docente/<int:pk>',staff_member_required(views.ActualizarDocente.as_view(),login_url='index'), name = 'editar_docente'),  
    path('editar_administrador/<int:pk>',staff_member_required(views.ActualizarAdministrador.as_view(),login_url='index'), name = 'editar_administrador'),
    path('editar_evidencia/<int:pk>',staff_member_required(views.EditarEvidencia.as_view(),login_url='index'), name = 'editar_evidencia'),
    path('editar_banco_notificacion/<int:pk>',staff_member_required(views.EditarBancoNotificacion.as_view(),login_url='index'), name = 'editar_banco_notificacion'),
    path('editar_maestrante/<int:pk>',staff_member_required(views.ActualizarMaestrante.as_view(),login_url='index'), name = 'editar_maestrante'),
    path('editar_tribunal_perfil/<int:pk>',staff_member_required(views.EditarTribunalPerfil.as_view(),login_url='index'), name = 'editar_tribunal_perfil'),
    path('editar_tribunal_tesis/<int:pk>',staff_member_required(views.EditarTribunalTesis.as_view(),login_url='index'), name = 'editar_tribunal_tesis'),
    path('editar_programa/<int:pk>',staff_member_required(views.ActualizarPrograma.as_view(),login_url='index'), name = 'editar_programa'),  
    path('registrar_tema_tesis/<int:pk>',staff_member_required(views.RegistrarTemaTesis.as_view(),login_url='index'),name='registrar_tema_tesis'),    



    path('busqueda/',staff_member_required(views.Busqueda,login_url='index'),name="busqueda"),
    path('busqueda_varios/<int:pk>',staff_member_required(views.BusquedaVarios,login_url='index'),name='busqueda_varios'),    
    path('busquedahistorial/',staff_member_required(views.BusquedaHistorial,login_url='index'),name="busquedahistorial"),


    path('busquedaperfilhistorial/',staff_member_required(views.busquedaperfilhistorial,login_url='index'),name="busquedaperfilhistorial"),
    path('busquedatesishistorial/',staff_member_required(views.busquedatesishistorial,login_url='index'),name="busquedatesishistorial"),
    path('busquedahistorialindividual/',views.BusquedaHistorialIndividual,name="busquedahistorialindividual"),
    path('busquedaasistencia/',staff_member_required(views.BusquedaAsistencia,login_url='index'),name="busquedaasistencia"),
    path('busquedatesis/',staff_member_required(views.BusquedaTesis,login_url='index'),name="busquedatesis"),    
    path('maestrante_eliminar/<int:pk>',staff_member_required(views.MaestranteEliminar,login_url='index'), name = 'maestrante_eliminar'),
    
    path('docente_eliminar/<int:pk>',staff_member_required(views.DocenteEliminar,login_url='index'), name = 'docente_eliminar'),
    path('docente_habilitar/<int:pk>',staff_member_required(views.DocenteHabilitar,login_url='index'), name = 'docente_habilitar'),
    path('habilitar_numero/<int:pk>',staff_member_required(views.HabilitarNumero,login_url='index'), name = 'habilitar_numero'),
    path('deshabilitar_numero/<int:pk>',staff_member_required(views.DeshabilitarNumero,login_url='index'), name = 'deshabilitar_numero'),
    path('perfil_tesis_eliminar/<int:pk>',staff_member_required(views.EliminarPerfilTesis,login_url='index'), name = 'perfil_tesis_eliminar'),
    path('quitarlista/<int:pk>',staff_member_required(views.QuitarLista,login_url='index'), name = 'quitarlista'),



    path('maestrante_habilitar/<int:pk>',staff_member_required(requisitos.MaestranteHabilitar,login_url='index'), name = 'maestrante_habilitar'),
    path('actividad_01/<int:pk>',staff_member_required(requisitos.RegistrarActividad01,login_url='index'), name = 'actividad_01'),
    path('actividad_0/<int:pk>',staff_member_required(requisitos.RegistrarActividad0.as_view(),login_url='index'), name = 'actividad_0'),
    path('formulario_actividad_0/',staff_member_required(requisitos.FormularioActividad0,login_url='index'), name = 'formulario_actividad_0'),
        
    path('actividad_1/<int:pk>',staff_member_required(requisitos.RegistrarActividad1.as_view(),login_url='index'), name = 'actividad_1'),
    path('actividad_2/<int:pk>',staff_member_required(requisitos.RegistrarActividad2.as_view(),login_url='index'), name = 'actividad_2'),
    path('actividad_3/<int:pk>',staff_member_required(requisitos.RegistrarActividad3.as_view(),login_url='index'), name = 'actividad_3'),
    path('procedencia_perfil/<int:pk>',staff_member_required(requisitos.ProcedentePerfil,login_url='index'), name = 'procedencia_perfil'),
    path('improcedencia_perfil/<int:pk>',staff_member_required(requisitos.ImProcedentePerfil,login_url='index'), name = 'improcedencia_perfil'),
    path('procedencia_reporte/<int:pk>',staff_member_required(requisitos.ProcedenteReporte,login_url='index'), name = 'procedencia_reporte'),
    path('procedencia_reporte_tribunal_interno/<int:pk>',staff_member_required(requisitos.ProcedenteReporteTribunalInterno,login_url='index'), name = 'procedencia_reporte_tribunal_interno'),
    path('activar_reporte_2/<int:pk>',staff_member_required(requisitos.ActivarReporte2,login_url='index'), name = 'activar_reporte_2'),
    
    
    path('docente_guia_4/<int:pk>',staff_member_required(requisitos.RegistrarDocenteGuia.as_view(),login_url='index'), name = 'docente_guia_4'),
    
    
    path('actividad_6/',staff_member_required(requisitos.RegistrarActividad6,login_url='index'), name = 'actividad_6'),
    path('habilitar_prorroga/<int:pk>',staff_member_required(requisitos.HabilitarProrroga,login_url='index'), name = 'habilitar_prorroga'),
    
    path('actividad_7/<int:pk>',staff_member_required(requisitos.RegistrarActividad7.as_view(),login_url='index'), name = 'actividad_7'),
    path('actividad_9/',staff_member_required(requisitos.RegistrarActividad9,login_url='index'), name = 'actividad_9'),
    path('registrar_avance/<int:pk>',staff_member_required(requisitos.RegistrarAvance,login_url='index'), name = 'registrar_avance'),
    path('registrar_avance_2/<int:pk>',staff_member_required(requisitos.RegistrarAvance2,login_url='index'), name = 'registrar_avance_2'),
    path('registrar_avance_aprobado/<int:pk>',staff_member_required(requisitos.RegistrarAvanceAprobado,login_url='index'), name = 'registrar_avance_aprobado'),
    path('actividad_10/<int:pk>',staff_member_required(requisitos.RegistrarActividad10.as_view(),login_url='index'), name = 'actividad_10'),
    path('actividad_11/<int:pk>',staff_member_required(requisitos.RegistrarActividad11.as_view(),login_url='index'), name = 'actividad_11'),
    path('formulario_actividad_11/',staff_member_required(requisitos.FormularioActividad11,login_url='index'), name = 'formulario_actividad_11'),
    path('actividad_12/<int:pk>',staff_member_required(requisitos.RegistrarActividad12.as_view(),login_url='index'), name = 'actividad_12'),
    path('actividad_16/<int:pk>',staff_member_required(requisitos.RegistrarActividad16.as_view(),login_url='index'), name = 'actividad_16'),
    path('formulario_actividad_16/',staff_member_required(requisitos.FormularioActividad16,login_url='index'), name = 'formulario_actividad_16'),
    path('actividad_17/<int:pk>',staff_member_required(requisitos.RegistrarActividad17.as_view(),login_url='index'), name = 'actividad_17'),
    path('procedencia_tesis/<int:pk>',staff_member_required(requisitos.ProcedenteTesis,login_url='index'), name = 'procedencia_tesis'),
    path('improcedencia_tesis/<int:pk>',staff_member_required(requisitos.ImProcedenteTesis,login_url='index'), name = 'improcedencia_tesis'),
    path('actividad_19/<int:pk>',staff_member_required(requisitos.RegistrarActividad19.as_view(),login_url='index'), name = 'actividad_19'),
    path('formulario_actividad_19/',staff_member_required(requisitos.FormularioActividad19,login_url='index'), name = 'formulario_actividad_19'),
    path('actividad_20/<int:pk>',staff_member_required(requisitos.RegistrarActividad20.as_view(),login_url='index'), name = 'actividad_20'),
    path('formulario_actividad_20/',staff_member_required(requisitos.FormularioActividad20,login_url='index'), name = 'formulario_actividad_20'),
    path('actividad_21/<int:pk>',staff_member_required(requisitos.RegistrarActividad21.as_view(),login_url='index'), name = 'actividad_21'),
    path('formulario_actividad_21/',staff_member_required(requisitos.FormularioActividad21,login_url='index'), name = 'formulario_actividad_21'),
    path('actividad_22/<int:pk>',staff_member_required(requisitos.RegistrarActividad22.as_view(),login_url='index'), name = 'actividad_22'),
    path('formulario_actividad_22/',staff_member_required(requisitos.FormularioActividad22,login_url='index'), name = 'formulario_actividad_22'),
    path('actividad_23/<int:pk>',staff_member_required(requisitos.RegistrarActividad23.as_view(),login_url='index'), name = 'actividad_23'),
    path('formulario_actividad_23/',staff_member_required(requisitos.FormularioActividad23,login_url='index'), name = 'formulario_actividad_23'),
    path('actividad_24/<int:pk>',staff_member_required(requisitos.RegistrarActividad24.as_view(),login_url='index'), name = 'actividad_24'),
    path('formulario_actividad_24/',staff_member_required(requisitos.FormularioActividad24,login_url='index'), name = 'formulario_actividad_24'),

    path('listado_reporte_general/',views.ListadoReporteGeneral.as_view(),name='listar_reporte_general'),
    path('listado_reporte_general_tribunal_interno/',views.ListadoReporteGeneralTribunalInterno.as_view(),name='listar_reporte_general_tribunal_interno'),
    path('listado_reporte_general_guia/',views.ListadoReporteGeneralGuia.as_view(),name='listar_reporte_general_guia'),
    path('listado_informe_guia/',views.ListadoInformeGuia.as_view(),name='listar_informe_guia'),
    path('listado_informe_guia_pendiente/',views.ListadoInformeGuiaPendiente.as_view(),name='listar_informe_guia_pendiente'),
    path('listado_informe_guia_realizado/',views.ListadoInformeGuiaRealizado.as_view(),name='listar_informe_guia_realizado'),


    path('listado_informe_revisor/',views.ListadoInformeRevisor.as_view(),name='listar_informe_revisor'),    
    path('listado_informe_revisor_pendiente/',views.ListadoInformeRevisorPendiente.as_view(),name='listar_informe_revisor_pendiente'),    
    path('listado_informe_revisor_realizado/',views.ListadoInformeRevisorRealizado.as_view(),name='listar_informe_revisor_realizado'),    


    path('listado_avance/',views.ListarAvance.as_view(),name='listar_avance'),
    path('listado_avance_pendiente/',views.ListarAvancePendiente.as_view(),name='listar_avance_pendiente'),
    path('listado_avance_realizado/',views.ListarAvanceRealizado.as_view(),name='listar_avance_realizado'),

    path('listado_avance_2/',views.ListarAvance2.as_view(),name='listar_avance_2'),
    path('listado_avance_2_pendiente/',views.ListarAvance2Pendiente.as_view(),name='listar_avance_2_pendiente'),
    path('listado_avance_2_realizado/',views.ListarAvance2Realizado.as_view(),name='listar_avance_2_realizado'),

    path('listado_tesis/',views.ListarTesis.as_view(),name='listar_tesis'),    
    path('informacion_general/',views.InformacionGeneral.as_view(),name='informacion_general'),
    path('usuario_config/',views.change_password, name = 'usuario_config'),      
  
    path('editar_perfil_tesis/<int:pk>',views.EditarPerfilTesis.as_view(),name='editar_perfil_tesis'),
    path('editar_perfil_mejorado/<int:pk>/',views.EditarPerfilMejorado.as_view(),name='editar_perfil_mejorado'),
    path('editar_borrador_tesis/<int:pk>/',views.EditarBorradorTesis.as_view(),name='editar_borrador_tesis'),
    path('editar_tesis_mejorado/<int:pk>/',views.EditarTesisMejorado.as_view(),name='editar_tesis_mejorado'),
    path('editar_tesis_aprobacion/<int:pk>/',views.EditarTesisAprobacion.as_view(),name='editar_tesis_aprobacion'),
    path('editar_tesis_optimizado/<int:pk>/',views.EditarTesisOptimizado.as_view(),name='editar_tesis_optimizado'),
    
    
    path('registrar_informe_revisor/<int:pk>',views.RegistrarInformeRevisor.as_view(), name = 'registrar_informe_revisor'),
    path('registrar_informe_guia/<int:pk>',views.RegistrarInformeGuia, name = 'registrar_informe_guia'),
    path('registrar_reportegeneral/<int:pk>',views.RegistrarReporteGeneral.as_view(), name = 'registrar_reportegeneral'),
    path('registrar_reportegeneral2/<int:pk>',views.RegistrarReporteGeneral2.as_view(), name = 'registrar_reportegeneral2'),
    path('registrar_reportegeneral_tribunal_interno/<int:pk>',views.RegistrarReporteGeneralTribunalInterno.as_view(), name = 'registrar_reportegeneral_tribunal_interno'),
    
  
    path('editar_cronograma/<int:pk>',views.ActualizarCronograma.as_view(), name = 'editar_cronograma'),
    path('editar_cronograma2/<int:pk>',views.ActualizarCronograma2.as_view(), name = 'editar_cronograma2'),
   
    path('habilitarmaestranteguia/<int:pk>',views.HabilitarMaestranteGuia.as_view(), name = 'habilitarmaestranteguia'),
    
    path('actividades_maestrante',views.Actividades_Maestrante.as_view(),name='actividades_maestrante'),


    path('cronograma',views.ListaCronograma.as_view(),name='cronograma'),
    path('cronograma2',views.ListaCronograma2.as_view(),name='cronograma2'),
    path('cronograma_maestrante',views.CronogramMaestrante,name='cronograma_maestrante'),

    

    path('tesis_perfil/<int:pk>',views.TesisPerfil.as_view(),name='tesis_perfil'),
    path('tesis_perfil_mejorado/<int:pk>',views.TesisPerfilMejorado.as_view(),name='tesis_perfil_mejorado'),
    path('tesis_borrador/<int:pk>',views.TesisBorrador.as_view(),name='tesis_borrador'),
    path('tesis_mejorado/<int:pk>',views.TesisMejorado.as_view(),name='tesis_mejorado'),
    path('tesis_aprobado/<int:pk>',views.TesisAprobado.as_view(),name='tesis_aprobado'),
    path('tesis_optimizado/<int:pk>',views.TesisOptimizado.as_view(),name='tesis_optimizado'),
     
    path('seguimiento_tesis_actividades/<int:seguimiento>/',views.SeguimientoTesisActividades,name='seguimiento_tesis_actividades'), 
    path('registrar_perfil_tesis/<int:pk>/',views.RegistroPerfilTesis,name='registrar_perfil_tesis'),
    path('registrar_perfil_mejorado/<int:pk>/',views.RegistroPerfilMejorado,name='registrar_perfil_mejorado'),
    path('registrar_borrador/<int:pk>/',views.RegistroBorrador,name='registrar_borrador'),
    path('registrar_tesis_mejorado/<int:pk>/',views.RegistroTesisMejorado,name='registrar_tesis_mejorado'),
    path('registrar_tesis_aprobado/<int:pk>/',views.RegistroTesisAprobado,name='registrar_tesis_aprobado'),
    path('registrar_tesis_optimizado/<int:pk>/',views.RegistroTesisOptimizado,name='registrar_tesis_optimizado'),
    path('guardar_informe_revisor/',views.GuardarInformeRevisor,name='guardar_informe_revisor'),
    path('guardar_informe_guia/',views.GuardarInformeGuia,name='guardar_informe_guia'),
    
    
    
    

    
    path('registraract7obs/<int:pk>',views.RegistrarAct7obs.as_view(), name = 'registraract7obs'),
    path('actividad1_confirmar/<int:pk>',views.Act1Confirmar.as_view(),name='actividad1_confirmar'), 
    

   

    path('registro_avance/<int:pk>',views.RegistrarAvanceDocente.as_view(), name = 'registro_avance'),
    path('registro_avance_2/<int:pk>',views.RegistrarAvance2Docente.as_view(), name = 'registro_avance_2'),
      
    path('actividad_maestrante_guia/',views.ActividadMaestranteGuia.as_view(),name='actividad_maestrante_guia'),

    path('detalle_informe_guia/<int:pk>',views.DetalleInformeGuia, name = 'detalle_informe_guia'),
    path('detalle_informe_revisor/<int:pk>',views.DetalleInformeRevisor, name = 'detalle_informe_revisor'),
    
    path('detalle_reporte/<int:pk>',views.DetalleReporte.as_view(), name = 'detalle_reporte'),
    path('detalle_reporte2/<int:pk>',views.DetalleReporte2.as_view(), name = 'detalle_reporte2'),
    path('detalle_reporte_segunda_instancia/<int:pk>',views.DetalleReporteSegundaInstancia.as_view(), name = 'detalle_reporte_segunda_instancia'),
    path('detalle_avance/<int:pk>',views.DetalleAvance.as_view(), name = 'detalle_avance'),
    path('detalle_avance_2/<int:pk>',views.DetalleAvance2.as_view(), name = 'detalle_avance_2'),
    path('enviar-mensaje-por-defecto/',views.enviar_mensaje_por_defecto, name='enviar_mensaje_por_defecto'),
    
]



