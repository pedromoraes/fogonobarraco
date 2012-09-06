# -*- coding: utf-8 -*-

import gspread
import re

class SpreadsheetParser():
		#TODO: hackear essa lib pra não exigir que logue para acessar arquivos publicos
		gc = gspread.login('email@gmail.com','pass')
		sh = gc.open_by_key('0AmDlUHs6DSRYdEFydXhrUE9wYjFtNlNWN25yQm8ySkE')

		#indexes
		DATE_INDEX = 0
		SLUM_NAME_INDEX = 1 
		LOCATION_INDEX = 2
		POPULATION_INDEX = 3
		DESTROYED_INDEX = 4
		HOMELESS_INDEX = 5
		DEATHS_INDEX = 6
		EVIDENCES_INDEX = 7
		COMMENTS_INDEX = 8
		MAP_INDEX = 9

		INITIAL_ROW_INDEX = 5

		def get_year_data(self, year='2012'):
				worksheet = self.sh.worksheet(year) 
				col_count = 10
				row_count = len(worksheet.col_values(1))

				rows = []
				for i in range(self.INITIAL_ROW_INDEX, row_count+1):
					row_values = worksheet.row_values(i)
					row = {}
					row['date'] = row_values[self.DATE_INDEX]
					row['slum_name'] = row_values[self.SLUM_NAME_INDEX]
					row['location'] = row_values[self.LOCATION_INDEX]
					row['population'] = row_values[self.POPULATION_INDEX]
					row['destroyed'] = row_values[self.DESTROYED_INDEX]
					row['homeless'] = row_values[self.HOMELESS_INDEX]
					row['deaths'] = row_values[self.DEATHS_INDEX]
					row['evidences'] = row_values[self.EVIDENCES_INDEX]
					row['comments'] = row_values[self.COMMENTS_INDEX]

					p = re.compile('(?<=sll=)-?\d+.?\d+,?-?\d+.?\d+') #TODO: melhorar essa caca pra retornar uma lista de 2 objetos e eliminar esses splits abaixo
					coords = p.findall(row_values[self.MAP_INDEX])
					row['latitude'] = coords[0].split(",")[0]
					row['longitude'] = coords[0].split(",")[1]
					rows.append(row)
				return rows

			
