from django.db import models

class Occurrence(models.Model):
	slum_name = models.CharField(max_length=300)
	date = models.DateField()
	location = models.TextField()
	latitude = models.FloatField()
	longitude = models.FloatField()
	population = models.IntegerField(null=True)
	destroyed = models.IntegerField(null=True)
	homeless = models.IntegerField(null=True)
	deaths = models.IntegerField(null=True)
	evidences = models.TextField() #TODO: normalize this!
	comments = models.TextField()


