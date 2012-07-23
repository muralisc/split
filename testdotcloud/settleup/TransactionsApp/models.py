from django.db import models

# Create your models here.


class GroupsTable(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    members = models.ManyToManyField('users', related_name='groupsTable_members')
    adimns = models.ManyToManyField('users', related_name='groupsTable_admins')
    deleted = models.BooleanField(default=False)


class users(models.Model):    # {{{
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.EmailField(max_length=30)
    # current outstanding [dont specify as initial outstanding]
    outstanding = models.FloatField(blank=True, null=True)
    # deleting users is a complex operation. once delted cannot be retrievd
    # back so remove this field TODO
    deleted = models.BooleanField(default=False)
    lastLogin = models.DateTimeField()
    # PostsTable is in Quotes becase its declared down
    lastNotification = models.ForeignKey('PostsTable', blank=True, null=True, related_name='users_lastNotification')
    lastPost = models.ForeignKey('PostsTable', blank=True, null=True, related_name='users_lastPost')
    # groups = models.ManyToManyField(GroupsTable, blank=True, null=True)

    def __unicode__(self):
        return self.username
        #}}}


class transactions(models.Model):   # {{{
    description = models.CharField(max_length=50)
    amount = models.FloatField()
    user_paid = models.ForeignKey(users, related_name='transactions_set')
    users_involved = models.ManyToManyField(users, related_name='transactions_set1')
    timestamp = models.DateTimeField(auto_now_add=True)
    perpersoncost = models.FloatField(blank=True, null=True)
    deleted = models.BooleanField(default=False)
    group = models.ForeignKey(GroupsTable, blank=True, null=True, related_name='transactions_group')

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
    deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.id)
    # }}}
