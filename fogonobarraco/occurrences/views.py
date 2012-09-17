from django.conf import settings
from django.core.context_processors import request  
from django.shortcuts import render_to_response  
from django.template.context import Context, RequestContext  
from occurrences.models import *
from django.http import HttpResponse
import simplejson

def home(request):  
	c = Context({ 'years': settings.RESEARCH_YEARS })  
	return render_to_response("home.html", c, context_instance=RequestContext(request))

def get(request):
	#return HttpResponse(serializers.serialize('json', Occurrence.objects.all()),'application/json')
	all = []
	fields = "slum_name", "location", "formatted_date", "latitude", "longitude", "population", "destroyed", "homeless", "deaths", "injured", "evidences", "comments", "year" 
	for occ in Occurrence.objects.all():
		all.append(dict([(attr, getattr(occ, attr)) for attr in fields]))
	return HttpResponse(simplejson.dumps({"success": True, "occurrences": all}),'application/json')