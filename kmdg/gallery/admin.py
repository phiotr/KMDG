# -*- coding: utf-8 -*-
#
# KMDG -> Gallery -> admin
#

from django.contrib import admin
from ..gallery.models import GalleryModel, PhotoModel, ZipFileModel


class PhotoInLine(admin.TabularInline):
    model = PhotoModel
    extra = 5
    fields = ('photo', 'description', 'display_thumb',)
    readonly_fields = ('display_thumb', )


class ZipInLine(admin.TabularInline):
    model = ZipFileModel
    max_num = 1
    can_delete = False


class GalleryAdmin(admin.ModelAdmin):
    fieldsets = ((u"Informacje o galerii", {'fields': ['title', 'description']}), )
    list_display = ('title', 'create_date', 'photo_count', )
    inlines = [PhotoInLine, ZipInLine, ]

    class Media:
        css = {'all': ('/static/css/admin_textarea.css', )}


admin.site.register(GalleryModel, GalleryAdmin)
