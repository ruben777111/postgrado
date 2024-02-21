# Generated by Django 4.2.1 on 2024-02-07 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0012_avance_2_histoiral_docete_guia_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asistenciainduccion',
            old_name='fecha',
            new_name='fecha_realizada',
        ),
        migrations.AddField(
            model_name='asistenciainduccion',
            name='enlace_reunion',
            field=models.URLField(default=1, max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='asistenciainduccion',
            name='hora_realizada',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='asistenciainduccion',
            name='maestrante',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.maestrante'),
        ),
        migrations.AlterField(
            model_name='asistenciainduccion',
            name='obs',
            field=models.TextField(blank=True, max_length=700, null=True, verbose_name='Observaciones'),
        ),
    ]