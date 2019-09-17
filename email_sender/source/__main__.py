import sched
import time
import weakref

from aiohttp import web


async def make_app():
    app = web.Application()

    app['scheduler'] = sched.scheduler(time.time, time.sleep)
    app['tasks'] = weakref.WeakValueDictionary()

    return app
