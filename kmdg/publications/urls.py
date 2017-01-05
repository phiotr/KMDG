# -*- coding: utf8 -*-

#
# KMDG -> Publications -> urls
#

from django.conf import settings
if settings.DJ_VERSION >= '1.5':
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url


urlpatterns = patterns(settings.PROJECT_NAME + '.publications.views',

    url(r'^biuletyny/$', 'view_bulletins_list'),
    url(r'^biuletyny/rok/(?P<year>\d+)/$', 'view_bulletins_in_year'),
    url(r'^biuletyny/studium/(?P<tag_name>.*)/$', 'view_bulletins_in_tag'),
    url(r'^biuletyny/numer/(?P<n_in_year>\d+).(?P<n_global>\d+)/$', 'view_bulletin_number'),

    url(r'ksiazki/$', 'view_books_list'),
    url(r'cykle/$', 'view_series_list'),
)
