import sqlite3
import threading
import shutil
import pandas as pd
import pdb
import os
import subprocess
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from src.util import *
from datetime import date, datetime, timedelta
import src.configuration as config

MESSAGES = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
CONTACTS = '31bb7ba8914766d4ba40d6dfb6113c8b614be442'

CM_JOIN_PATH = 'data/chat_message_join.pck'
CH_JOIN_PATH = 'data/chat_handle_join.pck'
CONTACTS_PATH = 'data/contacts.pck'
MESSAGES_PATH = 'data/message.pck'
HANDLES_PATH = 'data/handle.pck'

process_lock = threading.Lock()

def guess_src():
    possible = []

    home = os.path.expanduser('~')
    backup_dir = os.path.join(home, "Library/Application Support/MobileSync/Backup/")

    if os.path.isdir(backup_dir):
        for item in os.listdir(backup_dir):
            #TODO: select the latest backup
            if item[0] == '.':
                continue
            possible.append(os.path.join(backup_dir, item))

    # TODO: add windows support
    return possible

# Returns:
# STATUS         | ADDITIONAL
# ------------------------------
# "failed"       | description
# "in progress"  | status
# "completed"    | None
# "unstarted"    | None
def process_progress():
    if process_lock.locked():
        return "in_progress", config.get_process_progress()

    progress = config.get_process_progress()
    if progress == -1:
        # something went wrong
        return "failed", config.get_last_error()
    elif progress == 100:
        return "completed", None
    else:
        return "unstarted", None

def clear():
    #TODO: shutdown process thread
    if process_lock.locked():
        print("processing in background: shit is about to go south")

    shutil.rmtree('./data/', ignore_errors=True)
    config.del_process_progress()
    config.del_last_error()


# Kicks off threads to asychronously analyze the data
# Returns:
#   False if process fails to start
#   Assorted stats if asychronous task is started
def process(backup_path):
    if backup_path == None:
        return False, 'backup path has not been set'

    if not process_lock.acquire(False):
        # lock wasn't acquired
        return False, 'process already in progress'


    # get quick stats to return immediately
    # TODO
    content = ['Analyzing over 200 messages',
               'from over 68 contacts',
               'in over 400 countries']

    # start non-blocking thread for heavy processing
    t = threading.Thread(target = _async_process,
                     name = 'processing',
                     args = (backup_path, process_lock))
    t.start()
    return True, content

def _async_process(path, lock):
    config.del_last_error()
    try:
        success, message = _process(path)
        if not success:
            config.set_process_progress(-1)
            config.set_last_error(message)
            print("Handled failure while processing")
            print(message)
            return

    except Exception as e:
        config.set_process_progress(-1);
        config.set_last_error(str(e))
        print("Unexpected error while processing")
        print(e)
        return

    config.set_process_progress(100)
    lock.release()

def _process_dummy(path):
    del path
    import time

    TIME = 20
    for i in range(TIME + 1):
        print (i)
        prog = int(100 * (i / float(TIME)))
        config.set_process_progress(prog)
        time.sleep(1)

    return True, None

def _process(backup_path):
    config.set_process_progress(1);
    print('find database')
    # Messages
    try:
        message_db = subprocess.check_output("find '" + backup_path + "' -iname '" + MESSAGES + "'", shell=True).splitlines()[0].decode("utf-8")
    except subprocess.CalledProcessError as e:
        return False, 'unable to find message database'

    config.set_process_progress(10);
    print('load database')
    connection = sqlite3.connect(message_db)
    cur = connection.cursor()
    message_df = pd.read_sql_query("SELECT * FROM message", connection)
    handle_df = pd.read_sql_query("SELECT * FROM handle", connection)
    ch_join = pd.read_sql_query("SELECT * FROM chat_handle_join", connection)
    cm_join = pd.read_sql_query("SELECT * FROM chat_message_join", connection)

    config.set_process_progress(20);
    print('datestamp lambda')
    # add datestamp
    # TODO: this is really slow
    message_df['timestamp'] = message_df['date'].apply(ts)
    print('datestamp manipulation')
    message_df['n_collapsed'] = 0
    message_df['last_send'] = message_df['timestamp']

    config.set_process_progress(30);
    # TODO: This could be skipped to save time
    print('number')
    # add number (0 for sent messages in groupchat)
    message_df = message_df.dropna(subset = ['handle_id'])
    message_df['handle_id'] = message_df.handle_id.astype(int)
    handle_reordered = handle_df.set_index(['ROWID'])
    # import pdb; pdb.set_trace()
    numbers = handle_reordered.loc[message_df.handle_id].id
    message_df['number'] = numbers.values

    config.set_process_progress(40);
    print('group info')
    # add group information
    message_df['is_group'] = 2
    message_ids = message_df.ROWID
    # TODO:
    chat_ids = cm_join.set_index(['message_id']).loc[message_ids].chat_id
    ch_counts = ch_join.chat_id.value_counts()
    ch_counts.loc[ch_counts <= 1] = 0
    ch_counts.loc[ch_counts > 1] = 1
    ch_counts = ch_counts.astype(bool)
    message_df['is_group'] = ch_counts[chat_ids].values

    config.set_process_progress(50);
    print('save')
    os.makedirs('data/', exist_ok=True)
    print("created dir")
    message_df.to_pickle('data/message.pck')
    handle_df.to_pickle('data/handle.pck')
    ch_join.to_pickle('data/chat_handle_join.pck')
    cm_join.to_pickle('data/chat_message_join.pck')
    cur.close()
    connection.close()

    config.set_process_progress(60);
    print('contacts')
    # Contacts
    try:
        contact_db = subprocess.check_output("find '" + backup_path + "' -iname '" + CONTACTS + "'", shell=True).splitlines()[0].decode("utf-8")
    except subprocess.CalledProcessError as e:
        # raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
        return False, 'contact database not in expected location'

    connection = sqlite3.connect(contact_db)
    cur = connection.cursor()

    query = """
        Select
            ABPerson.First,
            ABPerson.Last,
            ABMultiValue.value
        from
            ABPerson,
            ABMultiValue
        where
            ABMultiValue.value IS NOT NULL
                AND
            ABPerson.ROWID = ABMultiValue.record_id
        order by
            ABPerson.First,
            ABPerson.Last"""


    connection = sqlite3.connect(contact_db)
    cur = connection.cursor()
    df = pd.read_sql_query(query, connection)

    config.set_process_progress(70);
    # generate full name string
    first = list(map(lambda v: v or "", df["First"]))
    last = list(map(lambda v: v or "", df["Last"]))
    full = ["{} {}".format(a_, b_) for a_, b_ in zip(first, last)]
    full = [s.strip() for s in full]
    df['Name'] = full
    df = df.loc[df['Name'] != " "]

    config.set_process_progress(80);
    # simplify phone number data
    df['value'] = df['value'].map(lambda a: parse_num(a))

    df.to_pickle('data/contacts.pck')
    config.set_process_progress(100);
    return True, None


#: MARK: Methods that read directly from the pickled dataframes
def cm_join():
    return pd.read_pickle(CM_JOIN_PATH)

def ch_join():
    return pd.read_pickle(CH_JOIN_PATH)

def handles():
    return pd.read_pickle(HANDLES_PATH)

def contacts():
    return pd.read_pickle(CONTACTS_PATH)

# Get the messages df filtered by time, group, and sender
def messages(number=None, is_group=None, start=None, end=None):
    df = pd.read_pickle(MESSAGES_PATH)

    if number: df = df.loc[df.number == number]
    if is_group is not None: df = df.loc[df['is_group'] == is_group]
    # TODO: add temporal filter
    # if start_date: df = df.loc[df['is_group'] >= start_date]
    # if start_date: df = df.loc[df['is_group'] < end_date]
    return df

# deVf messages_for_number(num, ignore_groups=True):
#     ch_join = pd.read_pickle('data/chat_handle_join.pck')
#     handle = pd.read_pickle('data/handle.pck')
#     cm_join = pd.read_pickle('data/chat_message_join.pck')
#     messages = pd.read_pickle('data/message.pck')
#
#     handle_ids = handle.loc[handle['id'] == num]['ROWID'].tolist()
#     chat_ids = ch_join.loc[ch_join['handle_id'].isin(handle_ids)]['chat_id'].tolist()
#
#     if ignore_groups:
#         chats = []
#         for cid in chat_ids:
#             if ch_join.loc[ch_join['chat_id'] == cid].shape[0] == 1:
#                 chats.append(cid)
#         chat_ids = chats
#
#     filtered_messages = cm_join.loc[cm_join['chat_id'].isin(chat_ids)]
#     filtered_messages = filtered_messages.merge(messages, how='left', left_on='message_id', right_on='ROWID')
#     return filtered_messages
#
# def find_name(num):
#     contacts = pd.read_pickle('data/contacts.pck')
#     names = contacts.loc[contacts['value'] == num[-10:]].Name.tolist()
#     if len(names) == 0:
#         return ""
#     if len(names) > 1:
#         print("duplicate entries found:", num, names)
#     return names[0]

if __name__ == '__main__':
    preprocess()
