# Generated by Django 4.2.7 on 2024-01-21 09:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Errand",
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
