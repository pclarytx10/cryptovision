from django import forms
from django.forms import ModelForm
from .models import Holding

class HoldingForm(ModelForm):
    class Meta:
        model = Holding
        fields = ['location','exchange','wallet','self_custody','quantity','date','cost_basis','notes']
        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter the Name, Symbol, or API_ID...'}))

        