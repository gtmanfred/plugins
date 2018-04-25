# -*- coding: utf-8 -*-

try:
    import aiohttp
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
