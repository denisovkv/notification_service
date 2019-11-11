import logging
from asyncio import get_event_loop
from datetime import datetime

from aiohttp import web

from app import schemas
from app.tasks import send_email

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.view('/api/task/{id}')
class TaskView(web.View):
    async def delete(self):
        try:
            self.request.app['tasks'][self.request.match_info['id']].cancel()

            logger.info(f'Task {self.request.match_info["id"]} was cancelled')

            return web.HTTPOk()

        except KeyError:
            logger.error(f'Task {self.request.match_info["id"]} was not found')

            return web.HTTPNotFound()


@routes.view('/api/task')
class TaskCreateView(web.View):
    async def post(self):

        received_data = await self.request.json()

        input_schema = schemas.Notification()

        payload = input_schema.load(received_data)

        send_at = payload['send_at'].timestamp() - datetime.now().timestamp() + get_event_loop().time()

        self.request.app['tasks'][payload['id']] = get_event_loop().call_at(send_at, send_email, payload)

        logger.info(f'Task {payload["id"]} was created')

        return web.HTTPOk()
