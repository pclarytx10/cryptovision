from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Coin(models.Model):
    coin_name = models.CharField(max_length=50)
    api_id = models.CharField(max_length=250, blank=True)
    coin_symbol = models.CharField(max_length=10, blank=True)
    categories = models.CharField(max_length=250, blank=True)
    coin_usd = models.FloatField(default=0.00)
    # Pull en localization via API
    description = models.TextField(max_length=800, blank=True) 
    # Links is a one to many. Defer to another model. (homepage, blockchain site, etc.)
    # website == links.homepage
    website = models.CharField(max_length=250, blank=True)
    coin_change = models.FloatField(default=0.00)
    coin_mcap = models.FloatField(default=0.00)
    marketcap_rank = models.IntegerField(default=0) 
    coin_ath_percent = models.FloatField(default=0.00)
    coin_ath =  models.FloatField(default=0.00)
    coin_ath_date = models.DateField(blank=True, null=True)
    # coin_markets - future feature
    # coin_image == image.small
    coin_image = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('coin_name',)

    def __str__(self) -> str:
        return self.coin_name

    def get_absolute_url(self):
        return reverse('coins_detail', kwargs={'coin_id': self.id})

class User_Coin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    # Add a field to track user's coin holdings
    coin_holdings = models.FloatField(default=0.0)
    notes = models.TextField(max_length=500, blank=True)
    STATUS = (
        ('R', 'Researching'),
        ('H', 'Holding'),
        ('S', 'Sold'),
        ('O', 'Other')
    )
    status = models.CharField(max_length=1, choices=STATUS, default=STATUS[0][0])

    def __str__(self) -> str:
        return f'{self.user.username} {self.coin.coin_name}'

    class Meta:
        unique_together = ('user', 'coin')