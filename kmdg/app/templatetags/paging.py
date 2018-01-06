# -*- coding: utf8 -*-
from django import template


register = template.Library()


@register.inclusion_tag('main/pagination.html')
def insert_pagination(page, link_prefix):
    """Wygenerowanie bloku nawigacji stronnicowania"""
    return {'page': page, 'prefix': link_prefix}

