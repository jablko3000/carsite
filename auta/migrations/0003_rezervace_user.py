# Generated by Django 5.0 on 2024-01-10 15:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0002_alter_auto_cena_alter_auto_model_alter_auto_znacka'),
    ]

    operations = [
        migrations.AddField(
            model_name='rezervace',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
