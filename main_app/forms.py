from django.forms import ModelForm
from .models import Holding

class HoldingForm(ModelForm):
    class Meta:
        model = Holding
        fields = ['location','exchange','wallet','self_custody','quantity','date','cost_basis','notes']
        