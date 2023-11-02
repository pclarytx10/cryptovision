# Generated by Django 4.1.7 on 2023-11-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_alter_coin_coin_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holding',
            name='exchange',
            field=models.CharField(blank=True, choices=[('B', 'Binance'), ('U', 'Binanace.US'), ('X', 'Bittrex'), ('E', 'Cex.io'), ('C', 'Coinbase'), ('T', 'Crypto.com'), ('G', 'Gemini'), ('K', 'Kraken'), ('N', 'Kucoin'), ('O', 'Other')], max_length=1),
        ),
        migrations.AlterField(
            model_name='holding',
            name='wallet',
            field=models.CharField(blank=True, choices=[('A', 'Atomic Wallet'), ('C', 'Coinbase Wallet'), ('D', 'Daedalus Wallet'), ('E', 'Exodus'), ('L', 'Ledger'), ('M', 'Metamask'), ('R', 'Trezor'), ('T', 'Trust Wallet'), ('Y', 'Yoroi Wallet'), ('X', 'Xdefi Wallet'), ('O', 'Other')], max_length=1),
        ),
    ]