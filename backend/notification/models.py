from aiohttp import web
from bson.objectid import ObjectId
from bson.errors import InvalidId

from app import settings


class Notification:

    def __init__(self, db):
        self.collection = db[settings.NOTIFICATION_COLLECTION]

    async def get_or_404(self, _id):
        try:
            result = await self.collection.find_one({'_id': ObjectId(_id)})
            if result:
                return result
            else:
                raise web.HTTPNotFound(text='Notification with requested id is missing')
        except InvalidId:
            raise web.HTTPNotFound(text='Notification with requested id is missing')

    async def update_or_404(self, _id, payload):
        try:
            result = await self.collection.update_one({'_id': ObjectId(_id)}, payload)
            if not result:
                raise web.HTTPNotFound(text='Notification with requested id is missing')
        except InvalidId:
            raise web.HTTPNotFound(text='Notification with requested id is missing')

    async def insert(self, data):
        result = await self.collection.insert_one(data)
        return str(result.inserted_id)

    async def select(self, **filters):
        pass
