# -*- coding: utf8 -*-

#
# KMDG -> urls
#
from django.conf import settings
from django.views import static, generic
from django.contrib import admin
from django.contrib import auth
from django.conf.urls import include, url
from .app import views as app_views
from .activities import views as activities_views
from .gallery import views as gallery_views


admin.autodiscover()

# Error handlers
handler404 = app_views.view_404
handler500 = app_views.view_500

urlpatterns = [
    url(r'^$', app_views.view_home),

    url(r'^admin/logout/$', auth.logout, {'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^aktualnosci/$', generic.RedirectView.as_view(url='/aktualnosci/1/')),
    url(r'^aktualnosci/(?P<page_nr>\d+)/$', activities_views.view_news),

    url(r'^kalendarium/$', generic.RedirectView.as_view(url='/kalendarium/1/')),
    url(r'^kalendarium/(?P<page_nr>\d+)/$', activities_views.view_calendar),

    url(r'^publikacje/', include(settings.PROJECT_NAME + '.publications.urls')),
    url(r'^galerie/$', gallery_views.view_gallery_list),
    url(r'^galerie/(?P<gallery_id>\d+)/$', gallery_views.view_gallery_show),

    url(r'^zarzad/$', app_views.view_administration),

    # Files
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}),
    
    # Dev
    # url(r'^dev/$', app_views.sysinfo_view),
]
