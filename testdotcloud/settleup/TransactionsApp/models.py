from django.db import models

# Create your models here.


class users(models.Model):    # {{{
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    outstanding = models.FloatField(null=True)
    lastNotiView = models.DateTimeField()

    def __unicode__(self):
        return self.name
        #}}}


class transactions(models.Model):   # {{{
    description = models.CharField(max_length=50)
    amount = models.FloatField()
    user_paid = models.ForeignKey(users, related_name='transactions_set')
    users_involved = models.ManyToManyField(users, related_name='transactions_set1')
    timestamp = models.DateTimeField(auto_now_add=True)
    perpersoncost = models.FloatField(null=True)
    deleted = models.BooleanField(null=False)

    def __unicode__(self):
        return str(self.id)
        #}}}


class quotes(models.Model):      # {{{
    q = models.CharField(max_length=1000)
    shown = models.BooleanField()
                                     #}}}


class PostsTable(models.Model):   # {{{
    author = models.ForeignKey(users, related_name='PostsTable_author_set')
    desc = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    audience = models.ManyToManyField(users, related_name='PostsTable_audience_set')
    linkToTransaction = models.ForeignKey(transactions, blank=True, null=True)
    PostType = models.CharField(max_length=10)
    # }}}
