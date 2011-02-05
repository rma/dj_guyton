from django.conf.urls.defaults import *
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Enable the application for searching the simulation database.
    (r'^guyton/', include('guyton.urls')),

    # By default, redirect to the simulation database.
    (r'^$', redirect_to, {'url': '/guyton/'}),
)
