# Generated by Django 4.2.1 on 2023-09-06 15:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("usuario", "0006_cronograma2_borrador_tesis_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="maestrante",
            name="requerimiento",
        ),
    ]