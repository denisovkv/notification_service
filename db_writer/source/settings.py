from envparse import Env


env = Env()

DATABASE_URL = env.str('DATABASE_URL', default='sqlite:///../db/notification_service.db')
