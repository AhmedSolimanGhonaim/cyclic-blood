# Generated by Django 5.2.4 on 2025-07-13 19:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bloodrequests', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloodrequests',
            old_name='hospital_id',
            new_name='hospital',
        ),
        migrations.RemoveField(
            model_name='bloodrequests',
            name='blood_type',
        ),
    ]
