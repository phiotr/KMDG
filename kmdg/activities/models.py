# -*- coding: utf8 -*-

#
# KMDG -> Activities -> models
#

from django.db import models
from ..app.today import today
from ..app.trimhtml import html_preview
from ..publications.models import BulletinModel

class CalendarModel(models.Model):
    """Kalendarium spotkań"""

    date = models.DateField(verbose_name=u"Data", help_text="DD.MM.YYYY")
    referent = models.CharField(verbose_name="Prelegent", max_length=300)
    number_of_meeting = models.SmallIntegerField(verbose_name="Numer spotkania", unique=True,
        help_text=u"Jeśli istnieje biuletyn przypisany do tego spotkania to zostanie on podlinkowany na stronie Kalendarium")
    title = models.CharField(verbose_name="Temat", max_length=500, help_text=u"Prognozowany temat wystąpienia")

    def __unicode__(self):
        return u"Spotkanie {0}".format(self.date)

    def __str__(self):
        return self.__unicode__()

    def is_upcoming(self):
        """Flaga okreslajaca czy dane spotkanie jest przyszle, czy minone"""
        return self.date >= today()

    def has_bulletin(self):
        """Sprawdzenie, czy do wprowadzonego spotkania utworzono juz wczesniej biuletyn"""

        return BulletinModel.objects.filter(number_of_meeting=self.number_of_meeting).count() == 1

    def get_bulletin(self):
        """Pobranie biuletynu powiazanego porzez numer spotkania"""
        try:

            bulletin = BulletinModel.objects.get(number_of_meeting=self.number_of_meeting)
        # Brak buletynu, lub wiecej jak jeden
        except:
            bulletin = None

        finally:
            return bulletin

    is_upcoming.short_description = u"Nadchodzące"
    is_upcoming.boolean = True

    has_bulletin.short_description = u"Posiada biuletyn"
    has_bulletin.boolean = True

    class Meta:
        verbose_name = "Spotkanie"
        verbose_name_plural = "Spotkania"


class NewsModel(models.Model):
    """Aktualności"""

    date = models.DateField(verbose_name=u"Data", help_text="DD.MM.YYYY")
    description = models.TextField(verbose_name=u"Opis")

    def __unicode__(self):
        return u"{0}".format(self.date)

    def __str__(self):
        return self.__unicode__()

    def preview(self):
        return html_preview(self.description, 100) + "(...)"

    preview.short_description = u"Podgląd"

    class Meta:
        verbose_name = "Wydarzenie"
        verbose_name_plural = "Wydarzenia"
