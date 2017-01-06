# -*- coding: utf-8 -*-

#
#	KMDG -> App -> models
#

from ..app.today import today
from django.core.exceptions import ValidationError
from django.db import models

DEFAULT_SKIN = "skin_default.css"

SKINS = {DEFAULT_SKIN: u"Czerwona",
        "skin_gray.css": u"Szara",
        "skin_green.css": u"Zielona"}


class SkinModel(models.Model):

    skin = models.CharField(verbose_name=u"Skórka", max_length=30, choices=tuple(SKINS.items()))
    start = models.DateField(verbose_name=u"Od", help_text="DD.MM.YYYY")
    stop  = models.DateField(verbose_name=u"Do", help_text="DD.MM.YYYY")
    description = models.CharField(verbose_name=u"Krótki opis", max_length=100, blank=True, null=True)

    def __unicode__(self):
        return str(self.pk) + ") " + SKINS[self.skin] + "({0}, {1})".format(self.start, self.stop)

    def __str__(self):
        return self.__unicode__()

    def is_actual(self):
        """Czy dana skorka obowiazuje"""
        td = today()
        return self.start <= td and self.stop >= td

    def get_id(self):
        return self.id

    def clean(self):
        """Prosta walidacja (całego) modelu"""

        if self.start > self.stop:
            raise ValidationError(u"Błędny zakres dat")

    # Konfiguracja powyzszych metod
    is_actual.short_description = "Aktywna"
    is_actual.boolean = True

    get_id.short_description = "#"

    class Meta:
        verbose_name = u"Skórkę"
        verbose_name_plural = u"Skórki"
