# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from _spreadsheet_parser import *
from occurrences.models import *
import datetime
import exceptions


class Command(BaseCommand):
	args = '<year>'
	help = 'Busca dados de ano específico'
	
	def to_num(self, s):
		if (s == None):
			return -1
		try:
			return int(s)
		except exceptions.ValueError:
			return -1
	
	def handle(self, *args, **options):
		print args

		year = str(args[0])
		user = str(args[1])
		pwd = str(args[2])

		Occurrence.objects.filter(year=int(year)).delete()

		sheet = SpreadsheetParser()
		rows = sheet.get_year_data(year, user, pwd)    
			
		for row in rows:
			o = Occurrence()	
			o.slum_name = row['slum_name']
			try:
				o.date = datetime.datetime.strptime(row['date'], '%d/%m/%Y')
			except exceptions.ValueError:
				continue
			o.location = row['location']
			o.latitude = row['latitude']
			o.longitude = row['longitude']
			o.population = self.to_num(row['population'])
			o.destroyed = self.to_num(row['destroyed'])
			o.year = int(year)
			o.homeless = self.to_num(row['homeless'])
			o.deaths = self.to_num(row['deaths'])
			o.evidences = row['evidences']
			o.comments = row['comments']
			#verificar se já não existe
			o.save() 
