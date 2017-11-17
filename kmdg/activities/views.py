# -*- coding: utf-8 -*-

#
# KMDG -> Activities -> views
#

from django.conf import settings
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from ..activities.models import NewsModel, CalendarModel


@csrf_exempt
def view_news(_, page_nr=1):
    """Widok strony aktualności"""

    # Lista wszystkich "aktualnosci" w bazie
    news = NewsModel.objects.all().order_by('-date')
    # Podzielenie jej na strony po NEWS_PER_PAGE sztuk
    paginator = Paginator(news, settings.NEWS_PER_PAGE)

    # Proba zbudowania strony o zadanym numerze
    try:
        page = paginator.page(page_nr)
    # Jesli takiej strony nie ma, to 404
    except EmptyPage:
        raise Http404

    else:
        context = {'sitetitle': u"Aktualności", 'news_page': page}
        return render_to_response('pages/news.html', context)


@csrf_exempt
def view_calendar(_, page_nr=1):
    """Widok strony kalendarium spotkań"""

    # Lista wszystkich wydarzeń
    events = CalendarModel.objects.all().order_by('-date')
    # Podzielenie na strony
    pagination = Paginator(events, settings.EVENTS_PER_PAGE)

    try:
        page = pagination.page(page_nr)
    # Jesli takiej strony nie ma, to 404
    except EmptyPage:
        raise Http404
    else:
        context = {'sitetitle': u'Kalendarium spotkań', 'calendar_page': page, 'url': '/kalendarium'}
        return render_to_response('pages/calendar.html', context)
