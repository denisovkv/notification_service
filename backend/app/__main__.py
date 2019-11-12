from aiohttp import web
from app import settings
from motor.motor_asyncio import AsyncIOMotorClient
from notification.views import routes as notification_routes


async def on_notification_app_startup(notification_app):
    notification_app['client'] = AsyncIOMotorClient(settings.DATABASE_URL)
    notification_app['db'] = notification_app['client'][settings.MONGO_DB_NAME]


async def on_notification_app_shutdown(notification_app):
    notification_app['client'].close()


async def make_app():
    app = web.Application()
    notification_app = web.Application()

    notification_app.add_routes(notification_routes)

    notification_app.on_startup.append(on_notification_app_startup)
    notification_app.on_shutdown.append(on_notification_app_shutdown)

    app.add_subapp('/api/notification', notification_app)

    return app
