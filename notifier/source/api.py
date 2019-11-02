import logging
from asyncio import get_event_loop
from datetime import datetime

from aiohttp import web

from notification.schemas import Notification
from app.tasks import send_email

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.post('/api/tasks')
async def create_task(request):

    received_data = await request.json()

    input_schema = Notification()

    payload = input_schema.load(received_data)

    send_at = payload['send_at'].timestamp() - datetime.now().timestamp() + get_event_loop().time()

    request.app['tasks'][payload['id']] = get_event_loop().call_at(send_at,
                                                                   send_email,
                                                                   payload)
    logger.info(f'Task {payload["id"]} was created')
    return web.Response()


@routes.delete('/api/tasks/{id}')
async def cancel_task(request):
    try:
        request.app['tasks'][int(request.match_info['id'])].cancel()

        logger.info(f'Task {request.match_info["id"]} was cancelled')
    except KeyError:
        logger.error(f'Task {request.match_info["id"]} was not found')

    return web.Response()
