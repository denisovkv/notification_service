import weakref

from aiohttp import web

from source.api import routes


async def make_app():
    app = web.Application()

    app.add_routes(routes)

    app['tasks'] = weakref.WeakValueDictionary()

    return app
