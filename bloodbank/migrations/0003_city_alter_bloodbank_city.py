# Generated by Django 5.2.4 on 2025-07-19 06:17

import django.contrib.gis.db.models.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=40, null=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(geography=True, srid=4326)),
            ],
        ),
        migrations.AlterField(
            model_name='bloodbank',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bloodbank.city'),
        ),
    ]
