# Generated by Django 4.2.1 on 2024-03-11 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0003_alter_notification_text_alter_notification_verbo'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='maestrante',
            field=models.CharField(default=1, max_length=800),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='programa',
            field=models.CharField(default=1, max_length=800),
            preserve_default=False,
        ),
    ]
