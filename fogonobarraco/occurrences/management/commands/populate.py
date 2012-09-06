# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from _spreadsheet_parser import *
from occurrences.models import *

class Command(BaseCommand):
	args = '<year>'
	help = 'Busca dados de ano específico'
	
	def handle(self, *args, **options):
		year =  str(args[0])	
    
		sheet = SpreadsheetParser()
		rows = sheet.get_year_data(year)    
			
		for row in rows:
			o = Occurrence()	
			o.slum_name = row['slum_name']
			o.date = row['date']
			o.location = row['location']
			o.latitude = row['latitude']
			o.longitude = row['longitude']
			o.population = row['population']
			o.destroyed = row['destroyed']
			o.homeless = row['homeless']
			o.deaths = row['deaths']
			o.evidences = row['evidences']
			o.comments = row['comments']
			#verificar se já não existe
			o.save() 
