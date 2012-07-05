from django import forms
from TransactionsApp.models import transactions, users, PostsTable


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
        exclude = (
                'outstanding',
                'lastNotiView',
                )
        widgets = {
                'password': forms.PasswordInput(),
                }
        #}}}


class PostsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        # change a widget attribute:
        self.fields['audience'].label = 'Visible for'
        self.fields['desc'].label = 'Post Desc'

    class Meta:
        model = PostsTable
        widgets = {
                'desc': forms.Textarea(attrs={'class': 'textInput'}),
                'audience': forms.CheckboxSelectMultiple(),
                }
        exclude = (
                   'author',
                   'timestamp',
                   'linkToTransaction',
                   'PostType',
                )
