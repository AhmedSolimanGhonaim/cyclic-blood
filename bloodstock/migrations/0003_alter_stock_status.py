# Generated by Django 5.2.4 on 2025-07-19 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bloodstock', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('expired', 'Expired'), ('used', 'Used'), ('check-failed', 'Check-Failed')], default='available', max_length=20),
        ),
    ]
