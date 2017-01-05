# -*- coding: utf-8 -*-

import os
from django.conf import settings


def get_absolute_path_of_file(filefield, media_subdir):
    """Nieszczesne pola FileField, ImageField nie potrafia wskazywac poprawnej sicezki z podkatalogach MEDIA_ROOT.
    Ta funkcja naprawia ten brak poprzez doklejenie w odpowienie miejsce brakujcej nazwy katalogu.

    Parametry:
        filefield - instancja pola django.db.models.FileField
        media_subdir - pominiety katalog, a ktory jest ustawiony w filefield jako parametr "upload_to"

    Zwracana wartosc:
        Slownik: fname - nazwa pliku wraz z rozszerzeniem, fdir - bezposrednia sciezka do tego pliku
            pdir - sciezka rodzica, tj. katalogu nadrzednego
    """

    # Nazwa pliku na ktory wskazuje filefield
    file_name = os.path.basename(filefield.path)

    # Katalog nadrzedny (w MEDIA_ROOT)
    directory = os.path.join(settings.MEDIA_ROOT, media_subdir)

    # Absolutna sciezka do pliku
    file_path = os.path.join(directory, file_name)

    return {'fname': file_name, 'fdir': file_path, 'pdir': directory}



