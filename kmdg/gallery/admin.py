# -*- coding: utf-8 -*-

#
#	KMDG -> Gallery -> admin
#

from django.contrib import admin
from ..gallery.models import GalleryModel, PhotoModel

# Tabela zaleznych Zdjec wstawiana do widoku tworzenia Galerii
class PhotoInLine(admin.TabularInline):
    model = PhotoModel
    extra = 5


class GalleryAdmin(admin.ModelAdmin):

    fieldsets = (
        (u"Informacje o galerii", {'fields': ['title', 'description']}), )

    inlines = [PhotoInLine]

    list_display = ('title', 'create_date', 'photo_count', )

    class Media:
        js = ('/static/js/ckeditor/ckeditor.js',
                '/static/js/html_editor.js',)

        css = {'all': ('/static/css/admin_textarea.css', )}


admin.site.register(GalleryModel, GalleryAdmin)
