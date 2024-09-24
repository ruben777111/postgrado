# Generated by Django 4.2.1 on 2023-09-06 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("usuario", "0007_remove_maestrante_requerimiento"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avance_2_histoiral",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="usuario.maestrante",
            ),
        ),
        migrations.AlterField(
            model_name="avancehistorial",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="usuario.maestrante",
            ),
        ),
    ]