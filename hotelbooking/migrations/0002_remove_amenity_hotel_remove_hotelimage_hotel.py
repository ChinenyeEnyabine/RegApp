# Generated by Django 4.2.5 on 2023-10-11 08:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotelbooking', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amenity',
            name='hotel',
        ),
        migrations.RemoveField(
            model_name='hotelimage',
            name='hotel',
        ),
    ]
