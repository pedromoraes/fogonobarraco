from django.db import models

# Create your models here.
class Region(models.Model):
	name = models.CharField(max_length=100)
	latitude = models.FloatField()
	longitude = models.FloatField()
