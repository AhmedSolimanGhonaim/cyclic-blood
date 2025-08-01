# Generated by Django 5.2.4 on 2025-07-19 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0003_city_alter_bloodbank_city'),
        ('city', '0001_initial'),
        ('users', '0003_alter_customuser_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloodbank',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='city.city'),
        ),
        migrations.DeleteModel(
            name='City',
        ),
    ]
