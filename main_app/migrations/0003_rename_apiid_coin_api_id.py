# Generated by Django 4.1.5 on 2023-02-07 03:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_alter_coin_options_rename_api_id_coin_apiid_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coin',
            old_name='apiid',
            new_name='api_id',
        ),
    ]
