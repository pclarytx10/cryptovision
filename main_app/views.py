from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Coin, User_Coin, Holding
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import HoldingForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import login_required to protect def views
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

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
    coins = Coin.objects.all()
    return render(request, 'coins/index.html', { 'coins': coins })

# Define the coins detail view
@login_required
def coins_detail(request, coin_id):
    coin = Coin.objects.get(id=coin_id)
    create_user_coin_url = reverse('user_coins_create', kwargs={'coin_id': coin_id})
    # return render(request, 'coins/detail.html', { 
    #     'coin': coin
    # })
    return render(request, 'coins/detail.html', {
        'coin': coin, 
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

# Define the user coins index view
@login_required
def user_coins_index(request):
    user_coins = User_Coin.objects.filter(user=request.user)
    coins = Coin.objects.all()
    return render(request, 'user_coins/index.html', { 
        'user_coins': user_coins,
        'coins': coins 
    })

# Define the user coins detail view
@login_required
def user_coins_detail(request, user_coin_id):
    user_coin = User_Coin.objects.get(id=user_coin_id)
    holding = Holding.objects.filter(user_coin_id=user_coin_id)
    exchange_coins = Holding.objects.filter(id__in = holding.all().values_list('id'))
    # print(exchange_coins)
    # instantiate HoldingForm to be rendered in the template
    holding_form = HoldingForm()
    return render(request, 'user_coins/detail.html', { 
        'user_coin': user_coin,
        'exchange_coins': exchange_coins,
        'holding_form': holding_form
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
    fields = ('status', 'coin_holdings', 'notes')
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
