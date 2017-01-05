# -*- coding: utf8 -*-

#
# KMDG -> publications -> models
#

import os

from django import forms
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from ..app.image_utils import create_thumbnail, is_image
from ..app.media_utils import get_absolute_path_of_file
from ..app.mimetypes import get_icon_by_extension
from ..app.roman import convert2roman

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Rozmiar do ktorego bedziemy skalowac okladki biuletynow
COVER_SIZE = (160, 135)

# Lokalizacja zapisu "okladki" biuletynu
COVER_DIR = u"covers/"


class TagModel(models.Model):
    """Etykietka tagu przypisana do biuletynu. Wyszukiwanie biuletynów wg tagu również ma być możliwe"""

    tag_name = models.CharField(verbose_name=u"Nazwa", max_length=100, unique=True)

    def __unicode__(self):
        return self.tag_name

    def bulletins_count(self):
        return 0

    bulletins_count.short_description = u"Liczba biuletynów"

    class Meta:
        verbose_name = u'Studium Wiedzy'
        verbose_name_plural = u'Studia Wiedzy'


class EditorModel(models.Model):
    """Redaktor biuletynu"""

    first_name = models.CharField(verbose_name=u"Imię", max_length=40)
    last_name = models.CharField(verbose_name=u"Nazwisko", max_length=50)

    def __unicode__(self):
        return u"{0} {1}".format(self.first_name, self.last_name)


    def full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    full_name.short_description = u"Redaktor"

    class Meta:
        verbose_name = u'Redaktora'
        verbose_name_plural = u'Redaktorzy'


class BulletinModel(models.Model):
    """Reprezentacja Biuletynu:
        - numer wydania (w roku)
        - numer wydania (ciagly)
        - ikona wydania
        - autor
        - data odczytu
        - data wydania
        - * numer spotkania *
        - kategoria (studium wiedzy / tag)
        - temat spotkania
        - tresc biuletynu
        - osoby redagujace (może być kilka)
    """

    number_in_year = models.SmallIntegerField(verbose_name=u"Numer w roku")
    number = models.IntegerField(verbose_name=u"Numer ogólny", help_text="Unikalny numer wydania (ciągły)", unique=True)

    cover = models.ImageField(verbose_name=u"Ikona numeru", upload_to=COVER_DIR, null=True, blank=True,
            help_text=u"Obraz zostanie przeskalowany maksymalnie do rozmiaru {0}x{1} px".format(COVER_SIZE[0], COVER_SIZE[1]))

    referent = models.CharField(verbose_name=u"Prelegent", max_length=300)
    reading = models.DateField(verbose_name=u"Data odczytu", help_text="DD.MM.YYYY")
    publication = models.DateField(verbose_name=u"Data wydania", help_text="DD.MM.YYYY")
    number_of_meeting = models.SmallIntegerField(verbose_name="Numer spotkania", null=True, blank=True)

    tag = models.ForeignKey(TagModel, verbose_name=u"Studium", null=True, blank=True)

    title = models.CharField(verbose_name=u"Temat", max_length=500)
    content = models.TextField(verbose_name=u"Treść biuletynu")

    editors = models.ManyToManyField(EditorModel, verbose_name=u"Redaktorzy")

    def __unicode__(self):
        """Reprezentacja tekstowa"""
        return self.display_number() + " / " + self.display_year()

    def get_number(self):
        """Zwraca numer biuletynu służący do konstrukcji adresu url"""
        return "{0}.{1}".format(self.number_in_year, self.number)

    def display_number(self):
        """Przyjazny format wyswietlania numeru wydania"""
        return "{0} ({1})".format(self.number_in_year, self.number)

    def display_year(self):
        """Wyswietlenie numeru roku mierzonego od momentu zalorzenia kola"""

        y = self.publication.year
        r = convert2roman(y - settings.FIRST_BULLETIN_AT_YEAR + 1)

        return r + ': ' + unicode(y)

    def thumbnail(self):
        """Miniaturka okladki wyswietlana na liscie w panelu administracyjnym"""

        if self.cover:
            return """<img src="{0}{1}"/>""".format(settings.MEDIA_URL, self.cover)
        else:
            return ""

    def save(self, force_update=True):
        """Akcja zapisu obiektu do bazy"""

        # Aktualiacja Biuletynu
        try:            
            old = BulletinModel.objects.get(pk=self.id)

        # Obiekt nie byl wczesniej zapisywany
        except:
            pass

        else:
            # Skasowanie starego pliku z dysku, jesli zostal on zaktualizowany
            if old.cover and old.cover != self.cover:
                # Usuniecie starej okladki
                try:
                    st, path = old.cover.storage, old.cover.path
                    st.delete(path)

                except OSError as oe:
                    logger.error(oe.message)

        finally:
            # Zapis do bazy
            super(BulletinModel, self).save()

    def delete(self, *args, **kwargs):
        """Usuwanie obiektu z bazy"""

        if(self.cover):
            # Pobranie lokalizacji plikow okladki
            storage, path = self.cover.storage, self.cover.path

            # Usuniecie obiektu
            super(BulletinModel, self).delete(*args, **kwargs)

            # Usuniecie pliku okladki
            try:
                storage.delete(path)
            except OSError as oe:
                logger.error(oe.message)
        else:
            super(BulletinModel, self).delete(*args, **kwargs)


    # Dodatkowe parametry wyzej wymienionych metod
    display_number.short_description = "Numer"
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Miniaturka'

    class Meta:
        """Metadane relacji obiektu z baza danych"""

        verbose_name = u'Biuletyn'
        verbose_name_plural = u'Biuletyny'


@receiver(signal=post_save, sender=BulletinModel)
def bulletin_post_save_handler(sender, **kwargs):
    """Zdarzenie polegajace na przygotowaniu miniatury okladki po zapisaniu biuletynu"""

    bulletin = kwargs['instance']

    # Jesli biuletyn posiada okladke, to zostanie ona przeskalowana
    if bulletin.cover:        
        cover_location = get_absolute_path_of_file(bulletin.cover, COVER_DIR)['fdir']

        # Przeprowadzenie minimalizacji obrazka
        create_thumbnail(cover_location, cover_location, COVER_SIZE)


class StorageModel(models.Model):
    """Model odpowiedzialny za umieszczanie różnego rodzaju plików na serwerze"""

    any_file = models.FileField(verbose_name="Prześlij plik", upload_to=u"storage/")
    description = models.CharField(verbose_name="Opis", max_length=300, null=True, blank=True)

    def __unicode__(self):
        return os.path.basename(self.any_file.path)

    def icon(self):
        return """<a href="{0}" target="_blank"><img src="/static/icons/{1}"/></a>""".format(self.url(), get_icon_by_extension(self.any_file.file.name))

    def url(self):
        """Wzgledny adres URL do umieszczonego pliku"""
        return self.any_file.url

    def filename(self):
        """Nazwa osadzonego pliku"""
        return os.path.basename(self.any_file.path)

    def delete(self, *args, **kwargs):
        """Usuwanie obiektu z bazy"""
        # Pobranie lokalizacji plikow okladki
        storage, path = self.any_file.storage, self.any_file.path

        # Usuniecie obiektu
        super(StorageModel, self).delete(*args, **kwargs)

        # Usuniecie pliku okladki
        storage.delete(path)

    # Dodatkowe parametry wyzej wymienionych metod
    icon.allow_tags = True
    icon.short_description = u"Pobierz"
    url.short_description = u"Adres URL"
    filename.short_description = u"Nazwa pliku"

    class Meta:
        verbose_name = u'Plik'
        verbose_name_plural = u'Pliki'


class BookModel(models.Model):
    """ Definicja książki:
        - numer tomu
        - ISBN
        - Autor
        - Tytuł
        - data wydania
        - liczba stron
    """

    number = models.PositiveSmallIntegerField(verbose_name=u"Numer tomu", unique=True)
    isbn = models.CharField(verbose_name=u"ISBN", max_length=20, null=True, blank=True)
    author = models.CharField(verbose_name=u"Autor", max_length=60)
    title = models.CharField(verbose_name=u"Tytuł", max_length=200)
    publication = models.PositiveIntegerField(verbose_name=u"Rok wydania")
    pages = models.IntegerField(verbose_name=u"Liczba stron")

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u"Książkę"
        verbose_name_plural = u"Książki"


class SeriesModel(models.Model):
    """Cykl zaknięty"""

    name = models.CharField(verbose_name=u"Nazwa cyklu", max_length=300, unique=True)

    def __unicode__(self):
        return self.name

    def entries_count(self):
        return SeriesEntryModel.objects.filter(series=self).count()

    entries_count.short_description = u"Liczba pozycji w cyklu"

    class Meta:
        verbose_name = u"Cykl zamknięty"
        verbose_name_plural = u"Cykle zamknięte"


class SeriesEntryModel(models.Model):
    """ Konkretna część cyklu:
        - numer
        - autor
        - tytuł
        - liczba stron
    """
    series = models.ForeignKey(SeriesModel)

    number = models.PositiveSmallIntegerField(verbose_name=u"Numer")
    author = models.CharField(verbose_name=u"Autor", max_length=60)
    title = models.CharField(verbose_name=u"Tytuł", max_length=300)
    pages = models.IntegerField(verbose_name=u"Liczba stron")

    def __unicode__(self):
        return u"{0} / {1} / {2}".format(self.title, self.author, self.pages)

    class Meta:
        verbose_name = u"Pozycja"
        verbose_name_plural = u"Pozycje"
