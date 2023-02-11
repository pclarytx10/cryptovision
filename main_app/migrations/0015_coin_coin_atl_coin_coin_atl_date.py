# Generated by Django 4.1.5 on 2023-02-11 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_coin_genesis_date_coin_hashing_algorithm'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='coin_atl',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='coin',
            name='coin_atl_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]