from aiohttp import web
from marshmallow import ValidationError

from source.models import NotificationManager
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

        async with request.app['pool'].acquire() as con:
            result = await NotificationManager(con).create(**payload)

        return web.Response(body=output_schema.dumps(result))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.get('/notifications')
async def get_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationSearch()
        output_schema = NotificationOutput()

        payload = input_schema.load(received_data)

        async with request.app['pool'].acquire() as con:
            result = NotificationManager(con).get(**payload)

        return web.Response(body=output_schema.dumps(result))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.patch('/notifications/{id}')
async def patch_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationUpdatePayload()
        output_schema = NotificationId()

        payload = input_schema.load(received_data)

        async with request.app['pool'].acquire() as con:
            result = NotificationManager(con).update(record_id=request.match_info['id'], **payload)

        return web.Response(body=output_schema.dumps(result))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.delete('/notifications/{id}')
async def delete_handler(request):

    output_schema = NotificationId()

    async with request.app['pool'].acquire() as con:
        result = NotificationManager(con).delete(record_id=request.match_info['id'])

    return web.Response(body=output_schema.dumps(result))
