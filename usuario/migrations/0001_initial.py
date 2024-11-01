# Generated by Django 5.0.6 on 2024-10-02 18:43

import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Usuario')),
                ('ci_usuario', models.BigIntegerField(null=True)),
                ('ru', models.IntegerField(blank=True, null=True)),
                ('nombre_usuario', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombre')),
                ('paterno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Paterno')),
                ('materno', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellido Materno')),
                ('cel_usuario', models.IntegerField(blank=True, null=True)),
                ('cel_usuario2', models.IntegerField(blank=True, null=True)),
                ('correo', models.CharField(blank=True, max_length=240, null=True, verbose_name='Correo personal')),
                ('correo_inst', models.CharField(blank=True, max_length=240, null=True, verbose_name='Correo institucional')),
                ('notificacion', models.BooleanField(default=False)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('fecha_registro', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('cambio_password', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('tipo_usuario', models.IntegerField(blank=True, choices=[(1, 'Maestrante'), (2, 'Docente'), (3, 'Técnico  de Postgrado/Coordinación de investigación'), (5, 'Coordinación de Postgrado')], null=True)),
                ('rol_maestrante', models.BooleanField(default=False)),
                ('rol_docente', models.BooleanField(default=False)),
                ('rol_tecnico_investigacion', models.BooleanField(default=False)),
                ('rol_postgrado', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'usuario',
            },
        ),
        migrations.CreateModel(
            name='BancoNotificacion',
            fields=[
                ('id_notificacion', models.AutoField(primary_key=True, serialize=False)),
                ('numero_notificacion', models.IntegerField(unique=True)),
                ('titulo', models.CharField(max_length=400)),
                ('contenido', models.CharField(max_length=400)),
                ('descripcion', models.CharField(blank=True, max_length=400, null=True)),
                ('rol', models.CharField(blank=True, max_length=400, null=True)),
                ('enviar', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Banco de notificacion',
                'verbose_name_plural': 'Banco de notificaciones',
            },
        ),
        migrations.CreateModel(
            name='CorreoConfigurar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion_correo', models.IntegerField(blank=True, null=True)),
                ('correo', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Correo')),
                ('host_password', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Contraseña')),
                ('puerto_correo', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Correo',
                'verbose_name_plural': 'Correos',
            },
        ),
        migrations.CreateModel(
            name='Programa',
            fields=[
                ('id_programa', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_programa', models.TextField(blank=True, max_length=200, null=True, verbose_name='Programa ')),
                ('version', models.TextField(blank=True, max_length=200, null=True, verbose_name='Versión programa ')),
            ],
            options={
                'verbose_name': 'Programa',
                'verbose_name_plural': 'Programas',
            },
        ),
        migrations.CreateModel(
            name='Requisitos',
            fields=[
                ('id_requisito', models.AutoField(primary_key=True, serialize=False)),
                ('nro_requisito', models.IntegerField(unique=True)),
                ('actividad', models.TextField(max_length=1000, verbose_name='Actividad')),
                ('requisito', models.TextField(max_length=1000, verbose_name='Evidencia')),
                ('tiempo', models.IntegerField(null=True, verbose_name='Dias ')),
                ('rol1', models.BooleanField(default=False, verbose_name='Tecnico de Postgrado ')),
                ('rol2', models.BooleanField(default=False, verbose_name='Coordinación de investigación ')),
                ('rol3', models.BooleanField(default=False, verbose_name='Coordinación de Postgrado ')),
                ('requisito_habilitado', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Requisito',
                'verbose_name_plural': 'Requisitos',
            },
        ),
        migrations.CreateModel(
            name='Administracion',
            fields=[
                ('id_administracion', models.AutoField(primary_key=True, serialize=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
            },
        ),
        migrations.CreateModel(
            name='Docente',
            fields=[
                ('id_docente', models.AutoField(primary_key=True, serialize=False)),
                ('especialidad_docente', models.CharField(blank=True, max_length=130, null=True)),
                ('docente_interno', models.BooleanField(default=False)),
                ('docente_externo', models.BooleanField(default=False)),
                ('docente_activo', models.BooleanField(default=True)),
                ('mostrar_numero', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Docente',
                'verbose_name_plural': 'Docentes',
            },
        ),
        migrations.CreateModel(
            name='Docente_Revisor',
            fields=[
                ('id_revisor', models.AutoField(primary_key=True, serialize=False)),
                ('docente_activo', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Docente Revisor',
                'verbose_name_plural': 'Docentes Revisores',
            },
        ),
        migrations.CreateModel(
            name='DocenteProvisional',
            fields=[
                ('id_provisional', models.AutoField(primary_key=True, serialize=False)),
                ('docente_activo', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Docente Provisional',
                'verbose_name_plural': 'Docentes Provisionales',
            },
        ),
        migrations.CreateModel(
            name='Maestrante',
            fields=[
                ('id_maestrante', models.AutoField(primary_key=True, serialize=False)),
                ('gestion', models.IntegerField(null=True)),
                ('tesis_mejorado', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actividades/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('nombramiento_revisor', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/nombramiento_revisor/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('fecha_nombramiento', models.DateField(blank=True, null=True)),
                ('tema_perfil_postulado', models.CharField(blank=True, max_length=200, null=True, verbose_name='Perfil postulado')),
                ('tema_tesis_perfil', models.CharField(blank=True, max_length=200, null=True, verbose_name='Tema de perfil de Tesis')),
                ('tema_borrador_tesis', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título del borrador de tesis')),
                ('tema_tesis', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título de tesis')),
                ('titulo_de_tesis', models.CharField(blank=True, max_length=200, null=True, verbose_name='Título de la Tesis')),
                ('instancia', models.IntegerField(default=1)),
                ('instancia_defensa', models.IntegerField(default=1)),
                ('procedencia_tema', models.BooleanField(blank=True, null=True)),
                ('procedencia_tesis', models.BooleanField(blank=True, null=True)),
                ('avance_tesis', models.IntegerField(null=True)),
                ('dictamen_nota', models.IntegerField(null=True)),
                ('dictamen_escala', models.CharField(blank=True, max_length=200, null=True)),
                ('aprobacion_empaste', models.BooleanField(default=False)),
                ('tesis_recomendada', models.BooleanField(default=False)),
                ('observacion_empaste', models.TextField(blank=True, max_length=1000, null=True)),
                ('codigo_empaste', models.TextField(blank=True, max_length=100, null=True)),
                ('maestrante_activo', models.BooleanField(default=True)),
                ('maestrante_habilitado', models.BooleanField(default=False)),
                ('fecha_derivacion', models.DateField(blank=True, null=True)),
                ('tesis_segunda_instancia', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actividades/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('hoja_de_evaluacion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actividades/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('recepcion_solicitud', models.DateField(blank=True, null=True)),
                ('solicitud_area_finaciera', models.DateField(blank=True, null=True)),
                ('observacion_pago', models.TextField(blank=True, max_length=1000, null=True)),
                ('observacion_segunda_instancia', models.TextField(blank=True, max_length=1000, null=True)),
                ('tipo_maestrante', models.CharField(choices=[('1', 'Programa regular'), ('2', 'Programa antiguo')], max_length=20)),
                ('bloqueo_maestrante', models.BooleanField(default=False)),
                ('vigencia_matricula_regular_total', models.DateField(blank=True, null=True)),
                ('vigencia_matricula_antiguo', models.DateField(blank=True, null=True)),
                ('vigencia_matricula_antiguo_total', models.DateField(blank=True, null=True)),
                ('version', models.CharField(blank=True, max_length=220, null=True, verbose_name='Versión')),
                ('empaste_cd', models.BooleanField(default=False)),
                ('gestion_empastado', models.IntegerField(null=True)),
                ('tesis_terminado', models.BooleanField(default=False)),
                ('articulos_revision', models.BooleanField(default=False)),
                ('articulos_original', models.BooleanField(default=False)),
                ('guia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente')),
                ('provisional', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docenteprovisional')),
                ('revisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente_revisor')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maestrantes_usuario', to=settings.AUTH_USER_MODEL)),
                ('programa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.programa')),
            ],
            options={
                'verbose_name': 'Maestrante',
                'verbose_name_plural': 'Maestrantes',
            },
        ),
        migrations.CreateModel(
            name='InformeRevisor',
            fields=[
                ('id_informe_revisor', models.AutoField(primary_key=True, serialize=False)),
                ('capitulo', models.TextField(blank=True, max_length=500, null=True)),
                ('descripcion', models.TextField(blank=True, max_length=500, null=True)),
                ('sugerencia', models.TextField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Informe revisor formulario',
                'verbose_name_plural': 'Informes revisores formularios',
            },
        ),
        migrations.CreateModel(
            name='InformeGuiaFormulario',
            fields=[
                ('id_informe_guia', models.AutoField(primary_key=True, serialize=False)),
                ('capitulo', models.TextField(blank=True, max_length=500, null=True)),
                ('obs', models.TextField(blank=True, max_length=500, null=True)),
                ('opcion', models.TextField(blank=True, max_length=10, null=True)),
                ('pagina', models.TextField(blank=True, max_length=300, null=True)),
                ('fundamentacion', models.TextField(blank=True, max_length=500, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Informe guia formulario',
                'verbose_name_plural': 'Informes guias formularios',
            },
        ),
        migrations.CreateModel(
            name='InformeGuia',
            fields=[
                ('id_informe', models.AutoField(primary_key=True, serialize=False)),
                ('otras_obs', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('docente', models.TextField(blank=True, max_length=1000, null=True)),
                ('aceptar_guia', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Informe guia',
                'verbose_name_plural': 'Informes guias',
            },
        ),
        migrations.CreateModel(
            name='Informe',
            fields=[
                ('id_informe', models.AutoField(primary_key=True, serialize=False)),
                ('otras_obs', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('docente', models.TextField(blank=True, max_length=1000, null=True)),
                ('aceptar_revisor', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Informe reviso',
                'verbose_name_plural': 'Informes revisores',
            },
        ),
        migrations.CreateModel(
            name='Cronograma2',
            fields=[
                ('id_cronograma', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_avance1', models.DateField(blank=True, null=True)),
                ('fecha_avance2', models.DateField(blank=True, null=True)),
                ('fecha_borrador', models.DateField(blank=True, null=True)),
                ('fecha_borrador_prorroga', models.DateField(blank=True, null=True)),
                ('fecha_recepcion_borrador', models.DateField(blank=True, null=True)),
                ('borrador_tesis', models.BooleanField(default=False, verbose_name='Borrador de tesis con aval de docente guia')),
                ('fecha_formulario_revisor', models.DateField(blank=True, null=True)),
                ('fecha_formulario_guia', models.DateField(blank=True, null=True)),
                ('fecha_tesis_habilitada', models.DateField(blank=True, null=True)),
                ('fecha_reporte_general', models.DateField(blank=True, null=True)),
                ('fecha_reporte_general2', models.DateField(blank=True, null=True)),
                ('fecha_sustentacion', models.DateField(blank=True, null=True)),
                ('hora_sustentacion', models.TimeField(blank=True, null=True)),
                ('fecha_tesis_mejorada', models.DateField(blank=True, null=True)),
                ('fecha_reporte_general_tribunal_interno', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Cronograma de maestrantes en curso ',
                'verbose_name_plural': 'Cronograma de maestrantes en curso ',
            },
        ),
        migrations.CreateModel(
            name='Cronograma',
            fields=[
                ('id_cronograma', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_induccion', models.DateField(blank=True, null=True)),
                ('hora_induccion', models.TimeField(blank=True, null=True)),
                ('reunion_realizada', models.BooleanField(default=False)),
                ('fecha_1', models.DateField(blank=True, null=True)),
                ('fecha_2', models.DateField(blank=True, null=True)),
                ('fecha_3', models.DateField(blank=True, null=True)),
                ('hora_sustentacion', models.TimeField(blank=True, null=True)),
                ('fecha_4', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Cronograma hasta procedencia de tema',
                'verbose_name_plural': 'Cronograma hasta procedencia de tema',
            },
        ),
        migrations.CreateModel(
            name='AvanceHistorial',
            fields=[
                ('id_avance', models.AutoField(primary_key=True, serialize=False)),
                ('cap1', models.IntegerField(blank=True, null=True, verbose_name='Capitulo I')),
                ('cap2', models.IntegerField(blank=True, null=True, verbose_name='Capitulo II')),
                ('cap3', models.IntegerField(blank=True, null=True, verbose_name='Capitulo III')),
                ('cap1_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap2_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap3_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('aprobacion', models.CharField(choices=[('si', 'Aprobado'), ('no', 'No aprobado')], max_length=20)),
                ('fecha_registro', models.DateField(auto_now=True, verbose_name='Fecha de registro')),
                ('fecha_programada', models.DateField(blank=True, null=True)),
                ('aceptar_avance', models.BooleanField(default=False)),
                ('docete_guia', models.TextField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Avance 1 historial',
                'verbose_name_plural': 'Avances 1 historial',
            },
        ),
        migrations.CreateModel(
            name='Avance_2_Histoiral',
            fields=[
                ('id_avance', models.AutoField(primary_key=True, serialize=False)),
                ('cap4', models.IntegerField(blank=True, null=True, verbose_name='Capitulo IV')),
                ('cap5', models.IntegerField(blank=True, null=True, verbose_name='Capitulo V')),
                ('cap6', models.IntegerField(blank=True, null=True, verbose_name='Capitulo VI')),
                ('cap7', models.IntegerField(blank=True, null=True, verbose_name='REFERENCIAS')),
                ('cap4_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap5_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap6_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap7_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('aceptar_avance', models.BooleanField(default=False)),
                ('fecha_programada', models.DateField(blank=True, null=True)),
                ('docete_guia', models.TextField(blank=True, max_length=300, null=True)),
                ('aprobacion', models.CharField(choices=[('si', 'Aprobado'), ('no', 'No aprobado')], max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Avance 2 historial',
                'verbose_name_plural': 'Avances 2 historial',
            },
        ),
        migrations.CreateModel(
            name='Avance_2',
            fields=[
                ('id_avance', models.AutoField(primary_key=True, serialize=False)),
                ('docente', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap4', models.IntegerField(blank=True, null=True, verbose_name='Capitulo IV')),
                ('cap5', models.IntegerField(blank=True, null=True, verbose_name='Capitulo V')),
                ('cap6', models.IntegerField(blank=True, null=True, verbose_name='Capitulo VI')),
                ('cap7', models.IntegerField(blank=True, null=True, verbose_name='REFERENCIAS')),
                ('cap4_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap5_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap6_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap7_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('aceptar_avance', models.BooleanField(default=False)),
                ('aprobacion', models.CharField(choices=[('si', 'Aprobado'), ('no', 'No aprobado')], max_length=20)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Avance 2',
                'verbose_name_plural': 'Avances 2',
            },
        ),
        migrations.CreateModel(
            name='Avance',
            fields=[
                ('id_avance', models.AutoField(primary_key=True, serialize=False)),
                ('docente', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap1', models.IntegerField(blank=True, null=True, verbose_name='Capitulo I')),
                ('cap2', models.IntegerField(blank=True, null=True, verbose_name='Capitulo II')),
                ('cap3', models.IntegerField(blank=True, null=True, verbose_name='Capitulo III')),
                ('cap1_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap2_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('cap3_cualitativo', models.TextField(blank=True, max_length=1000, null=True)),
                ('aprobacion', models.CharField(choices=[('si', 'Aprobado'), ('no', 'No aprobado')], max_length=20)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('aceptar_avance', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Avance 1 ',
                'verbose_name_plural': 'Avances 1',
            },
        ),
        migrations.CreateModel(
            name='AsistenciaInduccion',
            fields=[
                ('id_asistencia', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asesoramiento', models.DateField(blank=True, null=True)),
                ('hora_asesoramiento', models.TimeField(blank=True, null=True)),
                ('fecha_realizada', models.DateField(blank=True, null=True)),
                ('hora_realizada', models.TimeField(blank=True, null=True)),
                ('enlace_reunion', models.URLField(blank=True, max_length=1000, null=True)),
                ('obs', models.TextField(blank=True, max_length=700, null=True, verbose_name='Observaciones')),
                ('hoja_reunion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('maestrante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Registro de asistencia',
                'verbose_name_plural': 'Registros de asistencias',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('cod_notificacion', models.IntegerField(blank=True, null=True)),
                ('rol', models.CharField(max_length=400)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('maestrante', models.CharField(max_length=800)),
                ('programa', models.CharField(max_length=800)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReporteGeneral',
            fields=[
                ('id_reportegeneral', models.AutoField(primary_key=True, serialize=False)),
                ('docente', models.TextField(blank=True, max_length=1000, null=True)),
                ('docente2', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('reporte', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Reporte ')),
                ('aceptar_revisor', models.BooleanField(default=False)),
                ('aprobacion', models.CharField(choices=[('si', 'Aprobado'), ('no', 'No aprobado')], max_length=20)),
                ('activar_reporte2', models.BooleanField(default=False)),
                ('reporte2', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Reporte ')),
                ('aceptar_revisor2', models.BooleanField(default=False)),
                ('fecha_registro2', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Reporte General',
                'verbose_name_plural': 'Reportes Generales',
            },
        ),
        migrations.CreateModel(
            name='ReporteGeneralTribunalInterno',
            fields=[
                ('id_reportegeneral', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateField(blank=True, null=True)),
                ('reporte', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/reporte/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('tribunal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente_revisor')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Reporte General Tribunal Interno',
                'verbose_name_plural': 'Reporte General Tribunal Interno',
            },
        ),
        migrations.CreateModel(
            name='CentroActividades',
            fields=[
                ('id_actividad', models.AutoField(primary_key=True, serialize=False)),
                ('instancia', models.TextField(blank=True, max_length=100, null=True)),
                ('observacion', models.TextField(blank=True, max_length=1000, null=True)),
                ('fecha_programada', models.DateField(blank=True, null=True)),
                ('fecha_realizado', models.DateField(blank=True, null=True)),
                ('fecha', models.DateField(auto_now_add=True, verbose_name='Fecha de registro')),
                ('evidencia', models.TextField(blank=True, max_length=220, null=True)),
                ('archivo_documento', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actividades/')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('maestrante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actividades_maestrante', to='usuario.maestrante')),
                ('actividad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.requisitos')),
            ],
            options={
                'verbose_name': 'Centro actividad',
                'verbose_name_plural': 'Centro actividades',
            },
        ),
        migrations.CreateModel(
            name='SustentacionPerfilHistorial',
            fields=[
                ('id_sustentacion', models.AutoField(primary_key=True, serialize=False)),
                ('tema_perfil', models.TextField(blank=True, max_length=500, null=True)),
                ('fecha_sustentacion', models.DateField(blank=True, null=True)),
                ('hora_sustentacion', models.TimeField(blank=True, null=True)),
                ('docente_guia', models.TextField(blank=True, max_length=500, null=True)),
                ('tribunal_perfil_1', models.TextField(blank=True, max_length=500, null=True)),
                ('tribunal_perfil_2', models.TextField(blank=True, max_length=500, null=True)),
                ('resultado', models.BooleanField(default=False)),
                ('instancia', models.IntegerField(null=True)),
                ('acta', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actas/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('hoja_evaluacion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/hoja_evaluacion/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('carta_externa', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/carta_externa/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('carta_externa_designacion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/carta_externa/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('documento_respaldo', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/documento_respaldo/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('fecha_recibido_perfil', models.DateField(blank=True, null=True)),
                ('fecha_recibido_documentos', models.DateField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Sustentacion de perfil historial',
                'verbose_name_plural': 'Sustentacion de perfiles historial',
            },
        ),
        migrations.CreateModel(
            name='SustentacionTesisHistorial',
            fields=[
                ('id_sustentacion', models.AutoField(primary_key=True, serialize=False)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('tema_tesis', models.TextField(blank=True, max_length=500, null=True)),
                ('fecha_sustentacion', models.DateField(blank=True, null=True)),
                ('hora_sustentacion', models.TimeField(blank=True, null=True)),
                ('docente_guia', models.TextField(blank=True, max_length=500, null=True)),
                ('tribunal_1', models.TextField(blank=True, max_length=500, null=True)),
                ('tribunal_2', models.TextField(blank=True, max_length=500, null=True)),
                ('resultado', models.BooleanField(default=False)),
                ('dictamen_nota', models.IntegerField(null=True)),
                ('dictamen_escala', models.CharField(blank=True, max_length=200, null=True)),
                ('acta', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/actas/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('hoja_evaluacion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/hoja_evaluacion/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('designacion', models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/carta_externa/', validators=[django.core.validators.FileExtensionValidator(['pdf'])])),
                ('instancia', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Sustentacion de tesis historial',
                'verbose_name_plural': 'Sustentacion de tesis historial',
            },
        ),
        migrations.CreateModel(
            name='TribunalPerfil',
            fields=[
                ('id_tribunal', models.AutoField(primary_key=True, serialize=False)),
                ('tribunal_perfil_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente')),
                ('tribunal_perfil_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente_revisor')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Tribunal de perfil',
                'verbose_name_plural': 'Tribunales de perfil',
            },
        ),
        migrations.CreateModel(
            name='TribunalTesis',
            fields=[
                ('id_tribunal', models.AutoField(primary_key=True, serialize=False)),
                ('tribunal_tesis_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente')),
                ('tribunal_tesis_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.docente_revisor')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante')),
            ],
            options={
                'verbose_name': 'Tribunal de tesis',
                'verbose_name_plural': 'Tribunales de tesis',
            },
        ),
    ]
