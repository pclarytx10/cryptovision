from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Coin(models.Model):
    coin_name = models.CharField(max_length=50)
    api_id = models.CharField(max_length=250, blank=True)
    coin_symbol = models.CharField(max_length=10, blank=True)
    # categories = models.CharField(max_length=250, blank=True)
    categories = models.ManyToManyField('Categories', blank=True)
    coin_usd = models.FloatField(default=0.00)
    # Pull en localization via API
    description = models.TextField(max_length=10000, blank=True) 
    hashing_algorithm = models.CharField(max_length=50, blank=True)
    genesis_date = models.DateField(blank=True, null=True)
    # Links is a one to many. Defer to another model. (homepage, blockchain site, etc.)
    # website == links.homepage
    website = models.CharField(max_length=250, blank=True)
    coin_change = models.FloatField(default=0.00)
    coin_mcap = models.FloatField(default=0.00)
    marketcap_rank = models.IntegerField(default=0) 
    coin_ath_percent = models.FloatField(default=0.00)
    coin_ath =  models.FloatField(default=0.00)
    coin_ath_date = models.DateField(blank=True, null=True)
    coin_atl = models.FloatField(default=0.00)
    coin_atl_date = models.DateField(blank=True, null=True)
    # coin_markets - future feature
    # coin_image == image.small
    coin_image = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('coin_name',)

    def __str__(self) -> str:
        return self.coin_name

    def get_absolute_url(self):
        return reverse('coins_detail', kwargs={'coin_id': self.id})

class Categories(models.Model):
    category_id = models.CharField(max_length=250, blank=True)
    category_name = models.CharField(max_length=250, blank=True)
    
    def __str__(self) -> str:
        return self.category_id

class User_Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    # Add a field to track user's coin holdings
    coin_holdings = models.FloatField(default=0.0)
    notes = models.TextField(max_length=500, blank=True)
    STATUS = (
        ('R', 'Researching'),
        ('A', 'Acumulating'),
        ('H', 'Holding'),
        ('L', 'Selling'),
        ('S', 'Sold'),
        ('O', 'Other')
    )
    status = models.CharField(max_length=1, choices=STATUS, default=STATUS[0][0])

    def __str__(self) -> str:
        return f'{self.user.username} {self.coin.coin_name}'

    class Meta:
        unique_together = ('user', 'coin')

class Holding(models.Model):
    user_coin = models.ForeignKey(User_Coin, on_delete=models.CASCADE)
    LOCATION = (
        ('E', 'Exchange'),
        ('W', 'Wallet'),
        ('O', 'Other')
    )
    location = models.CharField(max_length=1, choices=LOCATION, default=LOCATION[0][0])
    EXCHANGE = (
        ('B', 'Binance'),
        ('U', 'Binanace.US'),
        ('X', 'Bittrex'),
        ('E', 'Cex.io'),
        ('C', 'Coinbase'),
        ('G', 'Gemini'),
        ('K', 'Kraken'),
        ('O', 'Other')
    )
    exchange = models.CharField(max_length=1, choices=EXCHANGE, blank=True)
    WALLET = (
        ('A', 'Atomic Wallet'),
        ('C', 'Coinbase Wallet'),
        ('D', 'Daedalus Wallet'),
        ('E', 'Exodus'),
        ('L', 'Ledger'),
        ('M', 'Metamask'),
        ('R', 'Trezor'),
        ('T', 'Trust Wallet'),
        ('Y', 'Yoroi Wallet'),
        ('O', 'Other')
    )
    wallet = models.CharField(max_length=1, choices=WALLET, blank=True)
    location_name = models.CharField(max_length=50, blank=True)
    CUSTODY = (
        ('C', 'Custodial'),
        ('S', 'Self'),
        ('T', 'Smart Contract'),
        ('O', 'Other')
    )
    self_custody = models.CharField(max_length=1, choices=CUSTODY, default=CUSTODY[0][0])
    quantity = models.FloatField(default=0.00)
    date = models.DateField('Holding Date')
    cost_basis = models.FloatField(default=0.00)
    notes = models.TextField(max_length=500, blank=True)

    def __str__(self) -> str:
        return f'{self.user_coin.user.username} {self.user_coin.coin.coin_name} {self.date}'

    class Meta:
        ordering = ['-date']