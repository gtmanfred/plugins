# -*- coding: utf-8 -*-
'''
The main interface for management of the aio loop
'''
# Import python libs
import asyncio
import functools

__virtualname__ = 'loop'


def __virtual__(hub):
    return True


def create(hub):
    '''
    Create the loop at hub.loop.loop
    '''
    if not hasattr(hub.tools, '_loop'):
        hub.tools._loop = asyncio.get_event_loop()
    return hub.tools._loop


def call_soon(hub, fun, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop
    '''
    hub.tools._loop.call_soon(functools.partial(fun, *args, **kwargs))


def ensure_future(hub, fun, *args, **kwargs):
    '''
    Schedule a coroutine to be called when the loop has time. This needs
    to be called after the creation fo the loop
    '''
    asyncio.ensure_future(fun(*args, **kwargs))


def entry(hub):
    '''
    The entry coroutine to start a run forever loop
    '''
    hub.tools._loop.run_forever()


def start(hub, fun, *args, **kwargs):
    '''
    Start a loop that will run until complete
    '''
    return hub.tools.loop.create().run_until_complete(fun(*args, **kwargs))
