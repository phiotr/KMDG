# -*- coding: utf-8 -*-

#
# KMDG -> App -> views
#
from datetime import date
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from ..activities.models import CalendarModel, NewsModel


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
