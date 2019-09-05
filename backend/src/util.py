import pandas as pd
from datetime import date, datetime, timedelta

def ts(val):
    val = val / 10 ** 9
    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC
    delta = cocoa - unix
    timestamp = datetime.fromtimestamp(val) + delta
    timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return pd.to_datetime(timestamp)
