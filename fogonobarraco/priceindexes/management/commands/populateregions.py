# -*- coding: utf-8 -*-
#Bela Vista,Bom Retiro,Brás,Cambuci,Campos Elíseos,Consolação,Higienópolis,Liberdade,Pari,República,Santa Cecília,Santa Efigênia,Sé,Vila Buarque,Água Rasa,Alto da Mooca,Arthur Alvim,Belém,Cangaíba,Cidade Lider,Cidade Patriarca,Ermelino Matarazzo,Guaianazes,Iguatemi,Itaim Paulista,Itaquera,Jardim Anália Franco,Jardim Aricanduva,Jardim Avelino,Jardim Helena,José Bonifácio,Lajeado,Mooca,Parque do Carmo,Penha,Ponte Rasa,São Lucas,São Mateus,São Miguel Paulista,São Rafael,Sapopemba,Tatuapé,Vila Carrão,Vila Curuça,Vila Formosa,Vila Jacuí,Vila Matilde,Vila Prudente,Vila Zelina,Água Fria,Brasilândia,Casa Verde,Freguesia do Ó,Horto Florestal,Imirim,Jaçanã,Jardim São Paulo,Lauzane Paulista,Limão,Mandaqui,Parada Inglesa,Santa Terezinha,Santana,Serra da Cantareira,Tremembé,Tucuruvi,Vila Guilherme,Vila Maria,Vila Medeiros,Vila Nova Cachoeirinha,Água Branca,Alto da Lapa,Alto de Pinheiros,Anhanguera,Barra Funda,Butantã,Caxingui,Cidade Jardim,Jaguara,Jaguaré,Jaraguá,Jardim Peri,Lapa,Pacaembu,Parque dos Príncipes,Parque São Domingos,Perdizes,Perus,Pinheiros,Pirituba,Pompéia,Raposo Tavares,Rio Pequeno,Sumaré,Vila Leopoldina,Vila Madalena,Vila Romana,Vila São Francisco,Aclimação,Aeroporto,Água Funda,Alto da Boa Vista,Americanópolis,Bosque da Saúde,Brooklin,Campo Belo,Campo Grande,Campo Limpo,Capão Redondo,Capela do Socorro,Chácara Flora,Chácara Klabin,Chácara Santo Antônio,Cidade Ademar,Cidade Dutra,Cursino,Grajaú,Granja Julieta,Horto do Ipê,Ibirapuera,Interlagos,Ipiranga,Itaim Bibi,Jabaquara,Jardim América,Jardim Ângela,Jardim da Saúde,Jardim Europa,Jardim Marajoara,Jardim Paulista,Jardim São Luís,Jardim Sul,Jurubatuba,Mirandópolis,Moema,Morumbi,Panamby,Paraíso,Parelheiros,Pedreira,Real Parque,Sacomã,Santo Amaro,São Judas,Saúde,Vila Andrade,Vila Clementino,Vila das Mercês,Vila Gumercindo,Vila Mariana,Vila Mascote,Vila Nova Conceição,Vila Olímpia,Vila Santa Catarina,Vila Sônia

from django.core.management.base import BaseCommand, CommandError
import datetime
import exceptions
from priceindexes.models import *
from geopy import geocoders, distance, Point
from unidecode import unidecode
import time, urllib, simplejson

class Command(BaseCommand):
	args = '<regions>'
	help = 'Cria as regiões de cotação'
	
	def handle(self, *args, **options):
		
		if len(args) == 0:
			val = "Sé,Bela Vista,Bom Retiro,Brás,Cambuci,Campos Elíseos,Consolação,Higienópolis,Liberdade,Pari,República,Santa Cecília,Santa Efigênia,Vila Buarque,Água Rasa,Alto da Mooca,Arthur Alvim,Belém,Cangaíba,Cidade Lider,Cidade Patriarca,Ermelino Matarazzo,Guaianazes,Iguatemi,Itaim Paulista,Itaquera,Jardim Anália Franco,Jardim Aricanduva,Jardim Avelino,Jardim Helena,José Bonifácio,Lajeado,Mooca,Parque do Carmo,Penha,Ponte Rasa,São Lucas,São Mateus,São Miguel Paulista,São Rafael,Sapopemba,Tatuapé,Vila Carrão,Vila Curuça,Vila Formosa,Vila Jacuí,Vila Matilde,Vila Prudente,Vila Zelina,Água Fria,Brasilândia,Casa Verde,Freguesia do Ó,Horto Florestal,Imirim,Jaçanã,Jardim São Paulo,Lauzane Paulista,Limão,Mandaqui,Parada Inglesa,Santa Terezinha,Santana,Serra da Cantareira,Tremembé,Tucuruvi,Vila Guilherme,Vila Maria,Vila Medeiros,Vila Nova Cachoeirinha,Água Branca,Alto da Lapa,Alto de Pinheiros,Anhanguera,Barra Funda,Butantã,Caxingui,Cidade Jardim,Jaguaré,Jaraguá,Jardim Peri,Lapa,Pacaembu,Parque dos Príncipes,Parque São Domingos,Perdizes,Perus,Pinheiros,Pirituba,Pompéia,Raposo Tavares,Rio Pequeno,Sumaré,Vila Leopoldina,Vila Madalena,Vila Romana,Aclimação,Aeroporto,Água Funda,Alto da Boa Vista,Americanópolis,Bosque da Saúde,Brooklin,Campo Belo,Campo Grande,Campo Limpo,Capão Redondo,Capela do Socorro,Chácara Flora,Chácara Klabin,Chácara Santo Antônio,Cidade Ademar,Cidade Dutra,Cursino,Grajaú,Granja Julieta,Horto do Ipê,Ibirapuera,Interlagos,Ipiranga,Itaim Bibi,Jabaquara,Jardim América,Jardim Ângela,Jardim da Saúde,Jardim Europa,Jardim Marajoara,Jardim Paulista,Jardim São Luís,Jardim Sul,Jurubatuba,Mirandópolis,Moema,Morumbi,Panamby,Paraíso,Parelheiros,Pedreira,Real Parque,Sacomã,Santo Amaro,São Judas,Saúde,Vila Andrade,Vila Clementino,Vila das Mercês,Vila Gumercindo,Vila Mariana,Vila Mascote,Vila Nova Conceição,Vila Olímpia,Vila Santa Catarina,Vila Sônia"
		else:
			val = args[0]
			
		Region.objects.all().delete()

		sp = Point(-23.548999,-46.63854)

		for r in str(val).split(','):
			print r
			o = Region()
			o.name = r
			g = geocoders.Google()
			for place, (lat, lng) in g.geocode(unidecode(r) + ", Sao Paulo, Brazil", exactly_one=False):
				p = Point(lat, lng)
				d = distance.distance(sp, p)
				if (d < 50 and Region.objects.filter(latitude=lat,longitude=lng).count() == 0):
					o.latitude = lat
					o.longitude = lng
					
					name = unidecode(r.lower().replace(" ", "%20"))
					url = "http://www.zap.com.br/imoveis/fipe-zap/ajax.aspx?metodo=obterdadosgraficoindicezapimoveis&tipo=apartamento&transacao=venda&estado=sao%20paulo&cidade=sao%20paulo&bairro=" + name + "&periodo=todoperiodo&qtddormitorios=0"
					j = urllib.urlopen(url).read()
					indices = simplejson.loads(j)
					if len(indices) > 0:
						o.save()
						break
			
			time.sleep(2)
			  
