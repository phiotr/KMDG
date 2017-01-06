# -*- coding: utf-8 -*-

#
# KMDG -> Publications -> views
#

from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_exempt

from ..app.today import today
from ..publications.models import BulletinModel, TagModel, BookModel, SeriesModel, SeriesEntryModel


def years_list():
    """Lista rocznikow, od bierzacego, wstecz az do roku zalozenia kola"""
    return reversed(range(settings.FIRST_BULLETIN_AT_YEAR, today().year + 1))


def tags_list():
    """Lista wszystkich tagów biuletynów"""
    return TagModel.objects.all().order_by('tag_name')


@csrf_exempt
def view_bulletins_list(request):
    """Zakładka Biuletyny"""
    # Ostatnio opublikowany
    try:        
        lastest = BulletinModel.objects.all().order_by('-publication')[:3]

    except Exception as e:
        lastest = None

    c = RequestContext(request, {'sitetitle': u'Biuletyny', 'years': years_list(), 'lastest': lastest, 'tags': tags_list()})

    return render_to_response('pages/bulletins_list.html', c)


@csrf_exempt
def view_bulletins_in_year(request, year):
    """Strona zawierająca listę wszystkim biuletynów w danym roku"""

    bulletins = BulletinModel.objects.filter(publication__year=year).order_by('-number_in_year')

    c = RequestContext(request, {'sitetitle': u'Biuletyny {0}'.format(year),
                    'year': int(year), 'years': years_list(), 'bulletins':bulletins})

    return render_to_response('pages/bulletins_in_year.html', c)


@csrf_exempt
def view_bulletins_in_tag(request, tag_name):
    """Strona zawierająca listę wszystkich biuletynów o wskazanym tagu"""
    
    tag = get_object_or_404(TagModel, tag_name=tag_name)
    bulletins = BulletinModel.objects.filter(tag=tag).order_by('-reading')

    c = RequestContext(request, {'sitetitle': u'Biuletyny z serii "{0}"'.format(tag), 
        'tag': tag_name, 'tags': tags_list(), 'bulletins':bulletins})
                    
    return render_to_response('pages/bulletins_in_tag.html', c)


@csrf_exempt
def view_bulletin_number(request, n_in_year, n_global):
    """Strona wyświetlająca konkretny biuletyn (na podstawie jego numerów wydania)"""
    # Proba wydobycia z bazy konkretnego biuletynu
    bulletin = get_object_or_404(BulletinModel, number_in_year=n_in_year, number=n_global)

    c = RequestContext(request, {'sitetitle': "Biuletyn {0}".format(bulletin.display_number()),
                    'bulletin': bulletin})

    return render_to_response('pages/bulletin.html', c)


@csrf_exempt
def view_books_list(request):
    """Strona z listą wydanych książek"""
    books = BookModel.objects.all().order_by('number')
    
    c = RequestContext(request, {'sitetitle': u'Książki', 'books': books})
    
    return render_to_response('pages/books_list.html', c)


@csrf_exempt
def view_series_list(request):
    """Strona z listą zamknietych wydawnictw"""
    
    # Lista tupli postaci (seria, [wpisy w serii])
    series = [(s, SeriesEntryModel.objects.filter(series=s).order_by('number')) for s in SeriesModel.objects.all()]
        
    c = RequestContext(request, {'sitetitle': u'Cykle zamknięte', 'series': series})
    
    return render_to_response('pages/series_list.html', c)