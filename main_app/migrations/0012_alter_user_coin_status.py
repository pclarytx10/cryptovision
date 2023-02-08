# Generated by Django 4.1.5 on 2023-02-08 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0011_alter_holding_date_alter_holding_self_custody'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_coin',
            name='status',
            field=models.CharField(choices=[('R', 'Researching'), ('A', 'Acumulating'), ('H', 'Holding'), ('L', 'Selling'), ('S', 'Sold'), ('O', 'Other')], default='R', max_length=1),
        ),
    ]
