# Generated by Django 5.0 on 2023-12-28 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0011_rename_link_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auto',
            name='images',
        ),
        migrations.RemoveField(
            model_name='auto',
            name='notes',
        ),
    ]
