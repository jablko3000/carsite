# Generated by Django 5.0 on 2023-12-28 14:03

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0007_alter_customuser_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='auto',
            options={'verbose_name': 'Auto', 'verbose_name_plural': 'Auta'},
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Uživatel', 'verbose_name_plural': 'Uživatelé'},
        ),
        migrations.AlterModelOptions(
            name='rezervace',
            options={'verbose_name': 'Rezervace', 'verbose_name_plural': 'Rezervace'},
        ),
        migrations.AddField(
            model_name='auto',
            name='datum_nabidky',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
