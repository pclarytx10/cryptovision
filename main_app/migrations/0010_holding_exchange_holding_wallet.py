# Generated by Django 4.1.5 on 2023-02-08 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_holding'),
    ]

    operations = [
        migrations.AddField(
            model_name='holding',
            name='exchange',
            field=models.CharField(blank=True, choices=[('B', 'Binance'), ('U', 'Binanace.US'), ('X', 'Bittrex'), ('E', 'Cex.io'), ('C', 'Coinbase'), ('G', 'Gemini'), ('K', 'Kraken'), ('O', 'Other')], max_length=1),
        ),
        migrations.AddField(
            model_name='holding',
            name='wallet',
            field=models.CharField(blank=True, choices=[('A', 'Atomic Wallet'), ('C', 'Coinbase Wallet'), ('D', 'Daedalus Wallet'), ('E', 'Exodus'), ('L', 'Ledger'), ('M', 'Metamask'), ('R', 'Trezor'), ('T', 'Trust Wallet'), ('Y', 'Yoroi Wallet'), ('O', 'Other')], max_length=1),
        ),
    ]
