import json

from aiohttp import ClientSession, web
from marshmallow import ValidationError

from app import settings
from notification import schemas, warnings
from notification.models import Notification


routes = web.RouteTableDef()


@routes.view('/{id}')
class NotificationView(web.View):

    async def get(self):

        result = await Notification(self.request.app['db']).get_or_404(self.request.match_info['id'])

        return web.HTTPOk(content_type='application/json', body=schemas.Notification().dumps(result))

    async def patch(self):
        try:
            received_data = await self.request.json()

            payload = schemas.NotificationUpdatePayload().load(received_data)

            await Notification(self.request.app['db']).update_or_404(self.request.match_info['id'], {'$set': payload})

            result = await Notification(self.request.app['db']).get_or_404(self.request.match_info['id'])

            async with ClientSession() as session, \
                    session.delete(f'{settings.NOTIFIER_ENDPOINT}/{self.request.match_info["id"]}'), \
                    session.post(settings.NOTIFIER_ENDPOINT, json=schemas.Notification().dump(result)):
                return web.HTTPOk()

        except (ValueError, ValidationError):
            return web.HTTPBadRequest(text=warnings.INCORRECT_OR_MISSING_BODY)

    async def delete(self):

        await Notification(self.request.app['db']).delete(self.request.match_info['id'])

        async with ClientSession() as session, \
                session.delete(f'{settings.NOTIFIER_ENDPOINT}/{self.request.match_info["id"]}'):
            return web.HTTPOk()


@routes.view('')
class NotificationCreateAndSearchView(web.View):
    async def post(self):
        try:
            payload = schemas.NotificationPayload().load(await self.request.json())

            inserted_id = await Notification(self.request.app['db']).insert(payload)

            result = await Notification(self.request.app['db']).get_or_404(inserted_id)

            async with ClientSession() as session, \
                    session.post(settings.NOTIFIER_ENDPOINT, json=schemas.Notification().dump(result)):
                return web.HTTPOk(content_type='application/json', body=json.dumps({'id': inserted_id}))

        except (ValueError, ValidationError):
            return web.HTTPBadRequest(text=warnings.INCORRECT_OR_MISSING_BODY)

    async def get(self):
        try:
            filters = schemas.NotificationSearch().load(self.request.query)

            result = await Notification(self.request.app['db']).select(filters)

            return web.HTTPOk(content_type='application/json',
                              body=schemas.NotificationList().dumps({'result': result}))

        except (ValueError, ValidationError):
            return web.HTTPBadRequest(text=warnings.INCORRECT_OR_MISSING_BODY)


@routes.view('/confirm/{id}')
class NotificationConfirmView(web.View):
    async def patch(self):

        await Notification(self.request.app['db']).update_or_404(self.request.match_info['id'], {'$set': {'is_sent': True}})

        return web.HTTPOk()
