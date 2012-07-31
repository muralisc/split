# forms
from django import forms
from personalApp.models import Transfers


class transferForm(forms.ModelForm):   # {{{
    class Meta:
        model = Transfers

        widgets = {
                'fromCategory': forms.TextInput(attrs={'class': 'span10', 'placeholder': 'From Category'}),
                'toCategory': forms.TextInput(attrs={'class': 'span10', 'placeholder': 'To Category'}),
                'amount': forms.TextInput(attrs={'class': 'span8', 'placeholder': 'amount'}),
                'description': forms.TextInput(attrs={'class': 'span8', 'placeholder': 'Any xtra desc'}),
                'timestamp': forms.TextInput(attrs={'class': 'span9', 'placeholder': 'Time'}),
                }
