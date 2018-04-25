import sqlite3

__virtualname__ = 'sqlite'


def query(hub, query, commit=False, uri=':memory:'):
    conn = hub.context.setdefault(__name__, {}).setdefault(uri, sqlite3.connect(uri))
    cur = conn.cursor()
    cur.execute(query)
    ret = cur.fetchall()
    if commit is True:
        cur.commit()
    return ret
