# Generated by Django 4.2.5 on 2024-08-06 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelbooking', '0002_booking_guest_alter_hotelorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='guest',
            field=models.IntegerField(default=1),
        ),
    ]
