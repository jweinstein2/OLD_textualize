import sqlite3
import pandas as pd
import pdb
import os.path
import subprocess

from datetime import date, datetime, timedelta

# MARK: configuration
backup_path = '/Users/jaredweinstein/Library/Application Support/MobileSync/Backup/d8e6c828598040349ff13fbacbc8755e3a3c1d28'

# MARK: helper
def ts(val):
    val = val / 10 ** 9

    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC
    delta = cocoa - unix
    timestamp = datetime.fromtimestamp(val) + delta
    timestamp.strftime('%Y-%m-%d %H:%M:%S')
    return pd.to_datetime(timestamp)

# MARK: main
if __name__ == "__main__":
    messages = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
    contacts = '31bb7ba8914766d4ba40d6dfb6113c8b614be442'

    # Messages
    message_db = subprocess.check_output("find . -iname '" + messages + "'", shell=True).splitlines()[0].decode("utf-8")

    connection = sqlite3.connect(message_db)
    cur = connection.cursor()
    message_df = pd.read_sql_query("SELECT * FROM message", connection)
    handle_df = pd.read_sql_query("SELECT * FROM handle", connection)
    ch_join = pd.read_sql_query("SELECT * FROM chat_handle_join", connection)
    cm_join = pd.read_sql_query("SELECT * FROM chat_message_join", connection)

    # add datestamp
    message_df['timestamp'] = message_df.apply (lambda row: ts(row.at['date']), axis=1)

    message_df['n_collapsed'] = 0
    message_df['last_send'] = message_df['timestamp']

    os.mkdirs('src/')
    message_df.to_pickle('src/message.pck')
    handle_df.to_pickle('src/handle.pck')
    ch_join.to_pickle('src/chat_handle_join.pck')
    cm_join.to_pickle('src/chat_message_join.pck')
    cur.close()
    connection.close()

    # Contacts
    contact_db = subprocess.check_output("find . -iname '" + contacts + "'", shell=True).splitlines()[0].decode("utf-8")
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

    # generate full name string
    first = list(map(lambda v: v or "", df["First"]))
    last = list(map(lambda v: v or "", df["Last"]))
    full = ["{} {}".format(a_, b_) for a_, b_ in zip(first, last)]
    full = [s.strip() for s in full]
    df['Name'] = full
    df = df.loc[df['Name'] != " "]

    # simplify phone number data
    def parse_num(num):
        return "".join(list(filter(str.isdigit, num)))[-10:]

    df['value'] = df['value'].apply(parse_num)
    df.to_pickle('src/contacts.pck')

    print('successfully saved dataframes to src/')
