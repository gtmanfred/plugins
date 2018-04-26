# -*- coding: utf-8 -*-

import datetime


def __virtual__(hub):
    if 'aio' not in hub:
        return False, 'Load the `hub.mods.aio` pack'
    if 'http' not in hub.aio:
        return False, '`hub.aio.http` is not available: install `aiohttp`'
    return True


def uri(hub):
    return '/triage'


async def get(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    result = await conn.execute(users.select(users.c.triage))
    user = await result.fetchone()
    if not user:
        result = await conn.execute(users.select(users.c.enabled).order_by(users.c.order))
        user = await result.fetchone()
        await conn.execute(users.update().where(users.c.userid == user.userid).values(triage=True))
    return hub.aio.http.json_response({
        'triage': user.name,
        'date': user.date.strftime('%A, %B %d, %Y')
    })


async def put(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    result = await conn.execute(users.select(True).order_by(users.c.order))
    retusers = await result.fetchall()
    nextuser = False
    for user in retusers:
        if user.triage:
            await conn.execute(users.update().where(users.c.userid == user.userid).values(triage=False))
            nextuser = True
        elif not user.enabled:
            continue
        elif nextuser is True:
            newdate = datetime.datetime.utcnow()
            await conn.execute(users.update().where(users.c.userid == user.userid).values(
                triage=True,
                date=newdate,
            ))
            nextuser = False
            ret = {'nexttriage': user.name, 'date': newdate.strftime('%A, %B %d, %Y')}
            break
    if nextuser is True:
        for user in retusers:
            if user.enabled:
                newdate = datetime.datetime.utcnow()
                await conn.execute(users.update().where(users.c.userid == user.userid).values(
                    triage=True,
                    date=newdate
                ))
                ret = {'nexttriage': user.name, 'date': newdate.strftime('%A, %B %d, %Y')}
                break
    return hub.aio.http.json_response(ret)
