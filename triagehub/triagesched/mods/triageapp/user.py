# -*- coding: utf-8 -*-


def __virtual__(hub):
    if 'aio' not in hub:
        return False, 'Load the `hub.mods.aio` pack'
    if 'http' not in hub.aio:
        return False, '`hub.aio.http` is not available: install `aiohttp`'
    return True


def uri(hub):
    return '/user/{userid}'


async def get(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return hub.aio.http.json_response({'Error': f'Unable to find user: {userid}'}, status=404)
    return hub.aio.http.json_response({'user': hub.triagedb.db.to_dict(user)})


async def put(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return hub.aio.http.json_response({'Error': f'Unable to find user: {userid}'}, status=404)

    data = await request.json()
    data.pop('userid', None)
    data.pop('date', None)

    await conn.execute(users.update().where(users.c.userid == user.userid).values(**data))

    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    return hub.aio.http.json_response({'user': hub.triagedb.db.to_dict(user)})


async def delete(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    userid = request.match_info['userid']
    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if not user:
        return hub.aio.http.json_response({'Error': f'Unable to find user: {userid}'}, status=404)

    await conn.execute(users.delete().where(users.c.userid == userid))

    result = await conn.execute(users.select(users.c.userid == userid))
    user = await result.fetchone()
    if user:
        return hub.aio.http.json_response({'Error': 'Failed to delete: {userid}'}, status=500)
    return hub.aio.http.json_response({'message': 'success'})
