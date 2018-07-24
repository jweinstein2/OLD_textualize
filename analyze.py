import sqlite3
import pdb
import re
import enchant
import multiprocessing
import os.path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import date, datetime, timedelta

def find_name(num):
    contacts = pd.read_pickle('src/contacts.pck')
    names = contacts.loc[contacts['value'] == num[-10:]].Name.tolist()
    if len(names) == 0:
        return ""
    if len(names) > 1:
        print("duplicate entries found:", num, names)
    return names[0]

def collapse(messages, within=timedelta(minutes=10)):
    messages['delete'] = False

    for c in range(len(messages) - 1, 0, -1):
        p = c - 1
        prev = messages.loc[p]
        curr = messages.loc[c]
        if curr['is_from_me'] != prev['is_from_me']:
            continue
        if curr.timestamp - prev.timestamp > within:
            continue

        messages.loc[p, 'n_collapse'] += messages.loc[c, 'n_collapse']
        messages.loc[p, 'collapse_final_timestamp'] = messages.loc[c, 'collapse_final_timestamp']
        messages.loc[c, 'delete'] = True
        prev_text = messages.loc[p, 'text']
        curr_text = messages.loc[c, 'text']
        if curr_text == None: curr_text = ''
        if prev_text == None: prev_text = ''
        messages.loc[p, 'text'] =  curr_text + '\n' + prev_text

    messages = messages.loc[messages['delete'] == False]
    messages = messages.drop(['delete'], axis=1)
    messages = messages.reset_index(drop=True)
    return messages

def conversation_stats(messages, info_dict, convo_gap=timedelta(hours=14)):
    all_msgs = pd.read_pickle('src/message.pck')
    started = 0
    ended = 0
    total = 0

    their_rt = timedelta()
    them_tot = 0

    your_rt = timedelta()
    ignored = 0
    ignored_tot = 0

    for c in range(len(messages) - 1, 0, -1):
        p = c - 1
        prev = messages.loc[p]
        curr = messages.loc[c]

        # gap between conversations
        if curr.timestamp - prev.timestamp > convo_gap:
            if curr['is_from_me'] == 1: started += 1
            if prev['is_from_me'] == 1: ended += 1
            total += 1
            continue

        if prev['is_from_me'] and not curr['is_from_me']:
            their_rt = their_rt + (curr.timestamp - prev.timestamp)
            them_tot += 1

        # gap within conversations
        if not prev['is_from_me'] and curr['is_from_me']:
            your_rt = your_rt + (curr.timestamp - prev.timestamp)
            # check if there was a message sent in that time
            is_sent = all_msgs['is_from_me'] == 1
            is_time = all_msgs['timestamp'] > prev['timestamp']
            is_before = all_msgs['timestamp'] < curr['timestamp']
            is_ignored = len(all_msgs.loc[is_time & is_before & is_sent]) > 0
            ignored_tot += 1
            ignored += int(is_ignored)

    total = max(total, 1)
    ignored_tot = max(ignored_tot, 1)
    them_tot = max(them_tot, 1)
    your_rt = timedelta(seconds=int((your_rt / ignored_tot).total_seconds()))
    their_rt = timedelta(seconds=int((their_rt/ them_tot).total_seconds()))
    info_dict['convos started'] = round((started * 100.0) / total, 1)
    info_dict['convos ended'] = round((ended * 100.0) / total, 1)
    info_dict['ignored'] = round((ignored * 100.0) / ignored_tot, 1)
    info_dict['your_response_time'] = your_rt
    info_dict['their_response_time'] = their_rt
    return info_dict

def agg_stats_for_number(num):
    info_dict = {}
    info_dict['number'] = num
    info_dict['name'] = find_name(num)

    messages = messages_for_number(num)

    # collapse messages sent near each other
    should_collapse = True
    messages['n_collapse'] = 1
    messages['collapse_final_timestamp'] = messages['timestamp']
    if should_collapse:
        messages = collapse(messages)

    info_dict = conversation_stats(messages, info_dict)

    sent = messages.loc[messages['is_from_me'] == 1]
    recieved = messages.loc[messages['is_from_me'] == 0]

    info_dict['n_sent'] = len(sent)
    info_dict['n_recieved'] = len(recieved)
    if len(sent) < 100 or len(recieved) < 100:
        return

    sent_text = "\n".join(filter(None, sent['text'].tolist()))
    recieved_text ='\n'.join(filter(None, recieved['text'].tolist()))

    words_s = list(map(lambda s: s.lower(), re.compile('\w+').findall(sent_text)))
    words_r = list(map(lambda s: s.lower(), re.compile('\w+').findall(recieved_text)))
    dictionary = enchant.Dict("en_US")
    words_s = list(filter(lambda w: dictionary.check(w), words_s))
    words_r = list(filter(lambda w: dictionary.check(w), words_r))
    unique_s = len(set(words_s))
    unique_r = len(set(words_r))
    avg_len_s = sum(list(map(len, words_s))) / len(words_s)
    avg_len_r = sum(list(map(len, words_r))) / len(words_r)
    info_dict['vocab_sent'] = unique_s
    info_dict['vocab_recieved'] = unique_r
    info_dict['avg_wordlen_sent'] = avg_len_s
    info_dict['avg_wordlen_recieved'] = avg_len_r

    return info_dict

def messages_for_number(num, ignore_groups=True):
    ch_join = pd.read_pickle('src/chat_handle_join.pck')
    handle = pd.read_pickle('src/handle.pck')
    cm_join = pd.read_pickle('src/chat_message_join.pck')
    messages = pd.read_pickle('src/message.pck')

    handle_ids = handle.loc[handle['id'] == num]['ROWID'].tolist()
    chat_ids = ch_join.loc[ch_join['handle_id'].isin(handle_ids)]['chat_id'].tolist()

    if ignore_groups:
        chats = []
        for cid in chat_ids:
            if ch_join.loc[ch_join['chat_id'] == cid].shape[0] == 1:
                chats.append(cid)
        chat_ids = chats

    filtered_messages = cm_join.loc[cm_join['chat_id'].isin(chat_ids)]
    filtered_messages = filtered_messages.merge(messages, how='left', left_on='message_id', right_on='ROWID')
    return filtered_messages

def plt_frequency(num, save=None, period="M"):
    messages = messages_for_number(num)
    messages.sort_values(by='timestamp')

    periods = messages.timestamp.dt.to_period(period)
    first = periods[0].to_timestamp()
    last = periods.tail(1).values[0].to_timestamp()
    last = datetime.now()

    sent = messages.loc[messages['is_from_me'] == 1]
    recieved = messages.loc[messages['is_from_me'] == 0]
    count_sent = sent['timestamp'].groupby(periods).agg('count')
    count_recieved = recieved['timestamp'].groupby(periods).agg('count')

    dates = pd.date_range(first, last, freq=period)
    y_s = [count_sent.get(date, 0) for date in dates]
    y_r = [count_recieved.get(date, 0) for date in dates]

    x = np.arange(0, len(dates))
    fig, ax = plt.subplots(1,1)
    plt.plot(x, y_s, label='sent')
    plt.plot(x, y_r, label='received')
    num_ticks = 10
    stride = max(1, min(len(x), int(len(x) / 10)))
    ax.set_xticks(x[::stride])
    ax.set_xticklabels(dates.date[::stride])
    fig.autofmt_xdate()

    if save == None:
        plt.show()
    else:
        plt.savefig(save)
    plt.close('all')


if __name__ == "__main__":
    parallel = True
    overwrite = True

    if not os.path.isfile("stats.pck") or overwrite:
        handle = pd.read_pickle('src/handle.pck')
        numbers = handle.id.unique()

        if parallel:
            pool_num = multiprocessing.cpu_count()
            print("running on {} cpus".format(pool_num))
            pool = multiprocessing.Pool(pool_num)
            info_lst = list(pool.imap_unordered(agg_stats_for_number, numbers))
            pool.close()
            pool.join()
        else:
            print("running on single cpu")
            info_lst = [agg_stats_for_number(n) for n in numbers]

        info_lst = list(filter(None, info_lst))
        stats = pd.DataFrame(info_lst)
        stats = stats.sort_values(by='n_sent', ascending=False)
        stats = stats.reset_index(drop=True)

        os.mkdirs('pck')
        stats.to_pickle('pck/stats.pck')

    stats = pd.read_pickle('pck/stats.pck')

    os.mkdirs('/output')
    stats.to_csv('output/_stats.csv')

    # for i in range(len(stats)):
    #    plt_frequency(stats.number[i], save='output/'+stats.name[i])


