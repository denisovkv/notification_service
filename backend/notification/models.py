from datetime import datetime

from app import settings


class Notification:

    def __new__(cls, db):
        cls.collection = db[settings.NOTIFICATION_COLLECTION]

    async def save(self, user, msg):
        result = await self.collection.insert({'user': user, 'msg': msg, 'time': datetime.now()})
        return result

    async def get_messages(self):
        messages = self.collection.find().sort([('time', 1)])
        return await messages.to_list(length=None)
