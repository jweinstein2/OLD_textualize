import pickle
import pandas as pd
import json
from datetime import date, datetime, timedelta
import pdb

from src.util import *
import src.data_manager as data_manager


# TODO: add additional information name, number, sent, received
def handles(message_df, n):
    df = message_df.handle_id.value_counts()[:n]
    return df.to_dict()

def emojis(message_df, n):
    import emoji
    import regex

    text = message_df.text.str.cat(sep = " ")

    emoji_list = []
    data = regex.findall(r'\X', text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI for char in word):
            emoji_list.append(word)


    f = open('output.txt', 'w+', encoding='utf-8')
    f.write("".join(text))
    f.close()


    total_sent = len(emoji_list)
    value_count = pd.Series(emoji_list).value_counts()
    top_value_count = value_count[:n]
    top_value_count['other'] = value_count[n:].cumsum()[-1]

    return emoji_list

def sentiment(message_df):
    pass
    # from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    # analyser = SentimentIntensityAnalyzer()


    # sent = message_df.loc[message_df['is_from_me'] == 1]
    # received = message_df.loc[message_df['is_from_me'] == 0]

    # sent_text = sent.text.str.cat(sep = " ")
    # received_text = received.text.str.cat(sep = " ")
    # score1 = analyser.polarity_scores(sent_text)
    # score2 = analyser.polarity_scores(received_text)

    # print(score1)
    # print(score2)


def frequency(message_df, period='M'):
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
