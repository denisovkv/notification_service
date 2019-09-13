import aiojobs
import asyncio
from aiohttp import web


async def start_background_tasks(app):
    app['scheduler'] = await aiojobs.create_scheduler()


async def stop_background_tasks(app):
    await app['scheduler'].close()


async def make_app():
    app = web.Application()

    app.on_startup.append(start_background_tasks)
    app.on_shutdown.append(stop_background_tasks)

    return app
