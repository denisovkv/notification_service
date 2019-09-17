from aiohttp import web


routes = web.RouteTableDef()


@routes.post('/tasks')
async def post_handler(request):
    try:
        payload = await request.json()

        async with request.app['pool'].acquire() as con:
            result = await shield(NotificationManager(con).create(**payload))

        return web.Response(body=output_schema.dumps(result))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text='Request body is incorrect or missing')


@routes.patch('/tasks/{id}')
async def patch_handler(request):
    try:
        received_data = await request.json()

        input_schema = NotificationUpdatePayload()
        output_schema = NotificationId()

        payload = input_schema.load(received_data)

        async with request.app['pool'].acquire() as con:
            result = await shield(NotificationManager(con).update(record_id=request.match_info['id'], **payload))

        return web.Response(body=output_schema.dumps(result))

    except (ValueError, ValidationError):
        return web.Response(status=400,
                            text=f'Request body is incorrect or missing')


@routes.delete('/tasks/{id}')
async def delete_handler(request):

    output_schema = NotificationId()

    async with request.app['pool'].acquire() as con:
        result = await shield(NotificationManager(con).delete(record_id=request.match_info['id']))

    return web.Response(body=output_schema.dumps(result))
