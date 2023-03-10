from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('about/', views.about, name='about'),
    path('coins/', views.coins_index, name='index'),
    path('coins/search/', views.search, name='search'),
    path('coins/<int:coin_id>/', views.coins_detail, name='detail'),
    # path('coins/create/', views.CoinCreate.as_view(), name='coins_create'),
    path('coins/create/<coingecko_id>', views.API_CoinCreate.as_view(), name='coins_create'),
    path('coins/<int:pk>/update/', views.CoinUpdate.as_view(), name='coins_update'),
    path('coins/<int:pk>/delete/', views.CoinDelete.as_view(), name='coins_delete'),
    path('user_coins/', views.user_coins_index, name='user_coins_index'),
    path('user_coins/<int:user_coin_id>/', views.user_coins_detail, name='user_coins_detail'),
    path('user_coins/<int:user_coin_id>/add_holding/', views.add_holding, name='add_holding'),
    path('coins/<int:coin_id>/add_recommendation/', views.add_recommendation, name='add_recommendation'),
    # path('cats/<int:cat_id>/add_feeding/', views.add_feeding, name='add_feeding'),
    path('user_coins/create/<int:coin_id>/', views.User_CoinCreate.as_view(), name='user_coins_create'),
    path('user_coins/<int:pk>/update/', views.User_CoinUpdate.as_view(), name='user_coins_update'),
    path('user_coins/<int:pk>/delete/', views.User_CoinDelete.as_view(), name='user_coins_delete'),
    path('holdings/<int:holding_id>/', views.holdings_detail, name='holdings_detail'),
    path('holdings/<int:pk>/update/', views.HoldingUpdate.as_view(), name='holdings_update'),
    path('holdings/<int:pk>/delete/', views.HoldingDelete.as_view(), name='holdings_delete'),
    path('recommendations/<int:recommendation_id>/', views.recommendations_detail, name='recommendations_detail'),
    # path('recommendations/create/', views.RecommendationCreate.as_view(), name='recommendations_create'),
    path('recommendations/<int:pk>/update/', views.RecommendationUpdate.as_view(), name='recommendations_update'),  
    path('recommendations/<int:pk>/delete/', views.RecommendationDelete.as_view(), name='recommendations_delete'),
    path('accounts/signup/', views.signup, name='signup'),  
]