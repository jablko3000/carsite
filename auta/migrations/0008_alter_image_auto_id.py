# Generated by Django 5.0 on 2024-02-19 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0007_alter_auto_cena_alter_auto_rok_vyroby'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='auto_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auta.auto'),
        ),
    ]
