# Generated by Django 4.1.5 on 2023-02-07 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_user_coin_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_coin',
            name='status',
            field=models.CharField(choices=[('R', 'Researching'), ('H', 'Holding'), ('S', 'Sold'), ('O', 'Other')], default='R', max_length=1),
        ),
    ]
