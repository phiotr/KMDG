# -*- coding: utf8 -*-

#
# KMDG -> Activities -> admin
#

from django.contrib import admin
from ..activities.models import CalendarModel, NewsModel


class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'referent', 'title', 'number_of_meeting', 'has_bulletin', 'is_upcoming', )
    list_display_links = ('date', 'title', )
    search_fields = ('referent', 'title', )
    ordering = ('-date',)
    list_per_page = 50


class NewsAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'preview', )

    class Media:
        js = ('/static/js/ckeditor/ckeditor.js', '/static/js/html_editor.js')
        css = {'all': ('/static/css/admin_textarea.css', )}


admin.site.register(CalendarModel, CalendarAdmin)
admin.site.register(NewsModel, NewsAdmin)
