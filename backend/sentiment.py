from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import pdb
import numpy as np

import src.data_manager as dm
from scipy import interpolate


def process(msg_df):
    analyser = SentimentIntensityAnalyzer()

    x = []
    y = []
    vals = []

    i = 0

    for index, row in msg_df.iterrows():
        i += 1
        text = row.text
        time = row.timestamp.timestamp()
        row.timestamp
        result = analyser.polarity_scores(text)

        result['label'] = text

        if len(text.split()) > 5:
            vals.append(result)
            x.append(time)
            y.append(result['neg'])


    pos = sorted(vals, key= lambda x: x['pos'])
    com = sorted(vals, key= lambda x: x['compound'])
    neg = sorted(vals, key= lambda x: x['neg'])

    pdb.set_trace()

    f = interpolate.interp1d(x, y)

    num = 70
    xx = np.linspace(x[0], x[-1], num)
    yy = f(xx)

    #  plt.plot(x,y, 'bo-')
    plt.plot(xx,yy, 'g.-')
    plt.show()

    # plt.plot(x, y, linewidth=2.0)
    # plt.show()


msg = dm.messages(handle=1066, start=None, end=None)
process(msg)
