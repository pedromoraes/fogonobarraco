from django.conf import settings
from django.core.context_processors import request  
from django.shortcuts import render_to_response  
from django.template.context import Context, RequestContext  
from occurrences.models import *
from django.http import HttpResponse
from django.db.models import Count
import simplejson

def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """

    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = simplejson.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = simplejson.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator

def home(request):  
	c = Context({ 'years': settings.RESEARCH_YEARS })  
	return render_to_response("home.html", c, context_instance=RequestContext(request))

def get(request):
	#return HttpResponse(serializers.serialize('json', Occurrence.objects.all()),'application/json')
	all = []
	fields = "slum_name", "location", "formatted_date", "latitude", "longitude", "population", "destroyed", "homeless", "deaths", "injured", "evidences", "comments", "year" 
	for occ in Occurrence.objects.filter(status='P'):
		all.append(dict([(attr, getattr(occ, attr)) for attr in fields]))
	return HttpResponse(simplejson.dumps({"success": True, "occurrences": all}),'application/json')

@json_response
def per_year(request):
	qset = Occurrence.objects.filter(status='P').values('year').order_by().annotate(Count('year'))
	years = []
	for item in qset:
		years.append({'year': item['year'], 'count': item['year__count']})
	return {"success": True, "years": years}
