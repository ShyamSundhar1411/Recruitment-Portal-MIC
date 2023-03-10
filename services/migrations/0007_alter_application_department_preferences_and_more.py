# Generated by Django 4.1.6 on 2023-02-19 10:45

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0006_alter_application_department_preferences_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="department_preferences",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("Design and Content", "Design and Content"),
                    ("UI/UX", "UI/UX"),
                    ("Management", "Management"),
                    ("Sponsorship", "Sponsorship"),
                    ("Cybersecurity", "Cybersecurity"),
                    ("Competitive Programming", "Competitive Programming"),
                    ("Development - Web", "Development - Web"),
                    ("Development - App", "Development - App"),
                    ("AI/ML", "AI/ML"),
                    ("Video Editing and Photography", "Video Editing and Photography"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="recruitmentdrive",
            name="department",
            field=models.CharField(
                choices=[
                    ("Design and Content", "Design and Content"),
                    ("UI/UX", "UI/UX"),
                    ("Management", "Management"),
                    ("Sponsorship", "Sponsorship"),
                    ("Cybersecurity", "Cybersecurity"),
                    ("Competitive Programming", "Competitive Programming"),
                    ("Development - Web", "Development - Web"),
                    ("Development - App", "Development - App"),
                    ("AI/ML", "AI/ML"),
                    ("Video Editing and Photography", "Video Editing and Photography"),
                    ("All", "All"),
                ],
                default="All",
                max_length=100,
            ),
        ),
    ]
