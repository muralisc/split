from django import forms
from TransactionsApp.models import transactions, users, PostsTable, GroupsTable
from django.db.models import Q


class loginForm(forms.Form):
    username = forms.CharField(max_length=50, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class PasswordChangeForm(forms.Form):
    oldPassword = forms.CharField(widget=forms.PasswordInput)
    newPassword = forms.CharField(widget=forms.PasswordInput)


class transactionsForm(forms.ModelForm):   # {{{
    def __init__(self, usr, *args, **kwargs):
        super(transactionsForm, self).__init__(*args, **kwargs)
        # change a widget attribute:
        self.fields['users_involved'].queryset = users.objects.filter(
                                                    Q(name__in=usr.group.members.values_list('name')),
                                                    )
        self.fields['user_paid'].queryset = users.objects.filter(
                                                    Q(name__in=usr.group.members.values_list('name')),
                                                    )

    class Meta:
        model = transactions
        widgets = {
                'description': forms.TextInput(attrs={'class': '', 'rows': '1', 'placeholder': 'Category'}),
                'amount': forms.TextInput(attrs={'class': '', 'placeholder': 'Amount'}),
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
                'group',
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
                                                    ~Q(name__exact=usr.name),
                                                    name__in=[tempUsr.name for tempUsr in usr.group.members.all()],
                                                    )

    class Meta:
        model = PostsTable
        widgets = {
                'desc': forms.Textarea(attrs={'class': 'textInput', 'rows': '3'}),
                'audience': forms.CheckboxSelectMultiple(),
                }
        exclude = (
                   'author',
                   'timestamp',
                   'linkToTransaction',
                   'PostType',
                   'deleted',
                )


class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupsTable
        exclude = (
                    'members',
                    'adimns',
                    'deleted',
                )
