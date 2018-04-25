# -*- coding: utf-8 -*-

try:
    import psycopg2
except ImportError:
    HAS_PSQL = False
else:
    HAS_PSQL = True


def __virtual__(hub):
    if HAS_PSQL is True:
        return True, ''
    return False, f'Failed to load {__name__}: please install `psycopg2`'


def query(hub, query, commit=False, uri='postgresql://'):
    conn = hub.context.setdefault(__name__, {}).setdefault(uri, psycopg2.connect(uri))
    cur = conn.cursor()
    cur.execute(query)
    ret = cur.fetchall()
    if commit is True:
        cur.commit()
    return ret
