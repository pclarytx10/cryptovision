from django.contrib import admin
from .models import Coin, User_Coin, Holding, Categories, Recommendation, Note

# Register your models here.
admin.site.register(Coin)
admin.site.register(User_Coin)
admin.site.register(Holding)
admin.site.register(Categories)
admin.site.register(Recommendation)
admin.site.register(Note)
