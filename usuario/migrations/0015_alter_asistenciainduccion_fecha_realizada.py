# Generated by Django 4.2.1 on 2024-02-07 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0014_cronograma_reunion_realizada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asistenciainduccion',
            name='fecha_realizada',
            field=models.DateField(blank=True, null=True),
        ),
    ]
