from django import forms
from TransactionsApp.models import users


class EditUserForm(forms.ModelForm):  # {{{
    class Meta:
        model = users
        exclude = (
                'lastNotification',
                'lastPost',
                'groups',
                )
        widgets = {
                'password': forms.TextInput(),
                }
        #}}}
