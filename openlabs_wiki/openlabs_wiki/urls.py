from django.conf.urls import patterns, include, url
from wiki.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', fwd_home),
    url(r'^wiki/$', fwd_home),
    url(r'^wiki/_create$', create_wiki),
    url(r'^wiki/_save$', save_wiki),
    url(r'^wiki/_save-update$', save_update_wiki),
    url(r'^wiki/login/$', login),
    url(r'^wiki/(.*)/_update$', update_wiki),
    url(r'^wiki/(.*)/_delete$', delete_wiki),
    url(r'^wiki/(.*)/_history$', history_wiki),
    url(r'^wiki/(.*)/_history/(\d+)/$', history_show_wiki),
    url(r'^wiki/(.*)/activate/(\d+)/$', activate_wiki),
    url(r'^wiki/(.*)/_compare$', compare_wiki),
    url(r'^wiki/_pages$', list_wiki),
    url(r'^wiki/(.*)/$', show_wiki),

    url(r'^login_view$', login_view),
    url(r'^add_user$', add_user),
    url(r'^logout$', logout),

    url(r'^admin/', include(admin.site.urls)),
)
