from django import forms
from TransactionsApp.models import transactions, users


class loginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class transactionsForm(forms.ModelForm):   # {{{
    class Meta:
        model = transactions
        widgets = {
                'description': forms.Textarea(attrs={'class': 'textInput'}),
                'amount': forms.TextInput(attrs={'class': 'textInput'}),
                'users_involved': forms.CheckboxSelectMultiple(),
                }
        exclude = ('perpersoncost',
                   'deleted',
                )
        #}}}


class addUserForm(forms.ModelForm):  # {{{
    class Meta:
        model = users
        exclude = ('outstanding',
                )
        widgets = {
                'password': forms.PasswordInput(),
                }
        #}}}
