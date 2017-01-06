# -*- coding: utf8 -*-

#
# KMDG -> Publications -> urls
#

from django.conf.urls import url
from ..publications import views


urlpatterns = [
    url(r'^biuletyny/$', views.view_bulletins_list),
    url(r'^biuletyny/rok/(?P<year>\d+)/$', views.view_bulletins_in_year),
    url(r'^biuletyny/studium/(?P<tag_name>.*)/$', views.view_bulletins_in_tag),
    url(r'^biuletyny/numer/(?P<n_in_year>\d+).(?P<n_global>\d+)/$', views.view_bulletin_number),

    url(r'ksiazki/$', views.view_books_list),
    url(r'cykle/$', views.view_series_list),
]
