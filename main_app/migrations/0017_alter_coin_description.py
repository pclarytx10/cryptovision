# Generated by Django 4.1.5 on 2023-02-11 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_alter_coin_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='description',
            field=models.TextField(blank=True, max_length=10000),
        ),
    ]
