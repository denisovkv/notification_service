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
    notification = web.Application()

    notification.add_routes(notification_routes)

    app.add_subapp('/api/notification/', notification)

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
