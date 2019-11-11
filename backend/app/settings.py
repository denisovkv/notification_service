from envparse import Env


env = Env()

MONGO_HOST = env.str('MONGO_HOST', default='mongo')
MONGO_PORT = env.str('MONGO_PORT', default='27017')
MONGO_DB_NAME = env.str('MONGO_DB_NAME', default='notification_service')

NOTIFICATION_COLLECTION = env.str('NOTIFICATION_COLLECTION', default='notifications')

DATABASE_URL = f'mongodb://{MONGO_HOST}:{MONGO_PORT}'

NOTIFIER_ENDPOINT = env.str('NOTIFIER_ENDPOINT', default='http://notifier:8081/api/task')

TIMEZONE = env.str('TIMEZONE', default='Europe/Samara')
