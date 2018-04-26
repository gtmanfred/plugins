# -*- coding: utf-8 -*-

import aiohttp.web


def uri(hub):
    return '/users'


async def get(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    if 'enabled' in request.rel_url.query:
        result = await conn.execute(users.select(users.c.enabled == 1))
    else:
        result = await conn.execute(users.select(True))
    retusers = await result.fetchall()
    if not retusers:
        return aiohttp.web.json_response({'Error': 'No users defined'}, status=404)
    return aiohttp.web.json_response({'users': [hub.triagedb.db.to_dict(user) for user in retusers]})


async def post(hub, request):
    conn = hub.triagedb._conn
    users = hub.triagedb._users
    data = await request.json()
    name = data['name']
    order = data['order']
    await conn.execute(users.insert().values(name=name, order=order))
    return aiohttp.web.json_response({'message': 'success'})
