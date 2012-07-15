from django import forms
from TransactionsApp.models import transactions, users, PostsTable
from django.db.models import Q


class loginForm(forms.Form):
    username = forms.CharField(max_length=50,label='',widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    
class PasswordChangeForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)


class transactionsForm(forms.ModelForm):   # {{{
    def __init__(self, *args, **kwargs):
        super(transactionsForm, self).__init__(*args, **kwargs)
        # change a widget attribute:
        self.fields['users_involved'].queryset = users.objects.filter(
                                                    ~Q(name__exact='admin')
                                                    )
        self.fields['user_paid'].queryset = users.objects.filter(
                                                    ~Q(name__exact='admin')
                                                    )
    class Meta:
        model = transactions
        widgets = {
                'description': forms.Textarea(attrs={'class': 'textInput'}),
                'amount': forms.TextInput(attrs={'class': 'textInput'}),
                'users_involved': forms.CheckboxSelectMultiple(),
                }
        exclude = ('perpersoncost',
                   'group',
                   'deleted',
                )
        #}}}


class addUserForm(forms.ModelForm):  # {{{
    class Meta:
        model = users
        exclude = (
                'outstanding',
                'deleted',
                'lastLogin',
                'lastNotification',
                'lastPost',
                'groups',
                )
        widgets = {
                'password': forms.PasswordInput(),
                }
        #}}}


class PostsForm(forms.ModelForm):
    def __init__(self, usr, *args, **kwargs):
        super(PostsForm, self).__init__(*args, **kwargs)
        # change a widget attribute:
        self.fields['audience'].label = 'Visible to'
        self.fields['desc'].label = 'Post Desc'
        self.fields['audience'].queryset = users.objects.filter(
                                                    ~Q(name__exact=usr.name)
                                                    ).filter(
                                                    ~Q(name__exact="admin")
                                                    )
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
                   'deleted',
                )
