# Generated by Django 3.1.7 on 2021-04-15 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='appointment_duration',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_joined',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 15, 17, 30, 51, 49976)),
        ),
    ]
