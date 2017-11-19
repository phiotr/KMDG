# -*- coding: utf-8 -*-

#
#	KMDG -> Gallery -> models
#

import os

from ..app.image_utils import create_thumbnail
from ..app.media_utils import get_absolute_path_of_file

from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from ckeditor_uploader import fields as ckefields


# Rozmiar poglądowego obrazka
THUMB_SIZE = (240, 160)
PHOTO_MAX_SIZE = (800, 500)

# Prefiks doklejany do nazwy pliku
THUMB_PREFIX = "mini_"

# Wzgledna sciezka galerii (w MEDIA_ROOT)
GALLERY_DIR = u"gallery/"

# Plik okładki, jeśli galeria nie posiada swoich zdjęć
NO_PHOTOS_IN_URL = r"/static/images/photo-camera.png"


class GalleryModel(models.Model):

    title = models.CharField(verbose_name=u"Tytuł", max_length=300)
    description = ckefields.RichTextUploadingField(verbose_name=u"Opis")
    create_date = models.DateField(verbose_name=u"Data utworzenia", editable=False, auto_now_add=True)

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.__unicode__()

    def photo_count(self):
        """Metoda zwraca ilosc przypietych fotografii do tej galerii"""
        return PhotoModel.objects.filter(gallery__id=self.id).count()

    def get_gallery_cover(self):
        """Zwraca miniaturkę pierwszego zdjęcia umieszczonego w tej galerii"""

        try:
            first_url = PhotoModel.objects.filter(gallery=self.pk)[0].thumb.url
        except Exception:
            first_url = NO_PHOTOS_IN_URL

        return first_url

    photo_count.short_description = "Liczba fotografii"
    get_gallery_cover.short_description = u"Okładka galerii"
    get_gallery_cover.allow_tags = True

    class Meta:
        verbose_name = u"Galerię"
        verbose_name_plural = u"Galerie"


@receiver(pre_delete, sender=GalleryModel)
def gallery_pre_delete_handler(sender, **kwargs):
    """Zdarzenie polegajace na (dokladnym) usunieciu obiektow Zdjec podczas kasowania Galerii"""

    # Wydobycie obiekty galerii na ktorym zachodzi akcja DELETE
    gallery = kwargs['instance']

    try:
        photos = PhotoModel.objects.filter(gallery__id=gallery.id)

        for ph in photos:
            ph.delete()
    except:
        print("Kasowanie pustej galerii")


class PhotoModel(models.Model):

    gallery = models.ForeignKey(GalleryModel)

    photo = models.ImageField(verbose_name=u"Plik zjęcia", upload_to=GALLERY_DIR)
    thumb = models.ImageField(verbose_name=u"Miniaturka", upload_to=GALLERY_DIR, editable=False)

    description = models.CharField(verbose_name=u"Opis pod zjęciem", max_length=255, null=True, blank=True)

    def __unicode__(self):
        uni = u""
        try:
            uni = u"Zdjęcie({0})".format(self.photo.file.name)
        except Exception:
            uni = "Obrazek"
        finally:
            return uni

    def __str__(self):
        return self.__unicode__()

    def display_thumb(self):
        if self.thumb:
            return """<img src="{0}" alt="{1}"/>""".format(self.thumb.url, self.thumb.file.name)
        else:
            return ""
    display_thumb.short_description = u"Podgląd"
    display_thumb.allow_tags = True

    def save(self, *args, **kwargs):
        """Reakcja na zapis"""

        # Proba zaktualizowania pliku
        try:
            # Poprzednio zapisany obiekt w bazie (aktualizowany)
            old = PhotoModel.objects.get(id=self.id)

        # Wyjatek, jesli obiekt nie byl wczesnij zapisywany
        except:
            pass

        else:
            # Jesli zdjecie sie zmienilo
            if old.photo != self.photo:
                old.photo.delete()

            # Niestety ze wzglendu na dzialanie sygnalu pre_save nie mozna usunac
            # starej miniaturki :(

        finally:
            # Zapis obiektu do bazy
            super(PhotoModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Operacja usuwania obiektu"""

        # Pobranie lokalizacji plikow
        storage1, photo_path = self.photo.storage, self.photo.path
        storage2, thumb_path = self.thumb.storage, self.thumb.path

        # Wykasowanie obiektu z bazy
        super(PhotoModel, self).delete(*args, **kwargs)

        # Wykasowanie plików
        storage1.delete(photo_path)
        storage2.delete(thumb_path)

    class Meta:
        verbose_name = u"Zdjęcie"
        verbose_name_plural = u"Zdjęcia"
        # Szeregowanie zdjęć względem galerii
        order_with_respect_to = 'gallery'


@receiver(pre_save, sender=PhotoModel)
def photo_pre_save_handler(sender, **kwargs):
    """Zdarzenie polegajace na wyliczeniu nazwy pliku miniatury"""

    # Instnacja PhotoModel
    phm = kwargs['instance']

    # Wyznaczenie sciezki do miniaturki
    photo_name = os.path.basename(phm.photo.path)
    thumb_name = os.path.join(GALLERY_DIR, THUMB_PREFIX  + photo_name)

    # Ustawienie
    phm.thumb = thumb_name


@receiver(post_save, sender=PhotoModel)
def photo_post_save_handler(sender, **kwargs):
    """Zdarzenie polegajace na fizycznym utworzeniu pliku miniatury"""

    # Instnacja PhotoModel
    phm = kwargs['instance']

    photo = get_absolute_path_of_file(phm.photo, GALLERY_DIR)
    thumb = get_absolute_path_of_file(phm.thumb, GALLERY_DIR)

    # Utworzenie miniaturki
    create_thumbnail(photo['fdir'], thumb['fdir'], THUMB_SIZE)

    # Przesklowanie też dużego obrazka do takiego, żeby się w galerii mieścił
    create_thumbnail(photo['fdir'], photo['fdir'], PHOTO_MAX_SIZE)
