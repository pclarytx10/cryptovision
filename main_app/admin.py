from django.contrib import admin
from .models import Coin, User_Coin, Holding

# Register your models here.
admin.site.register(Coin)
admin.site.register(User_Coin)
admin.site.register(Holding)

