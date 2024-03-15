# Generated by Django 4.2.5 on 2024-03-05 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BillOperation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('billclass', models.CharField(blank=True, choices=[('recharge_card', 'recharge_card'), ('data', 'data'), ('sme_data', 'sme_data'), ('electricity', 'electricity'), ('cabletv', 'cabletv')], default='sme_data', max_length=250, null=True)),
                ('phone_no', models.CharField(blank=True, max_length=14, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('dataplan', models.CharField(blank=True, max_length=200, null=True)),
                ('rechargeplan', models.CharField(blank=True, max_length=200, null=True)),
                ('meterno', models.CharField(blank=True, max_length=100, null=True)),
                ('serviceops', models.CharField(blank=True, choices=[('dstv', 'dstv'), ('gotv', 'gotv'), ('showmax', 'showmax'), ('startimes', 'startimes')], default='gotv', max_length=100, null=True)),
                ('smart_card', models.CharField(blank=True, max_length=100, null=True)),
                ('selectbouquet', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]
