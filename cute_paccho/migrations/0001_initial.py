# Generated by Django 5.1.3 on 2024-11-30 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="stuff_work",
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
                ("name", models.CharField(max_length=100)),
                ("last_update", models.DateField()),
                ("project_name", models.CharField(max_length=100)),
                ("detail_line", models.CharField(max_length=200)),
                ("dead_line", models.DateField()),
                ("check_done", models.BooleanField()),
            ],
        ),
    ]
