from .forms import HoldingForm, SearchForm, RecommendationForm
from .models import Coin, User_Coin, Holding, Categories, Recommendation, Note
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Count, Sum, Value, F, OuterRef, Subquery
from django.db.models.functions import Coalesce 
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import login_required to protect def views
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Coingecko API
apiRoot ="https://api.coingecko.com/api/v3/"
# API Methods
global_method = "global" # Get cc global data
getList = 'coins/list' # List of all supported cc, cache for later queries
getCoin = 'coins/' # Pull coin info add coin id to string as input
getCategories = 'coins/categories/list' # List of all categories

# Create your views here.
# Define the home view
def home(request):
  return render(request, 'home.html')

# Define the about view
def about(request):
  return render(request, 'about.html')

# Define the coins index view
@login_required
def coins_index(request):
    # Pull the global market data from the Coingecko API
    url = apiRoot + global_method  

    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse("Error: " + str(e), status=404) 
    
    # Pull the global market data from the Coingecko API and store to calculate market cap percentage
    gbl_items = data['data'] 
    gbl_marketcap = gbl_items['total_market_cap']['usd']
    coins = Coin.objects.all()
   
    # Annotate the coins with the first buy up to value from the recommendation table and calculate the market cap percentage
    coins = Coin.objects.annotate(
        first_buy_up = Subquery(
            Recommendation.objects.filter(coin_id = OuterRef('id') ).values('buy_up_to')[:1]),
        buy_up_to=Coalesce(F('first_buy_up'), 0.0),
        mcap_percentage= F('coin_mcap') / Value(gbl_marketcap) * 100 )
    
    coins = coins.annotate( calc_rec = F('buy_up_to') - F('coin_usd') )
    
    coins = coins.order_by('-mcap_percentage')
    return render(request, 'coins/index.html', { 
        'coins': coins,
        'gbl_items': gbl_items })

# Define the coins detail view
@login_required
def coins_detail(request, coin_id):
    coin = Coin.objects.get(id=coin_id)
    recommendations = Recommendation.objects.filter(coin=coin_id)
    recommendation_form = RecommendationForm()
    create_user_coin_url = reverse('user_coins_create', kwargs={'coin_id': coin_id})
    
    return render(request, 'coins/detail.html', {
        'coin': coin,
        'recommendations': recommendations,
        # 'holding_form': holding_form,
        'recommendation_form': recommendation_form,
        'create_user_coin_url': create_user_coin_url
    })

class CoinCreate(LoginRequiredMixin, CreateView):
    model = Coin
    fields = ('coin_name', 'coin_symbol', 'description', 'coin_usd', 'website', 'api_id', 'coin_image')
    success_url = '/coins/'

    # This inherited method is called when a
    # valid coin form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the coin
        # Let the CreateView do its job as usual
        return super().form_valid(form)

# Define the coins update view
class CoinUpdate(LoginRequiredMixin, UpdateView):
    model = Coin
    fields = '__all__'
    success_url = '/coins/'

# Define the coins delete view
class CoinDelete(LoginRequiredMixin, DeleteView):
    model = Coin
    success_url = '/coins/'

# Search view for the CoinGecko API
@login_required
def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            query_lower = query.lower()
            
            # Grab the list of coins from the CoinGecko API
            url = apiRoot + getList    
            try:
                response = requests.get(url)
                data = response.json()
                results = []
                for coin in data:
                    if coin['name'].find(query) != -1 or coin['symbol'].find(query_lower) != -1 or coin['id'].find(query_lower) != -1:
                        results.append(coin)
                    
            except requests.exceptions.RequestException as e:
                return HttpResponse("Error: " + str(e), status=404) 
            
            return render(request, 'coins/search_results.html', {'coins': results})
    else:
        form = SearchForm()
    return render(request, 'coins/search.html', {'form': form})

# Define the user coins index view
@login_required
def user_coins_index(request):
    user_coins = User_Coin.objects.annotate(
        total_quantity=Coalesce(Sum('holding__quantity'),0.0),
        total_value = Coalesce(Sum('holding__quantity') * F('coin__coin_usd'),0.0)
        ).select_related('coin').filter(user=request.user).order_by('coin__marketcap_rank')
    ttl_my_coins = user_coins.aggregate(totalvalue=Sum('total_value'))['totalvalue']
    print(ttl_my_coins)
    return render(request, 'user_coins/index.html', { 
        'user_coins': user_coins,
        'ttl_my_coins': ttl_my_coins
    })

# Define the user coins detail view
@login_required
def user_coins_detail(request, user_coin_id):
    user_coin = User_Coin.objects.get(id=user_coin_id)
    holding = Holding.objects.filter(user_coin_id=user_coin_id)
    # QuerySet for each holding type
    exchange_holdings = holding.filter(location = 'E')
    wallet_holdings = holding.filter(location = 'W')
    other_holdings = holding.filter(location = 'O')
    # instantiate HoldingForm to be rendered in the template
    holding_form = HoldingForm()
    # Count the number of holdings and get the total quantity
    hold_values = holding.aggregate(count=Count('id'), total_quantity=Sum('quantity'))
    if hold_values['count'] == 0:
        ttl_value = 0
    else:
        ttl_value = hold_values.get('total_quantity') * user_coin.coin.coin_usd 
        
    return render(request, 'user_coins/detail.html', { 
        'user_coin': user_coin,
        'exchange_holdings': exchange_holdings,
        'wallet_holdings': wallet_holdings,
        'other_holdings': other_holdings,
        'holding_form': holding_form,
        'hold_values': hold_values,
        'ttl_value': ttl_value
    })
    
# Define the holdings detail view
@login_required
def holdings_detail(request, holding_id):
    holding = Holding.objects.get(id=holding_id)
    return render(request, 'holdings/detail.html', { 'holding': holding })

# Define the holdings update view
class HoldingUpdate(LoginRequiredMixin, UpdateView):
    model = Holding
    fields = '__all__'
    success_url = '/user_coins/'

# Define the holdings delete view
class HoldingDelete(LoginRequiredMixin, DeleteView):
    model = Holding
    success_url = '/user_coins/'

# Define adding a hodling to a user coin 
@login_required
def add_holding(request, user_coin_id):
    # create the ModelForm using the data in request.POST
    form = HoldingForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the user_coin_id assigned
        new_holding = form.save(commit=False)
        new_holding.user_coin_id = user_coin_id
        new_holding.save()
    return redirect('user_coins_detail', user_coin_id=user_coin_id)

# Define the recommendation detail view
@login_required
def recommendations_detail(request, recommendation_id):
    recommendation = Recommendation.objects.get(id=recommendation_id)
    return render(request, 'recommendations/detail.html', { 'recommendation': recommendation })

# Define the recommendatio update view
class RecommendationUpdate(LoginRequiredMixin, UpdateView):
    model = Recommendation
    fields = ['origin', 'buy_up_to', 'recommendation','buy_up_to']
    success_url = '/coins/'

# Define the recommendatio delete view
class RecommendationDelete(LoginRequiredMixin, DeleteView):
    model = Recommendation
    success_url = '/coins/'
    
# Define adding a hodling to a user coin 
@login_required
def add_recommendation(request, coin_id):
    # create the ModelForm using the data in request.POST
    form = RecommendationForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the user_coin_id assigned
        new_reccomendation = form.save(commit=False)
        new_reccomendation.user_id = request.user.id
        new_reccomendation.coin_id = coin_id
        new_reccomendation.save()
    return redirect('detail', coin_id=coin_id)

class User_CoinCreate(LoginRequiredMixin, CreateView):
    model = User_Coin
    fields = ('coin', 'status', 'coin_holdings', 'notes')
    success_url = '/user_coins/'

    # get the initial coin value for the form
    def get_initial(self):
        initial = super().get_initial()
        coin_id = self.kwargs.get('coin_id')
        initial['coin'] = coin_id
        initial['status'] = 'Researching'
        initial['coin_holdings'] = 0
        return initial

    # This inherited method is called when a
    # valid coin form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the coin
        # Let the CreateView do its job as usual
        return super().form_valid(form)

# Define the user coins update view
class User_CoinUpdate(LoginRequiredMixin, UpdateView):
    model = User_Coin
    fields = ('status', 'notes')
    success_url = '/user_coins/'

# Define the user coins delete view
class User_CoinDelete(LoginRequiredMixin, DeleteView):
    model = User_Coin
    success_url = '/user_coins/'

# Define the signup view
def signup(request):
  error_message = ''
  # If the request method is POST, this is a sign-up attempt
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('/')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class API_CoinCreate(LoginRequiredMixin, CreateView):
    model = Coin
    fields = ('api_id', 'coin_name',  'coin_symbol',  'categories', 'coin_usd', 'marketcap_rank', 'coin_ath', 'coin_ath_date',  'coin_ath_percent', 'coin_change',  'coin_mcap',  'coin_atl', 'coin_atl_date',  'coin_image', 'genesis_date', 'hashing_algorithm',  'website',  'description',)
    success_url = '/coins/'
    
    # Initialize the form with the coin data from the API
    # get the initial coin value for the form
    def get_initial(self):
        initial = super().get_initial()
        coingecko_id = self.kwargs.get('coingecko_id')
        
        url = apiRoot + getCoin + coingecko_id   
        # url = apiRoot + getCoin + 'categories/list'
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            return HttpResponse("Error: " + str(e), status=404)
         
        # Convert the categories to a list of category ids
        category_ids = []
        for item in data['categories']:
            query = Categories.objects.filter(category_name=item)
            category_ids.append(query[0].id)
            # print(item, query) # Use to troubleshoot Index Error in future
        
        # Test McapRank, provide default if not available
        if data['market_cap_rank']:
            marketcap_rank = data['market_cap_rank']
        else:
            marketcap_rank = 10000
        
        initial['api_id'] = data['id']
        initial['coin_name'] = data['name']
        initial['coin_symbol'] = data['symbol'].upper()
        initial['categories'] = category_ids
        initial['coin_usd'] = data['market_data']['current_price']['usd']
        initial['marketcap_rank'] = marketcap_rank
        initial['coin_ath'] = data['market_data']['ath']['usd']
        initial['coin_ath_date'] = data['market_data']['ath_date']['usd'][:10]
        initial['coin_ath_percent'] = data['market_data']['ath_change_percentage']['usd']
        initial['coin_change'] = data['market_data']['price_change_24h']
        initial['coin_mcap'] = data['market_data']['market_cap']['usd']
        initial['coin_atl'] = data['market_data']['atl']['usd']
        initial['coin_atl_date'] = data['market_data']['atl_date']['usd'][:10]
        initial['coin_image'] = data['image']['small']
        if data['genesis_date'] == None:
            initial['genesis_date'] = ''
        else:
            initial['genesis_date'] = data['genesis_date'][:10]
        initial['hashing_algorithm'] = data['hashing_algorithm']
        initial['website'] = data['links']['homepage'][0]
        initial['description'] = data['description']['en']
        return initial
    
    # This inherited method is called when a
    # valid coin form is being submitted
    def form_valid(self, form):
        # Assign the logged in user (self.request.user)
        form.instance.user = self.request.user  # form.instance is the coin
        # Let the CreateView do its job as usual
        return super().form_valid(form)
    
# Test view for testing query output
def test(request):
    # Pull the global market data from the Coingecko API
    url = apiRoot + global_method  

    try:
        response = requests.get(url)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse("Error: " + str(e), status=404) 
    
    gbl_items = data['data'] 
    
    gbl_marketcap = gbl_items['total_market_cap']['usd']
    
    coins = Coin.objects.all().order_by('marketcap_rank')
    # Calculate the market cap percentage
    coins = Coin.objects.annotate(
        mcap_percentage= F('coin_mcap') / Value(gbl_marketcap) * 100 ) #F('coin_mcap'))# * F('gbl_items__total_market_cap.usd' * 100),0.0))
    
    # print(coins.mcap_percentage)

    return render(request, 'test.html', { 
        'items': coins,
        'gbl_items': gbl_items })

