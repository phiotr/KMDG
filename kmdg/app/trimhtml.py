# -*- coding: utf8 -*-

import re

def html_preview(html, length):
    """Wydobycie z tekstu w formacie HTML lenght znakow czystego napisu"""

    return re.sub('<[^<]+?>', '', html).replace('\n', ' ')[:length]
