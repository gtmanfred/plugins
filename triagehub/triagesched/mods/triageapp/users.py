# -*- coding: utf-8 -*-


def __virtual__(hub):
    if 'aio' not in hub:
        return False, 'Load the `hub.mods.aio` pack'
    if 'http' not in hub.aio:
        return False, '`hub.aio.http` is not available: install `aiohttp`'
    return True


def uri(hub):
    return '/users'


async def get(hub, request):
    users = hub.triagedb.db.users()
    if 'enabled' in request.rel_url.query:
        result = await hub.triagedb.db.execute(users.select(users.c.enabled == 1))
    else:
        result = await hub.triagedb.db.execute(users.select(True))
    retusers = await result.fetchall()
    if not retusers:
        return hub.aio.http.json_response({'Error': 'No users defined'}, status=404)
    return hub.aio.http.json_response({'users': [hub.triagedb.db.to_dict(user) for user in retusers]})


async def post(hub, request):
    users = hub.triagedb.db.users()
    data = await request.json()
    name = data['name']
    order = data['order']
    await hub.triagedb.db.execute(users.insert().values(name=name, order=order))
    return hub.aio.http.json_response({'message': 'success'})
