from django.db import models

# Create your models here.


class Transfers(models.Model):
    fromCategory = models.CharField(max_length=100, blank=True)
    toCategory = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    description = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(blank=True)
    deleted = models.BooleanField(default=False, blank=True)
