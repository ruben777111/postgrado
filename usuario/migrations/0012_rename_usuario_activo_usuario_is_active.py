# Generated by Django 4.2.1 on 2023-09-25 00:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("usuario", "0011_remove_informerevisor_obs_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="usuario",
            old_name="usuario_activo",
            new_name="is_active",
        ),
    ]
