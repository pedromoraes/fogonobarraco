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
		
		cols = {'A':{'TYPE_INDEX':-1, 'DATE_INDEX':0, 'SLUM_NAME_INDEX':1, 'LOCATION_INDEX':2, 'POPULATION_INDEX':3, 'DESTROYED_INDEX':4, 
				'HOMELESS_INDEX':5, 'DEATHS_INDEX':6, 'INJURED_INDEX':7, 'EVIDENCES_INDEX':8, 'COMMENTS_INDEX':9, 'MAP_INDEX':10, 'INITIAL_ROW_INDEX':5},
				'B':{'TYPE_INDEX':1, 'DATE_INDEX':3, 'SLUM_NAME_INDEX':0, 'LOCATION_INDEX':[5,6], 'POPULATION_INDEX':12, 'DESTROYED_INDEX':10, 
				'HOMELESS_INDEX':11, 'DEATHS_INDEX':8, 'INJURED_INDEX':7, 'EVIDENCES_INDEX':13, 'COMMENTS_INDEX':14, 'MAP_INDEX':15, 'INITIAL_ROW_INDEX':5}}

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
					#print "\n\n\n NEW ROW:"
					row_values = worksheet.row_values(i)
					def get(x):
						try: return row_values[cols[x]] or ''
						except Exception: return ''
					#print get('TYPE_INDEX')
					if (ws_type == 'B' and get('TYPE_INDEX').lower() != 'favela'): continue
					row = {}
					row['date'] = get('DATE_INDEX')
					if (row['date'] == None): continue
					
					row['slum_name'] = get('SLUM_NAME_INDEX')

					l = cols['LOCATION_INDEX']
					if (isinstance(l, (list, tuple))):
						locationcols = []
						for lc in l: locationcols.append(worksheet.cell(i, lc+1).value or '')
						row['location'] = 'rua ' + ','.join(locationcols)
					else:
						row['location'] = get('LOCATION_INDEX')
					row['population'] = get('POPULATION_INDEX')
					row['destroyed'] = get('DESTROYED_INDEX')
					row['homeless'] = get('HOMELESS_INDEX')
					row['deaths'] = get('DEATHS_INDEX')
					row['injured'] = get('INJURED_INDEX')
					row['evidences'] = get('EVIDENCES_INDEX')
					row['comments'] = get('COMMENTS_INDEX')
					if (ws_type == 'B'):
						if row['comments'] == None: row['comments']  = 'Fonte: Defesa civil'
						else: row['comments'] = str(row['comments']) + ' Fonte: Defesa Civil'

					#print row

					sp = Point(-23.548999,-46.63854)
					coords = ''
					mapurl = get('MAP_INDEX')
					
					def in_range(p):
						d = distance.distance(p, sp)
						print d
						return (d > 0.1 and d < 50)
					
					if (mapurl):
						p = re.compile('(?<=ll=)-?\d+.?\d+,?-?\d+.?\d+') #TODO: melhorar essa caca pra retornar uma lista de 2 objetos e eliminar esses splits abaixo
						coords = p.findall(mapurl)					
						if len(coords) == 0 or not in_range(Point(*coords[0].split(","))):
							p = re.compile('(?<=q=)-?\d+.?\d+,?-?\d+.?\d+')
							coords = p.findall(mapurl)
							if len(coords) == 0 or not in_range(Point(*coords[0].split(","))): coords = ''
					elif (row['location']):
						try:
							g = geocoders.Google()
							for place, (lat, lng) in g.geocode(unidecode(row['location']) + ", Sao Paulo, Brazil", exactly_one=False):
								p = Point(lat, lng)
								if (in_range(p)):
									coords = [str(lat)+','+str(lng)]
									break
						except Exception:
							print 'GQueryError'
							
					if (len(coords) and len(coords[0].split(",")) == 2):
						row['latitude'] = coords[0].split(",")[0]
						row['longitude'] = coords[0].split(",")[1]
						#print ('saving', row['location'], coords)
						rows.append(row)
				return rows

			
