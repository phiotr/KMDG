# -*- coding: utf-8 -*-
#
# KMDG -> Gallery -> views
#

from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..gallery.models import GalleryModel, PhotoModel


@csrf_exempt
def view_gallery_list(_):
    """Strona zawierająca listę wszystkich galerii"""
    galleries = GalleryModel.objects.all().order_by('-create_date')
    context = {'sitetitle': u'Lista Galerii', 'galleries': galleries}
    return render_to_response('pages/gallery_list.html', context)


@csrf_exempt
def view_gallery_show(_, gallery_id):
    """Strona wyświetlająca konkretną galerię ze zdjęciami"""
    gallery = get_object_or_404(GalleryModel, id=gallery_id)
    photos = PhotoModel.objects.filter(gallery=gallery_id)
    photo_urls = [p.photo.url for p in photos]
    photo_desc = [p.description if p.description else '' for p in photos]
    title = u"""Galeria "{0}" """.format(gallery.title)
    context = {'sitetitle': title, 'gallery': gallery, 'photos': photos, 'photo_urls': photo_urls, 'photo_descriptions': photo_desc}
    return render_to_response('pages/gallery.html', context)
