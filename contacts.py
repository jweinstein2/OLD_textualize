import sqlite3
import pandas as pd
import pdb

src = 'src/contacts.db'

if __name__ == "__main__":
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


    connection = sqlite3.connect(src)
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
    df.to_pickle('contacts.pck')
