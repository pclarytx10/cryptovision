# Generated by Django 4.1.5 on 2023-02-07 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_rename_apiid_coin_api_id'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coin',
            options={'ordering': ('coin_name',)},
        ),
        migrations.RenameField(
            model_name='coin',
            old_name='coinname',
            new_name='coin_name',
        ),
    ]
