from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Coin(models.Model):
    coin_name = models.CharField(max_length=50)
    apiid = models.CharField(max_length=250, blank=True)
    coinsymbol = models.CharField(max_length=10, blank=True)
    categories = models.CharField(max_length=250, blank=True)
    coinusd = models.FloatField(default=0.00)
    # Pull en localization via API
    description = models.TextField(max_length=800, blank=True) 
    # Links is a one to many. Defer to another model. (homepage, blockchain site, etc.)
    # website == links.homepage
    website = models.CharField(max_length=250, blank=True)
    coinchange = models.FloatField(default=0.00)
    coinmcap = models.FloatField(default=0.00)
    marketcaprank = models.IntegerField(default=0) 
    coinathpercent = models.FloatField(default=0.00)
    coinath =  models.FloatField(default=0.00)
    coinathdate = models.DateField(blank=True, null=True)
    # coin_markets - future feature
    # coin_image == image.small
    coinimage = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('coin_name',)

    def __str__(self) -> str:
        return self.coin_name

    def get_absolute_url(self):
        return reverse('coins_detail', kwargs={'coin_id': self.id})