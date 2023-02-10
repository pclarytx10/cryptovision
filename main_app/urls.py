from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('about/', views.about, name='about'),
    path('coins/', views.coins_index, name='index'),
    path('coins/<int:coin_id>/', views.coins_detail, name='detail'),
    path('coins/create/', views.CoinCreate.as_view(), name='coins_create'),
    path('coins/<int:pk>/update/', views.CoinUpdate.as_view(), name='coins_update'),
    path('coins/<int:pk>/delete/', views.CoinDelete.as_view(), name='coins_delete'),
    path('user_coins/', views.user_coins_index, name='user_coins_index'),
    path('user_coins/<int:user_coin_id>/', views.user_coins_detail, name='user_coins_detail'),
    path('user_coins/<int:user_coin_id>/add_holding/', views.add_holding, name='add_holding'),
    path('user_coins/create/<int:coin_id>/', views.User_CoinCreate.as_view(), name='user_coins_create'),
    path('user_coins/<int:pk>/update/', views.User_CoinUpdate.as_view(), name='user_coins_update'),
    path('user_coins/<int:pk>/delete/', views.User_CoinDelete.as_view(), name='user_coins_delete'),
    path('holdings/<int:holding_id>/', views.holdings_detail, name='holdings_detail'),
    path('holdings/<int:pk>/update/', views.HoldingUpdate.as_view(), name='holdings_update'),
    path('holdings/<int:pk>/delete/', views.HoldingDelete.as_view(), name='holdings_delete'),
    path('accounts/signup/', views.signup, name='signup'),  
]