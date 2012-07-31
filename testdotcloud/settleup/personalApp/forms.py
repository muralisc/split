# forms
from django import forms
from django.db.models import Count
from django.db.models import Q
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


class filterForm(forms.Form):
    fromCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'span12'}), empty_value="------", required=False)
    toCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'span12'}), required=False)
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'span12'}), required=False)
    description = forms.ChoiceField(widget=forms.Select(attrs={'class': 'span12'}), required=False)
    timeStart = forms.DateField(widget=forms.TextInput(attrs={'class': 'span12', 'placeholder': 'Start (%m %d)'}), input_formats='%m %d', required=False)
    timeEnd = forms.DateField(widget=forms.TextInput(attrs={'class': 'span12', 'placeholder': 'End (%m %d)'}), input_formats='%m %d', required=False)

    def __init__(self, dbrows, *args, **kwargs):
        super(filterForm, self).__init__(*args, **kwargs)
        self.fields['fromCategory'].choices = ((x['fromCategory'], x['fromCategory']) for x in dbrows.values('fromCategory').distinct())
        self.fields['fromCategory'].choices.insert(0, ('', '---------'))
        self.fields['toCategory'].choices = ((x['toCategory'], x['toCategory']) for x in dbrows.values('toCategory').distinct())
        self.fields['toCategory'].choices.insert(0, ('', '---------'))
        self.fields['description'].choices = ((x['description'], x['description']) for x in dbrows.values('description').distinct())
        self.fields['description'].choices.insert(0, ('', '---------'))
