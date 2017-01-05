#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Moduł poświęcony skalowaniu plików graficznych
"""
try:
    import Image
except ImportError:
    import PIL as Image

import imghdr


def is_image(some_file):
    """Test, czy wskazany plik jest plikiem graficznym, czy tez nie"""

    try:
        return not imghdr.what(some_file)

    except IOError as e:
        # plik nie istnieje, albo jakies inne klopoty
        print(e)
    finally:
        return(False)


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
