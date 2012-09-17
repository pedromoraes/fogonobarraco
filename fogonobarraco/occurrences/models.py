from django.db import models

class Occurrence(models.Model):
	slum_name = models.CharField(max_length=300, null=True)
	date = models.DateField()
	year = models.IntegerField()
	location = models.TextField(null=True)
	latitude = models.FloatField()
	longitude = models.FloatField()
	population = models.IntegerField(null=True)
	destroyed = models.IntegerField(null=True)
	homeless = models.IntegerField(null=True)
	deaths = models.IntegerField(null=True)
	injured = models.IntegerField(null=True)
	evidences = models.TextField(null=True) #TODO: normalize this!
	comments = models.TextField(null=True)

	@property
	def formatted_date(self):
		return self.date.strftime("%d/%m/%Y")