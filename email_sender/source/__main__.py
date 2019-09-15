import asyncpg
import aiojobs
from aiohttp import web

from source import settings
from source.jobs import email_task


async def start_background_tasks(app):
    app['pool'] = await asyncpg.create_pool(dsn=settings.DATABASE_URL,
                                            min_size=1,
                                            max_size=2)
    app['scheduler'] = await aiojobs.create_scheduler()
    await app['scheduler'].spawn(email_task(app))


async def stop_background_tasks(app):
    await app['pool'].close()
    await app['scheduler'].close()


async def make_app():
    app = web.Application()

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
