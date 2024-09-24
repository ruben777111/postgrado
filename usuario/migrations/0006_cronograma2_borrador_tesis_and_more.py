# Generated by Django 4.2.1 on 2023-09-05 02:49

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("usuario", "0005_cronograma2_fecha_borrador_prorroga"),
    ]

    operations = [
        migrations.AddField(
            model_name="cronograma2",
            name="borrador_tesis",
            field=models.BooleanField(
                default=False, verbose_name="Borrador de tesis con aval de docente guia"
            ),
        ),
        migrations.AddField(
            model_name="cronograma2",
            name="documento_respaldo",
            field=models.FileField(
                blank=True,
                max_length=254,
                null=True,
                upload_to="tesis/documento_respaldo/",
                validators=[django.core.validators.FileExtensionValidator(["pdf"])],
            ),
        ),
        migrations.AddField(
            model_name="cronograma2",
            name="fecha_recepcion_borrador",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="cronograma2",
            name="nombramiento_docente_revisor",
            field=models.FileField(
                blank=True,
                max_length=254,
                null=True,
                upload_to="tesis/nombramiento_docente_revisor/",
                validators=[django.core.validators.FileExtensionValidator(["pdf"])],
            ),
        ),
    ]