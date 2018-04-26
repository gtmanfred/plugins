# -*- coding: utf-8 -*-

try:
    import aiohttp
    import aiohttp.web
except ImportError:
    HAS_AIOHTTP = False
else:
    HAS_AIOHTTP = True


def __virtual__(hub):
    if HAS_AIOHTTP is True:
        return True, ''
    return False, f'Failed to load {__name__}: please install `aiohttp`'


async def query(hub, url, method='GET', data=None, headers=None):
    async with aiohttp.ClientSession(loop=hub.tools._loop) as session:
        async with getattr(session, method.lower())(url, data=data, headers=headers) as response:
            if response.status >= 400:
                raise Exception('{0} with {1} failed.'.format(method, data))
            ret = await response.text()
            return ret.strip()


def json_response(hub, data, status=200):
    return aiohttp.web.json_response(data, status=status)


def web(hub, mods, prefix='', static=None, staticpath=None, listen_ip='127.0.0.1', listen_port='5000'):
    app = aiohttp.web.Application()
    for modname in mods:
        if isinstance(mods, dict):
            hub.tools.pack.add(modname, pypath=mods[modname])
        for module in getattr(hub, modname):
            for method in ['get', 'post', 'put', 'delete', 'options', 'head', 'connect']:
                if hasattr(module, method) and hasattr(module, 'uri'):
                    app.router.add_route(method.upper(), f'{prefix}{module.uri()}', getattr(module, method))
    if static is not None:
        if staticpath is None:
            staticpath = '/static/'
        app.router.add_static(staticpath, path=static, name='static')
    handler = app.make_handler()
    loop = hub.tools.loop.create()
    f = loop.create_server(handler, '0.0.0.0', 5000)
    srv = loop.run_until_complete(f)
    print('serving on', srv.sockets[0].getsockname())
    try:
        hub.tools.loop.entry()
    except KeyboardInterrupt:
        pass
    finally:
        hub.tools.loop.start(handler.finish_connections, 1.0)
        srv.close()
        hub.tools.loop.start(srv.wait_closed())
        hub.tools.loop.start(app.finish())
