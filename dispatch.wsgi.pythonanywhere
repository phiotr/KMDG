# -*- coding: utf-8 -*-

import os, sys

sys.path.append("/home/sylwiak/public_html/kmdg/");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kmdg.settings")
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/sylwiak/.python_egg_cache")

import django.core.handlers.wsgi as wsgi


technical_break = r"""<!DOCTYPE html><html><head><title>KMDG</title><meta charset="UTF-8"><meta http-equiv="refresh" content="300"></head><body><h2 align='center'><u>.:: Przerwa techniczna ::.</u></h2></body></html>"""
server_overload = r"""<!DOCTYPE html><html><head><title>KMDG</title><meta charset="UTF-8"><meta http-equiv="refresh" content="10"></head><body><h4>Chwilowe przeciążenie serwera. Przepraszamy i zapraszamy za moment...</h4></body></html>"""


def custom_site(html, start_response):
    response_headers = [('Content-type', 'text/html'), ('Content-Length', str(len(html)))]
    start_response('200 OK', response_headers)
    return [html]


def application(environ, start_response):

    # Przerwa techniczna, odkomentuj nastepna linie jesli zajdzie taka potrzeba
    return custom_site(technical_break, start_response)

    # Przekazanie sterowania do silnika django
    try:
        return wsgi.WSGIHandler().__call__(environ, start_response)
    except Exception as e:
        return custom_site(server_overload, start_response)

