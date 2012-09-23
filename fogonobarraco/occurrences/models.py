from django.db import models

class Occurrence(models.Model):
	OCCURRENCE_STATUS = (
        ('N', 'New'),
        ('P', 'Published'),
    )

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
	evidences = models.TextField(null=True) #TODO: normalize!
	comments = models.TextField(null=True)
	status = models.CharField(max_length=2, choices=OCCURRENCE_STATUS) 
	signature = models.CharField(max_length=32, null=False)	
	
	@property
	def formatted_date(self):
		return self.date.strftime("%d/%m/%Y")
	

	def similar(self):
		similars = Occurrence.objects.filter(date=self.date)
		return similar
