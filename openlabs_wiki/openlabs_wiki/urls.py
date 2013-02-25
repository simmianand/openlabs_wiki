from django.conf.urls import patterns, include, url
from wiki.views import fwd_home, create_wiki, save_wiki, update_wiki, \
    delete_wiki, history_wiki, history_show_wiki, compare_wiki,\
    list_wiki, show_wiki, login

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', fwd_home),
    url(r'^wiki/$', fwd_home),
    url(r'^wiki/_create$', create_wiki),
    url(r'^wiki/_save$', save_wiki),
    url(r'^wiki/login/$', login),
    url(r'^wiki/(.*)/_update$', update_wiki),
    url(r'^wiki/(.*)/_delete$', delete_wiki),
    url(r'^wiki/(.*)/_history$', history_wiki),
    url(r'^wiki/(.*)/_history/(\d+)/$', history_show_wiki),
    url(r'^wiki/(.*)/_compare$', compare_wiki),
    url(r'^wiki/_pages$', list_wiki),
    url(r'^wiki/(.*)/$', show_wiki),

    url(r'^admin/', include(admin.site.urls)),
)
