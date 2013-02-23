from django.conf.urls import patterns, include, url
from wiki.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', create_wiki),
    url(r'^create_wiki$', create_wiki),
    url(r'^save_wiki$',save_wiki),
    url(r'^show_wiki$',show_wiki),
    url(r'^update_wiki$',update_wiki),
    # url(r'^openlabs_wiki/', include('openlabs_wiki.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^/', include(openlabs_wiki.wiki.views.home_page)),
)
