from django.db import models
from django import forms


# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    outstanding = models.FloatField()

    def __unicode__(self):
        return self.username

class transactions(models.Model):
    description = models.CharField(max_length=50)
    amount = models.FloatField()
    user_paid = models.ForeignKey(users,related_name='transactions_set')
    users_involved = models.ManyToManyField(users,related_name='transactions_set1')
    timestamp = models.DateTimeField(auto_now_add=True)
    perpersoncost = models.FloatField(null=True)

class transactionsForm(forms.ModelForm):
    class Meta:
        model = transactions
        widgets = {
                'description':forms.Textarea(attrs={'class':'textInput'}),
                'amount':forms.TextInput(attrs={'class':'textInput'}),
                'users_involved':forms.CheckboxSelectMultiple(),
                }
        exclude = ('perpersoncost',
                )

class addUserForm(forms.ModelForm):
    class Meta:
        model = users
        exclude = ('outstanding',
                )
        widgets ={
                'password': forms.PasswordInput(),
                }
