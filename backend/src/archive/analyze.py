import sqlite3
import pdb
import re
import enchant
import multiprocessing
import os.path
import nltk

from src.util import *

import pandas as pd
import numpy as np

from datetime import date, datetime, timedelta

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
    all_msgs = pd.read_pickle('data/message.pck')
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

def generate_summary():
    parallel = True

    if not os.path.isfile("data/summary.pck"):
        handle = pd.read_pickle('data/handle.pck')
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

        stats.to_pickle('data/summary.pck')

    summary = pd.read_pickle('data/summary.pck')
    return True
