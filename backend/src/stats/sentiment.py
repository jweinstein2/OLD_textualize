from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def contact_summary(messages):
    info_dict = {}
    analyser = SentimentIntensityAnalyzer()

    def extremes(df):
        polarity = df.text.apply(lambda x: analyser.polarity_scores(x))
        df['compound'] = polarity.apply(lambda x: x['compound'])
        df_sort = df.sort_index(by='compound')
        pos = df_sort[-3:][['text', 'compound']]
        neg = df_sort[:3][['text', 'compound']]
        pos_dict = pos.to_dict(orient='records')
        neg_dict = neg.to_dict(orient='records')
        return pos_dict, neg_dict

    sent, rcvd = split_sender(messages)
    info_dict['pos_sent'], info_dict['neg_sent'] = extremes(sent)
    info_dict['pos_received'], info_dict['neg_received'] = extremes(rcvd)
    return info_dict

def summary(messages):
    pass
