# Generated by Django 4.2.1 on 2024-01-26 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_alter_tribunaltesis_tribunal_tesis_1'),
    ]

    operations = [
        migrations.AddField(
            model_name='sustentaciontesishistorial',
            name='dictamen_escala',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sustentaciontesishistorial',
            name='dictamen_nota',
            field=models.IntegerField(null=True),
        ),
    ]
