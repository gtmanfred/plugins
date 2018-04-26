# -*- coding: utf-8 -*-

import aiohttp


def uri(hub):
    return '/user/{userid}'


async def get(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return aiohttp.web.json_response({'Error': f'Unable to find user: {userid}'}, status=404)
    return aiohttp.web.json_response({'user': hub.triagedb.db.to_dict(user)})


async def put(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return aiohttp.web.json_response({'Error': f'Unable to find user: {userid}'}, status=404)

    data = await request.json()
    data.pop('userid', None)
    data.pop('date', None)

    await conn.execute(users.update().where(users.c.userid == user.userid).values(**data))

    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    return aiohttp.web.json_response({'user': hub.triagedb.db.to_dict(user)})


async def delete(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return aiohttp.web.json_response({'Error': f'Unable to find user: {userid}'}, status=404)

    await conn.execute(users.delete().where(users.c.userid == userid))

    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if user:
        return aiohttp.web.json_response({'Error': 'Failed to delete: {userid}'}, status=500)
    return aiohttp.web.json_response({'message': 'success'})
