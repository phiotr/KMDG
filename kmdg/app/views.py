# -*- coding: utf-8 -*-

#
#	KMDG -> App -> views
#
from datetime import date
from django.template import  RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ..activities.models import CalendarModel, NewsModel


@csrf_exempt
def view_404(request):
    "Strona błędu adresu"""
    return render_to_response('pages/404.html', RequestContext(request))


@csrf_exempt
def view_500(request):
    """Strona błędy serwera"""
    return render_to_response('pages/500.html', RequestContext(request))


@csrf_exempt
def view_home(request):
    """Strona główna"""

    try:
        news = NewsModel.objects.all().order_by('-date')[0:3]
    except IndexError:
        news = None    
    
    events = CalendarModel.objects.filter(date__gte=date.today()).order_by('date')

    c = RequestContext(request, {'sitetitle': u'Strona główna', 'news': news, 'events': events})
    return render_to_response('pages/home.html', c)


@csrf_exempt
def view_administration(request):
    """Strona "Zarząd" """
    c = RequestContext(request, {'sitetitle': 'Skład zarządu',})
    return render_to_response('pages/administration.html', c)


@csrf_exempt
def sysinfo_view(request):
    import sys, os, pip
    c = RequestContext(request, {'path': sys.path, 'env': os.environ, 'libs': pip.get_installed_distributions()})
    return render_to_response('pages/sysinfo.html', c)
