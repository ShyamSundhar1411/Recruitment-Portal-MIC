# Generated by Django 4.1.6 on 2023-02-05 04:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="application",
            old_name="deparment_preferences",
            new_name="department_preferences",
        ),
    ]