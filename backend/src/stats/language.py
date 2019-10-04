import textstat
import enchant

import src.data_manager as data_manager
from src.util import *

def contact_summary(messages):
    info_dict = {}
    sent, received = split_sender(messages)
    dictionary = enchant.Dict("en_US")

    def process(txt, messages):
        words, text = extract_words(messages)
        n_words = len(words)
        dict_words = list(filter(lambda w: dictionary.check(w), words))
        n_dict_words = len(dict_words)
        perc_proper = round(len(dict_words) / len(words) * 100, 1)
        avg_len = sum(list(map(len, words))) / len(words)
        info_dict[txt + '_readability'] = textstat.text_standard(text, float_output=False)
        info_dict[txt + '_avg_wordlen'] = round(avg_len, 2)
        info_dict[txt + '_perc_proper'] = perc_proper

    process('received', received)
    process('sent', sent)

    # unique words
    (words, text) = extract_words(messages)
    (all_words, all_text) = extract_words(data_manager.messages())
    uni = unique(words, all_words)
    df = pd.DataFrame({'name': uni.index, 'value': uni.values})
    info_dict['unique'] = df.to_dict(orient='records')

    return info_dict

def summary(messages):
    pass

def wordcloud(number):
    df = pd.read_pickle('data/message.pck')
