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
    users = hub.triagedb.db.users()
    result = await hub.triagedb.db.execute(users.select(users.c.triage))
    user = await result.fetchone()
    if not user:
        result = await hub.triagedb.db.execute(users.select(users.c.enabled).order_by(users.c.order))
        user = await result.fetchone()
        await hub.triagedb.db.execute(users.update().where(users.c.userid == user.userid).values(triage=True))
    result = await hub.triagedb.db.execute(users.select(users.c.enabled).order_by(users.c.order))
    all_users = await result.fetchall()
    for n, a in enumerate(all_users):
        if a.triage:
            if n >= len(all_users) - 1:
                next_user = all_users[0]
            else:
                next_user = all_users[n + 1]
    return hub.aio.http.json_response({
        'triage': user.name,
        'date': user.date.strftime('%A, %B %d, %Y'),
        'next_user': next_user.name,
    })


async def put(hub, request):
    users = hub.triagedb.db.users()
    result = await hub.triagedb.db.execute(users.select(True).order_by(users.c.order))
    retusers = await result.fetchall()
    nextuser = False
    for user in retusers:
        if user.triage:
            await hub.triagedb.db.execute(users.update().where(users.c.userid == user.userid).values(triage=False))
            nextuser = True
        elif not user.enabled:
            continue
        elif nextuser is True:
            newdate = datetime.datetime.utcnow()
            await hub.triagedb.db.execute(users.update().where(users.c.userid == user.userid).values(
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
                await hub.triagedb.db.execute(users.update().where(users.c.userid == user.userid).values(
                    triage=True,
                    date=newdate
                ))
                ret = {'nexttriage': user.name, 'date': newdate.strftime('%A, %B %d, %Y')}
                break
    return hub.aio.http.json_response(ret)
