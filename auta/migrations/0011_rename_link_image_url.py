# Generated by Django 5.0 on 2023-12-28 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0010_alter_image_options_alter_note_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='link',
            new_name='url',
        ),
    ]
