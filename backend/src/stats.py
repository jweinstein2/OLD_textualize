import pickle
import pandas as pd
import json
from datetime import date, datetime, timedelta
import pdb

from src.util import *

def contacts(message_df, n):
    df = message_df.number.value_counts()[:n]
    return json.dumps(df.to_dict())

def frequency(message_df, number=None, period='M'):
    # if number != None:
    #     messages = messages_for_number(number)
    # else:
    #     messages = pd.read_pickle('data/message.pck')

    message_df = message_df.sort_values(by='timestamp').reset_index()

    periods = message_df.timestamp.dt.to_period(period)
    first = periods[0].to_timestamp()
    # last = periods.tail(1).values[0].to_timestamp()
    last = datetime.now()

    sent = message_df.loc[message_df['is_from_me'] == 1]
    recieved = message_df.loc[message_df['is_from_me'] == 0]
    count_sent = sent['timestamp'].groupby(periods).agg('count')
    count_recieved = recieved['timestamp'].groupby(periods).agg('count')

    dates = pd.date_range(first, last, freq=period)
    y_s = [count_sent.get(date, 0) for date in dates]
    y_r = [count_recieved.get(date, 0) for date in dates]

    data = [{'Label': str(l), 'Sent': int(s), 'Received': int(r)} for l, s, r in zip(dates, y_s, y_r)]
    return json.dumps(data)


def summary():
    if not os.path.isfile("data/summary.pck"):
        if not generate_summary():
            return {}

    df = pd.read_pickle('data/summary.pck')
    # sanitize by converting datetime to seconds
    df.their_response_time = stats.their_response_time.map(lambda d: d.seconds)
    df.your_response_time = stats.your_response_time.map(lambda d: d.seconds)

    summary_payload = {}

    # meta data
    summary_payload['meta'] = {}
    cols = df.columns.values.tolist()
    cols.insert(0, cols.pop(cols.index('name')))
    summary_payload['meta']['columns'] = cols
    summary_payload['meta']['n_rows'] = len(df)

    # contact rows
    summary_payload['data'] = df.to_dict(orient='records')
    return json.dumps(summary_payload)

def wordcloud(number):
    df = pd.read_pickle('data/message.pck')

def contact():
    pass

def person():
    pass
