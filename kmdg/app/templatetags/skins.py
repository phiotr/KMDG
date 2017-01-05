# -*- coding: utf-8 -*-

from django import template

# Folder wyzej
from ...app.today import today
from ...app.models import SkinModel, DEFAULT_SKIN

register = template.Library()

@register.simple_tag
def get_skin():
    
    td = today()

    skins = SkinModel.objects.filter(start__lte=td, stop__gte=td).order_by('-pk')

    if skins:
        return skins[0].skin
    else:
        return DEFAULT_SKIN
