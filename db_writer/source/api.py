import json

from aiohttp import ClientSession, web
from marshmallow import ValidationError

from source.models import notifications
from source import settings
from source.schemas import NotificationId, NotificationPayload, NotificationUpdatePayload, \
    NotificationSearch, NotificationOutput, Notification, SendingConfirmation

routes = web.RouteTableDef()


@routes.post('/api/notifications')
async def post_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationPayload()
        output_schema = NotificationId()

        payload = input_schema.load(received_data)

        notification_id = await request.app['database'].execute(query=notifications.insert(),
                                                                values=payload)
        received_data['id'] = notification_id

        async with ClientSession() as session, session.post(settings.EMAIL_SENDER_ENDPOINT,
                                                            json=received_data):

            return web.Response(body=output_schema.dumps({'id': notification_id}))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.get('/api/notifications/{id}')
async def get_handler(request):

    output_schema = Notification()

    query = notifications.select().where(notifications.c.id == request.match_info['id'])

    result = await request.app['database'].fetch_one(query=query)

    return web.Response(body=output_schema.dumps(result))


@routes.get('/api/search/notifications')
async def search_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationSearch()
        output_schema = NotificationOutput()

        payload = input_schema.load(received_data)

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

        result = await request.app['database'].fetch_all(query=query)

        return web.Response(body=output_schema.dumps({'result': result}))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.patch('/api/notifications/{id}')
async def patch_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationUpdatePayload()

        payload = input_schema.load(received_data)

        query = notifications.update().where(notifications.c.id == request.match_info['id'])

        await request.app['database'].execute(query=query,
                                              values=payload)

        query = notifications.select().where(notifications.c.id == request.match_info['id'])

        result = await request.app['database'].fetch_one(query=query)

        if result:
            async with ClientSession() as session:
                async with session.delete(f'{settings.EMAIL_SENDER_ENDPOINT}/{request.match_info["id"]}'):
                    pass

                async with session.post(settings.EMAIL_SENDER_ENDPOINT, json=Notification().dump(result)):
                    pass
            return web.Response()
        else:
            return web.Response(status=400,
                                text='Notification with requested id is missing')
    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.patch('/api/confirm/notifications/{id}')
async def confirm_handler(request):
    try:
        received_data = await request.json()

        input_schema = SendingConfirmation()

        payload = input_schema.load(received_data)

        query = notifications.update().where(notifications.c.id == request.match_info['id'])

        await request.app['database'].execute(query=query,
                                              values=payload)

        return web.Response()

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.delete('/api/notifications/{id}')
async def delete_handler(request):

    query = notifications.update().where(notifications.c.id == request.match_info['id'])

    await request.app['database'].execute(query=query,
                                          values={'is_deleted': True})

    async with ClientSession() as session, session.delete(f'{settings.EMAIL_SENDER_ENDPOINT}/{request.match_info["id"]}'):
        return web.Response()
