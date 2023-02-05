# Generated by Django 4.1.6 on 2023-02-05 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0003_rename_end_data_time_recruitmentdrive_end_date_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="recruitmentdrive",
            name="department",
            field=models.CharField(
                choices=[
                    ("Design and Content", "Design and Content"),
                    ("UI/UX", "UI/UX"),
                    ("Management", "Management"),
                    ("Finance", "Finance"),
                    ("Sponsership", "Sponsership"),
                    ("Cybersecurity", "Cybersecurity"),
                    ("Competitive Programming", "Competitive Programming"),
                    ("Development - Web", "Development - Web"),
                    ("Development - App", "Development - App"),
                    ("All", "All"),
                ],
                default="All",
                max_length=100,
            ),
        ),
    ]