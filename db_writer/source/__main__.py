import asyncpg
from aiohttp import web

from source import settings
from source.api import routes


async def start_background_tasks(app):
    app['pool'] = await asyncpg.create_pool(dsn=settings.DATABASE_URL,
                                            min_size=settings.POOL_MIN_SIZE,
                                            max_size=settings.POOL_MAX_SIZE)


async def stop_background_tasks(app):
    await app['pool'].close()


async def make_app():
    app = web.Application()

    app.add_routes(routes)

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
