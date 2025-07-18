# Generated by Django 5.2.4 on 2025-07-16 03:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodbank', '0001_initial'),
        ('bloodstock', '0003_stock_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='bank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bloodbank.bloodbank'),
        ),
        migrations.AddField(
            model_name='stock',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
