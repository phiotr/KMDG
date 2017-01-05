# -*- coding: utf-8 -*-

import datetime as dt

    
def today():
    """Pobranie aktualnej daty wzgledem Polskiej strfy czasowej"""

    try:
        import pytz
        return dt.datetime.now(pytz.timezone('Europe/Warsaw')).date()

    except ImportError: 
        return (dt.datetime.utcnow() + dt.timedelta(hours=2)).date()
