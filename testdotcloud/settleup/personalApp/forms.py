# forms
from django import forms
# from django.db.models import Count
# from django.db.models import Q
from personalApp.models import Categories


class transferForm(forms.Form):   # {{{
    fromCategory = forms.CharField(widget=forms.TextInput(attrs={'class': 'span10', 'placeholder': 'From Category'}), required=False)
    toCategory = forms.CharField(widget=forms.TextInput(attrs={'class': 'span10', 'placeholder': 'To Category'}), required=False)
    amount = forms.FloatField(widget=forms.TextInput(attrs={'class': 'span8', 'placeholder': 'amount'}), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'span8', 'placeholder': 'Any xtra desc'}), required=False)
    timestamp = forms.DateTimeField(widget=forms.TextInput(attrs={'class': 'span9', 'placeholder': '%m/%d/%Y'}), required=False)


class filterForm(forms.Form):
    fromCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'filters span12'}), empty_value="------", required=False)
    toCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'filters span12'}), required=False)
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'filters span12'}), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'filters span12'}), required=False)
    timeStart = forms.DateField(widget=forms.TextInput(attrs={'class': 'filters span12', 'placeholder': 'Start (%m %d)'}), input_formats='%m %d', required=False)
    timeEnd = forms.DateField(widget=forms.TextInput(attrs={'class': 'filters span12', 'placeholder': 'End (%m %d)'}), input_formats='%m %d', required=False)
    timeSortType = forms.ChoiceField(widget=forms.Select(attrs={'class': 'filters span12'}), required=False)

    def __init__(self, dbrows, *args, **kwargs):
        super(filterForm, self).__init__(*args, **kwargs)
        self.fields['fromCategory'].choices = ((x.pk, x.name) for x in dbrows.filter(category_type='source'))
        self.fields['fromCategory'].choices.insert(0, ('', '---------'))
        self.fields['fromCategory'].choices.insert(1, ('CWS', 'CATEGORY WISE SPLIT'))
        self.fields['toCategory'].choices = ((x.pk, x.name) for x in dbrows.filter(category_type='leach'))
        self.fields['toCategory'].choices.insert(0, ('', '---------'))
        self.fields['toCategory'].choices.insert(1, ('CWS', 'CATEGORY WISE SPLIT'))
        self.fields['timeSortType'].choices = (('Month', 'Month'), ('Week', 'Week'), ('Day', 'Day'))
        self.fields['timeSortType'].choices.insert(0, ('', '---------'))


class CreateCategory(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'span12'}))
    category_type = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'span12'}), choices=(('source', 'source'), ('leach', 'leach')))
    initial_amt = forms.FloatField(widget=forms.TextInput(attrs={'class': 'span12'}))

    class Meta:
        model = Categories
        fields = ('name', 'category_type', 'initial_amt')
