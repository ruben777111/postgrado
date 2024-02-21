# Generated by Django 4.2.1 on 2024-02-09 21:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0016_alter_asistenciainduccion_enlace_reunion'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistenciainduccion',
            name='hoja_reunion',
            field=models.FileField(blank=True, max_length=254, null=True, upload_to='tesis/', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
