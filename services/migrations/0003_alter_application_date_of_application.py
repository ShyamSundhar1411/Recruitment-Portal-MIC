# Generated by Django 4.1.6 on 2023-02-11 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_alter_application_department_preferences_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="date_of_application",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
