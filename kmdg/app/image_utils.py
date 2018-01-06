#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Moduł poświęcony skalowaniu plików graficznych
"""
try:
    import Image
except ImportError:
    import PIL.Image as Image


def is_image(some_file):
    """Test, czy wskazany plik jest plikiem graficznym, czy tez nie"""
    try:
        import imghdr
        return imghdr.what(some_file) in ('jpeg', 'jpg', 'tiff', 'gif', 'png')
    except IOError as e:
        return False


def create_thumbnail(src_image, out_image, scale):
    """
    Przygotowanie miniaturki obrazu

    Parametry:
        src_image - ścieżka do obrazu źródłowego
        out_image - ścieżka pod którą ma zostać zapisana miniatura
        scale - rozmiar miniaturki. Np scale=(120, 100)
    """
    try:
        img = Image.open(src_image)
        img.thumbnail(scale, Image.ANTIALIAS)
    except Exception as e:
        print(e)
    else:
        img.save(out_image)
