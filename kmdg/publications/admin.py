# -*- coding: utf-8 -*-

#
# KMDG -> Publications -> admin
#

from django.contrib import admin
from django.db.models import ManyToManyField
from django.forms.widgets import CheckboxSelectMultiple
from ..publications.models import BulletinModel, StorageModel, TagModel, EditorModel, BookModel
from ..publications.models import SeriesModel, SeriesEntryModel


class BulletinAdmin(admin.ModelAdmin):
    """Interface klasy BulletinModel w panelu administracyjnym"""

    fieldsets = [
        ("Numer wydania", {'fields': ['number_in_year', 'number']}),
        ("Publikacja", {'fields': ['referent', 'number_of_meeting', 'reading', 'publication', 'tag', 'editors']}),
        ("Biuletyn", {'fields': ['title', 'cover', 'content']}),
    ]

    formfield_overrides = {
        ManyToManyField: {'widget': CheckboxSelectMultiple, 'help_text': ''},
    }

    list_display = ('display_number', 'title', 'referent', 'reading', 'publication', 'thumbnail', )

    search_fields = ('referent', 'title', )
    # date_hierarchy = 'reading'
    ordering = ('-number', '-publication', )
    list_per_page = 50


class EditorAdmin(admin.ModelAdmin):
    """Interfejs klasy EditorModel w panelu administracyjnym"""
    list_display = ('full_name', )


class StorageAdmin(admin.ModelAdmin):
    """Interfejs klasy StorageModel w panelu administracyjnym"""
    list_display = ('filename', 'description', 'url', 'icon', )
    actions = None


class BooksAdmin(admin.ModelAdmin):
    """Interfejs klasy BooksModel w panelu administracyjnym"""
    list_display = ('title', 'author', 'publication', 'isbn', 'pages', 'number', )
    ordering = ('-number', 'publication', )


class EntryInline(admin.TabularInline):
    model = SeriesEntryModel
    extra = 2
    ordering = ('number',)


class SeriesAdmin(admin.ModelAdmin):
    """Interfejs klasy SeriesModel w panelu administracyjnym"""
    list_display = ('name', 'entries_count',)
    inlines = [EntryInline]


admin.site.register(BulletinModel, BulletinAdmin)
admin.site.register(TagModel)
admin.site.register(EditorModel, EditorAdmin)
admin.site.register(StorageModel, StorageAdmin)
admin.site.register(BookModel, BooksAdmin)
admin.site.register(SeriesModel, SeriesAdmin)
