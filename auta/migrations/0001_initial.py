# Generated by Django 4.2.6 on 2024-01-03 09:03

import auta.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("znacka", models.CharField(max_length=50)),
                ("model", models.CharField(max_length=200)),
                (
                    "rok_vyroby",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1880),
                            django.core.validators.MaxValueValidator(2050),
                        ]
                    ),
                ),
                (
                    "cena",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "datum_nabidky",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "stav_tachometru",
                    models.IntegerField(
                        validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                ("palivo", models.CharField(max_length=25)),
                ("barva", models.CharField(max_length=25)),
                ("prevodovka", models.CharField(max_length=50)),
                ("motor", models.CharField(max_length=75)),
                ("popis", models.CharField(max_length=1000)),
            ],
            options={
                "verbose_name": "Auto",
                "verbose_name_plural": "Auta",
            },
        ),
        migrations.CreateModel(
            name="Rezervace",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datum_a_cas", models.DateTimeField()),
                (
                    "auto",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auta.auto"
                    ),
                ),
            ],
            options={
                "verbose_name": "Rezervace",
                "verbose_name_plural": "Rezervace",
            },
        ),
        migrations.CreateModel(
            name="Note",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=1500)),
                ("order", models.IntegerField(default=1)),
                (
                    "auto_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auta.auto"
                    ),
                ),
            ],
            options={
                "verbose_name": "Poznámka",
                "verbose_name_plural": "Poznámky",
            },
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("url", models.CharField(max_length=200)),
                ("order", models.IntegerField(default=1)),
                (
                    "auto_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="auta.auto"
                    ),
                ),
            ],
            options={
                "verbose_name": "Obrázek",
                "verbose_name_plural": "Obrázky",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone", models.CharField(max_length=15)),
                ("full_name", models.CharField(max_length=200)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("is_superuser", models.BooleanField(default=False)),
                (
                    "date_joined",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("last_login", models.DateTimeField(blank=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Uživatel",
                "verbose_name_plural": "Uživatelé",
                "db_table": "customuser",
            },
            managers=[
                ("objects", auta.models.CustomUserManager()),
            ],
        ),
    ]
