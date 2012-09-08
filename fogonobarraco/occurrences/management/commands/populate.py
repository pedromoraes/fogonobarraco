# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand, CommandError
from _spreadsheet_parser import *
from occurrences.models import *
import datetime
import exceptions


class Command(BaseCommand):
	args = '<year>'
	help = 'Busca dados de anos específicos (ex: 2010-2012 ou 2008,2009,2010)'
	
	def to_num(self, s):
		if (s == None):
			return -1
		try:
			return int(s)
		except exceptions.ValueError:
			return -1
	
	def handle(self, *args, **options):
		year_selection = str(args[0])
		self.user = str(args[1])
		self.pwd = str(args[2])
		
		if 	year_selection.find('-') != -1:
			a, b = 	year_selection.split('-')
			years = range(int(a), int(b)+1)
		else:
			years = year_selection.split(',')
		
		print years
		
		for year in years:
			self.consume(str(year))


	def consume(self, year):
		Occurrence.objects.filter(year=int(year)).delete()

		sheet = SpreadsheetParser()
		rows = sheet.get_year_data(year, self.user, self.pwd)    
			
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
