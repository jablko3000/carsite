# Generated by Django 5.0 on 2023-12-28 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auta', '0009_image_auto_images_note_auto_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Obrázek', 'verbose_name_plural': 'Obrázky'},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': 'Poznámka', 'verbose_name_plural': 'Poznámky'},
        ),
    ]
