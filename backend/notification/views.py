from aiohttp import ClientSession, web
from marshmallow import ValidationError

from notification.models import notifications
from app import settings
from notification.schemas import NotificationId, NotificationPayload, NotificationUpdatePayload, \
    NotificationSearch, NotificationOutput, Notification


routes = web.RouteTableDef()


@routes.view('/{id}')
class NotificationView(web.View):

    async def get(self):

        output_schema = Notification()

        query = notifications.select().where(notifications.c.id == self.request.match_info['id'])

        result = await self.request.app['database'].fetch_one(query=query)

        return web.Response(body=output_schema.dumps(result))

    async def patch(self):
        try:
            received_data = await self.request.json()

            input_schema = NotificationUpdatePayload()

            payload = input_schema.load(received_data)

            query = notifications.update().where(notifications.c.id == self.request.match_info['id'])

            await self.request.app['database'].execute(query=query,
                                                       values=payload)

            # TODO: timezone
            # TODO: вынести в модель
            query = notifications.select().where(notifications.c.id == self.request.match_info['id'])

            result = await self.request.app['database'].fetch_one(query=query)

            if result:
                async with ClientSession() as session:
                    async with session.delete(f'{settings.NOTIFIER_ENDPOINT}/'
                                              f'{self.request.match_info["id"]}'):
                        pass

                    async with session.post(settings.NOTIFIER_ENDPOINT, json=Notification().dump(result)):
                        pass
                return web.Response()
            else:
                return web.Response(status=400,
                                    text='Notification with self.requested id is missing')

        except (ValueError, ValidationError):
            return web.Response(status=400,
                                text='Request body is incorrect or missing')

    async def delete(self):

        query = notifications.update().where(notifications.c.id == self.request.match_info['id'])

        await self.request.app['database'].execute(query=query,
                                                   values={'is_deleted': True})

        async with ClientSession() as session, session.delete(f'{settings.NOTIFIER_ENDPOINT}/'
                                                              f'{self.request.match_info["id"]}'):
            return web.Response()


@routes.view('/')
class NotificationCreateView(web.View):
    async def post(self):
        try:
            received_data = await self.request.json()

            input_schema = NotificationPayload()
            output_schema = NotificationId()

            payload = input_schema.load(received_data)

            notification_id = await self.request.app['database'].execute(query=notifications.insert(),
                                                                         values=payload)
            received_data['id'] = notification_id

            async with ClientSession() as session, session.post(settings.NOTIFIER_ENDPOINT,
                                                                json=received_data):

                return web.Response(body=output_schema.dumps({'id': notification_id}))

        except (ValueError, ValidationError):
            return web.Response(status=400,
                                text='Request body is incorrect or missing')


@routes.view('/search')
class NotificationSearchView(web.View):
    async def get(self):
        try:
            input_schema = NotificationSearch()
            output_schema = NotificationOutput()

            payload = input_schema.load(self.request.query)

            column_map = {
                'id': notifications.c.id,
                'title': notifications.c.title,
                'send_to': notifications.c.send_to,
                'is_sent': notifications.c.is_sent,
                'is_deleted': notifications.c.is_deleted
            }

            query = notifications.select()

            for key, value in payload.items():
                query = query.where(column_map[key] == value)

            result = await self.request.app['database'].fetch_all(query=query)

            return web.Response(body=output_schema.dumps({'result': result}))

        except (ValueError, ValidationError):
            return web.Response(status=400,
                                text='Request body is incorrect or missing')


@routes.view('/confirm/{id}')
class NotificationConfirmView(web.View):
    async def get(self):

        query = notifications.update().where(notifications.c.id == self.request.match_info['id'])

        await self.request.app['database'].execute(query=query,
                                                   values={'is_sent': True})
        return web.Response()