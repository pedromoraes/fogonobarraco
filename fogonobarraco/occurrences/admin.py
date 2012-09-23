from django.contrib import admin
from occurrences.models import Occurrence
from django.core.urlresolvers import *
from django.utils.html import *


def similar(obj):
	similars = Occurrence.objects.filter(date=obj.date).exclude(pk=obj.pk)
	similars_result = ""

	app_label = obj._meta.app_label
	model = obj._meta.module_name
	
	for similar in similars:
		similars_result += mark_safe("<a href='" + reverse('admin:%s_%s_change' % (app_label, model), args=(obj.id,)) + "'>" + str(similar.slum_name) + "</a>, ") 
	return similars_result
similar.allow_tags = True

class OccurrenceAdmin(admin.ModelAdmin):
	list_display = ('slum_name', 'location', 'status', similar)
	list_editable = ('status',)
	list_filter = ('status','year',) 
	pass	

admin.site.register(Occurrence, OccurrenceAdmin)

