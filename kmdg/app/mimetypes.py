# -*- coding: utf8 -*-

mimetypes = {
    # Dokumenty biurowe
    'doc': 'doc.png',
    'docx': 'doc.png',
    'ppt': '.png',
    'pps': '.png',
    'xls': 'xls.png',
    'xlsb': 'xls.png',
    'rtf': 'rtf.png',
    'pdf': 'pdf.png',

    # Pliki graficzne
    'png': 'img.png',
    'bmp': 'img.png',
    'gif': 'img.png',
    'jpg': 'img.png',
    'jpeg': 'img.png',
    'svg': 'img.png',
    'tiff': 'img.png',

    # Archiwa
    'rar': 'rar.png',
    'tar': 'tar.png',
    'zip': 'zip.png',
    'gz': 'gz.png',
    'tgz': 'gz.png',
    'jar': 'jar.png',

    # Pliki muzyczne
    'mp3': 'music.png',
    'mp4': 'music.png',
    'ogg': 'music.png',
    'Wav': 'music.png',

    # Pliki wideo
    'avi': 'video.png',
    'wmv': 'video.png',
    'flv': 'video.png',
    'flx': 'video.png',
    'divx': 'video.png',
    'mpeg': 'video.png',
    'mpg': 'video.png',
    'rm': 'video.png',

    # Inne
    'py': 'py.png',
}

UNKNOWN = 'none.png'

def get_icon_by_extension(some_file):

    try:
        ext = some_file.split('.')[-1]

    except IndexError:
        return UNKNOWN

    else:
        return mimetypes.get(ext, UNKNOWN)
