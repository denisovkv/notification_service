from aiohttp import web


routes = web.RouteTableDef()


@routes.post('/tasks')
async def create_task(request):

    return web.Response()


@routes.patch('/tasks/{id}')
async def update_task(request):

    return web.Response()


@routes.delete('/tasks/{id}')
async def cancel_task(request):

    return web.Response()
