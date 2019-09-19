from aiohttp import web
from databases import Database

from source import settings
from source.api import routes
from source.models import create_models


async def start_background_tasks(app):
    app['database'] = Database(settings.DATABASE_URL)
    await app['database'].connect()


async def stop_background_tasks(app):
    await app['database'].disconnect()


async def make_app():
    app = web.Application()

    app.add_routes(routes)

    create_models()

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
