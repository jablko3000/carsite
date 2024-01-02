# Generated by Django 5.0 on 2024-01-02 16:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0015_remove_auto_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='auto',
            name='barva',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='motor',
            field=models.CharField(default='', max_length=75),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='palivo',
            field=models.CharField(default='Benzín', max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='popis',
            field=models.CharField(default='Auto na prodej', max_length=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='prevodovka',
            field=models.CharField(default='Manuální, 6-stupňová', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='auto',
            name='stav_tachometru',
            field=models.IntegerField(default=42520, validators=[django.core.validators.MinValueValidator(0)]),
            preserve_default=False,
        ),
    ]
