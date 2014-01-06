from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'botdisplay_webinterface.views.home', name='home'),
    # url(r'^botdisplay_webinterface/', include('botdisplay_webinterface.foo.urls')),
    url(r'^$', 'botdisplay.views.index'),
    url(r'^botdisplay/$', 'botdisplay.views.index'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
