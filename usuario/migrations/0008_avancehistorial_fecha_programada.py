# Generated by Django 4.2.1 on 2024-02-06 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0007_remove_avance_anexos_remove_avance_bibliografia_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='avancehistorial',
            name='fecha_programada',
            field=models.DateField(auto_now=True, verbose_name='Fecha programada'),
        ),
    ]