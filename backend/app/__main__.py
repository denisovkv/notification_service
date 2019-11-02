from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient

from app import settings
from notification.views import routes as notification_routes


async def start_background_tasks(app):
    app['client'] = AsyncIOMotorClient(settings.DATABASE_URL)
    app['db'] = app['client'][settings.MONGO_DB_NAME]


async def stop_background_tasks(app):
    app['client'].close()


async def make_app():
    app = web.Application()

    api = web.Application()
    notification = web.Application()

    app.add_subapp('/api/', api)
    app.add_subapp('/notification/', notification)

    notification.add_routes(notification_routes)

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
