from django.db import models

# Create your models here.

class Transfers(models.Model):
	fromCategory = models.CharField(max_length=100)
	toCategory = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=10,decimal_places=2)
	description = models.CharField(max_length=100)
	timestamp = models.DateTimeField()
	deleted = models.BooleanField(default=False)
