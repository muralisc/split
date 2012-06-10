from django import forms

class addUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)


class addTransactionForm(forms.Form):
    description = forms.CharField()
    user_paid = forms.ChoiceField()
    users_involved = forms.BooleanField()

