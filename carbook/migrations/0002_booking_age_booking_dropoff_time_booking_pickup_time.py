# Generated by Django 4.2.5 on 2023-10-05 19:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='age',
            field=models.IntegerField(default=18),
        ),
        migrations.AddField(
            model_name='booking',
            name='dropoff_time',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AddField(
            model_name='booking',
            name='pickup_time',
            field=models.TimeField(default=datetime.time(8, 0)),
        ),
    ]
