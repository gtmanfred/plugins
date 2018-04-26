# -*- coding: utf-8 -*-

import aiohttp.web
import datetime


def uri(hub):
    return '/triage'


async def get(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    result = await conn.execute(users.select(users.c.enabled is True))
    user = await result.fetchone()
    if not user:
        result = await conn.execute(users.select(True).order_by(users.c.order))
        user = await result.fetchone()
        await conn.execute(users.update().where(users.c.userid == user.userid).values(triage=True))
    return aiohttp.web.json_response({
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
        if user.triage is True:
            await conn.execute(users.update().where(users.c.userid == user.userid).values(triage=False))
            nextuser = True
        elif user.enabled == 0:
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
            if user.enabled == 1:
                newdate = datetime.datetime.utcnow()
                await conn.execute(users.update().where(users.c.userid == user.userid).values(
                    triage=True,
                    date=newdate
                ))
                ret = {'nexttriage': user.name, 'date': newdate.strftime('%A, %B %d, %Y')}
                break
    return aiohttp.web.json_response(ret)
