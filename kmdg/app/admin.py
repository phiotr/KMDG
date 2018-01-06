# -*- coding: utf-8 -*-

#
# KMDG -> App -> admin
#

from django.contrib import admin
from ..app.models import SkinModel


class SkinAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ['skin']}),
        (u"Daty obowiązywania", {'fields': ['start', 'stop']}),
        (u"Dodatkowe", {'fields': ['description']}), )

    list_display = ('get_id', 'skin', 'start', 'stop', 'description', 'is_actual', )
    list_display_links = ('get_id', 'skin',)
    date_hierarchy = None


admin.site.register(SkinModel, SkinAdmin)
