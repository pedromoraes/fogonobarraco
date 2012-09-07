from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'fogonobarraco.views.home', name='home'),
    # url(r'^fogonobarraco/', include('fogonobarraco.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'occurrences.views.home'),  
    (r'^occurrences\.json', 'occurrences.views.get'),
    (r'^regions\.json', 'priceindexes.views.regions'),
    (r'^region/(?P<id>\d+)/indices\.json', 'priceindexes.views.indices'),
    (r'^chart/(?P<id>\d+)/', 'occurrences.views.chart')
   
)
