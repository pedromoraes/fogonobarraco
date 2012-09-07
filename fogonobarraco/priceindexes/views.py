from django.conf import settings
from django.core.context_processors import request  
from django.shortcuts import render_to_response  
from django.template.context import Context, RequestContext  
from priceindexes.models import *
from django.http import HttpResponse
from unidecode import unidecode
import simplejson
import urllib

def regions(request):
	all = []
	fields = "name", "latitude", "longitude", "pk"
	for occ in Region.objects.all():
		all.append(dict([(attr, getattr(occ, attr)) for attr in fields]))
	return HttpResponse(simplejson.dumps({"success": True, "regions": all}),'application/json')

def indices(request, id):
	region = Region.objects.get(pk=id)
	n = unidecode(region.name.lower().replace(" ", "%20"))
	url = "http://www.zap.com.br/imoveis/fipe-zap/ajax.aspx?metodo=obterdadosgraficoindicezapimoveis&tipo=apartamento&transacao=venda&estado=sao%20paulo&cidade=sao%20paulo&bairro=" + n + "&periodo=todoperiodo&qtddormitorios=0"
	j = urllib.urlopen(url).read()
	indices = simplejson.loads(j)
	return HttpResponse(simplejson.dumps({"success": True, "indices": indices}),'application/json')