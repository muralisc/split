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


class formForTransactions(forms.Form):
    fromForTransactions = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'filters span9'}), required=False)

    def __init__(self, dbrows, *args, **kwargs):
        super(formForTransactions, self).__init__(*args, **kwargs)
        self.fields['fromForTransactions'].choices = ((x['pk'], x['name']) for x in dbrows.filter(category_type='source').values('pk', 'name'))


class filterForm(forms.Form):
    fromCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'filters span12'}), required=False)
    toCategory = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'filters span12'}), required=False)
    amount = forms.CharField(widget=forms.TextInput(attrs={'class': 'filters span12'}), required=False)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'filters span12'}), required=False)
    timeStart = forms.DateField(widget=forms.TextInput(attrs={'class': 'filters span12', 'placeholder': 'Start Time'}), required=False)
    timeEnd = forms.DateField(widget=forms.TextInput(attrs={'class': 'filters span12', 'placeholder': 'End Time'}), required=False)
    timeSortType = forms.ChoiceField(
                                    widget=forms.Select(attrs={'class': 'filters span12'}),
                                    choices=(('', '---------'), ('Month', 'Month'), ('Week', 'Week'), ('Day', 'Day')),
                                    required=False
                                    )

    def __init__(self, dbrows, *args, **kwargs):
        super(filterForm, self).__init__(*args, **kwargs)
        if dbrows != None:
            CHOICES = (('', '---------'), ('CWS', 'CATEGORY WISE SPLIT'))
            fromCategory_CHOICES = [(x['pk'], x['name']) for x in dbrows.filter(category_type='source').values('pk', 'name')]
            netFromCHOICES = CHOICES + tuple(fromCategory_CHOICES)
            self.fields['fromCategory'] = forms.TypedChoiceField(
                                                widget=forms.Select(attrs={'class': 'filters span12'}),
                                                choices=netFromCHOICES,
                                                required=False
                                                )
            toCategory_CHOICES = [(x['pk'], x['name']) for x in dbrows.filter(category_type='leach').values('pk', 'name')]
            netToCHOICES = CHOICES + tuple(toCategory_CHOICES)
            self.fields['toCategory'] = forms.TypedChoiceField(
                                                widget=forms.Select(attrs={'class': 'filters span12'}),
                                                choices=netToCHOICES,
                                                required=False
                                                )

    def clean(self):
        super(filterForm, self).clean()
        if 'toCategory' in self._errors:
            del self._errors['toCategory']
        return self.cleaned_data


class CreateCategory(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'span12'}))
    category_type = forms.TypedChoiceField(widget=forms.Select(attrs={'class': 'span12'}), choices=(('source', 'source'), ('leach', 'leach')))
    initial_amt = forms.FloatField(widget=forms.TextInput(attrs={'class': 'span12'}))

    class Meta:
        model = Categories
        fields = ('name', 'category_type', 'initial_amt')
