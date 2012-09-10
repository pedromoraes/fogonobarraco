# -*- coding: utf-8 -*-

import gspread, re
from unidecode import unidecode
from geopy import geocoders, distance, Point

class SpreadsheetParser():
		#TODO: hackear essa lib pra não exigir que logue para acessar arquivos publicos
		#user = raw_input('username: ')
		#pwd = raw_input('password: ')

		#indexes
		
		INITIAL_ROW_INDEX = 5
		
		cols = {'A':{'DATE_INDEX':0, 'SLUM_NAME_INDEX':1, 'LOCATION_INDEX':2, 'POPULATION_INDEX':3, 'DESTROYED_INDEX':4, 
				'HOMELESS_INDEX':5, 'DEATHS_INDEX':6, 'EVIDENCES_INDEX':7, 'COMMENTS_INDEX':8, 'MAP_INDEX':9, 'INITIAL_ROW_INDEX':5},
				'B':{'DATE_INDEX':3, 'SLUM_NAME_INDEX':0, 'LOCATION_INDEX':[5,6], 'POPULATION_INDEX':12, 'DESTROYED_INDEX':10, 
				'HOMELESS_INDEX':11, 'DEATHS_INDEX':8, 'EVIDENCES_INDEX':13, 'COMMENTS_INDEX':14, 'MAP_INDEX':15, 'INITIAL_ROW_INDEX':5}}

		def get_year_data(self, year, user, pwd):
		
				gc = gspread.login(user, pwd)
				sh = gc.open_by_key('0AmDlUHs6DSRYdEFydXhrUE9wYjFtNlNWN25yQm8ySkE')
				
				worksheet = sh.worksheet(year) 
				col_count = 10
				row_count = len(worksheet.col_values(2))

				rows = []
				print len(worksheet.row_values(0))
				if(worksheet.cell(3, 1).value == 'Dados fornecidos pela Defesa Civil ; DC_ = campo dos dados fornecidos pela Defesa Civil'):
					ws_type = 'B'
				else:
					ws_type = 'A'
					
				print ws_type, row_count
				cols = self.cols[ws_type]
				for i in range(cols['INITIAL_ROW_INDEX'], row_count+1):
					get = lambda x: worksheet.cell(i, x+1).value or ''
					if (ws_type == 'B' and get(1).lower() != 'favela'): continue
					row = {}
					row['date'] = get(cols['DATE_INDEX'])
					if (row['date'] == None): continue
					
					row['slum_name'] = get(cols['SLUM_NAME_INDEX'])

					if (isinstance(cols['LOCATION_INDEX'], (list, tuple))):
						row['location'] = ','.join(map(get, cols['LOCATION_INDEX']))
					else:
						row['location'] = get(cols['LOCATION_INDEX'])
					row['population'] = get(cols['POPULATION_INDEX'])
					row['destroyed'] = get(cols['DESTROYED_INDEX'])
					row['homeless'] = get(cols['HOMELESS_INDEX'])
					row['deaths'] = get(cols['DEATHS_INDEX'])
					row['evidences'] = get(cols['EVIDENCES_INDEX'])
					row['comments'] = get(cols['COMMENTS_INDEX'])
					if (ws_type == 'B'):
						if row['comments'] == None: row['comments']  = 'Fonte: Defesa civil'
						else: row['comments'] = str(row['comments']) + ' Fonte: Defesa Civil'

					print row

					sp = Point(-23.548999,-46.63854)
					coords = ''

					if (get(cols['MAP_INDEX'])):
						p = re.compile('(?<=.ll=)-?\d+.?\d+,?-?\d+.?\d+') #TODO: melhorar essa caca pra retornar uma lista de 2 objetos e eliminar esses splits abaixo
						coords = p.findall(worksheet.cell(i, cols['MAP_INDEX']+1).value)
						if len(coords) == 0:
							p = re.compile('(?<=q=)-?\d+.?\d+,?-?\d+.?\d+')
							coords = p.findall(worksheet.cell(i, cols['MAP_INDEX']+1).value)
					elif (row['location']):
						print 'geocode'
						try:
							g = geocoders.Google()
							for place, (lat, lng) in g.geocode(unidecode(row['location']) + ", Sao Paulo, Brazil", exactly_one=False):
								p = Point(lat, lng)
								d = distance.distance(p, sp)
								print d
								if (d > 0.1 and d < 50):
									coords = [str(lat)+','+str(lng)]
									break
						except Exception:
							print 'GQueryError'
							
					if (len(coords) and len(coords[0].split(",")) == 2):
						row['latitude'] = coords[0].split(",")[0]
						row['longitude'] = coords[0].split(",")[1]
						print ('saving', row['location'], coords)
						rows.append(row)
				return rows

			
