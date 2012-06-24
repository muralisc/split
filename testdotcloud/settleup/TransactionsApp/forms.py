from django import forms

class loginForm(form.Form):
    username = form.CharField(max_length=50)
    password = form.CharField(widget=forms.PasswordInput)


