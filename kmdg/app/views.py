# -*- coding: utf-8 -*-

#
# KMDG -> App -> views
#
from datetime import date
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from ..activities.models import CalendarModel, NewsModel
from ..activities.views import number_of_news_pages, number_of_calendar_pages
from ..gallery.views import get_list_of_gall_indexes
from ..publications.views import years_list


@csrf_exempt
def view_404(_):
    "Strona błędu adresu"""
    return render_to_response('pages/404.html')


@csrf_exempt
def view_500(_):
    """Strona błędu serwera"""
    return render_to_response('pages/500.html')


@csrf_exempt
def view_home(_):
    """Strona główna"""
    try:
        news = NewsModel.objects.all().order_by('-date')[0:3]
    except IndexError:
        news = None    

    events = CalendarModel.objects.filter(date__gte=date.today()).order_by('date')
    context = {'sitetitle': u'Strona główna', 'news': news, 'events': events}
    return render_to_response('pages/home.html', context)


@csrf_exempt
@cache_page(2 * 24 * 60 * 60)  # 2 days
def view_sitemap(_):
    domain_url = 'http://kmdg.grudziadz.pl'
    context = {'domain_url': domain_url,
               'activity_tabs': range(1, number_of_news_pages() +1),
               'calendar_tabs': range(1, number_of_calendar_pages() + 1),
               'galleries_list': get_list_of_gall_indexes(),
               'bulletin_years': years_list(),
               }

    return render_to_response('main/sitemap.xml', context, content_type='application/xml')


@csrf_exempt
def view_administration(_):
    """Strona "Zarząd" """
    context = {'sitetitle': 'Skład zarządu',}
    return render_to_response('pages/administration.html', context)


@login_required
@user_passes_test(lambda user: user.is_active and user.is_superuser)
def sysinfo_view(_):
    import sys, os, pip
    context = {'path': sys.path, 'env': os.environ, 'libs': pip.get_installed_distributions()}
    return render_to_response('dev/sysinfo.html', context)
