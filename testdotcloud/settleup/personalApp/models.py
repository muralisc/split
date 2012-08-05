from django.db import models


class Categories(models.Model):
    name = models.CharField(max_length=100, blank=True)
    category_type = models.CharField(max_length=100, blank=True)
    initial_amt = models.FloatField(blank=True, null=True)
    userID = models.IntegerField(blank=True, null=True)


class Transfers(models.Model):
    fromCategory = models.ForeignKey('Categories', blank=True, null=True, related_name='transfers_fromCategory')
    toCategory = models.ForeignKey('Categories', blank=True, null=True, related_name='transfers_toCategory')
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(blank=True)
    deleted = models.BooleanField(default=False, blank=True)
    userID = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return str(self.id)
