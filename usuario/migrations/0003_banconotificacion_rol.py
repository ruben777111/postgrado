# Generated by Django 4.2.1 on 2024-05-04 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_post_cod_notificacion_post_rol_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='banconotificacion',
            name='rol',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
