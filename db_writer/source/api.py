from aiohttp import web
from marshmallow import ValidationError

from source.models import notifications
from source.schemas import NotificationId, NotificationPayload, NotificationUpdatePayload, \
                           NotificationSearch, NotificationOutput

routes = web.RouteTableDef()


@routes.post('/notifications')
async def post_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationPayload()
        output_schema = NotificationId()

        payload = input_schema.load(received_data)

        notification_id = await request.app['database'].execute(query=notifications.insert(),
                                                                values=payload)

        # TODO: await create_task

        return web.Response(body=output_schema.dumps({'id': notification_id}))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.get('/notifications')
async def get_handler(request):
    try:
        input_schema = NotificationSearch()
        output_schema = NotificationOutput()

        payload = input_schema.load(request.query)

        result = await request.app['database'].fetch_all(query=notifications.select())

        # TODO: await create_task

        return web.Response(body=output_schema.dumps({'result': result}))
    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.patch('/notifications/{id}')
async def patch_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationUpdatePayload()

        payload = input_schema.load(received_data)

        query = notifications.update().where(notifications.c.id == request.match_info['id'])

        await request.app['database'].execute(query=query,
                                              values=payload)

        # TODO: await create_task

        return web.Response()

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text=f'Request body is incorrect or missing')


@routes.delete('/notifications/{id}')
async def delete_handler(request):

    query = notifications.update().where(notifications.c.id == request.match_info['id'])

    await request.app['database'].execute(query=query,
                                          values={'is_deleted': True})

    # TODO: await create_task

    return web.Response()
