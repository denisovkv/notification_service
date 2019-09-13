from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/notifications')
async def get_handler(request):
    pass


@routes.post('/notifications')
async def post_handler(request):
    pass


@routes.patch('/notifications/{id}')
async def patch_handler(request):
    pass


@routes.delete('/notifications/{id}')
async def delete_handler(request):
    pass
