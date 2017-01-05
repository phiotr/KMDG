# -*- coding: utf8 -*-

#
# KMDG -> urls
#

from django.conf import settings

if settings.DJ_VERSION >= '1.5':
    from django.conf.urls import patterns, include, url
else:
    from django.conf.urls.defaults import patterns, include, url
    
from django.views.generic import RedirectView
from django.contrib import admin

admin.autodiscover()

# Obsluga bledow
handler404 = settings.PROJECT_NAME + '.app.views.view_404'
handler500 = settings.PROJECT_NAME + '.app.views.view_500'


urlpatterns = patterns('',

    url(r'^$', settings.PROJECT_NAME + '.app.views.view_home'),

    url(r'^admin/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
    

    url(r'^aktualnosci/$', RedirectView.as_view(url='/aktualnosci/1/')),
    url(r'^aktualnosci/(?P<page_nr>\d+)/$', settings.PROJECT_NAME + '.activities.views.view_news'),

    url(r'^kalendarium/$', RedirectView.as_view(url='/kalendarium/1/')),
    url(r'^kalendarium/(?P<page_nr>\d+)/$', settings.PROJECT_NAME + '.activities.views.view_calendar'),

    url(r'^publikacje/', include(settings.PROJECT_NAME + '.publications.urls')),
    url(r'^galerie/$', settings.PROJECT_NAME + '.gallery.views.view_gallery_list'),
    url(r'^galerie/(?P<gallery_id>\d+)/$', settings.PROJECT_NAME + '.gallery.views.view_gallery_show'),

    url(r'^zarzad/$', settings.PROJECT_NAME + '.app.views.view_administration'),


    # Pliki
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.STATIC_ROOT}),
)
