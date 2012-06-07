from django.db import models

# Create your models here.

class users(models.Model):
    name = models.CharField(max_length=10)
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=50)
    outstanding = models.FloatField()

class transactions(models.Model):
    description = models.CharField(max_length=50)
    amount = models.FloatField()
    user_paid = models.ForeignKey(users,related_name='transactions_set')
    users_involved = models.ManyToManyField(users,related_name='transactions_set1')
    timestamp = models.DateTimeField(auto_now_add=True)
    perpersoncost = models.FloatField()

