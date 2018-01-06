# -*- coding: utf-8 -*-
#
# KMDG -> Gallery -> models
#

import os

from ..app.image_utils import create_thumbnail, is_image
from ..app.media_utils import get_absolute_path_of_file
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from ckeditor_uploader import fields as ckefields


# Rozmiar poglądowego obrazka
THUMB_SIZE = (240, 160)
PHOTO_MAX_SIZE = (1200, 800)
THUMB_PREFIX = "mini_"  # Prefiks doklejany do nazwy pliku
GALLERY_DIR = u"gallery/"  # Wzgledna sciezka galerii (w MEDIA_ROOT)

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

    photo_count.short_description = u"Liczba fotografii"
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
        photos_in_gallery = PhotoModel.objects.filter(gallery__id=gallery.id)
        for photo in photos_in_gallery:
            photo.delete()
    except:
        print("Kasowanie pustej galerii")


class PhotoModel(models.Model):
    gallery = models.ForeignKey(GalleryModel)
    photo = models.ImageField(verbose_name=u"Plik zjęcia", upload_to=GALLERY_DIR)
    thumb = models.ImageField(verbose_name=u"Miniaturka", upload_to=GALLERY_DIR, editable=False)
    description = models.CharField(verbose_name=u"Opis pod zjęciem", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return u"Zdjęcie({0})".format(self.photo)

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
        photo_storage, photo_path = self.photo.storage, self.photo.path
        thumb_storage, thumb_path = self.thumb.storage, self.thumb.path

        # Wykasowanie obiektu z bazy
        super(PhotoModel, self).delete(*args, **kwargs)
        # Wykasowanie plików
        try:
            photo_storage.delete(photo_path)
            thumb_storage.delete(thumb_path)
        except IOError as e:
            print(e)

    class Meta:
        verbose_name = u"Zdjęcie"
        verbose_name_plural = u"Zdjęcia"
        # Szeregowanie zdjęć względem galerii
        order_with_respect_to = 'gallery'


@receiver(pre_save, sender=PhotoModel)
def photo_pre_save_handler(sender, **kwargs):
    """Zdarzenie polegajace na wyliczeniu nazwy pliku miniatury"""
    # Instnacja PhotoModel
    photo_model = kwargs['instance']
    # Wyznaczenie sciezki do miniaturki
    photo_name = os.path.basename(photo_model.photo.path)
    thumb_name = os.path.join(GALLERY_DIR, THUMB_PREFIX  + photo_name)
    # Ustawienie
    photo_model.thumb = thumb_name


@receiver(post_save, sender=PhotoModel)
def photo_post_save_handler(sender, **kwargs):
    """Zdarzenie polegajace na fizycznym utworzeniu pliku miniatury"""
    # Instnacja PhotoModel
    photo_model = kwargs['instance']
    photo = get_absolute_path_of_file(photo_model.photo, GALLERY_DIR)
    thumb = get_absolute_path_of_file(photo_model.thumb, GALLERY_DIR)
    # Utworzenie miniaturki
    create_thumbnail(photo['fdir'], thumb['fdir'], THUMB_SIZE)
    # Przesklowanie też dużego obrazka do takiego, żeby się w galerii mieścił
    create_thumbnail(photo['fdir'], photo['fdir'], PHOTO_MAX_SIZE)


class ZipFileModel(models.Model):
    gallery = models.ForeignKey(GalleryModel)
    zip = models.FileField(upload_to='tmp', help_text='Dodaj wiele zdjęć na raz spakowanych w archiwum ZIP')

    def delete(self, *args, **kwargs):
        zip_storage, zip_path = self.zip.storage, self.zip.path
        super(ZipFileModel, self).delete(*args, **kwargs)
        try:
            zip_storage.delete(zip_path)
        except IOError as e:
            print(e)

    class Meta:
        verbose_name = u"Archiwum ze zdjęciami"
        verbose_name_plural = verbose_name


@receiver(post_save, sender=ZipFileModel)
def zip_post_save_handler(sender, **kwargs):
    import zipfile, io

    zipfile_model = kwargs['instance']
    gallery_model = zipfile_model.gallery

    with zipfile.ZipFile(zipfile_model.zip, 'r') as archive:
        for entry in archive.namelist():
            file_name = entry.split('/')[-1]
            file_body = archive.read(entry)

            if is_image(io.BytesIO(file_body)):
                PhotoModel(gallery=gallery_model,
                           photo=SimpleUploadedFile(name=file_name, content=file_body),
                           description='')\
                    .save()

    zipfile_model.delete()
